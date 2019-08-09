import unittest
import time
import logging
from common.utils import Server, ResetDevice, ParserLog, get_current_func_name, run_cmd
from config import DEBUG
from common.utils import Client

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


class SCTest(unittest.TestCase):

    restore_time_for_one_device = 20
    parser_log_wait_time = 45

    @classmethod
    def setUpClass(cls):
        cls.device_count = cls._get_device_count()
        LOGGER.info('Found device count:{}'.format(cls.device_count))

    @classmethod
    def _get_device_count(cls):
        return int(run_cmd('lsusb | grep "03e7" | wc -l'))

    def _run_server(self, case_id, config={}, run_time=30, stop=True):
        self.server = Server(case_id)
        self.server.config.modify_option('device_snapshot_mode', 'full')
        self.server.config.modify_option('total_device_num', str(self.device_count), 'autoboot')
        for option, option_value in config.items():
            self.server.config.modify_option(option, option_value)
        self.server.start_run(file='{}_server.log'.format(case_id))
        time.sleep(run_time)
        if stop:
            self.server.stop_run()

    def _get_device_id(self, device_ids):
        device_ids = device_ids[1:]
        return [device_id.split('(')[0] for device_id in device_ids]

    @unittest.skip("aa")
    def test_SC001(self):
        """Check unique ID"""
        RUN_TIMES = 20
        device_ids = []
        case_id = get_current_func_name()[5:]
        LOGGER.info('Begin run:{}'.format(case_id))

        for i in range(RUN_TIMES):
            self._run_server('{}_{}'.format(case_id, i), config={'mvnc_log_level': 0})
            time.sleep(self.parser_log_wait_time)
            with open(self.server.get_log()) as f:
                for line in f:
                    LOGGER.debug('{}'.format(line))
                    if 'SERVICE IS READY' in line:
                        break
                    elif 'Device ID is' in line:
                        device_ids.append(int(line.split(' ')[-1].strip()))
            LOGGER.info('Ran {} times.Device_Ids:{}'.format(i, device_ids))
            # device id is unique
            self.assertEqual(len(device_ids), len(set(device_ids)), ''.format(device_ids))
            # device count equals cls.device_count
            self.assertEqual(len(device_ids), self.device_count)
            device_ids.clear()
            # device_ids.sort()
            # device id must be continuous
            # self.assertEqual(device_ids, list(range(device_ids[0], device_ids[0] + len(device_ids))),
            #                  'device id must continus int,actual({})'.format(device_ids))

    @unittest.skip("aaa")
    def test_SC002(self):
        """Boot up  MYDX"""
        RUN_TIMES = 20
        rv = None
        case_id = get_current_func_name()[5:]
        for i in range(RUN_TIMES):
            self._run_server('{}_{}'.format(case_id, i))
            time.sleep(self.parser_log_wait_time)
            with open(self.server.get_log()) as f:
                for line in f:
                    if 'SERVICE IS READY' in line:
                        rv = True
                        break
                    elif 'ERROR' in line:
                        rv = False
            LOGGER.info('Ran {} times.'.format(i))
            # can normally start hddldamon
            self.assertTrue(rv)

    @unittest.skip("aaa")
    def test_SC003(self):
        """Hard reset whole HDDL-R AIC"""
        RUN_TIMES = 30
        case_id = get_current_func_name()[5:]

        self._run_server('{}'.format(case_id), stop=False)
        parser = ParserLog(self.server.get_log())
        parser.start()
        # waitting parser log read log
        time.sleep(self.parser_log_wait_time)

        try:
            device_ids = self._get_device_id(parser.get_device_snapshot()[0])
        except IndexError:
            raise ValueError('please set device_snapshot_mode: full')
        rs = ResetDevice()
        restore_time = min(self.restore_time_for_one_device * self.device_count, 60)
        try:
            for i in range(1, RUN_TIMES):
                for device_id in device_ids:
                    rs.reset(device_id)
                time.sleep(restore_time)
                result = parser.get_device_snapshot()[6][1:]
                LOGGER.info('reset {} times({})'.format(i, result))
                self.assertEqual([str(i)]*len(result), result)
        finally:
            self.server.stop_run()
            parser.stop()

    def test_SC003_with_inference(self):
        RUN_TIMES = 30
        case_id = get_current_func_name()[5:]

        self._run_server('{}'.format(case_id), stop=False)
        parser = ParserLog(self.server.get_log())
        parser.start()
        # waitting parser log read log
        time.sleep(self.parser_log_wait_time)

        clinet = Client()
        pids = clinet.is_running()
        if pids:
            clinet.stop(pids)
        clinet.inference()
        try:
            device_ids = self._get_device_id(parser.get_device_snapshot()[0])
        except IndexError:
            raise ValueError('please set device_snapshot_mode: full')
        rs = ResetDevice()
        restore_time = min(self.restore_time_for_one_device * self.device_count, 60)
        LOGGER.info('Set device restore time is {}s'.format(restore_time))
        try:
            for i in range(1, RUN_TIMES):
                for device_id in device_ids:
                    rs.reset(device_id)
                time.sleep(restore_time)
                result = parser.get_device_snapshot()[6][1:]
                LOGGER.info('reset {} times({})'.format(i, result))
                self.assertEqual([str(i)] * len(result), result)
        finally:
            pids = clinet.is_running()
            if pids:
                clinet.stop(pids)
            self.server.stop_run()
            parser.stop()

    @unittest.skip("aaa")
    def test_SC004(self):
        """Hard reset each MYDX"""
        RUN_TIMES = 30
        case_id = get_current_func_name()[5:]

        self._run_server('{}'.format(case_id), stop=False)
        parser = ParserLog(self.server.get_log())
        parser.start()
        # waitting parser log read log
        time.sleep(self.parser_log_wait_time)

        try:
            device_ids = self._get_device_id(parser.get_device_snapshot()[0])
        except IndexError:
            raise ValueError('please set device_snapshot_mode: full')
        rs = ResetDevice()
        try:
            for index, device_id in enumerate(device_ids):
                for i in range(1, RUN_TIMES):
                    rs.reset(device_id)
                    time.sleep(self.restore_time_for_one_device)
                    result = parser.get_device_snapshot()[6][1:]
                    LOGGER.info('reset {}-{} times, ({})'.format(device_id, i, result))
                    result = [int(device_id) for device_id in result]
                    result.sort()
                    LOGGER.debug('i:{}.index:{},result:{}'.format(i, index, result))
                    self.assertEqual(i, result[len(result)-index-1])
        finally:
            self.server.stop_run()
            parser.stop()

    @unittest.skip("aaa")
    def test_SC004_with_inference(self):
        RUN_TIMES = 30
        case_id = get_current_func_name()[5:]

        self._run_server('{}'.format(case_id), stop=False)
        parser = ParserLog(self.server.get_log())
        parser.start()
        # waitting parser log read log
        time.sleep(self.parser_log_wait_time)
        clinet = Client()
        pids = clinet.is_running()
        if pids:
            clinet.stop(pids)
        clinet.inference()
        try:
            device_ids = self._get_device_id(parser.get_device_snapshot()[0])
        except IndexError:
            raise ValueError('please set device_snapshot_mode: full')
        rs = ResetDevice()
        try:
            for index, device_id in enumerate(device_ids):
                for i in range(1, RUN_TIMES):
                    rs.reset(device_id)
                    time.sleep(self.restore_time_for_one_device)
                    result = parser.get_device_snapshot()[6][1:]
                    LOGGER.info('reset {}-{} times, ({})'.format(device_id, i, result))
                    result = [int(device_id) for device_id in result]
                    result.sort()
                    LOGGER.debug('i:{}.index:{},result:{}'.format(i, index, result))
                    self.assertEqual(i, result[len(result) - index - 1])
        finally:
            pids = clinet.is_running()
            if pids:
                clinet.stop(pids)
            self.server.stop_run()
            parser.stop()

    @unittest.skip("aaa")
    def test_SC005(self):
        """Soft reset each MYDX"""
        RUN_TIMES = 30
        case_id = get_current_func_name()[5:]
        rv = None
        for i in range(RUN_TIMES):
            self._run_server('{}_{}'.format(case_id, i))
            with open(self.server.get_log()) as f:
                for line in f:
                    if 'SERVICE IS READY' in line:
                        rv = True
                        break
                    elif 'ERROR' in line:
                        rv = False
            # can normally start hddldamon
            boot_device_count = int(run_cmd('lsusb| grep "f63b"|wc -l'))
            LOGGER.info('Ran {} times.'.format(i))
            self.assertEqual(self.device_count, boot_device_count)
            self.assertTrue(rv)


# class SampleTest(unittest.TestCase):
#
#         base_dir = os.path.join(HDDL_SOURCE_DIR, 'hddl-samples')
#
#     def setUpClass(cls):
#         if not os.path.exists(cls.base_dir):
#             raise ValueError('HDDL Sample source Dir not exists')
#         current_pwd = os.getcwd()
#         os.chdir(os.path.join(cls.base_dir,))
#         _root_no_password('')
#
#     def test_barrier(self):
#         pass
#
#     def test_cross_road(self):
#         pass
#
#     def test_indoor(self):
#         pass