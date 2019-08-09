import subprocess
import time
import re
import os
import shutil
import json
import psutil
import threading
import signal
import logging
from collections.abc import Iterable
from config import BASE_DIR, PASSWORD
from config import DEBUG
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level)
formatter = logging.Formatter(fmt='%(asctime)s [%(threadName)s] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s')
handler = logging.StreamHandler()
handler.setLevel(level)
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

LOGS_DIR = os.path.join(BASE_DIR, "output{}logs".format(os.sep), time.strftime("%Y%m%d_%H%M%S"))


def run_cmd(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    LOGGER.debug('Execute cmd: {}\nResult: {}'.format(cmd, output))
    if status:
        raise ValueError("Cmd error:({})\n{}".format(cmd, output))
    return output


def get_current_func_name():
    import sys
    return sys._getframe().f_back.f_code.co_name


def _root_no_password(cmd):
    cmd = "echo {} | sudo -S {}".format(PASSWORD, cmd)
    return run_cmd(cmd)


def rmmodprobe(drive_name, times):
    """rmmod/modprobe driverName N times"""
    try:
        for i in range(times):
            run_cmd(_root_no_password("rmmod {}".format(drive_name)))
            time.sleep(0.5)
            run_cmd(_root_no_password("modprobe {}".format(drive_name)))
            time.sleep(0.5)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def get_hddl_install_dir():
    hddl_install_dir = os.environ.get('HDDL_INSTALL_DIR')
    if not hddl_install_dir:
        raise ValueError('Not check EnvVar(HDDL_INSTALL_DIR),Please set it!')
    return hddl_install_dir


def get_hddl_bin_by_name(name):
    bin_path = os.path.join(get_hddl_install_dir(), 'bin', name)
    if not os.path.exists(bin_path):
        bin_path = None
    return bin_path


def get_allpid_with_name(process_name):
    relate_pids = []
    pids = psutil.pids()
    for pid in pids:
        try:
            process = psutil.Process(pid)
        except Exception:
            continue
        for pattern in process_name:
            if re.fullmatch(pattern, process.name()):
                relate_pids.append(pid)
    return relate_pids


def get_myx_count():
    booted_count = 0
    unboot_count = 0
    if os.name == 'nt':
        import wmi
        w = wmi.WMI()
        usb_devices = w.Win32_USBControllerDevice()
        for usb_device in usb_devices:
            caption = usb_device.Dependent.Caption
            if 'Movidius' in caption:
                unboot_count += 1
            elif 'VSC Loopback Device' in caption:
                booted_count += 1
    else:
        booted_count = int(run_cmd('lsusb | grep "f63b" | wc -l'))
        unboot_count = int(run_cmd('lsusb | grep "2485" | wc -l'))
    LOGGER.info('Found {} myx device.(booted:{}, unboot:{})'.format(booted_count+unboot_count,
                                                                    booted_count,
                                                                    unboot_count))
    myx_count = booted_count + unboot_count
    return myx_count, booted_count, unboot_count


class BslReset(object):

    generate_rel_path_linux = 'build/src/bsl_reset'
    generate_rel_path_windows = 'build/output/bin/bsl_reset.exe'

    def __init__(self):
        self.bsl_reset_src = os.path.join(get_hddl_install_dir(), 'hddl-bsl')
        if os.name == 'nt':
            self.generate_rel_path = self.generate_rel_path_windows
            self.dropped_place = 'nul'
            self.prefix = ''
        else:
            self.generate_rel_path = self.generate_rel_path_linux
            self.dropped_place = '/dev/null'
            self.prefix = './'
        self.bsl_reset_bin = os.path.join(self.bsl_reset_src, self.generate_rel_path)
        if not os.path.exists(self.bsl_reset_bin):
            if os.name == 'posix':
                self._compile_bsl_reset(self.bsl_reset_src)
            else:
                raise ValueError('please manully compile bsl_reset')

    def _compile_bsl_reset(self, project_path):
        LOGGER.info('Compile bsl_reset source code.')
        current_dir = os.getcwd()
        os.chdir(project_path)
        _root_no_password('mkdir build')
        os.chdir('build')
        _root_no_password('cmake ..')
        _root_no_password('make')
        os.chdir(current_dir)

    def reset_device(self, did, mode):
        base_dir = os.path.dirname(self.bsl_reset_bin)
        old_dir = os.getcwd()
        os.chdir(base_dir)
        cmd_string = '{}{} -d {} -i {} > {}'.format(self.prefix,
                                                    os.path.basename(self.bsl_reset_bin),
                                                    mode, did,
                                                    self.dropped_place)
        LOGGER.debug("Reset a device cmdstring:{}".format(cmd_string))
        os.system(cmd_string)
        LOGGER.info('Reset device with id is {}'.format(did))
        os.chdir(old_dir)

    def reset_all(self):
        base_dir = os.path.dirname(self.bsl_reset_bin)
        old_dir = os.getcwd()
        os.chdir(base_dir)
        cmd_string = '{}{} > {}'.format(self.prefix,
                                        os.path.basename(self.bsl_reset_bin),
                                        self.dropped_place)
        LOGGER.debug("Reset all device cmdstring:{}".format(cmd_string))
        os.system(cmd_string)
        LOGGER.info('Reset All devices.')
        os.chdir(old_dir)

    def reset_devices(self, dids, mode):
        if not isinstance(dids, Iterable):
            dids = list(dids)
        for did in dids:
            self.reset_device(did, mode)

    def __str__(self):
        return '{}:<{}>'.format(self.__class__.__name__, self.bsl_reset_bin)


class ResetDevice(object):

    name = 'ResetDevice'

    def __init__(self):
        exec_path = get_hddl_bin_by_name(self.name)
        if exec_path is None:
            exec_path = os.path.join(BASE_DIR, 'source_cpp/tools/ResetDevice')
            os.system("chmod 755 {}".format(exec_path))

        self.bin = exec_path

    def reset(self, device_id):
        os.system('{} -d {} > /dev/null'.format(self.bin, device_id))

    def path(self):
        return self.bin

    def __str__(self):
        return self.path()


class BaseServer(object):

    hddl_install_dir = 'HDDL_INSTALL_DIR'
    logfile = 'server.log'
    output_dir = LOGS_DIR

    def __init__(self, pname, parse=True):
        self.pname = pname
        self.ready = False
        self.bin = self._get_hddldaemon_bin()
        self.pid = 0

        if parse:
            self.parser = ParserLog()

    def _get_hddldaemon_bin(self):
        hid = os.environ.get(self.hddl_install_dir, None)
        if hid is None:
            raise ValueError('Not found Environ Var(HDDL_INSTALL_DIR),Please check it!')
        hddldaemon_bin = os.path.join(hid, 'bin', self.pname)
        if not os.path.exists(hddldaemon_bin):
            raise ValueError('Not found {},May no install OpenVINO'.format(self.pname))
        return hddldaemon_bin

    def is_ready(self):
        return self.ready

    def start(self):
        raise NotImplementedError('Subclass must be implement.')

    def stop(self):
        if not self.pid:
            raise ValueError('Hddldaemon no starting...')
        os.kill(self.pid, signal.SIGKILL)
        try:
            psutil.Process(self.pid)
        except psutil.NoSuchProcess:
            self.pid = 0
            return True
        else:
            self.stop()

    def restart(self):
        if self.pid:
            self.stop()
        self.start()


class WinServer(BaseServer):

    def __init__(self):
        super().__init__(pname='hddldaemon.exe')

    def is_running(self):
        pids = psutil.pids()
        for pid in pids:
            process = psutil.Process(pid)
            if process.name() == self.pname:
                return pid
        return None

    def start(self, tcs_id):
        pid = self.is_running()
        if pid:
            os.kill(pid, signal.SIGKILL)

        self.config = ServerConfig(os.path.join(self.output_dir, str(tcs_id)))

        if self.is_running():
            self.stop_run()
        #############################
        # support matt windows test....
        if os.name == "nt":
            os.chdir(get_hddl_install_dir())
        #############################
        cmd_string = '{} -c {} --boot-config {}'.format(self.bin,
                                                        self.config.get_configpath('service'),
                                                        self.config.get_configpath('autoboot'))
        if log:
            self.logfile = os.path.join(self.config.get_path(), file)
            cmd_string = '{} > {} 2>&1'.format(cmd_string, self.logfile)
        if daemon:
            cmd_string = '{} &'.format(cmd_string)
        LOGGER.info('Starting Hddldaemon')
        # return os.system(cmd_string)
        rv = subprocess.Popen(cmd_string, shell=True)
        time.sleep(3)
        self.parser_log = ParserLog(self.logfile, self)
        self.parser_log.start()
        while not self.ready:
            time.sleep(1)
        time.sleep(5)
        LOGGER.info('Hddldaemon is ready.')
        return rv

class UnixServer(BaseServer):

    def __init__(self):
        super().__init__(pname='hddldamon')


class Server(object):

    output_dir = LOGS_DIR
    time_out = 3 * 60

    if os.name == "nt":
        process_name = ['hddldaemon.exe', 'autoboot.exe']
        name = process_name[0]
    else:
        process_name = ['hddldaemon', 'autoboot', r'^\d+\.\d+BOOT$']
        name = process_name[0]
        # process_name = ['3.2BOOT', '4.1BOOT', '4.2BOOT', '8.1BOOT', 'hddldaemon', 'autoboot']

    def __init__(self, testcase_id):
        ##############################
        # support matt windows test....
        self.bin = get_hddl_bin_by_name(self.name)
        ##############################
        self.logfile = None
        self.ready = False
        self.config = ServerConfig(os.path.join(self.output_dir, str(testcase_id)))
        self.parser_log = None
        if self.is_running():
            self.stop_run()

    def is_ready(self):
        return self.ready

    @classmethod
    def is_running(cls):
        pids = get_allpid_with_name(cls.process_name)
        if pids:
            LOGGER.debug('Found {} is Running!pids:({})'.format(cls.process_name[-2:], pids))
            return True
        return False

    def start_run(self, daemon=True, log=True, file='server.log'):
        run_time = 0
        cmd_string = '{} -c {} --boot-config {}'.format(self.bin,
                                                        self.config.get_configpath('service'),
                                                        self.config.get_configpath('autoboot'))
        if not log:
            if os.name == 'nt':
                self.logfile = 'nul'
            else:
                self.logfile = '/dev/null'
        else:
            self.logfile = os.path.join(self.config.get_path(), file)
        cmd_string = '{} > {} 2>&1'.format(cmd_string, self.logfile)
        if daemon:
            cmd_string = '{} &'.format(cmd_string)
        LOGGER.debug('Hddldaemon cmd_string:{}'.format(cmd_string))
        LOGGER.info('Starting Hddldaemon')
        rv = subprocess.Popen(cmd_string, shell=True)
        time.sleep(3)
        self.parser_log = ParserLog(self.logfile, self)
        self.parser_log.start()
        while not self.ready:
            time.sleep(1)
            run_time += 1
            if run_time >= self.time_out:
                self.stop_run()
                raise RuntimeError('Hddldaemon boot error.TIMEOUT({})'.format(run_time))
        time.sleep(5)
        LOGGER.info('Hddldaemon is ready.')
        return rv

    def get_log(self):
        rv = None
        if self.logfile not in ['nul', '/dev/null', None]:
            if os.path.exists(self.logfile):
                rv = self.logfile
        return rv

    def stop_run(self):
        pids = get_allpid_with_name(self.process_name)
        LOGGER.debug('Will kill pids: {}'.format(pids))
        for pid in pids:
            try:
                p = psutil.Process(pid)
            except Exception:
                pass
            else:
                LOGGER.info('kill {}(Pid:{})'.format(p.name(), pid))
                p.terminate()
                time.sleep(3)
        time.sleep(3)
        if self.parser_log:
            self.parser_log.stop()


class Client(object):

    inf_type = [
            'AsyncTestV2',
            'AsyncWaitTestV2',
            'AsyncCallbackWaitV2',
            'AsyncThreadV2',
            'SyncTestV2',
            'SyncTestFromMemoryV2',
            'AsyncMemoryPoolTest',
        ]

    def __init__(self, log_path=None):
        self.log_path = log_path

    @classmethod
    def is_running(cls):
        pids = get_allpid_with_name(cls.process_name)
        if pids:
            return True
        return False

    def stop(self, pids):
        for pid in pids:
            try:
                p = psutil.Process(pid)
                LOGGER.debug('kill {}(Pid:{})'.format(p.name(), pid))
            except Exception:
                pass
            else:
                p.terminate()

    def inference(self, inf_type="AsyncTestV2", image_path=None, graph_path=None, runtime=None):
        if graph_path is None:
            graph_path = 'graphs/google_graph.blob'
            image_path = 'images/224x224/'
        inf_path = 'source_cpp/hal_demo/HAL_11/{}'.format(inf_type)
        _root_no_password("chmod 755 {}".format(inf_path))
        cmd = '{} -s {} -g {}'.format(inf_path, image_path, graph_path)
        run_cmd(cmd)


class ParserLog(object):
    """parser hddldaemon server logs"""
    device_index = ['deviceId', 'device', 'util%', 'thermal', 'scheduler', 'comment',
                    'resetTimes', 'cacheNum', 'cacheGraph0', 'cacheGraph1','cacheGraph2','cacheGraph3']

    def __init__(self, logfile, server=None):
        self.logfile = logfile
        self.pre_device_snapshot = []
        self.device_snapshot = []
        self.server = server
        self.parser_log_thread = None
        self.parser_log_thread_stop = False

    def get_device_snapshot(self):
        if len(self.device_snapshot) == len(self.device_index):
            return self.device_snapshot
        else:
            return self.pre_device_snapshot

    def is_ready(self):
        return self.ready

    def parser(self):
        LOGGER.info('\033[32mParsering Hddldaemon log.({})\033[0m'.format(self.logfile))
        with open(self.logfile) as f:
            while True:
                current_pos = f.tell()
                line = f.readline()
                if self.parser_log_thread_stop:
                    break
                if not line or line[-1] != '\n':
                    f.seek(current_pos)
                    time.sleep(1)
                else:
                    self._handle_line(line)

    def _handle_line(self, line):
        if 'SERVICE IS READY' in line:
            self.server.ready = True
        if line.startswith('|'):
            if self.device_index[0] in line:
                if len(self.device_index) == len(self.device_snapshot):
                    self.pre_device_snapshot = self.device_snapshot.copy()
                # print('pre_device_snapshot:', self.pre_device_snapshot)
                self.device_snapshot.clear()
            for index in self.device_index:
                if '| '+index+' ' in line:
                    valided = list(map(str.strip, line.split('|')[1:-1]))
                    self.device_snapshot.append(valided)

    def start(self):
        self.parser_log_thread = threading.Thread(target=self.parser)
        self.parser_log_thread.start()

    def stop(self):
        LOGGER.info('\033[32mParserLog Closed...\033[0m')
        self.parser_log_thread_stop = True

    def __str__(self):
        return str(self.device_snapshot)


class ServerConfig(object):
    """
    hddldaemon service/autoboot config read/write items class
    """
    # Regular expression for comments
    comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )
    configs = {
        'service': 'hddl_service.config',
        'autoboot': 'hddl_autoboot.config',
    }

    def __init__(self, path):
        self.__path = path
        if not os.path.exists(path):
            os.makedirs(path)

        config_path = get_hddl_install_dir()
        shutil.copy(os.path.join(config_path, 'config', self.configs['service']), self.__path)
        shutil.copy(os.path.join(config_path, 'config', self.configs['autoboot']), self.__path)

    def get_path(self):
        return self.__path

    def get_configpath(self, config_type=None):
        if config_type not in self.configs.keys():
            raise ValueError('config_type not in ({})'.format(self.configs.keys()))
        return os.path.join(self.__path, self.configs[config_type])

    def _get_json(self, config_type):
        if config_type == 'service':
            return self._parse_json(self.get_configpath('service'))
        elif config_type == 'autoboot':
            return self._parse_json(self.get_configpath('autoboot'))

    def _parse_json(self, file):
        """handle notes for /*fds
        af*/config file.eg:// or /*  */"""
        with open(file) as f:
            content = ''.join(f.readlines())
            match = self.comment_re.search(content)
            while match:
                content = content[:match.start()] + content[match.end():]
                match = self.comment_re.search(content)
            return json.loads(content)

    def modify_options(self, kw={}, config_type='service'):
        for option, option_value in kw.items():
            self.modify_option(option, option_value, config_type)

    def modify_option(self, option, option_value, config_type='service'):
        # if isinstance(options,dict) and len(options)>0:
        dict_json = self._get_json(config_type)  # handle comments,load json data to dict_json
        new_dictjson = self._find_option(dict_json, option, option_value)
        filename = self.get_configpath(config_type)
        with open(filename, "w") as f:
            json.dump(new_dictjson, f, indent=4)

    def _find_option(self, dict_json, option, option_value):
        for key, value in dict_json.items():
            if isinstance(dict_json[key], dict):
                self._find_option(dict_json[key], option, option_value)
            elif option == key:
                dict_json[option] = option_value
        return dict_json

    def get_value_by_option(self, option, config_type='service'):
        dict_json = self._get_json(config_type)
        return self._get_value_by_option(dict_json, option)

    def _get_value_by_option(self, dict_json, option):
        for key, value in dict_json.items():
            if isinstance(dict_json[key], dict):
                self._find_option(dict_json[key], option)
            elif option == key:
                return dict_json[option]

    def __str__(self):
        return '<{}> service path:{}\n config path:{}'.format(self.__class__,
                                                              self.get_configpath('service'),
                                                              self.get_configpath('autoboot'))


if __name__ == '__main__':
    # s = Server('01')
    # s.config.modify_option('mvnc_log_level', 0)
    # s.start_run()
    print(get_myx_count())