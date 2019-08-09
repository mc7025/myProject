1. use python3
2. need pexpect module(pip3 install pexpect)

put test script under hddls_server_controller_receiver, like below:
   hddl@hddl-B360-N158:~/3_ww/hddls_server_controller_receiver$ ls *.py
   run_demo_cls_gr_v1_3.py test_main_oop.py

Run command for all testcase:
python3 test_main_oop.py

Run command for single testcase(special testcase defined in test_main_oop.py):
python3 -m unittest test_main_oop.TestGS.test_GSXXX
like as:
python3 -m unittest test_main_oop.TestGS.test_GS013 
   
Note:
Need to update the "stream_source=" in the test_main_oop.py 
or
put the relevant videos to the matched path
Video can get from "hddl@10.240.109.140:/home/hddl/hddl_s"