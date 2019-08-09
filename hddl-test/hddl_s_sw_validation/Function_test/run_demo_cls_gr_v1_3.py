# enconding:utf-8
# !/usr/bin/python3

import os
import sys
import time
import re
import json
import threading
from functools import wraps
import csv
import glob
from datetime import datetime

from hddl_s_sw_validation.main import BASE_PATH

try:
    import queue
except ImportError as e:
    print("Please use python3 to run the script!")
    exit()
q = queue.Queue()
try:
    import pexpect as expect
except ImportError as e:
    print("Please install pexpect(pip3 install pexpect)")
try:
    import cv2
except ImportError:
    cv_check = False
else:
    cv_check = True

"""
status = os.system("expect -v")
if status !=0 :
    os.system("echo intel123|sudo -s apt install expect")
"""

Log_info_collect_fold = os.path.join(BASE_PATH, "output{}{}".format(os.sep, datetime.now().strftime("%Y%m%d%H%M%S")))
HDDLS_CVDL_MODEL_PATH = os.environ.get("HDDLS_CVDL_MODEL_PATH")
if not HDDLS_CVDL_MODEL_PATH:
    raise ValueError("Please export HDDLS_CVDL_MODEL_PATH=<server_path>/models")
receiver_dir = os.path.join(HDDLS_CVDL_MODEL_PATH, "{0}{1}{0}{1}receiver".format(os.pardir, os.sep))
controller_dir = os.path.join(HDDLS_CVDL_MODEL_PATH, "{0}{1}{0}{1}controller".format(os.pardir, os.sep))
server_dir = os.path.join(HDDLS_CVDL_MODEL_PATH, "{0}{1}{0}{1}server".format(os.pardir, os.sep))
# file_position = 0


def create_json(filename="create_self.json", client_id=1, command_type=0, pipe_num=2,
                stream_source="/home/hddl/Videos/Video_multi_size/1600x1200.mp4",
                codec_type="H.264", algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2",
                loop_times=1, output_type=1):
    with cd(controller_dir):
        json_file = {
            "client_id": client_id,
            "command_type": command_type,
            "command_create":
                {
                    "pipe_num": pipe_num,
                    "stream_source": stream_source,
                    "codec_type": codec_type,
                    "output_type": output_type,
                    "cvdlfilter0":
                        {
                            "algopipeline": algopipeline
                        },
                    "loop_times": loop_times
                }
        }
        if os.path.exists(filename):
            os.system("rm %s" % filename)
        with open("./" + filename, "wt") as f:
            json.dump(json_file, f, indent=4)


def modify_json(old_str, new_str, filename="create_self.json"):
    with cd(controller_dir):
        cmd = "sed -i \'s#%s#%s#g\' %s" % (old_str, new_str, filename)
        os.system(cmd)


def destroy_json(filename="destroy.json", client_id=1, command_type=1, pipe_id=0):
    with cd(controller_dir):
        json_file = {
            "client_id": client_id,
            "command_type": command_type,
            "command_destroy":
                {
                    "pipe_id": pipe_id
                }
        }
        if os.path.exists(filename):
            os.system("rm %s" % filename)
        with open("./" + filename, "wt") as f:
            json.dump(json_file, f, indent=4)


def property_json(filename="property.json", client_id=1, command_type=2, pipe_id=0,
                  algopipeline="mobilenetssd ! tracklp"):
    with cd(controller_dir):
        json_file = {
            "client_id": client_id,
            "command_type": command_type,
            "command_set_property":
                {
                    "pipe_id": pipe_id,
                    "cvdlfilter0":
                        {
                            "algopipeline": algopipeline
                        }
                }
        }
        if os.path.exists(filename):
            os.system("rm %s" % filename)
        with open("./" + filename, "wt") as f:
            json.dump(json_file, f, indent=4)


class cd(object):
    current_path = BASE_PATH

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_value, track):
        os.chdir(cd.current_path)


def decorate_t(func):
    @wraps(func)
    def temp(*args, **kwargs):
        tt = threading.Thread(target=func, args=args, kwargs=kwargs)
        tt.start()

    return temp


class Hddls():
    def __init__(self, testcase="Sample", prompt="command>", pipe_count=2, isRtsp=False, log_level=0,
                 isErrorTest=False):
        self.testcase = testcase
        self.pipe_count = pipe_count
        self.prompt = prompt
        self.isRtsp = isRtsp
        self.log_level = log_level
        self.isErrorTest = isErrorTest
        self.path = os.path.join(Log_info_collect_fold, self.testcase)
        self.file_position = 0
        self.runServer()
        self.runReceive()
        self.runStop()
        self.child = self.runControl()

    @decorate_t
    def runServer(self):
        with cd(server_dir):
            # status = os.system('gnome-terminal -x bash -c "./hddls_server.js;read"')
            # path = os.path.join(Log_info_collect_fold,self.testcase)
            if os.path.exists(self.path):
                os.system("rm -rf {}".format(self.path))
            os.system("mkdir -p {}".format(self.path))
            os.system(
                "export GST_DEBUG={} && node hddl_server.js > {}/server.log 2>&1&".format(self.log_level, self.path))
            # os.system('gnome-terminal -x bash -c "export GST_DEBUG=%d && node hddl_server.js | tee %s/server.log 2>&1 "' % (self.log_level, self.path))

    @decorate_t
    def runReceive(self):
        time.sleep(1.5)
        # path = "{}/{}".format(Log_info_collect_fold, self.testcase)
        filename = "{}/receive.log".format(self.path)
        if not os.path.exists(filename):
            os.system("mkdir -p {}".format(self.path))
        try:
            logfile = open(filename, "ab")
            with cd(receiver_dir):
                child_rec = expect.spawn('node result_receiver.js', logfile=logfile)
                child_rec.interact()
        finally:
            child_rec.close(force=True)
            logfile.close()

    def runControl(self):
        time.sleep(2)
        with cd(controller_dir):
            child = expect.spawn('node controller_cli.js', encoding="utf-8", logfile=sys.stdout)
            child.expect("please enter server host & port")
            child.sendline("localhost:8445")
            child.expect([" ", self.prompt])
            child.sendline("help")
            return child

    def c_command(self, jsonfile="create_self.json"):
        self.child.expect([self.prompt])
        self.child.sendline("c %s" % jsonfile)

    # def pipe_command(self):
    #     try:
    #         self.child.expect(self.prompt)
    #     except expect.exceptions.TIMEOUT as e:
    #         print(e)
    #         pass
    #     self.child.sendline("pipe")
    #     self.child.expect("Rgiht now this client owns pipes as:")
    #     res = re.compile("[\d+,]*\d+")
    #     try:
    #         pipes_string = self.child.readline()[:-8]
    #     except TypeError:
    #         pipes_string = self.child.readline().decode("utf-8")[:-8]
    #     print("\r\033[32mPIPEs:" + str(res.findall(pipes_string)) + "\033[0m\n")
    #     return res.findall(pipes_string)

    def get_pipes(self, server_log="server.log"):
        # global file_position
        with open("%s/%s" % (self.path, server_log), 'rb') as f:
            f.seek(self.file_position)
            content = f.read().decode("utf-8")
            self.file_position = f.tell()
        res = re.compile("valid\s+pipe\s+(\d+)")
        pipes = list(set(res.findall(content)))
        return pipes

    def p_command(self, jsonfile="property.json"):
        pipes = self.get_pipes()
        while not pipes:
            time.sleep(2)
            pipes = self.get_pipes()
        pipe = pipes[0]
        self.child.expect([" ", self.prompt])
        cmd = "p %s %s" % (jsonfile, pipe)
        print("\r" + cmd + "\n")
        self.child.sendline(cmd)

    def d_command(self, jsonfile="destroy.json"):
        pipes = self.get_pipes()
        while not pipes:
            time.sleep(2)
            pipes = self.get_pipes()
        for pipe in pipes:
            self.child.expect([" ", self.prompt])
            cmd = "d %s %s" % (jsonfile, pipe)
            print("\r" + cmd + "\n")
            self.child.sendline(cmd)

    # def client_command(self):
    #     self.child.expect(self.prompt)
    #     self.child.sendline("client")
    #     self.child.expect("client id is")
    #     res = re.compile("\d+")
    #     pipes_string = child.readline().decode("utf-8")
    #     print("-" * 10)
    #     print("\033[32mClients:" + str(pipes_string) + "\033[0m")
    #     print("-" * 10)

    def m_command(self, model_path="models"):
        self.child.expect([self.prompt])
        self.child.sendline("m %s" % model_path)
        # self.child.expect("HERE ARE SERVER MODEL LISTS:")
        # self.child.expect(">")
        # print("-" * 10)
        # print(child.before.decode("utf-8")) 
        # print("-" * 10)

    def q_command(self):
        self.child.expect([self.prompt])
        self.child.sendline("q")

    @decorate_t
    def runStop(self, t1=60, t2=60):
        timestamp = 0
        receive_log = "{}/{}/receive.log".format(Log_info_collect_fold, self.testcase)
        server_log = "{}/{}/server.log".format(Log_info_collect_fold, self.testcase)
        while not (os.path.exists(receive_log) and os.path.exists(server_log)):
            time.sleep(1)
            timestamp += 1
            if timestamp > 30:
                q.put("1")
                return 1
        st_size = 170
        try_time = 5
        clock_count = 0
        if not self.isRtsp:
            while try_time > 0:
                st_size = os.stat(receive_log).st_size
                time.sleep(5)
                if os.stat(receive_log).st_size == st_size:
                    try_time -= 1
                if os.stat(receive_log).st_size > 20907:
                    break
                clock_count += 5
                if clock_count > t1:
                    q.put("1")
                    return 1
            client_exit = 0
            res = re.compile("Child exited with code:")
            seek_position = 0
            clock_count2 = 0
            try_time = 0
            begin = False
            while 1:
                with open(server_log) as f:
                    f.seek(seek_position)
                    clients = res.findall(f.read())
                    client_exit += len(clients)
                    if client_exit == self.pipe_count:
                        q.put("1")
                        return 1
                    elif client_exit > 1:
                        begin = True
                    temp = f.tell()
                    if temp == seek_position:
                        try_time += 1
                    else:
                        seek_position = temp
                        try_time = 0
                    time.sleep(1)
                    if begin:
                        if clock_count2 > t2:
                            q.put("1")
                            return 1
                        clock_count2 += 1
                    if try_time > 10:
                        q.put("1")
                        return 1
        else:
            t1 = 300
            while try_time > 0:
                st_size = os.stat(receive_log).st_size
                time.sleep(5)
                if os.stat(receive_log).st_size == st_size:
                    try_time -= 1
                clock_count += 5
                # print("\n\n try time: %d  clock_count: %d \n\n" % (try_time, clock_count))
                if clock_count > t1:
                    q.put("1")
                    return 1
            else:
                q.put("1")
                return 1

    def kill_js(self):
        while q.empty():
            time.sleep(1)
        else:
            if self.child.isalive():
                self.child.close(force=True)
            while not q.empty():
                q.get()
        os.system('''for pid in `ps -ef|grep ".js"|grep -v grep|awk '{print $2}'`;do kill -9 $pid;done''')
        time.sleep(2)
        os.system("rm -rf {}".format(os.path.join(server_dir, "ipc_socket" + os.sep + "unix.sock")))
        time.sleep(2)

    @staticmethod
    def get_position_datas(fileName):
        # res = re.compile("\((\d+,\d+)\)@(\d+x\d+)")
        res = re.compile("\"x\":\s+(\d+),\s+\"y\":\s+(\d+),\s+\"w\":\s+(\d+),\s+\"h\":\s+(\d+).*")
        with open(fileName, 'rt') as f:
            content = f.read()
        data_src = res.findall(content)
        return data_src

    @staticmethod
    def get_retangle_position(*args):
        # x,y = map(int,args[0][0].split(","))
        # width, height = map(int,args[0][1].split("x"))
        x = int(args[0][0])
        y = int(args[0][1])
        width = int(args[0][2])
        height = int(args[0][3])
        return (x, y), (x + width - 1, y + height - 1)

    @staticmethod
    def green_point(x, y, img):
        if 143 < img[y][x] < 158:
            return True
        return False

    @staticmethod
    def rectangle(img, pos1, pos2):
        (x0, y0), (x1, y1) = pos1, pos2
        x_t0 = x0 - 3
        y_t0 = y0 - 3
        x_t1 = x1 + 3
        y_t1 = y1 + 3
        if all((Hddls.green_point(x0, y0, img), Hddls.green_point(x1, y1, img),
                Hddls.green_point(x0, y1, img), Hddls.green_point(x1, y0, img))):
            try:
                if any((
                        (Hddls.green_point(x_t0, y0, img) and Hddls.green_point(x_t0, y1, img)),
                        (Hddls.green_point(x0, y_t0, img) and Hddls.green_point(x1, y_t0, img)),
                        (Hddls.green_point(x0, y_t1, img) and Hddls.green_point(x1, y_t1, img)),
                        (Hddls.green_point(x_t1, y0, img) and Hddls.green_point(x_t1, y1, img))
                )):
                    return False
            except IndexError:
                return True
            return True
        return False

    def checkResult(self, expect_keywords=None):
        result_record = {}
        result_record["Testcase"] = self.testcase
        result_record["Result"] = "Pass"
        result_record["Reason"] = []
        result_record["log_path"] = os.path.join(Log_info_collect_fold, self.testcase)
        receive_log = "{}/{}/receive.log".format(Log_info_collect_fold, self.testcase)
        server_log = "{}/{}/server.log".format(Log_info_collect_fold, self.testcase)
        controll_log = "{}/{}/controll.log".format(Log_info_collect_fold, self.testcase)
        # resA = re.compile("pipe\s+\d+")
        resA = re.compile("STDOUT:\s+(pipe\s+\d+)")
        resB = re.compile("Fail|error|FAIL|ERROR|[\[|:]ERR")
        try:
            with open(receive_log, "rt") as f:
                content = f.read()
                if resB.findall(content):
                    result_record["Result"] = "Fail"
                    result_record["Reason"].append("Recv:" + str(resB.findall(content)))
            with open(server_log, "rt") as f:
                content = f.read()
                temp_pipes = set(resA.findall(content))
            pipe = []
            for p_ in temp_pipes:
                pipe.append("_".join((p_.split(" "))))
            pipe_count = len(pipe)
            res = re.compile("objects")
            if pipe_count != 0:
                for piName in pipe:
                    os.system("mv {}/{} {}/{}".format(receiver_dir, piName, Log_info_collect_fold, self.testcase))
            for pipeName in pipe:
                pics = glob.glob(Log_info_collect_fold + "/" + self.testcase + "/%s" % pipeName + "/*.jpg")
                pics.sort(reverse=True)
                pic_count = len(pics)
                output_txt = Log_info_collect_fold + "/" + self.testcase + "/%s" % pipeName + "/output.txt"
                with open(output_txt, "rt") as f:
                    output_lines = len(res.findall(f.read()))
                if pic_count > output_lines or (pic_count < output_lines and not cv_check):
                    result_record["Result"] = "Fail"
                    result_record["Reason"].append(
                        "{}-Pic_count:{} != txtData:{}".format(pipeName, pic_count, output_lines))
                elif pic_count == output_lines:
                    pass
                else:
                    data_src = Hddls.get_position_datas(output_txt)
                    position = list(map(Hddls.get_retangle_position, data_src))
                    rectangle_count = 0
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    for pic_name in pics:
                        img_BGR = cv2.imread(pic_name)
                        img = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY)
                        for p in position[:]:
                            po1, po2 = p[0], p[1]
                            if Hddls.rectangle(img, po1, po2):
                                index = pics.index(pic_name)
                                rectangle_count += 1
                                cv2.putText(img_BGR, str(rectangle_count), po1, font, 3, (0, 165, 255), 2, cv2.LINE_AA)
                                cv2.imwrite(pic_name, img_BGR)
                                position.remove(p)
                    if position:
                        result_record["Result"] = "Fail"
                        result_record["Reason"].append("{}-Position{} not find in pic".format(pipeName, position))
                    if rectangle_count == output_lines:
                        continue
                    else:
                        result_record["Result"] = "Fail"
                        result_record["Reason"].append(
                            "{}-rectangle_coun:{} != txtData:{}".format(pipeName, rectangle_count, output_lines))
        except FileNotFoundError as e:
            result_record["Result"] = "Fail"
            result_record["Reason"].append(receive_log + "[" + e + "]")
        try:
            with open(server_log) as f:
                content = f.read()
            if not self.isErrorTest:
                if resB.findall(content):
                    result = "Fail"
                    result_record["Result"] = "Fail"
                    result_record["Reason"].append("Server:" + str(resB.findall(content)))
            if expect_keywords:
                res_expect = re.compile(expect_keywords)
                keywordsLine = res_expect.findall(content)
                if not keywordsLine:
                    result_record["Result"] = "Fail"
                    result_record["Reason"].append("Don't find the expect context(%s)" % expect_keywords)
                else:
                    result_record["Reason"].append("The expect context(%s)" % keywordsLine)
        except FileNotFoundError as e:
            result_record["Result"] = "Fail"
            result_record["Reason"].append(server_log + "[" + e + "]")
        with open("%s/testcase_result.csv" % Log_info_collect_fold, "at") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([result_record["Testcase"], result_record["Result"], str(result_record["Reason"]),
                             result_record["log_path"]])
        if result_record["Result"] == "Fail":
            return 0
        else:
            return 1


os.system('''for pid in `ps -ef|grep ".js"|grep -v grep|awk '{print $2}'`;do kill -9 $pid;done''')
if __name__ == "__main__":
    create_json()
    hddls = Hddls("GS001")
    hddls.c_command()
    hddls.kill_js()
    hddls.checkResult()

    hddls = Hddls("GS002")
    hddls.c_command()
    hddls.kill_js()
    hddls.checkResult()
