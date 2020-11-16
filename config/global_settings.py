#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : global_settings.py
@Time  : 2020/10/30 17:30
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os

# =============================
# --- Global Constant Settings
# =============================
VERSION = "1.0"
POSIX = os.name == "posix"
WINDOWS = os.name == "nt"

# Mails info, split to ";"
MAIL_TO_SELF = "tao.xu2008@outlook.com"
MAIL_TO_DEV = "tao.xu2008@outlook.com"
MAIL_TO_QA = "tao.xu2008@outlook.com"
MAIL_COUNT = dict(
    m_from="txu2k8@gmail.com",
    m_to="",  # split to ";"
    host="smtp.gmail.com",
    user="txu2k8@gmail.com",
    password="b29ndHl5YnlvdWF4a2l3aQ==",
    port=465,
    tls=True
)

if __name__ == '__main__':
    pass
