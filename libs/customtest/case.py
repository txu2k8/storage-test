#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : case.py
@Time  : 2020/11/6 14:27
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import unittest
from prettytable import PrettyTable

from libs.log import log

logger = log.get_logger()


class CustomTestCase(unittest.TestCase):
    """A custom class inherit from unittest.TestCase"""
    phase_list = []

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", self.shortDescription()])
        self.print_phase()

    def tearDown(self):
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
        self.print_phase()

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def print_phase(self):
        if len(self.phase_list) == 0:
            return True
        step_table = PrettyTable(['No.', 'TestCase', 'Result', 'Comments'])
        step_table.align['Step'] = 'l'
        step_table.align['Comments'] = 'l'
        for idx, step in enumerate(self.phase_list):
            step_status = [idx + 1] + step
            step_table.add_row(step_status)
        logger.info("\n{0}".format(step_table))
        return True


if __name__ == '__main__':
    pass
