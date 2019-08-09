import re
import time
import os
import glob
import subprocess
import unittest
import sys
import threading
from common.IOP_IE_Util import LOGS_DIR

if sys.version_info.major != 3:
    print("\033[33mPlease use python 3.xxx!\033[0m")
    exit(1)

from common.IOP_IE_Util import HDDL_INSTALL_DIR, MODEFILEPATH, IMAGPATH, NETWORKPATH, MO_OUTPUT, MO_PRIVATE_PUBLIC_CNN

if os.name == "nt":
    if os.path.exists(MO_OUTPUT):
        os.system("rmdir /S /Q {}/*".format(MO_OUTPUT))
else:
    if os.path.exists(MO_OUTPUT):
        os.system("rm -rf {}/*".format(MO_OUTPUT))

class AboutHddldaemon(object):
    
    save_path = LOGS_DIR
    config_path = os.path.join(HDDL_INSTALL_DIR,"config")

    @classmethod
    def runHddldaemon(cls):
        AboutHddldaemon.kill_server()
        if os.name == "nt":
            hddldaemon_exe = os.path.join(HDDL_INSTALL_DIR, "bin/hddldaemon.exe")
            cmd = hddldaemon_exe + " > " + "{}/hddldaemon.log".format(cls.save_path)
            t = threading.Thread(target=lambda cmd:os.system(cmd), args=(cmd,))
            t.setDaemon(True)
            t.start()
            pass
        else:
            os.system("{0}/bin/hddldaemon 2>&1 > {1}/hddldaemon.log&".format(HDDL_INSTALL_DIR,cls.save_path))

    @staticmethod
    def kill_server():
        if os.name == "nt":
            status = os.system("tasklist|findstr hddldaemon")
            while not status:
                os.system(r'taskkill /F /IM hddldaemon.exe')
                os.system(r'taskkill /F /IM autoboot.exe')
                status = os.system("tasklist|findstr hddldaemon")
        else:
            cmd = """for pid in `ps -ef|grep -e "autoboot\|hddldaemon" |grep -v "grep"|awk '{print $2}'`;do kill -9 $pid;done"""
            os.system(cmd)
        

class DL_MO_test(unittest.TestCase):

    def setUp(self):
        AboutHddldaemon.runHddldaemon()

    def tearDown(self): 
        AboutHddldaemon.kill_server()
        

for values in MO_PRIVATE_PUBLIC_CNN.map_network_re.values():
    for value in values:
        if value in MO_PRIVATE_PUBLIC_CNN.public_network:
            if value in ("yolov2","tiny_yolo_v2","faster_rcnn"):
                exec("""def test_{0}(self):\
                          test_c = MO_PRIVATE_PUBLIC_CNN();\
                          cmd1=test_c.convert_cmd('{0}','{1}');\
                          cmd2=test_c.do_inference_cmd('{0}');\
                          self.assertEqual(MO_PRIVATE_PUBLIC_CNN.run_cmd(cmd1,'{0}'),0,'There are some error or fail occurred in test progress, please check..');\
                          self.assertEqual(MO_PRIVATE_PUBLIC_CNN.run_cmd(cmd2,'{0}'),0,'There are some error or fail occurred in test progress, please check..');
                     """.format(value,"tf"))
            else:
                exec("""def test_{0}(self):\
                            test_c = MO_PRIVATE_PUBLIC_CNN();\
                            cmd1 = test_c.convert_cmd('{0}');\
                            cmd2 = test_c.do_inference_cmd('{0}');\
                            self.assertEqual(MO_PRIVATE_PUBLIC_CNN.run_cmd(cmd1,'{0}'),0,'There are some error or fail occurred in test progress, please check..');\
                            self.assertEqual(MO_PRIVATE_PUBLIC_CNN.run_cmd(cmd2,'{0}'),0,'There are some error or fail occurred in test progress, please check..');
                     """.format(value))
        else:
            exec("""def test_{0}(self):\
                        test_c = MO_PRIVATE_PUBLIC_CNN();\
                        cmd1 = test_c.do_inference_cmd('{0}');\
                        self.assertEqual(MO_PRIVATE_PUBLIC_CNN.run_cmd(cmd1,'{0}'),0,'There are some error or fail occurred in test progress, please check..');
                 """.format(value))
        exec("DL_MO_test.test_{0} = test_{0}".format(value))
    
    
if __name__ == "__main__":
    unittest.main()
