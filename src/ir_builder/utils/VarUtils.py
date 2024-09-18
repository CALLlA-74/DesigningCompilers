import typing

from ir_builder.exceptions.CompileException import CompileException
from llvmlite import ir as llvmir
from ir_builder.context import TypesEnum, EmbeddedTypesEnum, Constructs
#from ir_builder.context.EmbeddedTypes import AbstractType
#from ir_builder.context.Context import ModuleContext, ProcedureContext


def parse_real(number: str) -> float:
    try:
        return float(number)
    except Exception as e:
        raise CompileException(f'{str(e)}')


def parse_int(number: str) -> int:
    try:
        return int(number)
    except Exception as e:
        raise CompileException(f'{str(e)}')


"""def create__const_int_var(name:str, builder:llvmir.IRBuilder, val:int = 0, is_global:bool = False, is_const:bool = False):
    int64 = llvmir.IntType(64)
    if is_global or is_const:
        variable = llvmir.GlobalVariable(builder.module, int64, name=name)
        variable.linkage = "private"
        variable.global_constant = is_const
    else:
        variable = builder.alloca(int64, name=name)

    builder.store(llvmir.Constant(int64, val), variable)
    return variable


def create_const_real_var(name:str, builder:llvmir.IRBuilder, val:float = 0.0, is_global:bool = False, is_const:bool = False):
    float64 = llvmir.DoubleType()
    if is_global or is_const:
        variable = llvmir.GlobalVariable(builder.module, float64, name=name)
        variable.linkage = "private"
        variable.global_constant = is_const
    else:
        variable = builder.alloca(float64, name=name)

    builder.store(llvmir.Constant(float64, val), variable)
    return variable


def create_const_string_var(name:str, builder:llvmir.IRBuilder, val:str = '', is_global:bool = False, is_const:bool = False):
    val_bytes = bytearray(val, encoding="utf-8")
    string = llvmir.ArrayType(llvmir.types.IntType(8), len(val_bytes))
    if is_global or is_const:
        variable = llvmir.GlobalVariable(builder.module, string, name=name)
        variable.linkage = "private"
        variable.global_constant = is_const
    else:
        variable = builder.alloca(string, name=name)

    builder.store(llvmir.Constant(string, val_bytes), variable)
    return variable


def create_const_char_var(name:str, builder:llvmir.IRBuilder, val:str = None, is_global:bool = False, is_const:bool = False):
    if len(val) > 1:
        raise CompileException(f"Got string \'{val}\' but char expected")
    elif len(val) < 1:
        raise CompileException(f"Char variable isn\'t initialized")
    val_bytes = bytearray(val, encoding="utf-8")
    char = llvmir.ArrayType(llvmir.types.IntType(8), len(val_bytes))
    if is_global or is_const:
        variable = llvmir.GlobalVariable(builder.module, char, name=name)
        variable.linkage = "private"
        variable.global_constant = is_const
    else:
        variable = builder.alloca(char, name=name)

    builder.store(llvmir.Constant(char, val_bytes), variable)
    return variable


def create_const_var_(name:str, typ:TypesEnum, builder:llvmir.IRBuilder, val, is_global:bool = False,
                      is_const:bool = False):
    if typ == TypesEnum.INT_LITERAL:
        return create__const_int_var(name=name, builder=builder, val=val, is_global=is_global, is_const=is_const)
    elif typ == TypesEnum.REAL_LITERAL:
        return create_const_real_var(name=name, builder=builder, val=val, is_global=is_global, is_const=is_const)
    elif typ == TypesEnum.STRING_LITERAL:
        return create_const_string_var(name=name, builder=builder, val=val, is_global=is_global, is_const=is_const)
    elif typ == TypesEnum.CHAR_LITERAL:
        return create_const_char_var(name=name, builder=builder, val=val, is_global=is_global, is_const=is_const)"""


def create_var_(name:str, typ: Constructs.Type, context,        # typing.Union[ModuleContext, ProcedureContext]
                init_val=None, is_global:bool = False, is_const:bool = False):
    if init_val is None:
        init_val = typ.default_val  # get_init_val()
    if is_global or is_const:
        variable = llvmir.GlobalVariable(context.module, typ.instruct, name=name)
        variable.linkage = "private"
        variable.global_constant = is_const
        variable.initializer = init_val
    else:
        variable = context.get_ir_builder().alloca(typ.instruct, name=name)
        context.get_ir_builder().store(value=init_val, ptr=variable)

    return variable


def is_primitive(operand) -> bool:
    if isinstance(operand, Constructs.Variable) or \
            isinstance(operand, Constructs.Value) or \
            isinstance(operand, Constructs.Const):
        if operand.typ and operand.typ.typ_val.get_type() == EmbeddedTypesEnum.IDENTIFIER:
            return True

    return False


def not_(operand:typing.Union[Constructs.Variable, Constructs.Value, Constructs.Const],
         context):                                          # typing.Union[ModuleContext, ProcedureContext]
    if not is_primitive(operand):
        raise CompileException(f"Expected primitive type for operator NOT, but got {type(operand)}")
    if operand.typ.instruct != llvmir.IntType(1):   # если тип не boolean
        raise CompileException(f"Inoperable type {operand.typ.instruct} for operator NOT")

    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    return Constructs.Value(typ=operand.typ, val=None, instruct=ir_builder.not_(operand.instruct))
