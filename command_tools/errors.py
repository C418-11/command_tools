# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1"

from typing import Union

from command_tools import types_


class UserAlreadyExistError(Exception):
    def __init__(self, *, user_name=None):
        self.user_name = user_name

    def __str__(self):
        return f"User {self.user_name} already exists!"


class OperateLevelException(Exception):
    pass


class DontHavePermissionError(OperateLevelException):  # 权限等级错误
    def __init__(self, *, level_need: Union[float, types_.OperateLevel] = None, level_now: Union[float, types_.OperateLevel] = None):
        self.op_levels = level_need, level_now

    def __str__(self):
        return "You don't have permissions do it! (need {0}, now {1})".format(*self.op_levels)


class OperateLevelAlreadyExistError(OperateLevelException):
    def __init__(self, *, level_name=None):
        self.level_name = level_name

    def __str__(self):
        return f"Operate level {self.level_name} already exists!"


class CommandException(Exception):
    pass


class CommandAlreadyExistError(CommandException):  # 指令已存在错误
    def __init__(self, *, command_name: str = None):
        self.command_name = command_name

    def __str__(self):
        return f"Command {self.command_name} already exists!"


class CommandNotFindError(CommandException):
    def __init__(self, *, command_name: str = None):
        self.command_name = command_name

    def __str__(self):
        return f"Command Not Find! (Command: {self.command_name})"


class LeadCharNotFindError(CommandException):
    pass


if __name__ == '__main__':
    pass
