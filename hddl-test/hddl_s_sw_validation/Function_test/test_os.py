"""
A test for linux os
"""
import platform
import os
import time
import unittest
import subprocess

from .config import (LINUX_VERSION, GCC_VERSION, GPP_VERSION, PYTHON_VERSION, OPENVINO_VERSION,
                     OPENCL_VERSION, HDDL_R_VERSION, OPENCV_SOURCE_DIR, OPENCV_VERSION, KERNEL_VERSION,
                     )


def run_cmd(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        raise ValueError("Cmd error:({})\n{}".format(cmd, output))
    return output


def rmmodprobe(drive_name, times):
    """rmmod/modprobe driverName N times"""
    try:
        for i in range(times):
            run_cmd("sudo rmmod {}".format(drive_name))
            time.sleep(0.5)
            run_cmd("sudo modprobe {}".format(drive_name))
            time.sleep(0.5)
    except Exception as e:
        print(e)
        return False
    else:
        return True


class OsTest(unittest.TestCase):

    def test_OS001(self):
        """Check OS version"""
        actual = platform.dist()
        self.assertTupleEqual(LINUX_VERSION, actual)

    def test_OS002(self):
        """Check compile tool version"""
        # check gcc version
        actual = run_cmd("gcc -dumpversion")
        self.assertGreaterEqual(actual, GCC_VERSION)
        # check g++ version
        actual = run_cmd("g++ -dumpversion")
        self.assertGreaterEqual(actual, GPP_VERSION)
        # check python version
        actual = platform.python_version()
        self.assertGreaterEqual(actual, PYTHON_VERSION)

    def test_OS003(self):
        """Check OpenVINO version"""
        self.assertTrue(os.path.exists("".join(("/opt/intel/computer_vision_sdk_",
                                                OPENVINO_VERSION))))

    def test_OS004(self):
        """Check OpenCL version"""
        with open(r"/opt/intel/opencl-sdk/version.txt") as f:
            contents = f.readline()
        actual = contents.rstrip("\n").split("=")[1]
        self.assertEqual(OPENCL_VERSION, actual)

    def test_OS005(self):
        """Check HDDL-R version"""
        out = run_cmd("rpm -qa | grep HDDL-R")
        actual = out.split("-")[-1][0:-7]
        self.assertEqual(HDDL_R_VERSION, actual)

    def test_OS006(self):
        """Check OpenCV version"""
        cur_dir = os.getcwd()
        os.chdir(OPENCV_SOURCE_DIR)
        actual = run_cmd("git rev-parse HEAD")
        os.chdir(cur_dir)
        self.assertEqual(OPENCV_VERSION, actual)

    def test_OS007(self):
        """Check kernel version"""
        actual = platform.release().split("-")[0]
        self.assertEqual(KERNEL_VERSION, actual)

    def test_OS008(self):
        """Check Support ASM1042 driver integrated into kernel module"""
        out = run_cmd(r'lspci | grep "ASM1042A USB 3.0 Host Controller"')
        self.assertIsNotNone(out)

    def test_OS009(self):
        """Verify the function of ASM1042"""
        count = run_cmd(r'lspci | grep "ASM1042A USB 3.0 Host Controller" | wc -l')
        lines = run_cmd(r'lspci -xxx | grep -A4 "ASM1042A USB 3.0 Host Controller" | wc -l')
        self.assertEqual(int(count) * 6 - 1, int(lines))

    def test_OS010(self):
        """Check the i2c_i801 driver"""
        out = run_cmd("lsmod | grep i2c_i801")
        self.assertIsNotNone(out, "not found i2c_i801 driver")

    def test_OS011(self):
        """rmmod/modprobe i2c_i801 10 times"""
        rv = rmmodprobe("i2c_i801", 10)
        self.assertTrue(rv)

        out = run_cmd("lsmod | grep i2c_i801")
        self.assertIsNotNone(out)

    def test_OS012(self):
        """Check the SMBus device"""
        actual = run_cmd("lspci | grep SMBus")
        self.assertIn("SMBus", actual)

    @unittest.skip("Need to confirm the test difference between coffelake and hddl-s module")
    def test_OS013(self):
        """Verify the function of SMBus"""
        pass

    def test_OS014(self):
        """Check the VSC driver"""
        out = run_cmd(" lsmod | grep myd_vsc")
        self.assertNotEqual(out, "")

    def test_OS015(self):
        """rmmod/modprobe myd_vsc 10 times"""
        rv = rmmodprobe("myd_vsc", 10)
        self.assertTrue(rv)

        out = run_cmd("lsmod | grep myd_vsc")
        self.assertIsNotNone(out)

    def test_OS016(self):
        """Check the VSC device"""
        out = run_cmd("dmesg | grep vsc")
        self.assertNotEqual(out, "", msg="\033[31m not found myd_vsc device\033[0m")

    def test_OS017(self):
        """Check the ion driver"""
        out = run_cmd("lsmod | grep ion")
        self.assertNotEqual(out, "")

    def test_OS018(self):
        """rmmod/modprobe myd_ion 10 times"""
        rv = rmmodprobe("myd_ion", 10)
        self.assertTrue(rv)

        out = run_cmd("lsmod | grep myd_ion")
        self.assertIsNotNone(out)

    def test_OS019(self):
        """Check the ION device"""
        out = run_cmd("ls /dev/ion")
        self.assertNotEqual(out, "", msg="\033[31m not found myd_vsc device\033[0m")

    @unittest.skip("Need to confirm the test difference between coffelake and hddl-s module")
    def test_OS020(self):
        """Verify the function of ion"""
        pass
    

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(OsTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)