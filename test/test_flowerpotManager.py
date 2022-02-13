import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import flowerpotManager
import unittest


class TestFlowerpot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')


    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')


    def setUp(self):
        self.pot = flowerpotManager.flowerpot(42, 'testpot')


    def tearDown(self):
        pass


    def test_set_expected_moisture(self):
        self.assertEqual(0, self.pot.expected_moisture)

        self.pot.set_expected_moisture(33)
        self.assertEqual(33, self.pot.expected_moisture)


    def test_set_actual_moisture(self):
        self.assertEqual(flowerpotManager.measurement, self.pot.actual_moisture)

        self.pot.set_actual_moisture(33)
        self.assertEqual(33, self.pot.actual_moisture)


    def test_activate_deactivate(self):
        self.assertTrue(self.pot.is_active)
        
        self.pot.deactivate()
        self.assertFalse(self.pot.is_active)

        self.pot.activate()
        self.assertTrue(self.pot.is_active)


    def test_needs_water(self):
        self.pot.set_actual_moisture(33)
        self.pot.set_expected_moisture(34)
        self.assertTrue(self.pot.needs_water())

        self.pot.set_expected_moisture(33)
        self.assertTrue(self.pot.needs_water())

        self.pot.set_expected_moisture(32)
        self.assertFalse(self.pot.needs_water())


class TestFlowerpotManager(unittest.TestCase):
    
    def test_HELLO(self):
        pass


if __name__ == '__main__':
    unittest.main()