# tippy/tests/config_test.py
import os
import sys

test_dir = os.path.abspath(os.path.dirname(__file__))
tippy_dir = os.path.abspath(os.path.join(test_dir, '..'))

sys.path.extend([test_dir, tippy_dir])

test_amount = 5.00
test_percent = 50

expected_check_to_tip = (2.50, 7.50)
expected_check_to_rtip = (3.00, 8.00)
