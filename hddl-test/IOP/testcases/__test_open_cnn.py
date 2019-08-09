import os
import unittest
import time

from IOP.common.utils import LOGS_DIR, Server
from IOP.common.hal_util import Model, GRAPH_DIR, CheckResult, BASE_CONFIG
import IOP.common.IE_Util

DEVICE_NUM = 8
if os.name == "posix":
    BIN_PATH = "~/inference_engine_samples_build/intel64/Release"
else:
    pass


class OpenCnnDownloadTest(unittest.TestCase):

    def test_Download_Convert_googlenetv1(self):
        """Download and Convert the GoogleNet V1 caffe model"""
        model_name = "googlenet-v1"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result_d = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [224, 224])
        check.write_result()
        self.assertTrue(result_d, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 224, 224],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_googlenetv2(self):
        """Download and Convert the GoogleNet V2 caffe model"""
        model_name = "googlenet-v2"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [224, 224])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 224, 224],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_vgg16(self):
        """Download and Convert the VGG16 caffe model"""
        model_name = "vgg16"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [224, 224])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 224, 224],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_alexnet(self):
        """Download and Convert the AlexNet caffe model"""
        model_name = "alexnet"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [227, 227])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 227, 227],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_mobilenetssd(self):
        """Download and Convert the mobilenet-ssd caffe model"""
        model_name = "mobilenet-ssd"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [300, 300])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 300, 300],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_mobilenetv1(self):
        """Download and Convert the mobilenetv1 caffe model"""
        model_name = "mobilenet-v1-1.0-224"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [224, 224])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 224, 224],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_mobilenetv2(self):
        """Download and Convert the mobilenetv2 caffe model"""
        model_name = "mobilenet-v2"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [224, 224])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 224, 224],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_squeezenetv10(self):
        """Download and Convert the squeezenetv10 caffe model"""
        model_name = "squeezenet1.0"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [227, 227])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 227, 227],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))

    def test_Download_Convert_squeezenetv11(self):
        """Download and Convert the squeezenetv11 caffe model"""
        model_name = "squeezenet1.1"
        log_path = os.path.join(LOGS_DIR, "Download_{}".format(model_name))
        model = Model(model_name, log_path)
        model.download_model(GRAPH_DIR)
        check = CheckResult(log_path)
        result = check.no_error() and check.model_file(model_name) and check.model_dim(model_name, [227, 227])
        check.write_result()
        self.assertTrue(result, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))
        # convert cnn
        model_path = check.get_model_path()
        input_proto = os.path.join(model_path, "{}.prototxt".format(model_name))
        input_model = os.path.join(model_path, "{}.caffemodel".format(model_name))
        model.convert_cnn(input_proto=input_proto, input_model=input_model, input_shape=[1, 3, 227, 227],
                          output_dir=model_path)
        result_c = check.ir_model(model_name)
        check.write_result()
        self.assertTrue(result_c, msg="Please see '{}{}hal_result.csv' for detail.".format(LOGS_DIR, os.sep))


class OpenCnnRun(unittest.TestCase):

    @staticmethod
    def __run_server(test_case, mod_config=BASE_CONFIG, is_run=True):
        server = Server(testcase_id=test_case)
        server.config.modify_options(mod_config)
        server.config.modify_option("total_device_num", str(DEVICE_NUM), "autoboot")
        log_path = server.config.get_path()
        if is_run:
            server.start_run()
        return log_path, server

    def test_run_yolo_tiny_v1(self):
        """run yolo_tiny_v1 with benchmark_app"""
        test_case = "run_yolo_tiny_v1"
        case_path = BIN_PATH
        ir_path = B




