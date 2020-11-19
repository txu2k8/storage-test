#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : raw_ut_test.py
@Time  : 2020/11/19 9:41
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import json
import unittest
from parameterized import parameterized, param

from storagetest.libs import log
from storagetest.libs.customtestcase import CustomTestCase
from storagetest.pkgs.raw.ut import RawUT

logger = log.get_logger()


def custom_name_func():
    def custom_naming_func(testcase_func, param_num, param):
        return '{0}_{1}_{2}'.format(testcase_func.__name__, param_num, parameterized.to_safe_name(param.args[0]))
        # return testcase_func.__name__ + '_' + parameterized.to_safe_name(param.args[0])

    return custom_naming_func


class RawUnitTestCase(CustomTestCase):
    """raw unittest"""
    _device = "/dev/sdx"
    _case_id_list = []
    _case_priority_list = []

    @classmethod
    def setUpClass(cls):
        logger.info("Start sanity test on raw device {}".format(cls._device))

    @classmethod
    def tearDownClass(cls):
        logger.info("Sanity test on raw device {} complete!".format(cls._device))

    def test_sanity(self):
        raw = RawUT("/dev/sdb")
        logger.info(raw.__doc__)
        self.assertTrue(raw.sanity())

    raw_parameterized = []
    raw_ut = RawUT(_device)
    tc_list = raw_ut.load_tcs()
    for test in tc_list:
        if _case_id_list and test['case_id'] not in _case_id_list:
            continue
        if _case_priority_list and test['case_priority'] not in _case_priority_list:
            continue
        p = param(test['case_name'], test)  # str(test['case_id']) + '_' +
        raw_parameterized.append(p)

    @parameterized.expand(raw_parameterized, name_func=custom_name_func())
    def test_raw(self, _, case_info):
        # logger.info('=' * 50)
        logger.info(self._device)
        logger.info('CaseID: {0}'.format(case_info['case_id']))
        logger.info('CaseName: {0}'.format(case_info['case_name']))
        logger.info('StepLoop: {0}'.format(case_info['case_loop']))
        for step_id in case_info['steps'].keys():
            describe = case_info['steps'][step_id]['describe']
            expectation = case_info['steps'][step_id]['expectation']
            if expectation:
                logger.info('CaseStep: {0}. {1} --Expectation:{2}'.format(step_id, describe, expectation))
            else:
                logger.info('CaseStep: {0}. {1}'.format(step_id, describe))

        logger.info(json.dumps(case_info, indent=4))
        # logger.info('=' * 50)

        self.raw_ut.run(case_info)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(RawUnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
