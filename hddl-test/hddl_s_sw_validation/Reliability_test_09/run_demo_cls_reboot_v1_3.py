#enconding:utf-8
#!/usr/bin/python3

import os
import sys
import time
import re
import json
import threading
from functools import wraps
from datetime import datetime
import glob
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

"""
status = os.system("expect -v")
if status !=0 :
    os.system("echo intel123|sudo -s apt install expect")
"""

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
Log_info_collect_fold = os.path.join(BASE_PATH, datetime.now().strftime("%Y%m%d%H%M%S"))
receiver_dir = os.path.join(BASE_PATH,"receiver")
controller_dir = os.path.join(BASE_PATH,"controller")
server_dir = os.path.join(BASE_PATH, "server")

def create_json(filename="create_self.json",client_id=1,command_type=0, pipe_num = 2,
                stream_source="/home/hddl/Videos/Video_multi_size/1600x1200.mp4",
                codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2",
                loop_times=1):
    with cd(controller_dir):
        json_file = {
                        "client_id": client_id,
                        "command_type" : command_type,
                        "command_create":  
                        {
                           "pipe_num": pipe_num,
                           "stream_source": stream_source,
                           "codec_type": codec_type,
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
            json.dump(json_file, f)

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
    def __init__(self, testcase="Sample", prompt = "command>", pipe_count=2):
        self.testcase = testcase
        self.pipe_count = pipe_count
        self.prompt = prompt
        self.runServer()
        self.runReceive()
        self.runStop()
        self.child = self.runControl()

    @decorate_t
    def runServer(self):
        with cd(server_dir):
            path = os.path.join(Log_info_collect_fold,self.testcase)
            if os.path.exists(path):
                os.system("rm -rf {}".format(path))
            os.system("mkdir -p {}".format(path))
            os.system("node hddl_server.js |tee {}/server.log".format(path))
            #os.system('gnome-terminal -x bash -c "node hddl_server.js |tee {}/server.log"'.format(path))

    @decorate_t
    def runReceive(self):
        time.sleep(1.5)
        path = "{}/{}".format(Log_info_collect_fold, self.testcase)
        filename = "{}/receive.log".format(path)
        if not os.path.exists(filename):
            os.system("mkdir -p {}".format(path))
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
            child = expect.spawn('node controller_cli.js', encoding="utf-8",logfile=sys.stdout)
            child.expect("please enter server host & port")
            child.sendline("localhost:8445")
            child.expect([" ", self.prompt])
            child.sendline("help")
            return child

    def c_command(self, jsonfile="create_self.json"):
        self.child.expect([self.prompt])
        self.child.sendline("c %s" % jsonfile)  

    @decorate_t
    def runStop(self, t1=60, t2 = 60):
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
        while try_time > 0:
            if os.stat(receive_log).st_size > st_size:
                st_size = os.stat(receive_log).st_size
                try_time -= 1
            elif os.stat(receive_log).st_size > 20907:
                break
            time.sleep(1)
            clock_count += 1
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

@decorate_t
def showStatus():
    while 1:
        sys.stdout.write("\r{} Reboot times: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), times))
        time.sleep(1)
        
if __name__ == "__main__":
    times = len(glob.glob("2019*"))
    create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4")
    hddls = Hddls("RR05")
    hddls.c_command()
    showStatus()
    time.sleep(40)
    if times > 200:
        exit()
    files = "/home/hddl/work/hddls_server_controller_receiver/server/ipc_socket/unix.sock"
    while 1:
        if not  os.path.exists(files):
            break
        os.system("echo 'intel123'|sudo -S rm -rf {}".format(files))
        time.sleep(1)
    os.system("echo 'intel123'|sudo -S reboot")
