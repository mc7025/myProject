gnome-terminal -x bash -c ". /opt/intel/computer_vision_sdk/bin/setupvars.sh;echo 'intel123'|sudo -S rm -rf '/home/hddl/work/hddls_server_controller_receiver/server/ipc_socket/';sleep 2;export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/intel/mediasdk/lib64/pkgconfig;export HDDLS_CVDL_KERNEL_PATH=/usr/lib/x86_64-linux-gnu/libgstcvdl/kernels;export PATH=$PATH:/opt/intel/mediasdk/bin/;export HDDLS_CVDL_MODEL_PATH=/home/hddl/work/hddls_server_controller_receiver/server/models;export LD_LIBRARY_PATH=/opt/intel/mediasdk/lib64:/opt/intel/computer_vision_sdk/inference_engine/lib/ubuntu_16.04/intel64:/opt/intel/computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/omp/lib:/usr/lib/x86_64-linux-gnu/gstreamer-1.0:/usr/local/lib:/opt/intel/computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/hddl/lib:/opt/intel//computer_vision_sdk_2018.5.445/opencv/lib:/opt/intel/opencl:/opt/intel//computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/hddl/lib:/opt/intel//computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/gna/lib:/opt/intel//computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/mkltiny_lnx/lib:/opt/intel//computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/omp/lib:/opt/intel//computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/lib/ubuntu_16.04/intel64:/opt/intel//computer_vision_sdk_2018.5.445/deployment_tools/model_optimizer/bin:/opt/intel//computer_vision_sdk_2018.5.445/openvx/lib;cd /home/hddl/work/hddls_server_controller_receiver;. ~/.bashrc;python3 run_demo_cls_reboot_v1_3.py"
