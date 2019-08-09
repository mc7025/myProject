#enconding:utf-8
#!/usr/bin/python3

import os
import time
import re
import json
import threading
from functools import wraps
import sys
from datetime import datetime
#from runserver import *

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

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
Log_info_collect_fold = os.path.join(BASE_PATH, datetime.now().strftime("%Y%m%d%H%M%S"))
receiver_dir = os.path.join(BASE_PATH,"receiver")
controller_dir = os.path.join(BASE_PATH,"controller")
server_dir = os.path.join(BASE_PATH, "server")
prompt = "command>"
server_command = "node hddl_server.js"
contoller_command = "node controller_cli.js"
receive_command = "node result_receiver.js"

file_position = 0 
#old_pipes = set()
def create_json(filename="create_self.json",client_id=1,command_type=0, pipe_num = 2,
                stream_source="/home/hddl/Videos/1600x1200.mp4",
                codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2",
                loop_times=1):
    json_file = {
                    "client_id": client_id,
                    "command_type" : command_type,
                    "command_create":  
                    {
                       "pipe_num": pipe_num,
                       "stream_source": stream_source,
                       "codec_type": codec_type,
                       "output_type":0,
                       "cvdlfilter0":
                       {
                           "algopipeline": algopipeline
                       },
                       "loop_times": loop_times
                    }
                }
    with cd(controller_dir):
        if os.path.exists(filename):
            os.system("rm %s" % filename)
        with open("./" + filename, "wt") as f:
            json.dump(json_file, f)

def destroy_json(filename="destroy.json", client_id=1, command_type=1, pipe_id=0):
    json_file = {
                  "client_id":client_id,
                  "command_type":command_type,
                  "command_destroy":
                  {
                     "pipe_id":pipe_id
                  }
                }
    with cd(controller_dir):
        with open("./" + filename, "wt") as f:
            json.dump(json_file, f)

def c_command(child, jsonfile="create_self.json"):
    child.expect([prompt])
    child.sendline("c %s" % jsonfile)

def pipe_command(child):
    global file_position
    try:
        child.expect(prompt)
    except expect.exceptions.TIMEOUT as e:
        print(e)
        pass
    child.sendline("pipe\n")
    child.expect([" ",prompt,"Set"])
    child.sendline("help")
    res = re.compile("Set\s+\{(.*)\}")
    current_pipes = []
    with open("./controller_log.log", "rb") as f:
        f.seek(file_position)
        content = f.read()
        file_position = f.tell()
    pipes_from_re = res.findall(content.decode("utf-8"))
    for record in pipes_from_re:
        current_pipes.extend(record.split(","))
    pipes = set(current_pipes)
    return pipes

def p_command(child, jsonfile="property.json"):
    child.expect([" ", prompt])
    pipe_set = pipe_command(child)[0].split(",")
    time.sleep(5)
    child.expect([" ",prompt]) 
    cmd = "p ./%s %s" % (jsonfile, pipe_set[-1])
    print(cmd)
    child.sendline(cmd)
    child.expect("set_property command!!!")
    child.sendline("-c")

def d_commandi_o(child, jsonfile="destroy.json"):
    child.expect([" ",prompt])
    time.sleep(1)
    pipes = pipe_command(child)
    if pipes:
        for pipe in pipes:
            child.expect([" ", prompt])
            cmd = "d ./%s %s" % (jsonfile, pipe.strip())
            print("\r" + cmd + "\n")
            child.sendline(cmd)
    child.close(force=True)

def d_command(child, jsonfile="destroy.json"):
    with cd(controller_dir):
        global file_position
        child.expect([" ",prompt])
        time.sleep(1)
        #server run with "hddls_server.js >> ./controller/server_log.log 2>&1"
        with open("./server_log.log", "rb") as f:
            f.seek(file_position)
            content = f.read().decode("utf-8")
            file_position = f.tell()
        res = re.compile("valid\s+pipe\s+(\d+)")
        pipes = set(res.findall(content))
        if pipes:
            for pipe in pipes:
                child.expect([" ", prompt])
                cmd = "d ./%s %s" % (jsonfile, pipe.strip())
                print("\r" + cmd + "\n")
                child.sendline(cmd)

def decorate_t(func):
    @wraps(func)
    def temp(*args, **kwargs):
        tt = threading.Thread(target=func, args=args, kwargs=kwargs)
        tt.start()
    return temp

@decorate_t
def runReceive(testcase="GS01"):
    filename = "{}/{}/receive.log".format(Log_info_collect_fold, testcase)
    if not os.path.exists(filename):
        os.system("mkdir -p {}/{}".format(Log_info_collect_fold, testcase))
    try:
        logfile = open(filename, "ab")
        with cd(receiver_dir):            
            child_rec = expect.spawn(receive_command, logfile=logfile)
            child_rec.interact()
    finally:
        child_rec.close(force=True)
        logfile.close()

class cd():
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        os.chdir(self.path)
    def __exit__(self,exc_type, exc_value, trac):
        os.chdir(BASE_PATH)

def kill_server():
    cmd = "kill -9 `ps -ef|grep hddl_server.js|grep -v grep|awk '{print $2}'`"
    os.system(cmd)

def run_server():
    kill_server()
    files = "/home/hddl/work/hddls_server_controller_receiver/server/ipc_socket/unix.sock"
    while 1:
        if not  os.path.exists(files):
            break
        os.system("echo 'intel123'|sudo -S rm -rf {}".format(files))
        time.sleep(1)
    time.sleep(2)
    cmd = 'gnome-terminal -x bash -c "{}|tee {}/server_log.log"'.format(server_command, controller_dir)
    os.system(cmd)

def runControl():
    time.sleep(2)
    if not os.path.exists("controller_cli.js"):
        os.chdir(controller_dir)
    controller_log = open("controller_log.log","at")
    child = expect.spawn(contoller_command, encoding="utf-8",logfile=controller_log)
    child.expect("please enter server host & port")
    child.sendline("localhost:8445")
    child.expect([" ", prompt])
    child.sendline("help")      
    return child

def chose_json(mode):
    if mode == "uc1_5":
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0016",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
    elif mode == "uc1_4":
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000",codec_type="H.264",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2")
    elif mode == "uc2_5":
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0016",codec_type="H.265",algopipeline="mobilenetssd ! tracklp ! lprnet")
    elif mode == "uc2_4":
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0000",codec_type="H.264",algopipeline="mobilenetssd ! tracklp ! lprnet")
    elif mode == 'uc3_5':
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0027",codec_type="H.265",algopipeline="yolov2tiny ! reid")
    elif mode == 'uc3-4':
        create_json(stream_source="rtsp://10.240.109.164:1554/simu0011",codec_type="H.264",algopipeline="yolov2tiny ! reid")
    else:
        print("Error mode")

def runUC(mode):
    child = runControl()
    chose_json(mode)
    c_command(child)
    time.sleep(15)
    d_command(child)
    time.sleep(1)
    
@decorate_t
def showStatus():
    while 1:
        sys.stdout.write("\r\033[32mTestRun, UC1: {}, UC2:{}, UC3:{}, Mixed:{}\033[0m".format(count_UC1, count_UC2, count_UC3, count_UC4))
        time.sleep(3)
    
if __name__ == "__main__":
    
    with cd(server_dir):
        run_server()
    
    count_UC1, count_UC2, count_UC3, count_UC4 = 0, 0, 0, 0
    showStatus()    
    runReceive() 
    destroy_json()
     
    for i in range(2):
        runUC("uc1_5")
        runUC("uc1_4")
        count_UC1 += 1  
        

    for i in range(2):
        runUC("uc2_5")
        runUC("uc2_4")
        count_UC2 += 1
    
    for i in range(2):
        runUC("uc3_5")
        runUC("uc3_4")
        count_UC3 += 1

    for i in range(2):
        runUC("uc1_5")
        runUC("uc1_4")
        runUC("uc2_5")
        runUC("uc2_4")
        runUC("uc3_5")
        runUC("uc3_4")
        count_UC4 += 1

    with open(Log_info_collect_fold + "/UC_1_2_3_4.log","at") as f:
        f.write("At last run times: {} {} {} {}".format(count_UC1, count_UC2, count_UC3, count_UC4))

    #os.system("./start_reboot.sh")

