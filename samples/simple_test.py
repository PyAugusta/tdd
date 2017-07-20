# samples/OurTests.py
import unittest


# Start by creating a TestCase class
class OurTests(unittest.TestCase):
    # We can overwrite the unittest.TestCase.setUp method
    # to ensure the tests have access to the same value
    def setUp(self):
        self.our_value = 1

    # Then, add custom test functions to the class

    def test_is_int(self):
        self.assertIsInstance(self.our_value, int)

    def test_is_one(self):
        self.assertEqual(self.our_value, 1)

    def test_is_two(self):
        self.assertEqual(self.our_value, 2)


# Now, we can tell out test to run if the
# script is called from the command line
if __name__ == '__main__':
    unittest.main()
