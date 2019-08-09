import os
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
import HTMLTestRunner
import config

if len(sys.argv) > 3:
    config.USER = sys.argv[2]
    config.PASSWORD = sys.argv[3]
else:
    print("\n\n Usage: {} <component_id> <host_username> <host_password> \n\n".format(sys.argv[0]))
    sys.exit(-1)

config.CARD_TYPE = sys.argv[4]
config.DEVICE_NUM = sys.argv[5]

log_dir = os.path.join(config.BASE_DIR, 'output')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def run_module(path, pattern, component):
    with open(os.path.join(log_dir, 'report.html'), 'wb') as fp:
        suite = unittest.TestLoader().discover(path, pattern=pattern)
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, verbosity=2,
                                               title='IOP Test Report ---- {}'.format(component),
                                               description='IOP')
        runner.run(suite)


def main():

    if sys.version_info.major != 3:
        print("\033[33mPlease use python 3.xxx!\033[0m")
        exit(1)

    # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from IE", 4:"Test all of POR's Open CNN", 5:"Custom"
    component_id = sys.argv[1]

    if len(sys.argv) > 7:
        path = sys.argv[6]
        pattern_value = sys.argv[7]
    else:
        path = 'IOP{}testcases'.format(os.sep)
        pattern_value = ""

    if component_id == "0":
        run_module(path=path, pattern='test*.py', component='ALL')
    elif component_id == "1":
        run_module(path=path, pattern='test_os.py', component='OS&&Driver')
    elif component_id == "2":
        run_module(path=path, pattern='test_sc.py', component='System Control')
    elif component_id == "3":
        run_module(path=path, pattern='test_ie_others.py', component='Do Inference from IE')
    elif component_id == "4":
        run_module(path=path, pattern='test_ie_mo_n.py', component='Test all of POR\'s Open CNN')
    elif component_id == "5":
        run_module(path=path, pattern=pattern_value, component='Custom Component')


if __name__ == '__main__':
    main()
