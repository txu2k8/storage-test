#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sys_info.py
@Time  : 2020/11/12 15:07
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
TODO
"""

import platform
import psutil
import kmgt

"""Get/Print System Information"""


def cpu_info():
    cpu_times = psutil.cpu_times()

    def cpu_memory_info(memory):
        """Get cpu's memory info"""
        print(memory)
        return {
            'total': kmgt(memory.total),
            'used': kmgt(memory.used),
            'free': kmgt(memory.free),
            'percent': str(memory.percent) + '%',
            'available': kmgt(memory.available) if hasattr(memory, 'available') else '',
            'active': kmgt(memory.active) if hasattr(memory, 'active') else '',
            'inactive': kmgt(memory.inactive) if hasattr(memory, 'inactive') else '',
            'wired': kmgt(memory.wired) if hasattr(memory, 'wired') else ''
        }
    return {
        'cpu_times': psutil.cpu_times(),
        'cpu_physical_count': psutil.cpu_count(logical=False),
        'cpu_logical_count': psutil.cpu_count(),
        'cpu_percent': psutil.cpu_percent(percpu=True),
        'virtual_memory': cpu_memory_info(psutil.virtual_memory()),
        'swap_memory': cpu_memory_info(psutil.swap_memory()),
        'up_time': {
            pro: getattr(cpu_times, pro) for pro in dir(cpu_times) if pro[0:1] != '_' and pro not in ('index', 'count')
        },
    }


def sys_info():
    return {
        'system': platform.system(),
        'platform': platform.platform(),
        'version': platform.version(),
        'architecture': platform.architecture(),
        'machine': platform.machine(),
        'node': platform.node(),
        'processor': platform.processor()
    }


if __name__ == '__main__':
    pass
