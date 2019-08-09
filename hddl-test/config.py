# basic configuration info
import os

USER = ""
PASSWORD = ""

CARD_TYPE = ""
DEVICE_NUM = ""
###############################

HDDL_SOURCE_DIR = r'/home/hddl/work/ww08_2019'
# OS_001
LINUX_VERSION = ("Ubuntu", "16.04", "xenial")
# OS_002
KERNEL_VERSION = "4.14.20"

DEBUG = False

MO_FILE = r"/opt/intel/openvino/deployment_tools/model_optimizer/mo.py"

# The path where can find the so file "libinference_engine.so"
InferenceEngine_lib = r"/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

