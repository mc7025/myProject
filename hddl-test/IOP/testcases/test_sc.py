import os
import unittest
import time
import logging
from common.utils import Server, ResetDevice, ParserLog, get_current_func_name
from config import DEBUG, CARD_TYPE
from common.utils import Client, _root_no_password, BslReset, get_myx_count, BASE_DIR

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
file_hdl = logging.FileHandler('{}/log.log'.format(BASE_DIR))
file_hdl.setLevel(logging.DEBUG)
file_hdl.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.addHandler(file_hdl)


class SCTest(unittest.TestCase):

    restore_time_for_one_device = 20
    parser_log_wait_time = 45
    card_type = {
        'RVP': 'mcu',
        'UZEL': 'io',
        'IEI': 'io',
    }

    @classmethod
    def setUpClass(cls):
        cls.device_count = get_myx_count()[0]
        cls.device_mode = cls.card_type[CARD_TYPE]

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

    # @unittest.skip("aa")
    def test_SC001(self):
        """Check unique ID"""
        RUN_TIMES = 50
        device_ids = []
        case_id = get_current_func_name()[5:]
        for i in range(RUN_TIMES):
            self._run_server('{}_{}'.format(case_id, i), config={'mvnc_log_level': 0})
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

    # @unittest.skip("aaa")
    def test_SC002(self):
        """Boot up  MYDX"""
        RUN_TIMES = 50
        rv = None
        case_id = get_current_func_name()[5:]
        for i in range(RUN_TIMES):
            self._run_server('{}_{}'.format(case_id, i))
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

    # @unittest.skip("aaa")
    def test_SC003(self):
        """Bsl reset whole HDDL-R AIC"""
        RUN_TIMES = 50
        case_id = get_current_func_name()[5:]
        # _root_no_password('dmesg -c')
        bsl_reset = BslReset()
        for i in range(1, RUN_TIMES):
            server = Server(case_id)
            server.start_run()
            server.stop_run()
            out = get_myx_count()[1]
            self.assertEqual(self.device_count, out)
            bsl_reset.reset_all()
            if os.name == 'nt':
                time.sleep(10)
            else:
                time.sleep(1)
            booted, unbooted = get_myx_count()[1:]
            self.assertEqual(0, booted)
            self.assertEqual(self.device_count, unbooted)
            LOGGER.info('Ran BslReset {} times'.format(i))

    # @unittest.skip("aaa")
    def test_SC003_with_hddldaemon(self):
        RUN_TIMES = 50
        case_id = get_current_func_name()[5:]
        try:
            self._run_server('{}'.format(case_id), stop=False)
            reset = BslReset()
            pre_result = [0] * self.device_count
            restore_time = min(self.restore_time_for_one_device * self.device_count, 60)
            for i in range(1, RUN_TIMES):
                reset.reset_all()
                time.sleep(restore_time)
                result = self.server.parser_log.get_device_snapshot()[6][1:]
                result = [int(i) for i in result]
                result.sort()
                LOGGER.debug('pre_resettimes:{},cur_resettimes:{}'.format(pre_result, result))
                self.assertGreater(result, pre_result)
                self.assertEqual(len(result), self.device_count)
                pre_result = result.copy()
                LOGGER.info('Reset all device {} times({})'.format(i, result))
        finally:
            self.server.stop_run()
            self.server.parser_log.stop()

    # @unittest.skip("aaa")
    def test_SC004(self):
        """Hard reset each MYDX"""
        RUN_TIMES = 50
        case_id = get_current_func_name()[5:]

        # _root_no_password('dmesg -c')
        self._run_server('{}'.format(case_id), stop=False)
        # waitting parser log read log
        try:
            device_ids = self._get_device_id(self.server.parser_log.get_device_snapshot()[0])
        except IndexError:
            raise ValueError('please set device_snapshot_mode: full')
        device_ids = [int(did) for did in device_ids]
        LOGGER.info('Device ids: {}'.format(device_ids))
        self.server.parser_log.stop()
        self.server.stop_run()

        bsl_reset = BslReset()
        for times in range(1, RUN_TIMES):
            server = Server('{}_{}'.format(case_id, times))
            server.start_run()
            server.stop_run()
            out = get_myx_count()[1]
            self.assertEqual(self.device_count, out)
            for i, did in enumerate(device_ids):
                bsl_reset.reset_device(did, self.device_mode)
                if os.name == 'nt':
                    time.sleep(10)
                else:
                    time.sleep(1)
                booted, unbooted = get_myx_count()[1:]
                self.assertEqual(self.device_count-i-1, booted)
                self.assertEqual(i+1, unbooted)
            LOGGER.info('Ran BslReset {} times'.format(times))

    # @unittest.skip("aaa")
    def test_SC004_with_hddldaemon(self):
        RUN_TIMES = 50
        case_id = get_current_func_name()[5:]
        try:
            self._run_server('{}'.format(case_id), stop=False)
            # waitting parser log read log
            try:
                device_ids = self._get_device_id(self.server.parser_log.get_device_snapshot()[0])
            except IndexError:
                raise ValueError('please set device_snapshot_mode: full')
            LOGGER.info('Device ids: {}'.format(device_ids.sort()))
            reset = BslReset()
            pre_result = [0] * self.device_count
            restore_time = min(self.restore_time_for_one_device * self.device_count, 60)
            for i in range(1, RUN_TIMES):
                for did in device_ids:
                    reset.reset_device(did, self.device_mode)
                    time.sleep(5)
                time.sleep(restore_time)
                result = self.server.parser_log.get_device_snapshot()[6][1:]
                result = [int(i) for i in result]
                result.sort()
                LOGGER.debug('pre_resettimes:{},cur_resettimes:{}'.format(pre_result, result))
                self.assertGreater(result, pre_result)
                self.assertEqual(len(result), self.device_count)
                pre_result = result.copy()
                LOGGER.info('Reset device {} times({})'.format(i, result))
        finally:
            self.server.stop_run()
            self.server.parser_log.stop()

    # @unittest.skip("aaa")
    def test_SC005(self):
        """Soft reset each MYDX"""
        RUN_TIMES = 50
        case_id = get_current_func_name()[5:]
        rv = None
        try:
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
                boot_device_count = get_myx_count()[1]
                LOGGER.info('Ran {} times.'.format(i))
                self.assertEqual(self.device_count, boot_device_count)
                self.assertTrue(rv)
        finally:
            self.server.stop_run()
            self.server.parser_log.stop()


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