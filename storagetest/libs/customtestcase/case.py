#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : case.py
@Time  : 2020/11/6 14:27
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""
import time
from datetime import datetime
import unittest
from prettytable import PrettyTable
from collections import defaultdict

from storagetest.libs.log import log

logger = log.get_logger()


class CustomTestCase(unittest.TestCase):
    """A custom class inherit from unittest.TestCase"""
    tc_loop = defaultdict(int)

    def __init__(self, methodName='runTest', *args, **kwargs):
        super(CustomTestCase, self).__init__(methodName)
        self.args = args
        self.kwargs = kwargs
        self.phase_list = []
        self.str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))

    @staticmethod
    def parametrize(testcase_class, *args, **kwargs):
        """Return a suite of all test cases contained in testCaseClass"""
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        if not testnames and hasattr(testcase_class, 'runTest'):
            testnames = ['runTest']
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name, *args, **kwargs))
        return suite

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()

    def tearDown(self):
        end_time = datetime.now()
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure
        status = "PASS" if ok else "FAIL"
        self.phase_list[-1][1] = status
        self.phase_list[-1][2] = str(end_time - self.start_time).split('.')[0]
        self.print_phase()
        self.tc_loop[self.id()] += 1

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def print_phase(self):
        if len(self.phase_list) == 0:
            return True
        step_table = PrettyTable(['No.', 'TestCase', 'Result', 'Elapsed', 'Comments'])
        step_table.align['TestCase'] = 'l'
        step_table.align['Comments'] = 'l'
        for idx, step in enumerate(self.phase_list):
            step_status = [idx + 1] + step
            step_table.add_row(step_status)
        logger.info("\n{0}".format(step_table))
        return True

    def get_case_name_desc(self):
        """Return the dict: {"name": "desc"}"""

        def should_include_method(attrname):
            if not attrname.startswith("test"):
                return False
            test_func = getattr(self, attrname)
            if not callable(test_func):
                return False
            full_name = f'%s.%s' % (
                self.__module__, attrname
            )
            from fnmatch import fnmatchcase
            test_name_patterns = None
            return test_name_patterns is None or \
                   any(fnmatchcase(full_name, pattern) for pattern in test_name_patterns)

        name_desc = defaultdict(dict)
        test_fn_names = list(filter(should_include_method, dir(self)))
        for test_fn_name in test_fn_names:
            test_method = getattr(self, test_fn_name)
            doc = test_method.__doc__
            desc = doc.strip().split("\n")[0].strip() if doc else None
            name_desc[test_fn_name.split("test_")[-1]] = desc

        return name_desc


if __name__ == '__main__':
    ctc = CustomTestCase()
    ctc.get_case_name_desc()

