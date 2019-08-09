import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
import unittest
import HTMLTestRunner

if len(sys.argv) < 2:
    print("\n\n Usage: {} <component_id> \n\n".format(sys.argv[0]))
    sys.exit(-1)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

log_dir = os.path.join(BASE_PATH, 'output')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def run_module(path, pattern, component):
    with open(os.path.join(log_dir, 'report.html'), 'wb') as fp:
        suite = unittest.TestLoader().discover(path, pattern=pattern)
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, verbosity=2,
                                               title='HDDL-S Sanity Test Report ---- {}'.format(component),
                                               description='HDDL-S')
        runner.run(suite)


def main():
    component_id = sys.argv[1]

    if len(sys.argv) > 3:
        path = sys.argv[2]
        pattern_value = sys.argv[3]
    else:
        path = 'hddl_s_sw_validation{}Function_test'.format(os.sep)
        pattern_value = ""

    if component_id == "0":
        run_module(path=path, pattern='test*.py', component='ALL')
    elif component_id == "1":
        run_module(path=path, pattern='test_os.py', component='Linux OS')
    elif component_id == "2":
        run_module(path=path, pattern='test_main_oop.py', component='GStreamer And Plugin')
    elif component_id == "3":
        run_module(path=path, pattern='test_remoteController.py', component='Remote Controller')
    elif component_id == "4":
        run_module(path=path, pattern=pattern_value, component='Custom Component')


if __name__ == '__main__':
    main()