# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1"

import pickle
from typing import Union

from command_tools import errors


class CommandList:
    def __init__(self, list_: dict = None):
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
    def __init__(self, list_: list):
        self.list_ = list_

    def __getitem__(self, item):
        return self.list_.__getitem__(item)


class OperateLevel(float):
    pass


class OperateLevelList:
    def __init__(self):
        self.level_list = {}

    def append(self, name, level: float):
        try:
            self.level_list.__getitem__(name)
        except KeyError:
            self.level_list.__setitem__(name, level)
        else:
            raise errors.OperateLevelAlreadyExistError(level_name=name)

    def save(self, file):
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        return pickle.load(file)

    def __getitem__(self, item) -> OperateLevel:
        return self.level_list.__getitem__(item)


class UserList:
    def __init__(self, default_level: Union[float, OperateLevel] = 0):
        self.user_list = {}
        self.default_level = default_level

    def append(self, user_name, op_level: Union[float, OperateLevel]):
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
        self.user_list.__setitem__(user_name, op_level)

    def save(self, file):
        if type(file) == str:
            file = open(file, mode="wb")
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        if type(file) == str:
            file = open(file, mode="rb")
        return pickle.load(file)


if __name__ == '__main__':
    pass
