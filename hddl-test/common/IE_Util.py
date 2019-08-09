import re
import time
import os
import glob
import subprocess
import unittest
import sys
import threading
import shutil
import inspect
import datetime
import socket
#from .utils import LOGS_DIR
if sys.version_info.major != 3:
    print("\033[33mPlease use python 3.xxx!\033[0m")
    exit(1)
import pexpect
from config import InferenceEngine_lib, MO_FILE, PASSWORD
import queue

q = queue.Queue()
BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if os.name != "nt":
    IE_Release = os.path.join(os.getenv("HOME"),"inference_engine_samples_build/intel64/Release")
    HDDL_DEMO = os.path.join(BASE_PATH,"source_cpp/hddl_demo/hddl_demo")
    REID_DEMO = os.path.join(BASE_PATH,"source_cpp/hddl_demo/reid_demo")
    HDDL_DEMO_S_C = os.path.join(BASE_PATH,"source_cpp/hddl_demo/HDDL_DEMO_S_C")
    HDDL_DEMO_R_C = os.path.join(BASE_PATH,"source_cpp/hddl_demo/HDDL_DEMO_R_C")
    perfcheck = os.path.join(IE_Release, "perfcheck")
    classification_s = os.path.join(IE_Release, "classification_sample")
    classification_as = os.path.join(IE_Release, "classification_sample_async")
    detection_sample_ssd = os.path.join(IE_Release, "object_detection_sample_ssd")
    HDDL_INSTALL_DIR = os.getenv("HDDL_INSTALL_DIR")
    MO_FILE = os.path.join(HDDL_INSTALL_DIR[:HDDL_INSTALL_DIR.rfind("/inference_engine")], "model_optimizer", "mo.py")
else:
    if not os.path.exists(os.path.join("c:",os.getenv("HOMEPATH"),"Desktop\openvino_s")):
        print("Create shortcut for openvino path")
        hddl_install_dir = os.getenv("HDDL_INSTALL_DIR")
        openvino_install_dir = hddl_install_dir[:hddl_install_dir.rfind("\\deploy")]
        cmd = "mklink /d " + os.path.join("c:",os.getenv("HOMEPATH"),r"Desktop\openvino_s") + ' "{}"'.format(openvino_install_dir)
        os.system(cmd)
        time.sleep(1)
    OPENVINO_DIR = os.path.join("c:",os.getenv("HOMEPATH"),r"Deszktop\openvino_s")
    SETUPVARS = os.path.join(OPENVINO_DIR, "bin", "setupvars.bat") 
    HDDL_INSTALL_DIR = os.path.join(OPENVINO_DIR, "inference_engine/external/hddl")
    MO_FILE = os.path.join(OPENVINO_DIR, "deployment_tools\model_optimizer", "mo.py")
    IE_Release = os.path.join("c:",os.getenv("HOMEPATH"),r"Documents\Intel\OpenVINO\inference_engine_samples_build_2015\intel64\Release")
    pscp = os.path.join(BASE_PATH,"source_cpp/hddl_demo/pscp.exe")
    HDDL_DEMO = os.path.join(BASE_PATH,"source_cpp/hddl_demo/hddl_demo.exe")
    REID_DEMO = os.path.join(BASE_PATH,"source_cpp/hddl_demo/reid_demo.exe")
    HDDL_DEMO_S_C = os.path.join(BASE_PATH,"source_cpp/hddl_demo/HDDL_DEMO_S_C.exe")
    HDDL_DEMO_R_C = os.path.join(BASE_PATH,"source_cpp/hddl_demo/HDDL_DEMO_R_C.exe")
    perfcheck = os.path.join(BASE_PATH, "source_cpp/hddl_demo/perfcheck.exe")
    classification_s = os.path.join(BASE_PATH, "source_cpp/hddl_demo/classification_sample.exe")
    classification_as = os.path.join(BASE_PATH, "source_cpp/hddl_demo/classification_sample_async.exe")
    detection_sample_ssd = os.path.join(BASE_PATH, "source_cpp/hddl_demo/object_detection_sample_ssd.exe")
        

MODEFILEPATH = os.path.join(BASE_PATH, "HDDL_AUTO/All_network_mode_cur")
IMAGPATH = os.path.join(BASE_PATH, "images")
NETWORKPATH = os.path.join(BASE_PATH, "HDDL_AUTO/NetWorks")
MO_OUTPUT = os.path.join(BASE_PATH, "MO_Outpath")


LOGS_DIR = os.path.join(BASE_PATH, 'output/logs/IE/{}'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))


if os.path.exists(LOGS_DIR):
    pass
else:
    os.makedirs(LOGS_DIR)


TIMESTAMP = "time_" + datetime.datetime.now().strftime("%Y%m%d")

if os.name == "nt":
    if os.path.exists(MO_OUTPUT):
        os.system("rmdir /S /Q {}/*".format(MO_OUTPUT))
else:
    if os.path.exists(MO_OUTPUT):
        os.system("rm -rf {}/*".format(MO_OUTPUT))

class cd(object):
    current_dir = os.getcwd()
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, ex_t, ex_v, ex_tr):
        os.chdir(self.current_dir)


def build_IE_demo():
    HOME_PATH = os.getenv("HOME")
    INTEL_CVSDK_DIR = os.getenv("INTEL_CVSDK_DIR")
    if not INTEL_CVSDK_DIR:
        print("\033[31mPlease check the enviroment variable!\033[0m")
        return 0
    InferenceEngine_DIR = os.getenv("InferenceEngine_DIR")
    if InferenceEngine_DIR:
        sample_path = os.path.join(os.path.dirname(InferenceEngine_DIR), "samples")
    else:
        sample_path = INTEL_CVSDK_DIR + "/deployment_tools/inference_engine/samples"
        if not os.path.exists(sample_path):
            print("\033[31mDon't found the path {}!\033[0m".format(sample_path))
            return 0
    with cd(sample_path):
        os.system(os.path.join(sample_path, "./build_samples.sh") + " > {}/temp_IE_build.log".format(LOGS_DIR))
        release_lib_path = IE_Release + "/lib"
        env_variable = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{}".format(release_lib_path)
        output = os.popen("cat {}/.bashrc".format(HOME_PATH)).read()
        if output.find(env_variable) != -1:
            pass
        else:
            with open("{}/.bashrc".format(HOME_PATH), "at") as f:
                f.write(env_variable)
        os.system('echo {}|sudo -S cp '.format(PASSWORD) + release_lib_path + "/libformat_reader.so " + InferenceEngine_lib + "/libformat_reader.so")

    hddl_demo_sh = BASE_PATH + "/source_cpp/hddl_demo/build_binary_file.sh"
    if not os.path.exists(hddl_demo_sh):
        print("\033[31mDon't found the file {0}!\033[0m, \nplease git clone all the test code include {0}........".format(hddl_demo_sh))
        return 0
    hddl_demo_path = os.path.dirname(os.path.abspath(hddl_demo_sh))
    with cd(hddl_demo_path):
        os.system("chmod 755 {}".format("build_binary_file.sh"))
        os.system("bash ./build_binary_file.sh > /dev/null")           
        os.system("touch ./{}".format(TIMESTAMP))

def needcompile():
    binary_files = ["HDDL_DEMO_R_C", "hddl_demo", "HDDL_DEMO_S_C", "reid_demo"]
    date_now = datetime.datetime.now().strftime("%Y%m%d")
    hddl_demo_sh = BASE_PATH + "/source_cpp/hddl_demo/"
    files = os.listdir(hddl_demo_sh)
    for f in files:
        if f.startswith("time_"):
            stamp = f.split("_")[-1].strip()
            if stamp == date_now:
                for binaryfile in binary_files:
                    if os.path.exists(os.path.join(hddl_demo_sh,binaryfile)):
                        if oct(os.stat(os.path.join(hddl_demo_sh,binaryfile)).st_mode)[-3:] != '775':
                            os.chmod(os.path.join(hddl_demo_sh,binaryfile), 755)
                            return
    build_IE_demo()

def getallcases(dicts):
    global_s = dicts
    testcase = []
    for attr in global_s:
        try:
            new_t = eval(attr,global_s)
            if issubclass(new_t, unittest.TestCase):
                modulename = inspect.getmodule(new_t).__name__
                for ii in dir(new_t):
                    if ii.startswith("test_"):
                        testcase.append(".".join([modulename,attr,ii]))
        except TypeError as e:
            #print(e)
            continue
    if testcase:
        str_c = ""
        for case in testcase:
            str_c += case + "\n"
        with open('{}/AllTestCases.txt'.format(BASE_PATH), "wt") as f:
            f.write(str_c)
        return str_c

def getVersion():
    print("Take some seconds to get the version of VPU, please wait.....")
    cmd_power = "powershell -WindowStyle Maximized -command \"Get-WmiObject -class Win32_Product|Select-Object -Property name,version|findstr 'VPUs'\""
    output = os.popen(cmd_power).read()
    if output:
        vpu_version = output.split()[-1].split(".")[-2:]
        return ".".join(vpu_version)
    else:
        print("please check if you have installed the openvino software.......")
        return 0

def getIR_caffeMode(host="10.240.108.33", username="hddl", password="intel123", src_path="/home/hddl/1_HDDL_MYDX/1_Neural_Networks/", dst_path=BASE_PATH, port=22):
    if os.name == "nt":
        _temp = getVersion()
        if not _temp:
            return
        OPENVINO_V = "2019." + _temp
    else:
        OPENVINO_V = os.path.basename(os.getenv("INTEL_OPENVINO_DIR")).split("_")[-1]
    dirname = "HDDL_AUTO"
    src_path_ = src_path
    src_path = os.path.join(src_path_, "l_openvino_toolkit_p_" + OPENVINO_V) + "/" + dirname
    src_path_manual = os.path.join(src_path_, "_".join(("l_openvino_toolkit_p",OPENVINO_V,"manual"))) + "/" + dirname
    Y_N = ""
    if os.path.exists(os.path.join(dst_path,dirname)):
        if os.path.exists(os.path.join(BASE_PATH,dirname,OPENVINO_V)):
            print("The file is exists........")
            return
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host,port))
    except OSError:
        print("\033[31mPlease check the connect to host {}\033[0m".format(host))
        print("\033[31mAnd some cases will run fail with download network files fail\033[0m")
        time.sleep(3)
        return 0
    finally:
        conn.close()
    if os.name != "nt":
        cmd_local = "df -h %s|grep -e '[0-9]\{1,3\}G'|awk '{print $4}'" % dst_path
        availableDiskVolume = float(os.popen(cmd_local).read().strip().strip("G"))
        cmd = "ssh {}@{} 'du -sh {}' > ./.filesize".format(username, host, src_path)
        cmd_manual = "ssh {}@{} 'du -sh {}' > ./.filesize".format(username, host, src_path_manual)
        child = pexpect.spawn("bash")
        def sendCMD(child, cmd):
            child.sendline(cmd)
            index = child.expect(["(yes/no)","password:", pexpect.TIMEOUT])
            if index == 0:
                child.sendline("yes")
                child.expect(["password:"])
                child.sendline(password)
            elif index == 1:
                child.sendline(password)
            elif index == 2:
                print("\033[31mCoonect to host:{} timeout.....\033[0m".format(host))
            else:
                pass
        sendCMD(child, cmd)
        time.sleep(3)
        content = ""
        if os.path.exists("./.filesize"):
            with open("./.filesize") as f:
                content = f.read()
            cmd = "scp -r {}@{}:{} {};exit".format(username, host, src_path, dst_path)
        if not content:
            sendCMD(child, cmd_manual)
            time.sleep(3)
            if os.path.exists("./.filesize"):
                with open("./.filesize") as f:
                    content = f.read()
        #os.remove("./.filesize")
            cmd = "scp -r {}@{}:{} {};exit".format(username, host, src_path_manual, dst_path)
        if content:
            Y_N = ""
            try:
                size = float(content.split()[0].strip().strip("G"))
            except ValueError:
                try:
                    size = float(content.split()[0].strip().strip("M"))
                except ValueError:
                    size = float(content.split()[0].strip().strip("K"))
            if availableDiskVolume < size:
                print("The disk volumne {} is not enough to save the files {}".format(availableDiskVolume, size))
                print("Download file fail and some case will fail in the future!")
                time.sleep(3)
                return
            child.sendline("")
            child.sendline(cmd)
            index = child.expect(["(yes/no)","password:", pexpect.TIMEOUT])
            if index == 0:
                child.sendline("yes")
                child.expect(["password:"])
                child.sendline(password)
            elif index == 1:
                child.sendline(password)
            elif index == 2:
                print("\033[31mCoonect to host:{} timeout.....\033[0m\n".format(host))
                print("\033[31mDownload Fail !\033[0m".format(host))
            else:
                pass
            def get_status(child):
                time.sleep(5)
                while child.isalive():
                    time.sleep(2)
                else:
                    res_S = re.compile("BASEPATHINSTEAD")
                    with open(os.path.join(BASE_PATH,dirname,OPENVINO_V), "wt"):
                        pass
                    for name in ("mtcnn.xml", "pva_fd.xml"):
                        try:
                            shutil.move(BASE_PATH + "/" + dirname + "/NetWorks/" + name, BASE_PATH + "/" + dirname + "/NetWorks/" + name + ".bak")
                            with open(BASE_PATH + "/" + dirname + "/NetWorks/" + name + ".bak") as f1, open(BASE_PATH + "/" + dirname + "/NetWorks/" + name,"w") as f2:
                                f2.write(re.sub(res_S, BASE_PATH, f1.read()))
                        except FileNotFoundError:
                            print("File {} not found".format(name))
                            pass
                child.close()
                print("Network Download finished..........")
                return 1
            try:
                t = threading.Thread(target=get_status,args=(child,)).start()
                child.interact()
            except OSError:
                pass
        else:
            child.close()
    else:
        scp_command = pscp + " -r -pw {} {}@{}:{} {} && exit".format(password, username, host, src_path, dst_path)
        cmd_manual = pscp + " -r -pw {} {}@{}:{} {} && exit".format(password, username, host, src_path_manual, dst_path)
        tag = False
        for cmd_ in [scp_command, cmd_manual]:
            status = os.system(cmd_)
            if status:
                continue
            else:
                print("Downloading the network file now.......")
                tag = True
                break
        if not tag:
            return        
        for name in ("mtcnn.xml", "pva_fd.xml"):
            try:
                res_S = re.compile("BASEPATHINSTEAD")
                with open(os.path.join(BASE_PATH,dirname,OPENVINO_V), "wt"):
                    pass
                shutil.move(BASE_PATH + "/" + dirname + "/NetWorks/" + name, BASE_PATH + "/" + dirname + "/NetWorks/" + name + ".bak")
                with open(BASE_PATH + "/" + dirname + "/NetWorks/" + name + ".bak") as f1, open(BASE_PATH + "/" + dirname + "/NetWorks/" + name,"w") as f2:
                    f2.write(re.sub(res_S, BASE_PATH, f1.read()))
            except FileNotFoundError:
                print("File {} not found".format(name))
                pass


def precondition():
    if os.name != "nt":
        res = re.compile("\d+.\d+")
        needcompile()
        if os.path.exists("./HDDL_AUTO") and os.path.exists("./.filesize"):
            with open("./.filesize") as f:
                rec_size = res.findall(f.read())[0].strip()
            curr_s = res.findall(os.popen("du -sh ./HDDL_AUTO").read())[0].strip()
            if float(curr_s) >= float(rec_size):
                return
    getIR_caffeMode()

precondition()

class MO_PRIVATE_PUBLIC_CNN(object):
    public_network = ["MobileNetV1","MobileNetV2","googlenetV2","squeezenetv1_0","squeezenetv1_1","resnet50","resnet101",
                      "bvlc_goolgnet","vgg_d","resnet_18","tiny_yolo_v1", "alexnet", "MobileSSD","faster_rcnn","yolov2","tiny_yolo_v2"]
    map_network_re = {'224x224':["googlenetv2","resnet50","resnet101","squeezenetv1_0","squeezenetv1_1","faster_rcnn","MobileNetV1","MobileNetV2","resnet_18","vgg_d","bvlc_goolgnet"],
                      '227x227':["alexnet"],
                      '300x300':["MobileSSD"],
                      '416x416':["yolov2","tiny_yolo_v2"],
                      '448x448':["tiny_yolo_v1"],
                      '736x416':["pvaPvdFull"],
                      '416x256':["pvapvd"],
                      '192x192':["vasfrfp16"],
                      '992x544':["icvpd"],
                      '24x94':["icvlprnet"],
                      '62x62':["agegendernet"],
                      '480x270':["pva_fd","mtcnn"]}

    @staticmethod
    def convert_cmd(networkname, frame_type="caffe"):
        cmd = ""
        if frame_type == "caffe":
            cmd = "python3 " + MO_FILE + " --framework caffe --data_type FP16 --input_proto " + "{0}/{1}/{1}.prototxt --input_model {0}/{1}/{1}.caffemodel ".format(MODEFILEPATH,networkname)
            if networkname in ("tiny_yolo_v1", "alexnet", "MobileSSD"):
                if "tiny_yolo_v1" == networkname:
                    input_shape = "--input_shape [1,3,448,448]"
                elif "alexnet" == networkname:
                    input_shape = "--input_shape [1,3,227,227]"
                else:
                    input_shape = "--input_shape [1,3,300,300]"
                input_shape += " --scale 255 --reverse_input_channels "
            else:
                if networkname in ("bvlc_goolgnet","vgg-d","resnet_18"):
                    input_shape = "--input_shape [1,3,224,224] --mean_file {}/{}/imagenet_mean.binaryproto ".format(MODEFILEPATH, networkname)
                elif networkname in ["squeezenetv1_0","squeezenetv1_1"]:
                    input_shape = "--input_shape [1,3,227,227] -ms [104,117,123] -n {} ".format(networkname)
                else:
                    #MobileNetV1,MobileNetV2,googlenetV2,squeezenet_v1.0,squeezenet_v1.1,resnet-50,resnet-101
                    input_shape = "--input_shape [1,3,224,224] -ms [104,117,123] -n {} ".format(networkname)
            cmd += input_shape + " -o {}/{}/".format(MO_OUTPUT, networkname)
        elif frame_type == "tf":
            cmd = "python3 " + MO_FILE + " --framework tf --input_model {0}/{1}/{1}.pb --data_type FP16 ".format(MODEFILEPATH,networkname)
            if networkname == "faster_rcnn":
                input_shape = '--input_shape [1,224,224,3] --scale 255 --reverse_input_channels --tensorflow_use_custom_operations_config {0}/{1}/faster_rcnn_support.json --extensions {0}/{1}/custom_mo_extensions --tensorflow_object_detection_api_pipeline_config {0}/{1}/pipeline.config -n faster_rcnn '.format(MODEFILEPATH, networkname)
            else:
                input_shape = "--input_shape [1,416,416,3] --scale 255 --reverse_input_channels "
            cmd += input_shape + "--output_dir {}/{}/".format(MO_OUTPUT, networkname)
        return cmd

    def do_inference_cmd(self, networkname):
        cmd = ""
        xml_file = "{}/{}.xml".format(NETWORKPATH,networkname)
        if networkname in ("reidembedding","reiddistancefp16"):
            cmd = "{0} HDDL {1}/reidembedding.xml {1}/reiddistancefp16.xml {2}/128x64/000_45.bmp  {2}/128x64/000_45.bmp 0.2".format(REID_DEMO,NETWORKPATH,IMAGPATH)
        elif networkname in self.public_network:
            try:
                xml_file = "{0}/{1}/{1}.xml".format(MO_OUTPUT, networkname)
            except (FileNotFoundError,IndexError) as e:
                print("\033[31mDon't found the covertted IR file!!!!!!!!!!!!!\033[0m\n")
                xml_file = "{}/{}.xml".format(NETWORKPATH,networkname)
                pass
        for key, values in self.map_network_re.items():
            if networkname in values:
                imgs = glob.glob(IMAGPATH + "/" + key + "/*.bmp")
                try:
                    if networkname == "faster_rcnn":
                        cmd = '{} -i {} -m {} -d HDDL -ni 10'.format(detection_sample_ssd,imgs[0],xml_file)
                    else:
                        cmd = '{} classify {} {} HW 0.2'.format(HDDL_DEMO, xml_file, imgs[0])
                except IndexError:
                    print(HDDL_DEMO, xml_file, imgs, IMAGPATH + "/" + key + "/*.bmp")
                    pass
        return cmd

    @staticmethod
    def run_cmd(cmd, casename=""):
        content_s = ""
        print("\033[34m{}\033[0m".format(cmd))
        run_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = run_process.communicate()
        res = re.compile("fail|failed|Error|Fail|error|FAIL|[\[|:]ERR")
        flag = False
        if stderr:
            content_s += stderr.decode("utf-8")
            print("\033[33m%s\033[0m\n" % stderr.decode("utf-8"))
            flag = True
        if stdout:
            content = stdout.decode("utf-8")
            find_result = res.findall(content)
            if find_result:
                content_s += "\n" + content
                flag = True
            print("\033[32m%s\033[0m\n" % stdout.decode("utf-8"))
        with open(os.path.join(LOGS_DIR,"hddldaemon.log")) as f:
            _position = f.read().find("SERVICE IS READY")
            position = 0 if _position == -1 else _position
            f.seek(position)
            content_ = f.read()
            re_temp = res.findall(content_)
            if re_temp:
                print("\033[32mSome Error occurred on server\033[0m\n")
                content_s += "\n" + content_
                flag = True
        if flag:
            with open("{}/".format(LOGS_DIR) + casename + ".txt", "at") as f:
                f.write(content_s)
            return 1
        return 0


class AboutHddldaemon(object):

    save_path = LOGS_DIR
    config_path = os.path.join(HDDL_INSTALL_DIR,"config")

    @classmethod
    def alter_config(cls, regx_str = " ", value = " ", filename="hddl_service.config"):
        res = re.compile(regx_str)
        with open(os.path.join(cls.config_path,filename),"rt") as f1, open(os.path.join(cls.save_path, filename),"wt") as f2:
            content_s = f1.read()
            f2.write(re.sub(res, value ,content_s))

    @classmethod
    def run_Hddldaemon(cls):
        AboutHddldaemon.kill_server()
        if os.name != "nt":
            os.system("{0}/bin/hddldaemon 2>&1 > {1}/hddldaemon.log&".format(HDDL_INSTALL_DIR, cls.save_path))
        else:
            cmd = r"{}\bin\hddldaemon > {}\hddldaemon.log".format(HDDL_INSTALL_DIR, cls.save_path)
            t = threading.Thread(target=lambda cmd:os.system(cmd), args=(cmd,))
            t.setDaemon(True)
            t.start()

    @classmethod
    def run_special_Hddldaemon(cls):
        AboutHddldaemon.kill_server()
        if os.name != "nt":
            os.system("{0}/bin/hddldaemon -c {1}/hddl_service.config --boot-config {1}/hddl_autoboot.config 2>&1 > {1}/hddldaemon.log&".format(HDDL_INSTALL_DIR, cls.save_path))
        else:
            cmd = r"{0}/bin/hddldaemon -c {1}/hddl_service.config --boot-config {1}/hddl_autoboot.config > {1}/hddldaemon.log".format(HDDL_INSTALL_DIR, cls.save_path)
            t = threading.Thread(target=lambda cmd:os.system(cmd), args=(cmd,))
            t.setDaemon(True)
            t.start()

    @staticmethod
    def kill_server():
        if os.name == "nt":
            os.system(r'taskkill /F /IM hddldaemon.exe')
        else:
            cmd = """for pid in `ps -ef|grep -e "autoboot\|hddldaemon" |grep -v "grep"|awk '{print $2}'`;do kill -9 $pid;done"""
            os.system(cmd)

def run_cmd(cmd, caseNo):
    run_prcoess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = run_prcoess.communicate()
    content = ""
    if stderr:
        q.put(stderr.decode("utf-8"))
        content += stderr.decode("utf-8")
    res = re.compile("fail|failed|Error|Fail|error|FAIL|[\[|:]ERR")
    find_res = res.findall(stdout.decode("utf-8"))
    if find_res:
        content += "\n" + stdout.decode("utf-8")
        q.put(str(find_res))
    if content:
        with open("{}/".format(LOGS_DIR) + caseNo + ".txt", "at") as f:
            f.write(content)

def check_res(q, casename, key_words=""):
    res_key = re.compile(key_words)
    strs = ""
    while not q.empty():
        strs += q.get()
    with open(os.path.join(LOGS_DIR,"hddldaemon.log")) as f:
        res = re.compile("fail|failed|Error|Fail|error|FAIL|[\[|:]ERR")
        content_all = f.read()
        find_key = res_key.findall(content_all)
        position_ = f.read().find("SERVICE IS READY")
        position = 0 if position_ == -1 else position_
        f.seek(position)
        content = f.read()
        find_res = res.findall(content)
    shutil.move(os.path.join(LOGS_DIR,"hddldaemon.log"), os.path.join(LOGS_DIR,"{}_hddldaemon.log".format(casename)))
    if strs or find_res:
        return 1
    if key_words and not find_key:
        return 2
    return 0







