# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "R 1.0.0.1"

# 版本名称规则
# R 正式版
# B | A 测试版
# T 临时版

"""

A simple func reg tool

"""


import sys

_RUN_VERSION = 3.10
if float(sys.winver) < _RUN_VERSION:
    raise ImportError("Python version Error (at lease {0} now {1})".format(_RUN_VERSION, sys.winver))

print(f"Command tools {__version__}")

__all__ = ['command', 'errors', 'types_']


if __name__ == '__main__':
    pass
