import os
import sys
import unittest

paths = ["etl", "editor"]

def run_tests():
    for path in paths:
        sys.path.insert(0, os.path.abspath(path))

    loader = unittest.TestLoader()
    tests = loader.discover("tests", pattern='*_test.py')

    testRunner = unittest.TextTestRunner()
    testRunner.run(tests)

if __name__ == '__main__':
    run_tests()
