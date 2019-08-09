1.Testcate for reliability, Kill and start HDDL pipeline 500 times
  UC1:stream_source="rtsp://10.240.109.140:8000/dahua0.265",codec_type="H.265",algopipeline="yolov1tiny ! opticalflowtrack ! googlenetv2"(rtsp://10.240.109.140:8000/dahua0.264)
  UC2:stream_source="rtsp://10.240.109.140:8000/dahua0.265",codec_type="H.265",algopipeline="mobilenetssd ! tracklp ! lprnet"(rtsp://10.240.109.140:8000/dahua0.264)
  UC3:stream_source="rtsp://10.240.109.140:8000/indoor11920x1080.265",codec_type="H.265",algopipeline="yolov2tiny ! reid"(rtsp://10.240.109.140:8000/indoor11920x1080.265)
  UC4: Mixed UC1/UC2/UC3                  

2.Put the script under ../hddls_server_controller_receiver/
  hddl@hddl-B360-N158:~/3_ww/hddls_server_controller_receiver$ ls
  controller                         run_RR_thr_F1_25.py
  install.md                         lib 
  server                             node_modules
  .....

3.Need pexpect python module
  sudo apt install python3-pipe
  sudo pip3 install pexpect

4.Run on local for rtsp stream, this is important:
  python3 run_RR_thr_F1_25.py 

Note:
Before run the test, please check the rtsp streams are normal.  
 
	