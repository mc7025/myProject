import os
import time
import threading
import unittest
import sys

if sys.version_info.major != 3:
    print("\033[33mPlease use python 3.xxx!\033[0m")
    exit(1)
from common.IOP_IE_Util import benchmark_app,benchmark_app_C_S,classification_as,IMAGPATH,NETWORKPATH
from common.IOP_IE_Util import AboutHddldaemon, run_cmd, check_res, q, device

class SanityIE(unittest.TestCase):
    
    def test_case001(self):
        """10 client run 5 times"""
        t = []
        AboutHddldaemon.run_Hddldaemon()
        cmd = benchmark_app + " -m " + os.path.join(NETWORKPATH,"googlenetv2.xml") + " -i " + IMAGPATH + "/224x224/imagenet12-ILSVRC2012_val_00000001.-224x224.bmp -d {} -nireq 10 -niter 1000".format(device)
        for i in range(5):
            for j in range(10):
                tt = threading.Thread(target=run_cmd, args=(cmd,"case001"))
                t.append(tt)
                tt.start()
            for tt in t:
                tt.join()
        AboutHddldaemon.kill_server()
        self.assertEqual(check_res(q,"case001"),0,"There are some error in logs, please check the relevant log")

    def test_case002(self):
        """fcfs scheduler 10 client 5 times """
        t = []
        AboutHddldaemon.alter_config(regx_str = '"task_scheduler":\s+"\w+",', value = '"task_scheduler":              "fcfs",', filename="hddl_service.config")
        AboutHddldaemon.alter_config(filename="hddl_autoboot.config")
        AboutHddldaemon.run_special_Hddldaemon()
        cmd = benchmark_app + " -m " + os.path.join(NETWORKPATH,"googlenetv2.xml") + " -i " + IMAGPATH + "/224x224/imagenet12-ILSVRC2012_val_00000001.-224x224.bmp -d {} -nireq 10 -niter 1000".format(device)
        for i in range(5):
            for j in range(10):
                tt = threading.Thread(target=run_cmd, args=(cmd,"case002"))
                t.append(tt)
                tt.start()
            for tt in t:
                tt.join()
        AboutHddldaemon.kill_server()
        result = check_res(q,"case_002","FCFS")
        if result == 2:
            self.assertFalse(2, "The keywords FCFS don't find in log")
        elif result == 1:
            self.assertFalse(1, "There are some error in logs, please check the relevant log")

    def test_case003(self):
        """1 or 8 devices 10 client"""
        t = []
        AboutHddldaemon.alter_config(filename="hddl_service.config")
        AboutHddldaemon.alter_config(regx_str = '"total_device_num":\s+\d+', value = '"total_device_num":            1', filename="hddl_autoboot.config")
        AboutHddldaemon.run_special_Hddldaemon()
        cmd = classification_as + " -m " + os.path.join(NETWORKPATH,"googlenetv2.xml") + " -i " + IMAGPATH + "/224x224/imagenet12-ILSVRC2012_val_00000001.-224x224.bmp -d {} -ni 5000 -nireq 60".format(device)
        start_t0 = time.time()
        for j in range(10):
            tt = threading.Thread(target=run_cmd, args=(cmd,"case003_1"))
            t.append(tt)
            tt.start()
        for tt in t:
            tt.join()
        elapse_time0 = time.time() - start_t0
        AboutHddldaemon.kill_server()
        self.assertEqual(check_res(q,"case_003_01"),0,"There are some error in logs, please check the relevant log")
        AboutHddldaemon.run_Hddldaemon()
        start_t0 = time.time()
        for j in range(10):
            tt = threading.Thread(target=run_cmd, args=(cmd,"case003_2"))
            t.append(tt)
            tt.start()
        for tt in t:
            tt.join()
        elapse_time1 = time.time() - start_t0
        AboutHddldaemon.kill_server()
        self.assertEqual(check_res(q,"case_003_02"),0, "There are some error in logs, please check the relevant log")
        print(elapse_time1,elapse_time0)
        self.assertTrue((elapse_time1 * 6 < elapse_time0), "Performance:{}(elapse_time1)*6 < {}(elapse_time0)".format(elapse_time1,elapse_time0))

    def test_case004(self):
        """Diff network spend time"""
        t = []
        AboutHddldaemon.run_Hddldaemon()
        record = {}
        graphs = ["googlenetv2.xml","MobileNetV1.xml","vgg_d.xml"]
        for graph in graphs:
            cmd = benchmark_app + " -m " + os.path.join(NETWORKPATH,graph) + " -i " + IMAGPATH + "/224x224/imagenet12-ILSVRC2012_val_00000001.-224x224.bmp -d {} -nireq 10 -niter 10000 -api sync".format(device)
            for i in range(2):
                tt = threading.Thread(target=run_cmd, args=(cmd,graph.split(".")[0] + "_case004_" + str(i)))
                t.append(tt)
                time_s = time.time()
                tt.start()
                record[tt.ident] = [graph, time_s]
        for tt in t:
            tt.join()
            if not tt.is_alive():
                time_e = time.time()
                record[tt.ident][1] = time_e - time_s
        AboutHddldaemon.kill_server()
        self.assertEqual(check_res(q,"case_004"),0, "There are some error in logs, please check the relevant log")
        print(record)
        for graph in graphs:
            temp = []
            for key, value in record.items():
                if graph == value[0]:
                    temp.append(value[1])
            self.assertTrue( (-2< temp[0]-temp[1] < 2), "Spend time not the same {} {} {}\n".format(graph,temp[0], temp[1]))
                    
    def test_case005(self):
        """StatusOnly with callback"""
        t = []
        AboutHddldaemon.run_Hddldaemon()
        cmd = benchmark_app_C_S + " -m " + os.path.join(NETWORKPATH,"googlenetv2.xml") + " -i " + IMAGPATH + "/224x224/imagenet12-ILSVRC2012_val_00000001.-224x224.bmp -d {} -nireq 10 -niter 2000".format(device)
        for i in range(5):
            for j in range(10):
                tt = threading.Thread(target=run_cmd, args=(cmd,"case005_"+str(i)+"_"+str(j)))
                t.append(tt)
                tt.start()
            for tt in t:
                tt.join()
        AboutHddldaemon.kill_server()
        self.assertEqual(check_res(q,"case_005"),0,"There are some error in logs, please check the relevant log")

    def test_case006(self):
        """ResultReady with callback"""
        t = []
        AboutHddldaemon.run_Hddldaemon()
        cmd = benchmark_app + " -m " + os.path.join(NETWORKPATH,"googlenetv2.xml") + " -i " + IMAGPATH + "/224x224/imagenet12-ILSVRC2012_val_00000001.-224x224.bmp -d {} -nireq 10 -niter 2000".format(device)
        for i in range(5):
            for j in range(10):
                tt = threading.Thread(target=run_cmd, args=(cmd,"case005_" + str(i) + "_" + str(j)))
                t.append(tt)
                tt.start()
            for tt in t:
                tt.join()
        AboutHddldaemon.kill_server()
        self.assertEqual(check_res(q,"case_006"),0,"There are some error in logs, please check the relevant log")


if __name__ == "__main__":
    unittest.main()
            
      
        
        
