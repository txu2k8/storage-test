#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : setup.py.py
@Time  : 2020/11/10 8:54
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
from setuptools import setup


# 读取文件内容
def read_file(filename):
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cur_dir, filename), encoding='utf-8') as f:
        long_desc = f.read()
    return long_desc


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='storage-test',
    python_requires='>=3.4.0',
    version='1.0.1',
    description="Storage Test tools/scripts.",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author="tao.xu",
    author_email='tao.xu2008@outlook.com',
    url='https://github.com/txu2k8/storage-test',
    packages=[
        'config',
        'libs',
        'pkgs',
        'storage',
    ],
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    license="MIT",
    keywords=['storage', 'filesystem', 'raw', 'cloud'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9.0',
    ],
)
