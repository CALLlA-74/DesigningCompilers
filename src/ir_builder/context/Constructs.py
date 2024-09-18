from llvmlite import ir as llvmir
from typing import Union, Optional, List
import typing

from ir_builder.context import TypesEnum
#from ir_builder.context.EmbededTypes import AbstractType


class Label:
    def __init__(self, ident:str, instruct=None):
        self.ident = ident
        self.typ = llvmir.LabelType()
        self.instruct = instruct


class Type:
    def __init__(self, ident:str, typ_val,  # :typing.Type[AbstractType]
                 instruct:typing.Type[llvmir.Instruction],
                 default_val:llvmir.Constant):     # = None
        self.ident = ident
        self.typ_val = typ_val
        self.instruct = instruct
        self.default_val = default_val

    """def get_init_val(self):
        return self.typ_val.get_init_val()"""


class Const:
    def __init__(self, ident:str, typ:Union[Type, TypesEnum], val, sign:str = '',
                 instruct:Union[llvmir.AllocaInstr, llvmir.GlobalVariable] = None):
        self.ident = ident
        self.typ = typ
        self.val = val
        self.sign = sign
        self.instruct = instruct


class Variable:
    def __init__(self, ident:str, typ:Union[Type],       # typing.Type[AbstractType]
                 instruct:Union[llvmir.Instruction] = None, init_val = None):
        self.ident = ident
        self.typ = typ
        self.instruct = instruct
        self.init_val = init_val


class ProcedureOrFunction:
    def __init__(self, ident:str, func_typ, arg_list:List[Variable] = None, func_instruct:llvmir.Function = None,
                 res_type=None, local_ctx=None, is_std=True):     # Context.ProcedureContext
        self.ident = ident
        self.arg_list = arg_list
        self.func_typ = func_typ
        self.func_instruct = func_instruct
        self.res_type = res_type
        self.local_ctx = local_ctx
        self.is_std = is_std

    def is_defined(self):
        return self.func_instruct is not None


class Value:
    def __init__(self, typ:Union[Type, TypesEnum], val, sign:str = None,
                 instruct:Union[llvmir.AllocaInstr, llvmir.GlobalVariable] = None):
        self.typ = typ
        self.val = val
        self.sign = sign
        self.instruct = instruct

    def get_val(self, context, search_scopes):              # :Union[Context.ModuleContext, Context.ProcedureContext]
        if self.typ == TypesEnum.IDENTIFIER or self.typ == TypesEnum.SIGNED_IDENTIFIER:
            return context.get_var_by_ident(ident=self.val, search_scopes=search_scopes).val
        return self.val
