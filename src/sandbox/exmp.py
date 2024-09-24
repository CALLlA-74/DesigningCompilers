import os

import llvmlite.binding as llvm
import llvmlite.ir as llvmir
from ctypes import CFUNCTYPE, c_int32


def create_global_string(builder: llvmir.IRBuilder, s: str, name: str) -> llvmir.Instruction:
    type_i8_x_len = llvmir.types.ArrayType(llvmir.types.IntType(8), len(s))
    constant = llvmir.Constant(type_i8_x_len, bytearray(s.encode('utf-8')))
    variable = llvmir.GlobalVariable(builder.module, type_i8_x_len, name)
    #variable.linkage = 'private'   # по умолчанию пишем всем private. external будет у interface-полей
    #variable.global_constant = True
    variable.initializer = constant
    variable.align = 1

    llvmir.Constant()

    zero = llvmir.Constant(llvmir.types.IntType(32), 0)
    variable_pointer = builder.gep(variable, [zero, zero], inbounds=True)
    return variable_pointer


def create_global_array(builder: llvmir.IRBuilder, length: int, name: str):
    type_i8_x_len = llvmir.types.ArrayType(llvmir.types.IntType(8), length)
    var = llvmir.GlobalVariable(builder.module, type_i8_x_len, name)
    var.linkage = 'private'
    var.global_constant = True
    var.align = 4
    zero = llvmir.Constant(llvmir.types.IntType(32), 0)
    return builder.gep(var, [zero, zero], inbounds=True)


def create_int_ptr(builder: llvmir.IRBuilder, val, name: str):
    int32 = llvmir.DoubleType()  # llvmir.types.IntType(32)
    variable = builder.alloca(int32, name=name)
    ptr = builder.gep(variable, [llvmir.Constant(llvmir.IntType(32), 0)], inbounds=True)

    builder.store(llvmir.Constant(llvmir.DoubleType(), val), ptr)

    return ptr


def create_str_ptr(builder: llvmir.IRBuilder, size: int, name: str):
    str_type = llvmir.ArrayType(llvmir.IntType(8), size)  # llvmir.types.IntType(32)
    variable = builder.alloca(str_type, name=name)
    zero = llvmir.Constant(llvmir.IntType(32), 0)
    ptr = builder.gep(variable, [zero, zero], inbounds=True)

    #builder.store(llvmir.Constant(str_type, bytearray('\0'.encode('utf-8'))), ptr)

    return ptr


def main():
    # common types
    type_i8p = llvmir.types.PointerType(llvmir.types.IntType(8))
    type_i32 = llvmir.types.IntType(32)
    type_i8 = llvmir.types.IntType(8)
    type_i32p = llvmir.types.PointerType(llvmir.types.IntType(32))

    module_ir = llvmir.Module('hello_world')
    builder = llvmir.IRBuilder()
    """FILE = module_ir.context.get_identified_type(name="FILE")



    # int printf(char* format, ...)
    type_func_fdopen = llvmir.FunctionType(llvmir.PointerType(FILE), [type_i32, type_i8p])
    #func_fdopen = module_ir.declare_intrinsic("fdopen", (), type_func_fdopen)

    type_func_setbuf = llvmir.FunctionType(llvmir.VoidType(), [llvmir.PointerType(FILE), type_i8p])
    func_setbuf = module_ir.declare_intrinsic('setbuf', (), type_func_setbuf)"""

    type_func_scanf = llvmir.types.FunctionType(type_i32, [type_i8p], var_arg=True)
    type_func_printf = llvmir.types.FunctionType(type_i32, [type_i8p], var_arg=True)
    func_scanf = module_ir.declare_intrinsic('scanf', (), type_func_scanf)
    func_printf = module_ir.declare_intrinsic('printf', (), type_func_printf)

    # int main()
    type_func_main = llvmir.types.FunctionType(return_type=type_i32, args=[])
    func_main = llvmir.Function(module_ir, type_func_main, 'main')
    zero = llvmir.Constant(type_i32, 0)

    # { printf("Hello, world\n"); return 0; }
    block_main = func_main.append_basic_block('entry')
    builder.position_at_end(block_main)

    file_mode = create_global_string(builder, "r\0", 'tt')
    #stdout = builder.gep(llvmir.GlobalVariable(module_ir, FILE, name='tt1'), [zero], name='stdout')
    #module_ir.context.get_identified_type()
    #builder.call(func_fdopen, [llvmir.Constant(type_i32, 1), file_mode])
    #builder.store(, stdout)

    #builder.call(func_setbuf, [, llvmir.Constant(llvmir.PointerType(type_i8), None)])

    str_p = create_global_string(builder, ' '*700*4 + '\n\0', 'a')
    for i in range(1):
        builder.call(func_printf, [str_p])
    ptr = create_int_ptr(builder, 0, 'inp')
    builder.call(func_scanf, [create_global_string(builder, '%lf\0', 'p2'), ptr])    # '%d\0'
    builder.call(func_printf, [create_global_string(builder, '%lf\n\0', 'pttrn'), builder.load(ptr)])  # '%d\0'

    ptr_str = create_str_ptr(builder, 2048, 'inp_str')
    builder.call(func_scanf, [create_global_string(builder, '%s\0', 'p5'), ptr_str])
    builder.call(func_printf, [ptr_str, create_global_string(builder, '\n\0', 'pttrn2')])

    builder.call(func_printf, [create_global_string(builder, '%d\n\0', 'pattern'), llvmir.Constant(type_i32, 32)])
    builder.call(func_printf, [create_global_string(builder, '3\0', 'b2')])

    #builder.alloca(llvmir.LabelType(), name='100')

    builder.ret(zero)

    print(module_ir)
    print()

    engine = init_execution_engine()
    compile_ir(engine, module_ir)

    """module = llvm.parse_assembly(str(module_ir))
    module.verify()
    obj = target_machine.emit_object(module)

    file = open('main.o', 'wb')
    file.write(obj)
    file.close()

    print('Compiling...')
    os.system('cc -o main main.o')
    print('Executing...')
    os.system('./main')"""


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
    return mod


if __name__ == '__main__':
    main()
