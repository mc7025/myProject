"""
A test for linux os
"""
import os
import platform
import unittest
from common.utils import run_cmd, get_myx_count
from config import LINUX_VERSION, KERNEL_VERSION, DEVICE_NUM, DEBUG
import logging
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


class OsTest(unittest.TestCase):

    def test_OS001(self):
        """Check OS version"""
        if os.name == 'nt':
            win_version = platform.platform()
            rel, vers, csd, ptype = win_version.split('-')
            self.assertEqual(rel, 'Windows')
            self.assertEqual(vers, '10')
            os_version = win_version
        else:
            actual = platform.dist()
            self.assertTupleEqual(LINUX_VERSION, actual)
            os_version = actual
        LOGGER.info('Verion of current OS: {}'.format(os_version))

    @unittest.skipIf(os.name == 'nt', 'Windows will skip the case')
    def test_OS002(self):
        """Check kernel version"""
        actual = platform.release().split("-")[0]
        self.assertEqual(KERNEL_VERSION, actual)
        LOGGER.info('Verion of current Kernel: {}'.format(actual))

    def test_OS003(self):
        """Check OpenVINO verion"""
        # duck test
        hddl_install_dir = os.environ.get('HDDL_INSTALL_DIR')

        self.assertIsNotNone(hddl_install_dir, 'msg="\033[31m No install Openvino or'
                                            'No source Openvino environment vars!\033[0m"')
        rv = self._get_parent_path(hddl_install_dir, 4)
        opvn_version = rv.split("_")[-1]
        LOGGER.info('Verion of current OpenVINO: {}'.format(opvn_version))

    def _get_parent_path(self, path, cs):
        for _ in range(cs):
            path = os.path.dirname(path)
        return path

    @unittest.skipIf(os.name == 'nt', 'Windows will skip the case')
    def test_OS004(self):
        """Check the VSC/ION driver"""
        out = run_cmd("lsmod | grep myd_vsc")
        self.assertNotEqual(out, "", msg="\033[31m not found myd_vsc driver\033[0m")
        out = run_cmd("lsmod | grep myd_ion")
        self.assertNotEqual(out, "", msg="\033[31m not found myd_ion driver\033[0m")

    @unittest.skipIf(os.name == 'nt', 'Windows will skip the case')
    def test_OS005(self):
        """Check the ION device"""
        out = run_cmd("ls /dev/ion")
        self.assertNotEqual(out, "", msg="\033[31m not found myd_vsc device\033[0m")

    def test_OS006(self):
        """Check Myx count"""
        devices_count = get_myx_count()[0]
        self.assertEqual(int(DEVICE_NUM), devices_count, msg="Expected device:{},"
                                                             "actualed device:{}".format(
            DEVICE_NUM, devices_count
        ))


# class WinOSTest(unittest.TestCase):
#
#     @unittest.skip('aa')
#     def test_Win001(self):
#         """Check  OS version"""
#         win_version = platform.platform()
#         rel, vers, csd, ptype = win_version.split('-')
#         self.assertEqual(rel, 'Windows')
#         self.assertEqual(vers, '10')
#         LOGGER.info('OS current version: {}'.format(win_version))
#
#     @unittest.skip('aa')
#     def test_Win002(self):
#         import wmi
#         c = wmi.WMI()
#         rv = c.Win32_USBControllerDevice()
#         print(rv)
    # def test_OS006(self):
    #     """Verify the function of ion"""
    #     current_pwd = os.getcwd()
    #     lib_path = os.path.join(HDDL_SOURCE_DIR, 'hddl-mvnc/mvnc/libion')
    #     os.chdir(lib_path)
    #     out = run_cmd('make test && ./test')
    #     os.chdir(current_pwd)
    #     self.assertNotEqual(out, "")
