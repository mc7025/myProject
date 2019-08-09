#encoding:utf-8
#export GST_DEBUG=4
import unittest
from hddl_s_sw_validation.Function_test.run_demo_cls_gr_v1_3 import *
import re

class TestGS(unittest.TestCase):
    res = re.compile("1.8.3")
    @staticmethod
    def exec_r(cmd):
        output = os.popen(cmd).read()
        return output
    
    def test_GS_001(self):
        output = self.exec_r("dpkg -l | grep -i libgstreamer |grep -v plugins")
        self.assertEqual(len(self.res.findall(output)),2,msg=str(output))

    def test_GS_002(self):
        output = self.exec_r("dpkg -l | grep gstreamer-plugins-base")
        self.assertEqual(len(self.res.findall(output)),2,msg=str(output))

    def test_GS_003(self):
        output = self.exec_r("dpkg -l | grep gstreamer-plugins-good")
        self.assertEqual(len(self.res.findall(output)),1,msg=str(output))

    def test_GS_004(self):
        output = self.exec_r("dpkg -l | grep gstreamer-plugins-bad")
        self.assertEqual(len(self.res.findall(output)),1,msg=str(output))

    def test_GS_005(self):
        output = self.exec_r("dpkg -l | grep gstreamer1.0-plugins-ugly")
        self.assertEqual(len(self.res.findall(output)),2,msg=str(output))

    def test_GS_006(self):
        cmd = "gst-inspect-1.0 cvdlfilter"
        self.exec_r(cmd)
        output = self.exec_r(cmd)
        res_check = re.compile("error|fail|Error|Fail|ERR")
        self.assertEqual(len(res_check.findall(output)),0,msg="Some error in display info")
        res_check2 = re.compile("(Factory Details:)|(Plugin Details:)|(Pad Templates:)|(Pads:)|(Element Properties:)")
        self.assertEqual(len(res_check2.findall(output)),5,msg=str(output))

    def test_GS007(self):
        hddls = Hddls(testcase="GS007")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="cvdlfilter"),1)

    def test_GS_008(self):
        cmd = "gst-inspect-1.0 resconvert"
        self.exec_r(cmd)
        output = self.exec_r(cmd)
        res_check = re.compile("error|fail|Error|Fail|ERR")
        self.assertEqual(len(res_check.findall(output)),0,msg="Some error in display info")
        res_check2 = re.compile("(Factory Details:)|(Plugin Details:)|(Pad Templates:)|(Pads:)|(Element Properties:)")
        self.assertEqual(len(res_check2.findall(output)),5,msg=str(output))
        
    def test_GS009(self):
        hddls = Hddls(testcase="GS009")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="resconvert"),1)

    def test_GS_010(self):
        cmd = "gst-inspect-1.0 ipcsink"
        self.exec_r(cmd)
        output = self.exec_r(cmd)
        res_check = re.compile("error|fail|Error|Fail|ERR")
        self.assertEqual(len(res_check.findall(output)),0,msg="Some error in display info")
        res_check2 = re.compile("(Factory Details:)|(Plugin Details:)|(Pad Templates:)|(Pads:)|(Element Properties:)")
        self.assertEqual(len(res_check2.findall(output)),5,msg=str(output))
    
    def test_GS011(self):
        hddls = Hddls(testcase="GS011")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="ipcsink"),1)
        
    def test_GS012_640P(self):
        hddls = Hddls(testcase="GS012_640P")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier640x480.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS012_720P(self):
        hddls = Hddls(testcase="GS012_720P")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1280x720.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS012_1080P(self):
        hddls = Hddls(testcase="GS012_1080P")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS013(self):
        hddls = Hddls(testcase="GS013")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/indoor11920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov2tiny")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxhevcdec"),1)

    #@unittest.skip("For long time run")
    def test_GS014(self):
        hddls = Hddls(testcase="GS014")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/cross_road1920x1080_hevc.mp4",codec_type="H.265",algopipeline="mobilenetssd")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxhevcdec"),1)

    def test_GS015(self):
        hddls = Hddls(testcase="GS015")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS016(self):
        hddls = Hddls(testcase="GS016")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS017(self):
        hddls = Hddls(testcase="GS017")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",algopipeline="yolov1tiny ! reid")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS018(self):
        hddls = Hddls(testcase="GS018")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",algopipeline="mobilenetssd ! tracklp ! lprnet")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS019(self):
        hddls = Hddls(testcase="GS019")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/indoor11920x1080.avi_avc.mp4",algopipeline="yolov2tiny ! reid")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS020(self):
        hddls = Hddls(testcase="GS020")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/cross_road1920x1080_avc.mp4",algopipeline="mobilenetssd ! tracklp")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS021(self):
        hddls = Hddls(testcase="GS021")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",algopipeline="yolov1tiny  ! tracklp")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(),1)

    def test_GS025(self):
        hddls = Hddls(testcase="GS025")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",algopipeline="yolov1tiny  ! tracklp")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxh264dec"),1)

    def test_GS027(self):
        hddls = Hddls(testcase="GS027")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxhevcdec"),1)
        
    def test_GS030(self):
        hddls = Hddls(testcase="GS030")
        with cd(server_dir):
            os.system("registeralgo -a example")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="example ! tracklp")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="example"),1)

    def test_GS033(self):
        hddls = Hddls(testcase="GS033")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxh264dec"),1)

    def test_GS034(self):
        hddls = Hddls(testcase="GS034")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxhevcdec"),1)

    def test_GS037(self):
        hddls = Hddls(testcase="GS037")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4",codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxh264dec"),1)

    def test_GS038(self):
        hddls = Hddls(testcase="GS038")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="mobilenetssd ! tracklp ! lprnet")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxhevcdec"),1)

    def test_GS041(self):
        hddls = Hddls(testcase="GS041")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/indoor11920x1080.avi_avc.mp4",codec_type="H.264",algopipeline="yolov2tiny ! reid")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxh264dec"),1)

    def test_GS042(self):
        hddls = Hddls(testcase="GS042")
        create_json(stream_source="/home/hddl/Videos/Video_multi_size/indoor11920x1080.avi_hevc.mp4",codec_type="H.265",algopipeline="yolov2tiny ! reid")
        hddls.c_command()
        hddls.kill_js()
        self.assertEqual(hddls.checkResult(expect_keywords="mfxhevcdec"),1)

if __name__ == "__main__":
    unittest.main()
