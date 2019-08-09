import unittest
import common.utils
import os
import sys


class Test_BslReset(unittest.TestCase):

    def setUp(self):
        self.bsl_reset = common.utils.BslReset()

    def test_init(self):
        hddl_install_dir = os.environ.get('HDDL_INSTALL_DIR')
        if os.name == 'nt':
            expectd = os.path.join(hddl_install_dir, 'build/output/bin/bsl_reset.exe')
            self.assertEqual(self.bsl_reset.bsl_reset_bin, expectd)
        elif os.name == 'posix':
            expectd = os.path.join(hddl_install_dir, 'hddl-bsl/build/src/bsl_reset')
            self.assertEqual(self.bsl_reset.bsl_reset_bin, expectd)
        else:
            raise ValueError('Not supported OS')
        self.assertTrue(os.path.exists(expectd))

    def test_reset_all(self):
        pass


class Test_Server(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hddl_install_dir = os.environ.get('HDDL_INSTALL_DIR')

    def setUp(self):
        self.server = common.utils.Server(1)

    def tearDown(self):
        if self.server.is_running():
            self.server.stop_run()

    def test_init(self):
        if os.name == 'nt':
            expected = os.path.join(self.hddl_install_dir, 'bin/hddldaemon.exe')
            self.assertEqual(self.server.bin, expected)
        elif os.name == 'posix':
            expected = os.path.join(self.hddl_install_dir, 'bin/hddldaemon')
            self.assertEqual(self.server.bin, expected)
        self.assertTrue(os.path.exists(expected))

        expected = os.path.join(self.server.output_dir, '1/hddl_service.config')
        self.assertTrue(os.path.exists(expected))
        expected = os.path.join(self.server.output_dir, '1/hddl_autoboot.config')
        self.assertTrue(os.path.exists(expected))

        self.assertFalse(self.server.is_running())

    def test_start_run(self):
        self.assertIsNone(self.server.parser_log)
        self.server.start_run()
        self.assertIsNotNone(self.server.parser_log)
        # add


    def test_is_ready(self):
        self.assertFalse(self.server.is_ready())
        self.server.start_run()
        self.assertTrue(self.server.is_ready())

    def test_is_runing(self):
        self.assertFalse(self.server.is_running())
        self.server.start_run()
        self.assertTrue(self.server.is_running())

    def test_get_log_exists(self):
        self.assertIsNone(self.server.logfile)
        self.server.start_run(file='1111.log')
        expected = os.path.join(self.server.output_dir, '1/1111.log')
        self.assertEqual(self.server.get_log(), expected)
        self.assertTrue(os.path.exists(expected))

    def test_get_log_no_exists(self):
        self.server.start_run(log=False)
        self.assertIs(self.server.get_log())

    def test_stop_run(self):
        self.server.start_run()
        self.assertTrue(self.server.is_running())
        self.assertIsNotNone(self.server.parser_log.parser_log_thread)
        self.server.stop_run()
        self.assertFalse(self.server.is_running())
        # add parser log thread is stop

def main():
    loader = unittest.TestLoader()
    suite1 = loader.loadTestsFromTestCase(Test_BslReset)
    suite2 = loader.loadTestsFromTestCase(Test_Server)
    suite = unittest.TestSuite([suite1, suite2])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(-1)


if __name__ == '__main__':
    main()
