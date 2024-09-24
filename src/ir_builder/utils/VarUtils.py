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
        variable = llvmir.GlobalVariable(context.get_module(), typ.instruct, name=name)
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


def not_(operand:typing.Union[Constructs.Value], context):           # typing.Union[ModuleContext, ProcedureContext]
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    return Constructs.Value(typ=None, val=None, instruct=ir_builder.not_(operand.instruct))


def inverse(operand:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    if operand.instruct.type == llvmir.IntType(64):
        res = ir_builder.mul(operand.instruct, llvmir.Constant(operand.instruct.type, -1))
    elif operand.instruct.type == llvmir.DoubleType():
        res = ir_builder.fmul(operand.instruct, llvmir.Constant(operand.instruct.type, -1))
    else:
        raise CompileException(f"Operator \'*\' is unsupportable for variable of type: {operand.instruct.type}")
    return Constructs.Value(typ=None, val=None, instruct=res)


def mulOperCalc(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], operator:str, context):
    if operator == '*':
        return mul(op1, op2, context)
    elif operator == '/':
        return slash(op1, op2, context)
    elif operator == 'div':
        return div(op1, op2, context)
    elif operator == 'mod':
        return mod(op1, op2, context)
    elif operator == 'and':
        return and_(op1, op2, context)


def mul(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        raise CompileException(f"Operator \'*\' is unsupportable for variable of type: {op1.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != op2.instruct.type:
        if op1.instruct.type == llvmir.DoubleType():
            instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())
        else:
            instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())

    if instr_1.type == llvmir.IntType(64):
        res = ir_builder.mul(instr_1, instr_2)
    else:
        res = ir_builder.fmul(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def slash(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        if op1.instruct.type not in targets:
            raise CompileException(f"Operator \'/\' is unsupportable for variable of type: {op1.instruct.type}")
        else:
            raise CompileException(f"Operator \'/\' is unsupportable for variable of type: {op2.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != llvmir.DoubleType():
        instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())
    if op2.instruct.type != llvmir.DoubleType():
        instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())

    res = ir_builder.fdiv(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def div(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.IntType(64)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        if op1.instruct.type not in targets:
            raise CompileException(f"Operator \'div\' is unsupportable for variable of type: {op1.instruct.type}")
        else:
            raise CompileException(f"Operator \'div\' is unsupportable for variable of type: {op2.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    res = ir_builder.sdiv(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def mod(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.IntType(64)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        if op1.instruct.type not in targets:
            raise CompileException(f"Operator \'mod\' is unsupportable for variable of type: {op1.instruct.type}")
        else:
            raise CompileException(f"Operator \'mod\' is unsupportable for variable of type: {op2.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    res = ir_builder.srem(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def and_(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.IntType(64), llvmir.IntType(1)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        if op1.instruct.type not in targets:
            raise CompileException(f"Operator \'and\' is unsupportable for variable of type: {op1.instruct.type}")
        else:
            raise CompileException(f"Operator \'and\' is unsupportable for variable of type: {op2.instruct.type}")
    if op1.instruct.type != op2.instruct.type:
        raise CompileException(f"Operator \'and\' is unsupportable for variables of not similar types: "
                               f"\'{op1.instruct.type}\' and \'{op2.instruct.type}\'")

    instr_1, instr_2 = op1.instruct, op2.instruct
    res = ir_builder.and_(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def addOperCalc(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], operator:str, context):
    if operator == '+':
        return plus(op1, op2, context)
    elif operator == '-':
        return mines(op1, op2, context)
    elif operator == 'or':
        return or_(op1, op2, context)


def plus(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        raise CompileException(f"Operator \'+\' is unsupportable for variable of type: {op1.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != op2.instruct.type:
        if op1.instruct.type == llvmir.DoubleType():
            instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())
        else:
            instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())

    if instr_1.type == llvmir.IntType(64):
        res = ir_builder.add(instr_1, instr_2)
    else:
        res = ir_builder.fadd(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def mines(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        raise CompileException(f"Operator \'-\' is unsupportable for variable of type: {op1.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != op2.instruct.type:
        if op1.instruct.type == llvmir.DoubleType():
            instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())
        else:
            instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())

    if instr_1.type == llvmir.IntType(64):
        res = ir_builder.sub(instr_1, instr_2)
    else:
        res = ir_builder.fsub(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def or_(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.IntType(64), llvmir.IntType(1)]
    if op1.instruct.type not in targets or op2.instruct.type not in targets:
        if op1.instruct.type not in targets:
            raise CompileException(f"Operator \'or\' is unsupportable for variable of type: {op1.instruct.type}")
        else:
            raise CompileException(f"Operator \'or\' is unsupportable for variable of type: {op2.instruct.type}")
    if op1.instruct.type != op2.instruct.type:
        raise CompileException(f"Operator \'or\' is unsupportable for variables of not similar types: "
                               f"\'{op1.instruct.type}\' and \'{op2.instruct.type}\'")

    instr_1, instr_2 = op1.instruct, op2.instruct
    res = ir_builder.or_(instr_1, instr_2)
    return Constructs.Value(typ=None, val=None, instruct=res)


def relOperCalc(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], operator:str, context):
    if operator == '=':
        return equal(op1, op2, context)
    elif operator == '<>':
        return not_equal(op1, op2, context)
    else:
        return lt_le_gt_ge(op1, op2, operator, context)


def equal(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]

    if isinstance(op1.instruct, llvmir.Constant):
        op1, op2 = op2, op1

    if (op1.instruct.type not in targets and not isinstance(op1.instruct.type, llvmir.PointerType)) \
            or (op2.instruct.type not in targets and not isinstance(op2.instruct.type, llvmir.PointerType)):
        raise CompileException(f"Operator \'=\' is unsupportable for variables of types: {op1.instruct.type} and {op2.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != op2.instruct.type:
        if op1.instruct.type == llvmir.DoubleType():
            instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())
        elif op2.instruct.type == llvmir.DoubleType():
            instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())

    if instr_1.type == llvmir.DoubleType():                             # llvmir.IntType(64)
        res = ir_builder.fcmp_ordered('==', instr_1, instr_2)
    else:
        res = ir_builder.icmp_signed('==', instr_1, instr_2)

    return Constructs.Value(typ=None, val=None, instruct=res)


def not_equal(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]

    if isinstance(op1.instruct, llvmir.Constant):
        op1, op2 = op2, op1

    if (op1.instruct.type not in targets and not isinstance(op1.instruct.type, llvmir.PointerType)) \
            or (op2.instruct.type not in targets and not isinstance(op2.instruct.type, llvmir.PointerType)):
        raise CompileException(f"Operator \'<>\' is unsupportable for variables of types: {op1.instruct.type} and {op2.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != op2.instruct.type:
        if op1.instruct.type == llvmir.DoubleType():
            instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())
        elif op2.instruct.type == llvmir.DoubleType():
            instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())

    if instr_1.type == llvmir.DoubleType():                             # llvmir.IntType(64)
        res = ir_builder.fcmp_ordered('!=', instr_1, instr_2)
    else:
        res = ir_builder.icmp_signed('!=', instr_1, instr_2)

    return Constructs.Value(typ=None, val=None, instruct=res)


def lt_le_gt_ge(op1:typing.Union[Constructs.Value], op2:typing.Union[Constructs.Value], operator:str, context):
    ir_builder:llvmir.IRBuilder = context.get_ir_builder()
    targets = [llvmir.DoubleType(), llvmir.IntType(64)]

    if (op1.instruct.type not in targets) \
            or (op2.instruct.type not in targets):
        raise CompileException(f"Operator \'{operator}\' is unsupportable for variables of types: {op1.instruct.type} "
                               f"and {op2.instruct.type}")

    instr_1, instr_2 = op1.instruct, op2.instruct
    if op1.instruct.type != op2.instruct.type:
        if op1.instruct.type == llvmir.DoubleType():
            instr_2 = ir_builder.sitofp(instr_2, llvmir.DoubleType())
        elif op2.instruct.type == llvmir.DoubleType():
            instr_1 = ir_builder.sitofp(instr_1, llvmir.DoubleType())

    if instr_1.type == llvmir.DoubleType():                             # llvmir.IntType(64)
        res = ir_builder.fcmp_ordered(operator, instr_1, instr_2)
    else:
        res = ir_builder.icmp_signed(operator, instr_1, instr_2)

    return Constructs.Value(typ=None, val=None, instruct=res)
