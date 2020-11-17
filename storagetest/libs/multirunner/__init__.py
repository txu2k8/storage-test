#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/10 16:03
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""
from .multi_runner import *
__all__ = ['MultiRunner']

"""
def train_a_model(batch_size,hidden_layer_number,learning_rate):
    #your code here
    return accuracy

from MultiRunner import MultiRunner

a=MultiRunner()
a.generate_ini([[16,64,256], [1,2], [0.001,0.01,0.1]])#注意这里，所有的参数列表要最后用一个list或者tuple括起来
a.run(train_a_model)
"""

if __name__ == '__main__':
    pass
