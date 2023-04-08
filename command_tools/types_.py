# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"


"""
You must import command_tools.errors first !!!

else

you might get a error like this

AttributeError: partially initialized module 'command_tools.types_' has no attribute 'OperateLevel' (most likely due to a circular import)
"""


import pickle
from typing import Union

from command_tools import errors


class CommandList:
    """
    指令列表
    """
    def __init__(self, list_: dict = None):
        """
        :param list_: 已存在的指令列表
        """
        if list_ is None:
            list_ = {}

        self.list_ = list_

    def keys(self):
        return self.list_.keys()

    def values(self):
        return self.list_.values()

    def __getitem__(self, item):
        return self.list_.__getitem__(item)

    def __setitem__(self, key, value):
        self.list_.__setitem__(key, value)


class LeadChar:
    """
    领导符列表
    """
    def __init__(self, list_: list):
        self.list_ = list_

    def __getitem__(self, item):
        return self.list_.__getitem__(item)


class OperateLevel(float):
    """
    权限等级
    """
    pass


class OperateLevelList:
    """
    权限等级注册表
    """
    def __init__(self):
        self.level_list = {}

    def append(self, name, level: float):
        """
        :param name: 权限等级名
        :param level: 等级对应数值
        """
        try:
            self.level_list.__getitem__(name)
        except KeyError:
            self.level_list.__setitem__(name, level)
        else:
            raise errors.OperateLevelAlreadyExistError(level_name=name)

    def save(self, file):
        """
        :param file: 文件路径
        """
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        """
        :param file: 文件路径
        """
        return pickle.load(file)

    def __getitem__(self, item) -> OperateLevel:
        return self.level_list.__getitem__(item)


class UserList:
    """
    用户列表
    """
    def __init__(self, default_level: Union[float, OperateLevel] = 0):
        """
        :param default_level: 默认权限等级
        """
        self.user_list = {}
        self.default_level = default_level

    def append(self, user_name, op_level: Union[float, OperateLevel]):
        """
        :param user_name: 用户名
        :param op_level: 权限等级
        """
        try:
            self.user_list.__getitem__(user_name)
        except KeyError:
            self.user_list.__setitem__(user_name, op_level)
        else:
            raise errors.UserAlreadyExistError(user_name=user_name)

    def __getitem__(self, item) -> OperateLevel:
        try:
            return self.user_list.__getitem__(item)
        except KeyError:
            return self.default_level

    def __setitem__(self, key, value):
        self.user_list.__setitem__(key, value)

    def reset_level(self, user_name, op_level):
        """
        :param user_name: 用户名
        :param op_level: 权限等级
        """
        self.user_list.__setitem__(user_name, op_level)

    def save(self, file):
        """
        :param file: 文件路径
        """
        if type(file) == str:
            file = open(file, mode="wb")
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        """
        :param file: 文件路径
        """
        if type(file) == str:
            file = open(file, mode="rb")
        return pickle.load(file)


if __name__ == '__main__':
    pass
