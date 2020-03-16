#!/usr/bin/env

'''
runs test for local workbench
'''

import unittest
import subprocess
import os
import logging


def main():
    """
    run workbench unit tests
    """

    # set loggin level
    logging.basicConfig(level=logging.INFO)
    if True:
        loader = unittest.TestLoader()
        start_dir = os.getcwd() + '/test'
        all_test = loader.discover(start_dir, pattern='test*.py')
        result = unittest.TestResult()
        for suite in all_test:
            for test in suite:
                test.run(result)

        print(result)
        if len(result.failures):
            print('----failures----')
            for f in result.failures:
                print(f)
        if len(result.errors):
            print('----errors----')
            for e in result.errors:
                print(e, '\n')


if __name__ == "__main__":
    main()