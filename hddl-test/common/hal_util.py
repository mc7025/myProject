import csv
import os
import subprocess
import shutil
import re
import sys
import time
import json

import psutil

from common.utils import run_cmd, get_allpid_with_name, LOGS_DIR, _root_no_password, get_hddl_bin_by_name, \
    get_hddl_install_dir
from config import BASE_DIR
try:
    from config import HDDL_SOURCE_DIR
except ImportError as e:
    print(e)
    HDDL_SOURCE_DIR = ''


GRAPH_DIR = os.path.join(BASE_DIR, "graphs")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
HAL_TEST_CODE = os.path.join(BASE_DIR, "source_cpp{}hal_demo".format(os.sep))
BUILD_BIN_DIR = os.path.join(HDDL_SOURCE_DIR,
                             "hddl-service-merged" + os.sep + "build" + os.sep + "output" + os.sep + "bin")
INTEL_OPENVINO_DIR = os.environ.get("INTEL_OPENVINO_DIR")
if not INTEL_OPENVINO_DIR:
    raise ValueError("NO SYSTEM VARIABLE OF INTEL_OPENVINO_DIR")
MODEL_DOWNLOAD = os.path.join(INTEL_OPENVINO_DIR, "deployment_tools{0}tools{0}model_downloader".format(os.sep))
MO_PATH = os.path.join(INTEL_OPENVINO_DIR, "deployment_tools{}model_optimizer".format(os.sep))
BUILD_SAMPLE_DIR = os.path.join(INTEL_OPENVINO_DIR, "inference_engine{}samples".format(os.sep))
BASE_CONFIG = {
            "server_max_task_number": "20000",
            "graph_identity": "name",
            "device_snapshot_mode": "full",
            "client_snapshot_mode": "base",
            "graph_snapshot_mode": "base",
        }


class ModifyDict(object):

    def __init__(self, kv={}):
        self.config = BASE_CONFIG.copy()
        self.kv = kv

    def add(self):
        for key, value in self.kv.items():
            self.config[key] = value
        return self.config

    def sub(self):
        for key, value in self.kv.items():
            self.config.pop(key)
        return self.config


class TestEnv(object):

    def __init__(self):
        self.graph_file = os.path.join(GRAPH_DIR, "google_graph.blob")
        self.graph_dir = os.path.join(GRAPH_DIR, "google")
        self.images = os.path.join(IMAGE_DIR, "224x224")
        self.image_target_dir = os.path.join(IMAGE_DIR, "pic")

    def copy_google_graph(self):
        if os.path.exists(self.graph_dir):
            shutil.rmtree(self.graph_dir)
        os.mkdir(self.graph_dir)
        for item in range(1, 103):
            shutil.copy(self.graph_file, os.path.join(self.graph_dir, "google{}.blob".format(str(item))))

    def copy_image(self):
        for item in range(16):
            target = os.path.join(self.image_target_dir, "google{}".format(str(item)))
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(self.images, target)

    @staticmethod
    def compile_graph():
        if Server.is_running():
            Server.stop_run()
        ie_dir = os.environ.get('InferenceEngine_DIR')
        if not ie_dir:
            raise ValueError('Not check EnvVar(HDDL_INSTALL_DIR),Please set it!')
        if os.name == "posix":
            bin_path = ""
            myriad_compile = os.path.join(ie_dir, "{0}{1}lib{1}intel64{1}myriad_compile".format(os.pardir, os.sep))
        else:
            bin_path = os.path.join(ie_dir, "{0}{1}bin{1}intel64{1}Release".format(os.pardir, os.sep))
            myriad_compile = "myriad_compile.exe"
        for item in ["google", "yolo"]:
            if item == "google":
                ir_file = os.path.join(GRAPH_DIR, "bvlc_goolgnet.xml")
                graph_file = os.path.join(GRAPH_DIR, "google_graph.blob")
            else:
                ir_file = os.path.join(GRAPH_DIR, "tiny_yolo_v1.xml")
                graph_file = os.path.join(GRAPH_DIR, "yolo_graph.blob")
            cmd = "{} -m {} -ip U8 -o {}".format(myriad_compile, ir_file, graph_file)
            if os.path.exists(graph_file):
                os.remove(graph_file)
            if os.name == "nt":
                os.chdir(bin_path)
            os.system(cmd)

    def setup_env(self):
        self.compile_graph()
        self.copy_google_graph()
        self.copy_image()

    def clean_env(self):
        if os.path.exists(self.graph_dir):
            shutil.rmtree(self.graph_dir)
        if os.path.exists(self.image_target_dir):
            shutil.rmtree(self.image_target_dir)


class BuildCode(object):

    def __init__(self, is_cmake=False):
        self.source_dir = HDDL_SOURCE_DIR
        self.build_dir = os.path.join(self.source_dir, "hddl-service-merged{}build".format(os.sep))
        self.is_cmake = is_cmake

    def build(self):
        if self.is_cmake:
            self.__cmake()
        self.__make()

    def __cmake(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.mkdir(self.build_dir)
        os.chdir(self.build_dir)
        # print("\n\033[1;45;32m Cmake ... \033[0m\n")
        run_cmd("cmake ..")

    def __make(self):
        os.chdir(self.build_dir)
        # print("\n\033[1;45;32m Make ... \033[0m\n")
        run_cmd("make clean")
        run_cmd("make -j8")


class CodeOperation(object):

    def __init__(self, test_case, is_cmake=False):
        self.test_case = test_case

        self.build = BuildCode(is_cmake=is_cmake)

    def run(self):
        # self.__mod_code()
        if self.__code_path():
            shutil.copy(self.__code_path(),
                        os.path.join(HDDL_SOURCE_DIR, "hddl-service-merged{0}api{0}test{0}{1}"
                                     .format(os.sep, os.path.split(self.__code_path())[1])))
        else:
            return False
        self.build.build()

    def __code_path(self):
        test_path = os.path.join(HAL_TEST_CODE, str(self.test_case))
        if os.path.exists(test_path):
            file_list = os.listdir(test_path)
            for file in file_list:
                if file[-3:] == "cpp":
                    file_path = os.path.join(test_path, file)
                    return file_path
        else:
            return False

    # def __mod_code(self):
    #     try:
    #         if self.__code_path():
    #             code_path = self.__code_path()
    #             dir_name = os.path.dirname(code_path)
    #             with open(code_path, "r") as f1:
    #                 content = f1.read()
    #             res = re.compile("\s+std::string\s+imgPath\s+=\s+\"(.*)\";")
    #             img = res.findall(content)
    #             img_str = os.path.join(IMAGE_DIR, "pic/google")
    #             target = os.path.join(dir_name, "target.cpp")
    #             if img:
    #                 with open(target, "w") as f2:
    #                     new_content = re.sub(img[0], img_str, content)
    #                     f2.write(new_content)
    #                 os.remove(code_path)
    #                 os.rename(target, code_path)
    #             else:
    #                 return False
    #     except FileNotFoundError as e:
    #         print(e)


class Model(object):

    def __init__(self, model_name, log_path):
        self.model_name = model_name
        self.log_path = log_path
        if not self.log_path:
            os.makedirs(self.log_path)
        self.log_file = os.path.join(self.log_path, "client.log")

    def download_model(self, output_dir):
        os.chdir(MODEL_DOWNLOAD)
        cmd = "{} --name {} -o {} > {}".format(sys.executable, self.model_name, output_dir, self.log_file)
        os.system(cmd)
        return

    def convert_cnn(self, framework="caffe", data_type="FP16", input_proto=None, input_model=None,
                    input_shape=None, output_dir=None, mean_file=None):
        os.chdir(MO_PATH)
        cmd = "{} mo.py --framework {} --data_type {} --input_proto {} --input_model {} --input_shape {} " \
              "--output_dir {} > {}".\
            format(sys.executable, framework, data_type, input_proto, input_model, input_shape, output_dir,
                   self.log_file)
        if mean_file:
            cmd = "{} mo.py --framework {} --data_type {} --input_proto {} --input_model {} --input_shape {} " \
              "--output_dir {} --mean_file {}> {}".\
                format(sys.executable, framework, data_type, input_proto, input_model, input_shape, output_dir,
                       mean_file, self.log_file)
        os.system(cmd)
        return


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
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)

        config_path = get_hddl_install_dir()
        shutil.copy(os.path.join(config_path, 'config', self.configs['service']), self.path)
        shutil.copy(os.path.join(config_path, 'config', self.configs['autoboot']), self.path)

    def get_configpath(self, config_type=None):
        if config_type not in self.configs.keys():
            raise ValueError('config_type not in ({})'.format(self.configs.keys()))
        return os.path.join(self.path, self.configs[config_type])

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


class Server(object):

    output_dir = LOGS_DIR

    if os.name == "nt":
        process_name = ['hddldaemon.exe', 'autoboot.exe']
        name = 'hddldaemon.exe'
    else:
        process_name = [r'^\d+\.\d+BOOT$', 'hddldaemon', 'autoboot']
        name = 'hddldaemon'

    def __init__(self, testcase):
        self.bin = os.path.join('bin', self.name)
        self.logfile = None
        self.config = ServerConfig(os.path.join(self.output_dir, str(testcase)))
        self.parser_log = None

    def is_ready(self):
        position = 0
        res = re.compile(".*SERVICE IS READY.*")
        timeout = 120
        while timeout > 0:
            with open(self.logfile) as f:
                f.seek(position)
                content = f.read()
                position = f.tell()
            if res.findall(content):
                return True
            time.sleep(3)
            timeout -= 3
        print("Server not ready.")
        return False

    @classmethod
    def is_running(cls):
        pids = get_allpid_with_name(cls.process_name)
        if pids:
            return True
        return False

    def start_run(self, daemon=False, file='server.log'):
        if self.is_running():
            self.stop_run()
        os.chdir(get_hddl_install_dir())
        cmd = '{} -c {} --boot-config {}'.format(self.bin, self.config.get_configpath('service'),
                                                 self.config.get_configpath('autoboot'))
        if daemon:
            cmd = '{} -d'.format(cmd)
        self.logfile = os.path.join(self.config.path, file)
        with open(self.logfile, "w") as f:
            rv = subprocess.Popen(cmd, shell=True, stdout=f)

    @classmethod
    def stop_run(cls):
        pids = get_allpid_with_name(cls.process_name)
        for pid in pids:
            try:
                p = psutil.Process(pid)
            except Exception:
                pass
            else:
                p.terminate()
                time.sleep(2)
        time.sleep(3)


class Client(object):

    process_name = [
            'AsyncTestV2',
            'AsyncWaitTestV2',
            'AsyncCallbackWaitV2',
            'AsyncThreadV2',
            'SyncTestV2',
            'SyncTestFromMemoryV2',
            'AsyncMemoryPoolTest',
            'benchmark_app',
        ]

    if os.name == "nt":
        process_name = [item + ".exe" for item in process_name]

    def __init__(self, log_path, thread_index=1):
        self.log_path = log_path
        self.thread_index = thread_index

    @classmethod
    def is_running(cls):
        pids = get_allpid_with_name(cls.process_name)
        # print('Found {} running pid({})'.format(cls.process_name, pids))
        if pids:
            return True
        return False

    def inference(self,
                  case_path,
                  case_name="AsyncTestV2",
                  image_path=None,
                  graph_path=None,
                  runtime=None,
                  graph_tag=None,
                  stream_id=None,
                  device_tag=None,
                  runtime_priority=None,
                  bind_device=False):
        if os.name == "posix":
            _root_no_password("chmod 755 {}".format(os.path.join(case_path, case_name)))
            source_name = case_name + ".cpp"
        else:
            case_name = case_name + ".exe"
            source_name = case_name.split(".")[0] + ".cpp"
        cmd = "{}{}{}".format(case_path, os.sep, case_name)
        if os.path.dirname(case_path) == HAL_TEST_CODE:
            with open(os.path.join(case_path, source_name), "r") as f:
                content = f.read()
            res = re.compile("\s+std::string\s+imgPath.*")
            img = res.findall(content)
            if img:
                img_p = os.path.join(IMAGE_DIR, "pic{}google".format(os.sep))
                cmd = "{} {}".format(cmd, img_p)
        if image_path:
            cmd = "{} -s {} -g {}".format(cmd, image_path, graph_path)
        if runtime:
            cmd = "{} -t {}".format(cmd, str(runtime))
        if graph_tag:
            cmd = "{} --graphTag {}".format(cmd, str(graph_tag))
        if stream_id:
            cmd = "{} --streamId {}".format(cmd, str(stream_id))
        if device_tag:
            cmd = "{} --deviceTag {} --bindDevice {}".format(cmd, str(device_tag), str(bind_device))
        if runtime_priority:
            cmd = "{} --runtimePriority {}".format(cmd, str(runtime_priority))
        print(cmd)
        with open("{}{}client{}.log".format(self.log_path, os.sep, str(self.thread_index)), 'w') as f:
            ret = subprocess.Popen(cmd, stdout=f, shell=True)

    def benchmark_app(self, case_path, case_name="benchmark_app",
                      image_path=os.path.join(IMAGE_DIR, "224x224{}imagenet12-ILSVRC2012_val_00000001.-224x224.bmp"
                                       .format(os.sep)),
                      ir_path=None,
                      run_type="HDDL"):
        if os.name == "nt":
            case_name += ".exe"
        os.chdir(case_path)
        cmd = "{} -i {} -m {} -d {}".format(case_name, image_path, ir_path, run_type)
        print(cmd)
        with open("{}{}client.log".format(self.log_path, os.sep), "w") as f:
            subprocess.Popen(cmd, stdout=f, shell=True)


class CheckResult(object):

    def __init__(self, log_path, thread_num=1):
        self.log_path = log_path
        self.thread_num = thread_num
        self.test_case = os.path.split(log_path)[1]
        self.result = {}
        self.result["TestCase"] = self.test_case
        self.result["Result"] = "Pass"
        self.result["Reason"] = []

    def server_is_running(self):
        if not Server.is_running():
            self.result["Result"] = "Fail"
            self.result["Reason"].append("Server abort.")
            return False
        return True

    def keywords(self, keywords=[]):
        with open(os.path.join(self.log_path, "server.log")) as f:
            content = f.read()
        for keyword in keywords:
            res = re.compile(".*{}.*".format(keyword))
            if not res.findall(content):
                self.result["Result"] = "Fail"
                self.result["Reason"].append("Can not find the [ {} ] in server log".format(keyword))
                return False
        return True

    def error_tasks(self):
        res = re.compile("error_tasks_number\s+=\s+\d+")
        if self.__split_client_log():
            content_list, len_list = self.__split_client_log()
            for index in range(self.thread_num):
                content = content_list[index]
                check_len = len_list[index]
                if not res.findall(content[-check_len:]):
                    self.result["Result"] = "Fail"
                    self.result["Reason"].append(
                        "client{}.log can not find the key word of error_tasks_number.".format(str(index + 1)))
                    return False
        else:
            return False
        return True

    def client_num(self, client_num=1):
        res = re.compile(".*clientId.*")
        res_num = re.compile("\d+")
        with open(os.path.join(self.log_path, "server.log")) as f:
            content = f.read()
        client_str = " ".join(res.findall(content))
        c_num = len(set(res_num.findall(client_str)))
        if c_num != client_num:
            self.result["Result"] = "Fail"
            self.result["Reason"].append("The num of client is wrong. the client num is : {}".format(c_num))
            return False
        return True

    def graph_num(self, graph_num=1):
        res = re.compile("Load graph success")
        with open(os.path.join(self.log_path, "server.log")) as f:
            content = f.read()
        g_num = len(res.findall(content))
        if g_num != graph_num:
            self.result["Result"] = "Fail"
            self.result["Reason"].append("Only {} graphs load to server.".format(g_num))
            return False
        return True

    def device_num(self, device_num=8):
        res = re.compile(".*deviceNum.*")
        res_num = re.compile("(\d+)\s+/\s+\d+")
        with open(os.path.join(self.log_path, "server.log")) as f:
            content = f.read()
        device_list = res.findall(content)
        index = 0
        if device_list:
            for item in device_list:
                all_num = 0
                elements = item.split("|")
                for ele in elements:
                    num_list = res_num.findall(ele)
                    if num_list:
                        d_num = int(num_list[0])
                        all_num += d_num
                if all_num != device_num:
                    index += 1
                else:
                    index = 0
                if index >= 3:
                    self.result["Result"] = "Fail"
                    self.result["Reason"].append("{} devices running well.".format(all_num))
                    return False
        return True

    def load_graph_time(self):
        res_r = re.compile(".*\d+:\d+:(\d+\.\d+).*RegisterClient.*")
        res_l = re.compile(".*\d+:\d+:(\d+\.\d+).*Graph\s+loaded\s+on\s+service.*")
        if self.__split_client_log():
            content_list, len_list = self.__split_client_log()
            t_list = []
            for index in range(self.thread_num):
                content = content_list[index]
                check_len = len_list[index]
                t_start = float(res_r.findall(content[:check_len])[0])
                t_end = float(res_l.findall(content[:check_len])[0])
                t = t_end - t_start
                t_list.append(round(t, 4))
                self.result["Reason"].append("The time of load graph is: [ {}-- {} ].".format(index, round(t, 4)))
            if self.test_case == "HAL_09":
                if t_list[0] > t_list[4] and t_list[1] > t_list[5] and t_list[2] > t_list[6] and t_list[3] > t_list[7]:
                    pass
                else:
                    self.result["Result"] = "Fail"
                    self.result["Reason"].append("The time of load graph is wrong.")
                    return False
        else:
            return False
        return True

    def memory(self):
        mem_start = self.__memory_info()
        time.sleep(64)
        mem_mid = self.__memory_info()
        mem = int(mem_mid - mem_start)
        if mem not in range(245, 266):
            self.result["Result"] = "Fail"
            self.result["Reason"].append("Used memory has increase [ {}MB ].".format(mem))
            return False
        while Client.is_running():
            time.sleep(5)
        mem_end = self.__memory_info()
        if mem_end not in range((mem_start - 10), (mem_start + 11)):
            self.result["Result"] = "Fail"
            self.result["Reason"].append("MemoryStart: {}MB != MemoryEnd: {}MB.".format(mem_start, mem_end))
            return False
        return True

    def all_device_running(self, device_num=8):
        res = re.compile(".*status.*")
        while Client.is_running():
            time.sleep(5)
        with open(os.path.join(self.log_path, "server.log")) as f:
            content = f.read()
        status_content = res.findall(content)[-6:]
        for device_status in status_content:
            status_record = re.sub(" +", "", device_status)
            status_list = status_record.split("|")
            d_num = 0
            for elements in status_list:
                if "RUNNING" in elements:
                    d_num += 1
            if d_num != device_num:
                self.result["Result"] = "Fail"
                self.result["Reason"].append("Only [{}] deivce are running.".format(d_num))
                return False
        return True

    def write_result(self):
        with open(os.path.join(LOGS_DIR, "hal_result.csv"), 'a') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([self.result["TestCase"], self.result["Result"], str(self.result["Reason"])])
        return True

    def no_error(self, log_name="client.log"):
        res = re.compile("fail|failed|Error|Fail|error|FAIL|[\[|:]ERR")
        res2 = re.compile("Latency.*|Throughput.*")
        with open(os.path.join(self.log_path, log_name)) as f:
            content = f.read()
        result_error = res.findall(content)
        result = res2.findall(content)
        if result:
            self.result["Reason"].append(str(result))
        if result_error:
            self.result["Result"] = "Fail"
            self.result["Reason"].append("Some error in client log file : [{}]".format(result_error))
            return False
        return True

    def model_file(self, model_name):
        model_path = self.get_model_path()
        prototxt_file = os.path.join(model_path, "{}.prototxt".format(model_name))
        caffemodel_file = os.path.join(model_path, "{}.caffemodel".format(model_name))
        if os.path.exists(prototxt_file) and os.path.exists(caffemodel_file):
            self.result["Result"] = "Fail"
            self.result["Reason"].append("Can not find the model file")
            return True
        return False

    def model_dim(self, model_name, dim):
        model_path = self.get_model_path()
        prototxt_file = os.path.join(model_path, "{}.prototxt".format(model_name))
        res = re.compile(".*dim:\s+(\d+).*")
        with open(prototxt_file) as f:
            content = f.read()
        dim_list = res.findall(content)
        if [dim_list[2], dim_list[3]] == dim:
            return True
        self.result["Result"] = "Fail"
        self.result["Reason"].append("The dim is worng : {} != {}".format([dim_list[2], dim_list[3]], dim))
        return False

    def ir_model(self, model_name, log_name="client.log"):
        res = re.compile("\[\s+SUCCESS\s+\]\s+Generated\s+IR\s+model.*")
        with open(os.path.join(self.log_path, log_name)) as f:
            content = f.read()
        result = res.findall(content)
        model_path = self.get_model_path()
        xml_file = os.path.join(model_path, "{}.xml".format(model_name))
        bin_file = os.path.join(model_path, "{}.bin".format(model_name))
        if result and os.path.exists(xml_file) and os.path.exists(bin_file):
            return True
        self.result["Result"] = "Fail"
        self.result["Reason"].append("ir model convert fail")
        return False

    def get_model_path(self, log_name="client.log"):
        res = re.compile("={9}\s+Replacing\s+text\s+in\s+(.*)\s+={9}")
        with open(os.path.join(self.log_path, log_name)) as f:
            content = f.read()
        path_str = res.findall(content)[0]
        if path_str:
            path = os.path.dirname(path_str)
            return path
        else:
            self.result["Result"] = "Fail"
            self.result["Reason"].append("Can not find the model path")
            return False

    def __split_client_log(self):
        content_list = []
        len_list = []
        for index in range(1, (self.thread_num + 1)):
            try:
                while Client.is_running():
                    time.sleep(5)
                with open(os.path.join(self.log_path, "client{}.log".format(str(index)))) as f:
                    content = f.read()
            except FileNotFoundError as e:
                self.result["Result"] = "Fail"
                self.result["Reason"].append("client{}.log [ {} ].".format(str(index), e))
                return False
            content_len = len(content)
            check_len = int(content_len / 4)
            content_list.append(content)
            len_list.append(check_len)
        return content_list, len_list

    @staticmethod
    def __memory_info():
        output = run_cmd("free")
        mem_log = re.sub(' +', ' ', output.strip())
        mem_str = mem_log.split(" ")[7]
        mem = int(int(mem_str) / 1024)
        return mem


if __name__ == "__main__":
    config = ModifyDict()
    print(config)
