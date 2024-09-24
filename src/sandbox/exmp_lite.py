"""s = "fjghjfhfhf ffhfghf hfghjf fghfghg5 456///,\\538824\\3534gd34jg93j53jn345"
sb = bytearray(s, encoding='utf-8')
print(len(s))
print(len(sb))"""

from enum import Enum, unique


@unique
class Types(str, Enum):
    STRING = "string"
    STRING_LITERAL = "string_literal"


import llvmlite.binding as llvm
import llvmlite.ir as llvmir
from ctypes import CFUNCTYPE, c_int32


def init_execution_engine():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()

    default_mod = llvm.parse_assembly("")
    return llvm.create_mcjit_compiler(default_mod, target_machine)


def compile_ir(engine, llvm_ir):
    mod = llvm.parse_assembly(str(llvm_ir))
    mod.verify()

    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()

    func_ptr = engine.get_function_address("main")
    func = CFUNCTYPE(c_int32)(func_ptr)
    print(func())


def create_global_string(builder: llvmir.IRBuilder, s: str, name: str) -> llvmir.Instruction:
    var_bytes = bytearray(s, encoding="utf-8")
    type_i16_x_len = llvmir.types.ArrayType(llvmir.types.IntType(8), len(var_bytes))
    constant = llvmir.Constant(type_i16_x_len, var_bytes)
    variable = llvmir.GlobalVariable(builder.module, type_i16_x_len, name)
    # variable.linkage = 'private'   # по умолчанию пишем всем private. external будет у interface-полей
    # variable.global_constant = True
    variable.initializer = constant
    variable.align = 1

    zero = llvmir.Constant(llvmir.types.IntType(32), 0)
    variable_pointer = builder.gep(variable, [zero, zero], inbounds=False)
    return variable_pointer


module_ir = llvmir.Module("mod")
builder = llvmir.IRBuilder()

int32 = llvmir.types.IntType(32)
int8p = llvmir.PointerType(llvmir.types.IntType(8))

type_func_scanf = llvmir.types.FunctionType(int32, [int8p], var_arg=True)
type_func_printf = llvmir.types.FunctionType(int32, [int8p], var_arg=True)
type_func_realloc = llvmir.types.FunctionType(int8p, [int8p, int32])
func_scanf = module_ir.declare_intrinsic('scanf', (), type_func_scanf)
func_printf = module_ir.declare_intrinsic('printf', (), type_func_printf)
func_realloc = module_ir.declare_intrinsic('realloc', (), type_func_realloc)

type_func_main = llvmir.types.FunctionType(return_type=int32, args=[])
func_main = llvmir.Function(module_ir, type_func_main, 'main')
zero = llvmir.Constant(int32, 0)
block_main = func_main.append_basic_block('entry')
builder.position_at_end(block_main)

func_ptr_type = llvmir.PointerType(llvmir.FunctionType(int32, [int8p], var_arg=True))
func_ptr = llvmir.GlobalVariable(builder.module, func_ptr_type, name='func_ptr')

"""s = 'asdfsgff'
var_bytes = bytearray(s, encoding='utf-8')
string = llvmir.ArrayType(llvmir.types.IntType(8), 256)    #
var = llvmir.GlobalVariable(builder.module, string, name="b")
#var = builder.alloca(string, name='b')
var.linkage = "private"
var.global_constant = False
#var.initializer = llvmir.Constant(string, var_bytes)
#builder.store(llvmir.Constant(string, var_bytes), var)"""

# создаем указатель на динамическую строку
typ = llvmir.PointerType(llvmir.IntType(8))
var = llvmir.GlobalVariable(builder.module, typ, name="var")
var.initializer = llvmir.Constant(typ, None)
var.linkage = "private"
#res = builder.call(func_realloc, [builder.load(var), llvmir.Constant(int32, 256)])
#builder.store(res, var)

# сохраняем литеральную строку в динамическую
str_val = llvmir.GlobalVariable(builder.module, llvmir.ArrayType(llvmir.IntType(8), 3), name='str_val')
str_val.initializer = llvmir.Constant(llvmir.ArrayType(llvmir.IntType(8), 3), bytearray("abc", "utf-8"))
tmp = str_val.gep([zero, zero])
builder.store(tmp, var)

# сохраняем другую литеральную строку в динамическую
str_val_2 = llvmir.GlobalVariable(builder.module, llvmir.ArrayType(llvmir.IntType(8), 7), name='str_val_2')
str_val_2.initializer = llvmir.Constant(llvmir.ArrayType(llvmir.IntType(8), 7), bytearray("dededed", "utf-8"))
str_val_2.global_constant = False
builder.store(str_val_2.gep([zero, llvmir.Constant(int32, 0)]), var)
str_val_2.global_constant = True
str_val_2.initializer = llvmir.Constant(llvmir.ArrayType(llvmir.IntType(8), 7), bytearray("aaaaaaa", "utf-8"))
str_val_2.gep([])

"""# создаем дефолтную строку и записываем пустое строковое значение НЕ РАБОТАЕТ
typ_default_str = llvmir.ArrayType(llvmir.IntType(8), 256)
var = llvmir.GlobalVariable(builder.module, typ_default_str, name="var")
#var.initializer = llvmir.Constant(typ_default_str, bytearray("", "utf-8"))
var.linkage = "private"
builder.store(llvmir.Constant(typ_default_str, bytearray("adfsgjg", "utf-8")), ptr=var)"""

arr_type = llvmir.ArrayType(llvmir.ArrayType(llvmir.DoubleType(), 4), 2)
arr = builder.alloca(arr_type, name='arr')
val = [[0.0, 1.0, 2.0, 4E-5]]*2
builder.store(llvmir.Constant(arr_type, val), ptr=arr)


float_val = llvmir.GlobalVariable(module_ir, llvmir.DoubleType(), name="float_val")
float_val.initializer = llvmir.Constant(llvmir.DoubleType(), -5.5)

#builder.call(func_printf, [create_global_string(builder, ' ' * 100000 + '\n\0', 'a')])
#builder.call(func_printf, [create_global_string(builder, 'Русский тестим\n\0', 'p2')])
"""args = [create_global_string(builder, '%f\0', 'ddt100'), builder.gep(float_val, [zero])]
builder.call(func_scanf, args)       # builder.gep(var, [zero, zero], inbounds=True)"""


# создаю локальную переменную idx
idx = builder.alloca(llvmir.IntType(64), name='idx')
builder.store(llvmir.Constant(llvmir.IntType(64), 1), builder.gep(idx, [zero]))      # закидываю в нее 1

ptr_idx = builder.alloca(llvmir.PointerType(llvmir.IntType(64)), name="ptr_idx")
builder.store(builder.gep(idx, [zero]), ptr_idx)

builder.call(func_printf, [create_global_string(builder, '%s\n%d\n%f; %f\n\0', 'ddt'),
                           #llvmir.Constant(llvmir.IntType(1), None),
                           builder.load(var),
                           builder.load(builder.gep(idx, [zero])),
                           builder.load(ptr=builder.gep(ptr=arr, indices=[zero, zero, builder.load(builder.gep(idx, [zero]))], inbounds=True)),
                           builder.load(ptr=builder.gep(ptr=arr, indices=[zero, llvmir.Constant(llvmir.IntType(32), 1), llvmir.Constant(llvmir.IntType(32), 3)]))])
"""builder.call(func_printf, [create_global_string(builder, '%s\n\0', 'ddt3'),
                           builder.load(var)])  # builder.gep(var, [zero], inbounds=True)"""
# когда выводим переменную как строку (через %s) то строку (если она НЕ указатель) подаем просто инструкцию-alloca

# при выводе как символ (через %c) символ-строку (если НЕ указатель) подаем через load-инструкцию




# пример описания структуры с полем типа указателя на саму себя
struct2 = module_ir.context.get_identified_type("node")
struct3 = module_ir.context.get_identified_type("struct3")
struct2.set_body(*[struct3, llvmir.IntType(8), llvmir.DoubleType()])
struct3.set_body(*[llvmir.DoubleType(), llvmir.IntType(64)])

lst = builder.alloca(struct2, name="lst")



builder.store(llvmir.Constant(struct2, [None, 0, llvmir.Constant(llvmir.DoubleType(), 10.0)]), ptr=lst)
builder.store(llvmir.Constant(llvmir.DoubleType(), -100), ptr=builder.gep(ptr=lst, indices=[zero, llvmir.Constant(llvmir.IntType(32), 2)]))
builder.store(llvmir.Constant(llvmir.DoubleType(), -1), ptr=builder.gep(ptr=lst, indices=[zero, llvmir.Constant(llvmir.IntType(32), 2)]))
builder.store(llvmir.Constant(llvmir.IntType(64), -21), ptr=builder.gep(ptr=lst, indices=[zero, zero, llvmir.Constant(llvmir.IntType(32), 1)]))



# пытаюсь вывести значение по индексу из структуры
builder.call(func_printf, [create_global_string(builder, '%f; %f\n\0', 'ddt2'),
                           builder.load(builder.gep(ptr=lst, indices=[zero, llvmir.Constant(llvmir.IntType(32), 2)])),
                           builder.load(builder.gep(ptr=lst, indices=[zero]))])


builder.alloca(llvmir.IntType(64), name='aadfgfhf')
#builder.call(func_scanf, [create_global_string(builder, f'%d\n\0', 'ddt3')])
print(module_ir)


builder.ret(zero)


engine = init_execution_engine()
compile_ir(engine, module_ir)
