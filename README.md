# Test Driven Development with Python #

This tutorial and accompanying repository is intended to introduce you to the concept of Test Driven Development (TDD) with Python.

Simply put, the TDD concept is a development paradigm in which each class, function, line, etc... that comprises a project is written *after*
a unit test has been developed to ensure correct behaviour. This requires meticulous planning on the part of the developers; however, it has been
proven to be a sound strategy to creating reliable software.

Luckily, there are a number of unit testing frameworks to choose from when working with Python that make the process easier. The Python standard library
includes the **unittest** and **pydoc** modules, which are purpose-built just for TDD with Python. We will start by covering some of the basics of the unittest 
framework, and if we have time, we'll try out pydoc as well.

So, let's begin...

## Into to unittest #

Many of you may have seen the **assert** keyword in code before. What it does is test that a condition is True. If not, an **AssertionError** is raised.

    >>> assert 1 == 1 # nothing happens because it's True
    >>> assert 1 == 2
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AssertionError
    
The **assert** keyword is useful in itself for many of your testing needs; however, the unittest package greatly extends 
your testing options

    # samples/simple_test.py
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
        
From the command line, we can now run our test.

    $ cd samples/
    $ python simple_test.py
    
Which will output a report letting us know which tests passed and which failed.

    ..F
    ======================================================================
    FAIL: test_is_two (__main__.OurTests)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "simple_test.py", line 21, in test_is_two
        self.assertEqual(self.our_value, 2)
    AssertionError: 1 != 2
    
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s
    
    FAILED (failures=1)

Now that you have a basic idea of the structure of a Test Case, lets start a new project.

## Planning our Project #

For this tutorial, we'll be creating a simple Python library called **tippy** to help you determine the amount to tip 
after a night out at your favorite restaurant.

The file structure of this project will look like this:

```
+ tippy/
    |+ tests/
    |   |- monitor          # shell script runs tests periodically (*nix users only)
    |   |- config_tests.py  # sets up out testing environment
    |   |- test_tips.py     # matches code in tippy.tips
    |+ tippy/
    |   |- __init__.py      # the main tippy class 
    |   |- tips.py          # module to calculate tips
```

Now that we have an idea of how tippy will be structured, let's go through and plan/write/test each file.

## Creating our project with TDD

### tippy/tippy/tips.py - 1st iteration #

We've thought about our tip calculator a bit, and decided that we'll basically only need one class, with two methods:

1. check_to_tip: Takes some amount of money, and a tip percentage in order to determine the amount to tip.
2. check_to_rtip: Takes some amount of money, and a tip percentage, but rounds the tip so that the resulting total is 
a whole dollar.

Instead of diving straight in and writing a fully functioning class, we'll first make a simple skeleton of it that does 
pretty much nothing.

    # tippy/tippy/tips.py
    class Check(object):
    
        def __init__(self, amount):
            '''Initialize a Check object, which holds the bill amount'''
            self.amount = amount
            
        def check_to_tip(self, percent):
            '''Returns tuple with the tip amount and total bill after applying the tip'''
            pass
            
        def check_to_rtip(self, percent):
            '''Returns tuple the tip amount and total bill after adjusting the tip to
            ensure the total bill is a whole dollar amount'''
            pass

Now that we have our skeleton mapped out, lets start the fun stuff.

### tippy/tests/config_test.py #

This script simply helps us get set up to be able to easily import the tippy module into the test scripts we'll write 
next, and sets some variable for us to use.

    # tippy/tests/config_test.py
    import os
    import sys
    
    test_dir = os.path.abspath(os.path.dirname(__file__))
    tippy_dir = os.path.abspath(os.path.join(test_dir, '..'))
    
    sys.path.extend([test_dir, tippy_dir])
    
    test_amount = 43.67
    test_percent = 20
    

### tippy/tests/test_tips.py - 1st iteration #

Now, the important part for our TDD - the test script.

Essentially, what we will do is mirror tips.py. To start, lets just make sure that the return value from our two functions
are tuples as expected.

    # tippy/tests/test_tips.py
    import unittest
    import config_tests
    from tippy import tips
    
    
    class TestTips(unittest.TestCase):
    
        def setUp(self):
            self.check = tips.Check(config_tests.test_amount)
            self.percent = config_tests.test_percent
    
        def test_check_to_tip_rtype(self):
            self.assertIsInstance(self.check.check_to_tip(self.percent), tuple)
    
        def test_check_to_rtip_rtype(self):
            self.assertIsInstance(self.check.check_to_rtip(self.percent), tuple)
    
    
    if __name__ == '__main__':
        unittest.main()
        
Now, we can run our test and see the expected failures it produces.

    $ cd tippy/tests
    $ python test_tips.py
    
    FF
    ======================================================================
    FAIL: test_check_to_rtip_rtype (__main__.TestTips)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_tips.py", line 16, in test_check_to_rtip_rtype
        self.assertIsInstance(self.check.check_to_rtip(self.percent), tuple)
    AssertionError: None is not an instance of <class 'tuple'>
    
    ======================================================================
    FAIL: test_check_to_tip_rtype (__main__.TestTips)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_tips.py", line 13, in test_check_to_tip_rtype
        self.assertIsInstance(self.check.check_to_tip(self.percent), tuple)
    AssertionError: None is not an instance of <class 'tuple'>
    
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s
    
    FAILED (failures=2)

### tippy/tippy/tips.py - 2nd iteration #

Now that we have a working test script, the name of the game is ensuring that we pass the tests. At this point, we only
test that the return type is a tuple, so let's fix our code

    # tippy/tippy/tips.py
    class Check(object):
    
        def __init__(self, amount):
            '''Initialize a Check object, which holds the bill amount'''
            self.amount = amount
            
        def check_to_tip(self, percent):
            '''Returns tuple with the tip amount and total bill after applying the tip'''
            return ()
            
        def check_to_rtip(self, percent):
            '''Returns tuple the tip amount and total bill after adjusting the tip to
            ensure the total bill is a whole dollar amount'''
            return ()
            
Then, we can re-run our test to see if we're passing.

    $ python test_tips.py
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s
    
    OK
    
Eureka!!! But wait, we still need to make tippy do something useful...back to the test script.

### tippy/tests/test_tips.py - 3rd iteration #

Let's add tests to ensure that both values return by our functions are floats.

    # tippy/tests/test_tips.py
    import unittest
    import config_tests
    from tippy import tips
    
    
    class TestTips(unittest.TestCase):
    
        def setUp(self):
            self.check = tips.Check(config_tests.test_amount)
            self.percent = config_tests.test_percent
    
        def test_check_to_tip_rtype(self):
            self.assertIsInstance(self.check.check_to_tip(self.percent), tuple)
            
        def test_check_to_tip_floats(self):
            for val in self.check.check_to_tip(self.percent):
                self.assertIsInstance(val, float)
    
        def test_check_to_rtip_rtype(self):
            self.assertIsInstance(self.check.check_to_rtip(self.percent), tuple)
            
        def test_check_to_rtip_floats(self):
            for val in self.check.check_to_rtip(self.percent):
                self.assertIsInstance(val, float)
    
    
    if __name__ == '__main__':
        unittest.main()
        
If we run the test, we'll once again see those terrible FAILURES appear, so lets fix them.

### tippy/tippy/tips.py - 3rd iteration #

    # tippy/tippy/tips.py
    class Check(object):
        def __init__(self, amount):
            '''Initialize a Check object, which holds the bill amount'''
            self.amount = amount
    
        def check_to_tip(self, tip_percent):
            '''Returns tuple with the tip amount and total bill after applying the tip'''
            tip = self.amount * tip_percent / 100
            total = self.amount + tip
            return tip, total
    
        def check_to_rtip(self, tip_percent):
            '''Returns tuple with the tip amount and total bill after adjusting the tip to
            ensure the total bill is a whole dollar amount'''
            tip, total = self.check_to_tip(tip_percent)
            f_total = int(total)
            if total == f_total:
                return tip, total
            n_total = f_total + 1
            n_tip = tip + n_total - total
            return n_tip, n_total

Once again, it looks like we're passing with flying colors

### tippy/tests/config_tests.py - 2nd iteration #

So far, things are looking good, but we've yet to actually examine the values our calculator returns. So, lets make some
adjustments to our configuration, so that we have some expected results.

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
    
Next, let's add to our test

### tippy/tests/test_tips.py - 4th iteration #

    # tippy/tests/test_tips.py
    import unittest
    import config_tests
    from tippy import tips
    
    
    class TestTips(unittest.TestCase):
    
        def setUp(self):
            self.check = tips.Check(config_tests.test_amount)
            self.percent = config_tests.test_percent
    
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
        
Ok, we're pretty confident that we've got everything working the way we intended, so let's run our test and see the results.

    $ python test_tips.py
    .F....
    ======================================================================
    FAIL: test_check_to_rtip_floats (__main__.TestTips)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_tips.py", line 28, in test_check_to_rtip_floats
        self.assertIsInstance(val, float)
    AssertionError: 8 is not an instance of <class 'float'>
    
    ----------------------------------------------------------------------
    Ran 6 tests in 0.003s
    
    FAILED (failures=1)
    
Wait a second, what happened? If we examine the FAIL message, we'll see that our adjustments caused our float check to fail.
So, let's go back and examine our code and make changes to ensure that our return values are floats as intended.

### tippy/tippy/tips.py - 4th iteration #

While we're at it, let's go ahead and ensure that we round the tip amount properly to make sure the math makes sense.

    # tippy/tippy/tips.py
    class Check(object):
        def __init__(self, amount):
            '''Initialize a Check object, which holds the bill amount'''
            self.amount = amount
    
        def check_to_tip(self, tip_percent):
            '''Returns tuple with the tip amount and total bill after applying the tip'''
            tip = round(self.amount * tip_percent / 100, 2)
            total = self.amount + tip
            return tip, total
    
        def check_to_rtip(self, tip_percent):
            '''Returns tuple with the tip amount and total bill after adjusting the tip to
            ensure the total bill is a whole dollar amount'''
            tip, total = self.check_to_tip(tip_percent)
            f_total = int(total)
            if total == f_total:
                return tip, total
            n_total = float(f_total + 1)
            n_tip = tip + n_total - total
            return n_tip, n_total
            
Now, when we run our test, we see that our calculator is operating as expected.

### Conclusion #

TDD may seem time-consuming when working with small projects such as tippy; however, as your Python skill grows and your
projects become more ambitious and larger, having a solid testing framework will be invaluable.

