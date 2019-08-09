#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import shutil
from hddl_s_sw_validation.Function_test.run_demo_cls_gr_v1_3 import *


class TestRc(unittest.TestCase):

    def test_RC001(self):
        hddls = Hddls(testcase="RC001")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC005(self):
        hddls = Hddls(testcase="RC005", log_level=4)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="hddlspipe_create"), 1)

    def test_RC006(self):
        hddls = Hddls(testcase="RC006")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC007(self):
        hddls = Hddls(testcase="RC007", isRtsp=True, pipe_count=1)
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC008(self):
        hddls = Hddls(testcase="RC008", isRtsp=True, pipe_count=4)
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000", pipe_num=4)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC009(self):
        hddls = Hddls(testcase="RC009", isRtsp=True, pipe_count=8)
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000", pipe_num=8)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    @unittest.skip("Hang")
    def test_RC010(self):
        hddls = Hddls(testcase="RC010", isRtsp=True, pipe_count=16)
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000", pipe_num=16)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC011(self):
        hddls = Hddls(testcase="RC011", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.p4", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"ERROR:\s+Resource\s+not\s+found"), 1)

    def test_RC012(self):
        hddls = Hddls(testcase="RC012", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"ERROR:\s+\"/home/hddl/Videos/\"\s+is\s+a\s+directory"), 1)

    def test_RC013(self):
        hddls = Hddls(testcase="RC013", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/examples.desktop", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(
            hddls.checkResult(expect_keywords=r"ERROR:\s+This\s+file\s+is\s+invalid\s+and\s+cannot\s+be\s+played"), 1)

    def test_RC014(self):
        hddls = Hddls(testcase="RC014")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC015(self):
        hddls = Hddls(testcase="RC015", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", command_type=1, pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Error:\s+failed\s+to\s+create\s+pipeline"), 1)

    def test_RC016(self):
        hddls = Hddls(testcase="RC016", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", codec_type="H.26", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Error:\s+failed\s+to\s+create\s+pipeline"), 1)

    def test_RC017(self):
        hddls = Hddls(testcase="RC017", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", codec_type="H.265", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(
            hddls.checkResult(expect_keywords=r"ERROR:\s+GStreamer\s+encountered\s+a\s+general\s+stream\s+error"), 1)

    def test_RC018(self):
        hddls = Hddls(testcase="RC018", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", algopipeline="", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"get\s+empty\s+algopipeline"), 1)

    def test_RC019(self):
        hddls = Hddls(testcase="RC019", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", algopipeline="", pipe_num=1)
        modify_json("\"algopipeline\":\ \"\"", "")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"failed\s+to\s+get\s+algopipeline"), 1)

    def test_RC020(self):
        hddls = Hddls(testcase="RC020", isErrorTest=True, pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", algopipeline="qwed ! axfe ", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Not\s+support\s+this\s+algo"), 1)

    def test_RC022_emptyStr(self):
        hddls = Hddls(testcase="RC022_emptyStr")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", loop_times="")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC022_zero(self):
        hddls = Hddls(testcase="RC022_zero")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", loop_times=0)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC022_negative(self):
        hddls = Hddls(testcase="RC022_negative")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", loop_times=-123)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

    def test_RC023(self):
        hddls = Hddls(testcase="RC023", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, output_type=0)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"output\s+type\s+=\s+0"), 1)

    def test_RC024(self):
        hddls = Hddls(testcase="RC024", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(
            expect_keywords=r"STDOUT:\s+pipe\s+\d+:\s+index\s+=\s+\d+,\s+jpeg\s+size\s+.*"), 1)

    def test_RC025_string(self):
        hddls = Hddls(testcase="RC025_string", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, output_type="0")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(
            expect_keywords=r"STDOUT:\s+pipe\s+\d+:\s+index\s+=\s+\d+,\s+jpeg\s+size\s+.*"), 1)

    def test_RC025_negative(self):
        hddls = Hddls(testcase="RC025_negative", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, output_type=-123)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(
            expect_keywords=r"STDOUT:\s+pipe\s+\d+:\s+index\s+=\s+\d+,\s+jpeg\s+size\s+.*"), 1)

    def test_RC025_emptystring(self):
        hddls = Hddls(testcase="RC025_emptystring", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, output_type="")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(
            expect_keywords=r"STDOUT:\s+pipe\s+\d+:\s+index\s+=\s+\d+,\s+jpeg\s+size\s+.*"), 1)

    def test_RC027(self):
        hddls = Hddls(testcase="RC027", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"delete\s+pipe\s+\d+"), 1)

    def test_RC028(self):
        hddls = Hddls(testcase="RC028", pipe_count=1, isRtsp=True)
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000", pipe_num=1)
        destroy_json()
        hddls.c_command()
        time.sleep(6)
        hddls.d_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Dispatcher\s+destroy"), 1)

    @unittest.skip("Hang")
    def test_RC029(self):
        hddls = Hddls(testcase="RC029", pipe_count=16)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=16)
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"delete\s+pipe\s+\d+"), 1)

    def test_RC030(self):
        time.sleep(5)
        hddls = Hddls(testcase="RC030", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1)
        property_json(algopipeline="yolov1tiny")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC031(self):
        hddls = Hddls(testcase="RC031", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1)
        property_json(algopipeline="yolov1tiny ! opticalflowtrack")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC032(self):
        hddls = Hddls(testcase="RC032", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1,
                    algopipeline="yolov1tiny ! opticalflowtrack")
        property_json(algopipeline="yolov1tiny")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC033(self):
        hddls = Hddls(testcase="RC033", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1,
                    algopipeline="yolov1tiny ! opticalflowtrack")
        property_json(algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC034(self):
        hddls = Hddls(testcase="RC034", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, algopipeline="yolov1tiny")
        property_json(algopipeline="yolov1tiny ! opticalflowtrack")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC035(self):
        hddls = Hddls(testcase="RC035", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, algopipeline="yolov1tiny")
        property_json(algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC036(self):
        hddls = Hddls(testcase="RC036", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1,
                    algopipeline="mobilenetssd ! tracklp ! lprnet")
        property_json(algopipeline="mobilenetssd")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC037(self):
        hddls = Hddls(testcase="RC037", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1,
                    algopipeline="mobilenetssd ! tracklp ! lprnet")
        property_json(algopipeline="mobilenetssd ! tracklp")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC038(self):
        hddls = Hddls(testcase="RC038", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, algopipeline="mobilenetssd ! tracklp")
        property_json(algopipeline="mobilenetssd")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC039(self):
        hddls = Hddls(testcase="RC039", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, algopipeline="mobilenetssd ! tracklp")
        property_json(algopipeline="mobilenetssd ! tracklp ! lprnet")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC040(self):
        hddls = Hddls(testcase="RC040", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, algopipeline="mobilenetssd")
        property_json(algopipeline="mobilenetssd ! tracklp")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC041(self):
        hddls = Hddls(testcase="RC041", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4", pipe_num=1, algopipeline="mobilenetssd")
        property_json(algopipeline="mobilenetssd ! tracklp ! lprnet")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC042(self):
        hddls = Hddls(testcase="RC042", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/indoor.mp4", pipe_num=1, algopipeline="yolov2tiny ! reid")
        property_json(algopipeline="yolov2tiny")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC043(self):
        hddls = Hddls(testcase="RC043", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/indoor.mp4", pipe_num=1, algopipeline="yolov2tiny ! reid")
        property_json(algopipeline="reid")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC044(self):
        hddls = Hddls(testcase="RC044", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/indoor.mp4", pipe_num=1, algopipeline="yolov2tiny")
        property_json(algopipeline="reid")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC045(self):
        hddls = Hddls(testcase="RC045", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/indoor.mp4", pipe_num=1, algopipeline="yolov2tiny")
        property_json(algopipeline="yolov2tiny ! reid")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC046(self):
        hddls = Hddls(testcase="RC046", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/indoor.mp4", pipe_num=1, algopipeline="reid")
        property_json(algopipeline="yolov2tiny")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC047(self):
        hddls = Hddls(testcase="RC047", pipe_count=1)
        create_json(stream_source="/home/hddl/Videos/indoor.mp4", pipe_num=1, algopipeline="reid")
        property_json(algopipeline="yolov2tiny ! reid")
        hddls.c_command()
        time.sleep(2)
        hddls.p_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"Setting\s+property"), 1)

    def test_RC051_noModel(self):
        model_dir = os.path.join(server_dir, "models")
        with cd(model_dir):
            shutil.rmtree(model_dir)
        os.mkdir(model_dir)
        hddls = Hddls(testcase="RC048_noModel", isErrorTest=True)
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords=r"File\s+was\s+not\s+found"), 1)

    def test_RC051_updateModels(self):
        model_dir = os.path.join(server_dir, "models")
        with cd(model_dir):
            shutil.rmtree(model_dir)
        os.mkdir(model_dir)
        hddls = Hddls(testcase="RC048_updateModels")
        create_json(stream_source="/home/hddl/Videos/1600x1200.mp4")
        hddls.m_command()
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(), 1)

# def test_RC048_checkMD5(self):


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # suite = unittest.TestSuite()
    # testcases = []
    # for index in range(27, 45):
    #     testcase = TestRc("test_RC0{}".format(index))
    #     testcases.append(testcase)
    # suite.addTests(testcases)
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)
