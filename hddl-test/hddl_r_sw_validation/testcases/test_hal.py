import os
import random
import time
import unittest

from common.hal_util import TestEnv, ModifyDict, IMAGE_DIR, GRAPH_DIR, Client, CheckResult, BASE_CONFIG, \
    HAL_TEST_CODE, Server

DEVICE_NUM = 8
RUN_TIME = 300


class HALTest(unittest.TestCase):
    """Test Cases for HAL"""

    @staticmethod
    def __run_server(test_case, mod_config=BASE_CONFIG, is_cmake=False, is_run=True):
        # CodeOperation(test_case=test_case, is_cmake=is_cmake).run()
        server = Server(testcase=test_case)
        server.config.modify_options(mod_config)
        server.config.modify_option("total_device_num", str(DEVICE_NUM), "autoboot")
        server.config.modify_option("num", str(DEVICE_NUM), "autoboot")
        log_path = server.config.path
        if is_run:
            server.start_run()
        return log_path, server

    @classmethod
    def setUpClass(cls):
        TestEnv().setup_env()

    @classmethod
    def tearDownClass(cls):
        TestEnv().clean_env()

    # @unittest.skip("skip")
    def test_HAL01(self):
        """Multiple client mix sync/async test with MyraidX Device"""
        test_case = "HAL_01"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case, is_cmake=True)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime,)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num(16) and check.graph_num(4) \
                and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL02(self):
        """Multiple clients asynctest(wait) with MYDX Device"""
        test_case = "HAL_02"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncWaitTestV2"
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num(16) and check.graph_num(4) \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL03(self):
        """Do inference asynchronously(callback+wait)"""
        test_case = "HAL_03"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncCallbackWaitV2"
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL04(self):
        """Mix Sync/Async clients random connect/disconnect test"""
        test_case = "HAL_04"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            for thread_index in range(1, 17):
                runtime = str(random.randint(50, 60))
                Client(log_path=log_path, thread_index=thread_index).inference(case_path=case_path,
                                                                               image_path=image_path,
                                                                               graph_path=graph_path,
                                                                               runtime=runtime)
        while Client.is_running():
            time.sleep(5)
        check = CheckResult(log_path, thread_num=16)
        result = check.server_is_running() and check.error_tasks() and check.client_num(256) and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    @unittest.skipIf(os.name == "nt", "Only linux should run this case.")
    def test_HAL05(self):
        """Create/free Ion buffer"""
        test_case = "HAL_05"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "SyncTestV2"
        log_path, server = self.__run_server(test_case, is_run=False)
        Client(log_path=log_path).inference(case_path=case_path, case_name=case_name)
        check = CheckResult(log_path)
        result = check.memory() and check.error_tasks()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))

    # @unittest.skip("skip")
    def test_HAL06(self):
        """Enable monitor/display cached task information"""
        test_case = "HAL_06"
        config = ModifyDict({"task_snapshot_mode": "base"}).add()
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case, mod_config=config)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.keywords("TaskSnapshot") and check.error_tasks() \
                 and check.client_num() and check.graph_num() and check.device_num(DEVICE_NUM) \
                 and check.load_graph_time() and check.all_device_running(DEVICE_NUM)
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL07(self):
        """Check task ID information"""
        test_case = "HAL_07"
        config = ModifyDict({"task_snapshot_mode": "base"}).add()
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case, config)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.keywords("TaskId=") and check.error_tasks() \
                 and check.client_num() and check.graph_num() and check.device_num(DEVICE_NUM) \
                 and check.load_graph_time() and check.all_device_running(DEVICE_NUM)
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL08(self):
        """Check Squeeze mode"""
        test_case = "HAL_08"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        runtime = "300"
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            for thread_index in range(1, 9):
                image_path = os.path.join(IMAGE_DIR, "pic{}google{}".format(os.sep, str(thread_index)))
                graph_path = os.path.join(GRAPH_DIR, "google{}google{}.blob".format(os.sep, str(thread_index)))
                Client(log_path=log_path, thread_index=thread_index).inference(case_path=case_path,
                                                                               image_path=image_path,
                                                                               graph_path=graph_path,
                                                                               runtime=runtime)
                time.sleep(20)
        while Client.is_running():
            time.sleep(5)
        check = CheckResult(log_path, thread_num=8)
        result = check.server_is_running() and check.error_tasks() and check.client_num(8) and check.graph_num(8) \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL09(self):
        """Check the loading time for cached graph."""
        test_case = "HAL_09"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        runtime = "60"
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            for thread_index in range(1, 9):
                if thread_index > 4:
                    index = thread_index - 4
                else:
                    index = thread_index
                graph_path = os.path.join(GRAPH_DIR, "google{}google{}.blob".format(os.sep, str(index)))
                Client(log_path=log_path, thread_index=thread_index).inference(case_path=case_path,
                                                                               image_path=image_path,
                                                                               graph_path=graph_path,
                                                                               runtime=runtime)
                time.sleep(5)
        while Client.is_running():
            time.sleep(5)
        check = CheckResult(log_path, thread_num=8)
        result = check.server_is_running() and check.error_tasks() and check.client_num(8) and check.graph_num(4) \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time() and check.all_device_running(DEVICE_NUM)
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL10(self):
        """Check the performance for cached graph"""
        test_case = "HAL_10"
        config = ModifyDict({"graph_snapshot_mode": 1}).sub()
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}".format(os.sep))
        log_path, server = self.__run_server(test_case, config)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                image_path=image_path,
                                                graph_path=graph_path)
        while Client.is_running():
            time.sleep(5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num(1) \
                 and check.graph_num(102) and check.all_device_running(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL11(self):
        """Do inference asynchronously"""
        test_case = "HAL_11"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time() and check.all_device_running(DEVICE_NUM)
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL11_tinyyolov1(self):
        """Do inference asynchronously"""
        test_case = "HAL_11"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "448x448")
        graph_path = os.path.join(GRAPH_DIR, "yolo_graph.blob")
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time() and check.all_device_running(DEVICE_NUM)
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL12(self):
        """Do inference synchronously"""
        test_case = "HAL_12"
        case_name = "SyncTestV2"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL12_tinyyolov1(self):
        """Do inference synchronously"""
        test_case = "HAL_12"
        case_name = "SyncTestV2"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        image_path = os.path.join(IMAGE_DIR, "448x448")
        graph_path = os.path.join(GRAPH_DIR, "yolo_graph.blob")
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL13(self):
        """Do inference asynchronously(wait)"""
        test_case = "HAL_13"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncWaitTestV2"
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL13_tinyyolov1(self):
        """Do inference asynchronously(wait)"""
        test_case = "HAL_13"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncWaitTestV2"
        image_path = os.path.join(IMAGE_DIR, "448x448")
        graph_path = os.path.join(GRAPH_DIR, "yolo_graph.blob")
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL14(self):
        """Do inference AsyncMemoryPoolTest"""
        test_case = "HAL_14"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncMemoryPoolTest"
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL14_tinyyolov1(self):
        """Do inference AsyncMemoryPoolTest"""
        test_case = "HAL_14"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncMemoryPoolTest"
        image_path = os.path.join(IMAGE_DIR, "448x448")
        graph_path = os.path.join(GRAPH_DIR, "yolo_graph.blob")
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL15(self):
        """Do inference AsyncThreadV2"""
        test_case = "HAL_15"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncThreadV2"
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL15_tinyyolov1(self):
        """Do inference AsyncThreadV2"""
        test_case = "HAL_15"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "AsyncThreadV2"
        image_path = os.path.join(IMAGE_DIR, "448x448")
        graph_path = os.path.join(GRAPH_DIR, "yolo_graph.blob")
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL16(self):
        """Do inference SyncTestFromMemoryV2"""
        test_case = "HAL_16"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "SyncTestFromMemoryV2"
        image_path = os.path.join(IMAGE_DIR, "pic{}google0".format(os.sep))
        graph_path = os.path.join(GRAPH_DIR, "google{}google1.blob".format(os.sep))
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()

    # @unittest.skip("skip")
    def test_HAL16_tinyyolov1(self):
        """Do inference SyncTestFromMemoryV2"""
        test_case = "HAL_16"
        case_path = os.path.join(HAL_TEST_CODE, test_case)
        case_name = "SyncTestFromMemoryV2"
        image_path = os.path.join(IMAGE_DIR, "448x448")
        graph_path = os.path.join(GRAPH_DIR, "yolo_graph.blob")
        runtime = str(RUN_TIME)
        log_path, server = self.__run_server(test_case)
        if server.is_ready():
            Client(log_path=log_path).inference(case_path=case_path,
                                                case_name=case_name,
                                                image_path=image_path,
                                                graph_path=graph_path,
                                                runtime=runtime)
        time.sleep(RUN_TIME + 5)
        check = CheckResult(log_path)
        result = check.server_is_running() and check.error_tasks() and check.client_num() and check.graph_num() \
                 and check.device_num(DEVICE_NUM) and check.load_graph_time()
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(log_path, os.sep))
        server.stop_run()


if __name__ == "__main__":
    unittest.main(verbosity=2)