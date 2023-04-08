# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1"

from functools import wraps, update_wrapper
from typing import Union

from command_tools import errors
from command_tools import types_

default_command_list = types_.CommandList()
_default_lead_char = types_.LeadChar(
    ['!', '！',
     '#',
     '$', '￥',
     '//', '/',
     '\\\\', '\\',
     ':', '：'
     ]
)  # 利用python浅拷贝特性完成节省内存,所以套了N层


def _default_cut_rule(string: any, *_, **__):
    if type(string) != str:
        return string
    return string.split()


class Command:
    def __init__(self, name: Union[str, float],
                 op_level: Union[float, types_.OperateLevel] = 0,
                 *,
                 args_maker: callable = _default_cut_rule,
                 cut_rule=_default_cut_rule,
                 lead_char: Union[types_.LeadChar, None] = None,
                 help_: str = "Not defined!",
                 list_: Union[types_.CommandList, None] = None):

        """

        用于注册指令

        :param name: 指令名
        :param op_level: 需求权限等级
        :param args_maker: 对参数修改的函数
        :param cut_rule: 裁剪规则
        :param lead_char: 领导符
        :param help_: 指令的帮助文档
        :param list_: 指令注册表
        """

        if lead_char is None:
            lead_char = _default_lead_char
        if list_ is None:
            list_ = default_command_list

        self._name = name
        self._op_level = op_level
        self._args_maker = args_maker
        self._cut_rule = cut_rule
        self._lead_char = lead_char
        self._help_ = help_
        self._list_ = list_
        self._append_to_list = False

        self._data = {"help": self._help_,
                      "lead_char": self._lead_char,
                      "op_level": self._op_level,
                      "cut_rule": self._cut_rule,
                      "args_maker": self._args_maker}

    def __call__(self, func):

        if not self._append_to_list:  # 如果该func未尝试加入过指令列表
            self._append_to_list = True  # 设置标记位为已尝试加入过列表

            update_wrapper(func, self)  # 更新类装饰器到函数

            try:
                self._list_[self._name]  # 如果有同名指令已在列表(程序将跳转至else代码块
            except KeyError:  # 如果该指令尚未注册(指令不存在
                self._list_[self._name] = {"func": func, **self._data}  # 注册指令
            else:  # 如果try的代码块能正常运行就会跳转到else(指令存在
                raise errors.CommandAlreadyExistError(command_name=self._name)  # 指令已存在,进行报错

        @wraps(func)
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated


def _default_args_unpacker(*args, func, **kwargs):
    return func(*args, **kwargs)


class RunCommand:
    def __init__(self,
                 args_maker: callable = _default_cut_rule,
                 cut_rule=_default_cut_rule,
                 list_: Union[types_.CommandList, None] = None,
                 lead_char: Union[types_.LeadChar, None] = None,
                 args_unpacker: callable = None):

        """

        用于运行指令

        :param args_maker: 指令参数生成器
        :param cut_rule: 裁剪规则
        :param list_: 指令注册表
        """

        if list_ is None:
            list_ = default_command_list
        if lead_char is None:
            lead_char = _default_lead_char
        if args_unpacker is None:
            args_unpacker = _default_args_unpacker

        self._cut_rule = cut_rule
        self._list_ = list_
        self._lead_char = lead_char
        self._args_maker = args_maker
        self._args_unpacker = args_unpacker

    @staticmethod
    def _clear_lead_char(string: str, lead_char: types_.LeadChar) -> str:
        """

        清除领导符

        :param string: 原指令
        :param lead_char: 领导符列表
        :return: 根指令
        """
        for char in lead_char:
            try:
                temp_str = string[:len(char)]  # 可能会抛出ValueError
                if temp_str != char:  # 不为正确的领导符就报错（避免else里面执行
                    raise ValueError
            except ValueError:
                pass
            else:
                return string[0 + len(char):]  # 返回根指令字符串
        raise errors.LeadCharNotFindError

    def _get_command_obj(self, string: str, cut_rule) -> Union[bool, dict]:
        """

        获取指令对象

        :param string: 指令名
        :param cut_rule: 剪裁规则
        :return: 指令对应的对象
        """
        try:
            first_word = cut_rule(string)[0]  # 获取根指令
        except IndexError:
            return False

        cmds = set(self._list_.keys())  # 用集合加速查找
        if first_word in cmds:  # 查找指令
            return self._list_[first_word]  # 返回找到dict的对象
        return False

    def run_by_str(self, string: str, op_level: Union[types_.OperateLevel, float], *args, **kwargs):
        """

        以字符串运行指令

        :param string: 原始指令字符串
        :param op_level: 权限等级
        :param args: 额外向指令的位置参数
        :param kwargs: 额外向指令的关键字参数
        :return object: 指令运行后返回的返回值
        """
        try:
            no_lead_char = self._clear_lead_char(string, self._lead_char)  # 获取无领导符字符串
            cmd_obj = self._get_command_obj(no_lead_char, self._cut_rule)  # 获取指令对象

            self._clear_lead_char(string, cmd_obj["lead_char"])  # 是否为正确格式的领导符（没找到会抛出 LeadCharNotFindError
            # 如果cmd_obj为False则会因为没有__getitem__而抛出TypeError

            temp_obj = self._get_command_obj(no_lead_char, cmd_obj["cut_rule"])
            if cmd_obj != temp_obj:
                raise TypeError

        except TypeError:  # 如果没找到指令 就 进行报错
            raise errors.CommandNotFindError(
                command_name=string
            )
        except errors.LeadCharNotFindError:
            raise errors.CommandNotFindError(
                command_name=string
            )

        if op_level < cmd_obj["op_level"]:  # 执行权限检查
            raise errors.DontHavePermissionError(level_need=cmd_obj["op_level"], level_now=op_level)  # 如果没权限 就 进行报错

        global_maker_ret = self._args_maker(string=string, cmd_obj=cmd_obj, *args, **kwargs)  # 拿到全局

        maker = cmd_obj["args_maker"]  # 拿到局部
        maker_ret = maker(string=global_maker_ret, cmd_obj=cmd_obj, *args, **kwargs)

        ret = self._args_unpacker(maker_ret, func=cmd_obj["func"])  # 解包并运行

        return ret  # 返回执行结果

    def __call__(self, string: str, op_level: Union[types_.OperateLevel, float], *args, **kwargs):

        """

        运行run_by_str的快捷方式

        以字符串运行指令

        :param string: 原始指令字符串
        :param op_level: 权限等级
        :param args: 额外向指令的位置参数
        :param kwargs: 额外向指令的关键字参数
        :return object: 指令运行后返回的返回值

        """

        return self.run_by_str(string=string, op_level=op_level, *args, **kwargs)


if __name__ == '__main__':
    pass
