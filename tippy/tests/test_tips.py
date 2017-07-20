# tippy/tests/test_tips.py
import unittest
import config_tests
from tippy import tips


class TestTips(unittest.TestCase):
    def setUp(self):
        self.check = tips.Check(config_tests.test_amount)
        self.percent = config_tests.test_percent

    def test_bad_init(self):
        with self.assertRaises(TypError):
            check = tips.Check('bacon')

    def test_check_to_tip_rtype(self):
        self.assertIsInstance(self.check.check_to_tip(self.percent), tuple)

    def test_check_to_tip_floats(self):
        for val in self.check.check_to_tip(self.percent):
            self.assertIsInstance(val, float)

    def test_check_to_tip(self):
        result = self.check.check_to_tip(self.percent)
        self.assertEqual(result, config_tests.expected_check_to_tip)

    def test_check_to_rtip_rtype(self):
        self.assertIsInstance(self.check.check_to_rtip(self.percent), tuple)

    def test_check_to_rtip_floats(self):
        for val in self.check.check_to_rtip(self.percent):
            self.assertIsInstance(val, float)

    def test_check_to_rtip(self):
        result = self.check.check_to_rtip(self.percent)
        self.assertEqual(result, config_tests.expected_check_to_rtip)


if __name__ == '__main__':
    unittest.main()