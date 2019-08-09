1.Testcate for reliability,  Reset host 500 times                 

2.Sudo vim /etc/default/apport  set the value 0, disable the pop msg

3.Put the script under ../hddls_server_controller_receiver/
  hddl@hddl-B360-N158:~/3_ww/hddls_server_controller_receiver$ ls
  controller                         start_reboot.sh
  install.md                         run_demo_cls_reboot_v1_3.py 
  server                             node_modules
  .....

4.Alter the "run_demo_cls_reboot_v1_3.py"
  set stream_source to a actual source
  create_json(stream_source="/home/hddl/Videos/Video_multi_size/barrier1920x1080.avi_avc.mp4")

5.Check the env parameter in "start_reboot.sh" is all normall else update it.
  
6.Set "gnome-session-properties", and add "start_reboot.sh" to "gnome-session-properties"

7.Run:
  python3 run_demo_cls_reboot_v1_3.py

  
 
	