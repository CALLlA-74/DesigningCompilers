from typing import Dict, List
import typing
from llvmlite import ir
from llvmlite.ir import Module

from ir_builder.exceptions.CompileException import CompileException
from ir_builder.context import Scopes, TypesEnum, EmbeddedTypesEnum
import ir_builder.context.EmbeddedTypes as types
from ir_builder.context.EmbeddedTypes import Constructs
from ir_builder.utils import VarUtils

all_scopes = [Scopes.CONSTS, Scopes.VARS, Scopes.FUNCTIONS, Scopes.LABELS, Scopes.PROCEDURES, Scopes.RECORDS, Scopes.TYPES]
zero = ir.Constant(ir.IntType(32), 0)


class BaseContext:
    MAX_LEN_STR = 256

    def __init__(self, context_name):
        self.context_name = context_name
        """self.module: Module = ir.Module(context_name)
        self.__ir_builder = ir.IRBuilder()"""
        self.labels = dict()
        self.consts = dict()
        self.vars = dict()

    @staticmethod
    def type():
        return 'context'


class ModuleContext(BaseContext):
    def __init__(self, context_name):
        super().__init__(context_name)
        self.module: Module = ir.Module(context_name)
        self.__ir_builder = ir.IRBuilder()
        self.functions = dict()
        self.procedures = dict()
        self.types:Dict[Constructs.Type] = dict()

        """# !!!
        f:ir.Function = self.get_var_by_ident(ident=f'{context_name}_main', search_scopes=[Scopes.FUNCTIONS])
        self.get_ir_builder().ret(ir.Constant(ir.IntType(32), 0))
        # !!!"""

        self.__init_types()
        self.__init_lib()

    def get_module(self):
        return self.module

    @staticmethod
    def type():
        return 'module'

    def define_main(self):
        self.define_function(return_type=ir.IntType(32), args=[], name=f'{self.context_name}_main')     # 'main'

    def finish_main(self):
        self.get_ir_builder().ret(ir.Constant(ir.IntType(32), 0))

    def get_context_name(self):
        return self.context_name

    def abstract_type_to_type(self, typ:typing.Type[types.AbstractType]):
        if typ.get_type() == EmbeddedTypesEnum.IDENTIFIER:
            return self.get_var_by_ident(ident=typ.typ_ident, search_scopes=[Scopes.TYPES])
        else:
            return self.create_type(new_typ=types.CustomType(ident=None, typ_val=typ))

    def define_function(self, return_type:typing.Type[ir.Type], args:List[Constructs.Variable], name:str):
        if not self.is_unique_ident(name):
            raise CompileException("Function name is not unique")
        arg_types = [self.abstract_type_to_type(arg.typ).instruct for arg in args]

        type_func = ir.types.FunctionType(return_type=return_type, args=arg_types)
        func = ir.Function(self.module, type_func, name)
        block = func.append_basic_block('entry')
        self.__ir_builder.position_at_end(block)
        func_ctx = ProcedureContext(context_name=name, module_context=self)
        new_func = Constructs.ProcedureOrFunction(
            ident=name,
            func_typ=type_func,
            arg_list=args,
            func_instruct=func,
            local_ctx=func_ctx,
            is_std=False
        )   # {"ident": name, "type": type_func_main, "val": func}
        for arg, func_arg in zip(args, func.args):
            arg.init_val = func_arg
            func_ctx.define_variable(arg)
        self.functions[name] = new_func
        return new_func

    def call_func(self, func:Constructs.ProcedureOrFunction,
                  params:typing.List[typing.Union[Constructs.Const, Constructs.Variable, Constructs.Value]]):
        if func.local_ctx:
            args = []
            for p in params:
                args.append(p.instruct)
            self.__ir_builder.call(func.func_instruct, args=args)
        elif func.ident == "write" or func.ident == "writeln":
            fmt = ""
            args = []
            for p in params:
                if p.instruct.type == ir.IntType(64):
                    fmt += "%d"
                elif p.instruct.type == ir.IntType(8) or isinstance(p.instruct.type, ir.PointerType):
                    fmt += "%s"
                elif p.instruct.type == ir.DoubleType():
                    fmt += "%f"
                else:
                    continue
                args.append(p.instruct)
            fmt += "\n\0" if func.ident == "writeln" else "\0"
            fmt_str = self.__ir_builder.alloca(typ=ir.ArrayType(ir.IntType(8), len(fmt)))
            self.__ir_builder.store(ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt, "utf-8")), fmt_str)
            fmt_ptr = self.__ir_builder.alloca(ir.PointerType(ir.IntType(8)))
            self.__ir_builder.store(self.__ir_builder.gep(fmt_str, indices=[zero, zero]), fmt_ptr)
            args = [self.__ir_builder.load(fmt_ptr)] + args
            self.__ir_builder.call(func.func_instruct, args=args)

    def __init_types(self):
        typ_val = types.TypeIdentifier(typ_ident=TypesEnum.INTEGER)
        self.types[TypesEnum.INTEGER] = Constructs.Type(ident=TypesEnum.INTEGER,
                                                        typ_val=typ_val,
                                                        instruct=ir.IntType(64),
                                                        default_val=ir.Constant(ir.IntType(64), 0))

        typ_val = types.TypeIdentifier(typ_ident=TypesEnum.REAL)
        self.types[TypesEnum.REAL] = Constructs.Type(ident=TypesEnum.REAL,
                                                     typ_val=typ_val,
                                                     instruct=ir.DoubleType(),
                                                     default_val=ir.Constant(ir.DoubleType(), 0.0))

        typ_val = types.TypeIdentifier(typ_ident=TypesEnum.BOOLEAN)
        self.types[TypesEnum.BOOLEAN] = Constructs.Type(ident=TypesEnum.BOOLEAN,
                                                        typ_val=typ_val,
                                                        instruct=ir.IntType(1),
                                                        default_val=ir.Constant(ir.IntType(1), 0))

        typ_val = types.TypeIdentifier(typ_ident=TypesEnum.CHAR)
        self.types[TypesEnum.CHAR] = Constructs.Type(ident=TypesEnum.CHAR,
                                                     typ_val=typ_val,
                                                     instruct=ir.IntType(8),
                                                     default_val=ir.Constant(ir.IntType(8), 0))

        typ_val = types.TypeIdentifier(typ_ident=TypesEnum.STRING)
        self.types[TypesEnum.STRING] = Constructs.Type(ident=TypesEnum.STRING,
                                                       typ_val=typ_val,
                                                       instruct=ir.PointerType(ir.IntType(8)),
                                                       default_val=ir.Constant(ir.ArrayType(ir.IntType(8), 256),
                                                                               bytearray("", "utf-8")))       # ir.ArrayType(ir.IntType(8), self.MAX_LEN_STR)

    def __init_lib(self):
        int32 = ir.types.IntType(32)
        int16p = ir.PointerType(ir.types.IntType(8))
        io_func_type = ir.types.FunctionType(int32, [int16p], var_arg=True)

        write_proc = self.module.declare_intrinsic('printf', (), io_func_type)
        read_proc = self.module.declare_intrinsic('scanf', (), io_func_type)

        ident = "write"
        self.procedures[ident] = Constructs.ProcedureOrFunction(ident=ident, arg_list=io_func_type.args,
                                                                func_typ=io_func_type, func_instruct=write_proc)

        ident = "writeln"
        self.procedures[ident] = Constructs.ProcedureOrFunction(ident=ident, arg_list=io_func_type.args,
                                                                func_typ=io_func_type, func_instruct=write_proc)

        ident = "read"
        self.procedures[ident] = Constructs.ProcedureOrFunction(ident=ident, arg_list=io_func_type.args,
                                                                func_typ=io_func_type, func_instruct=read_proc)
        ident = "readln"
        self.procedures[ident] = Constructs.ProcedureOrFunction(ident=ident, arg_list=io_func_type.args,
                                                                func_typ=io_func_type, func_instruct=read_proc)

    def clear_stdout(self):
        pass    # вызвать writeln с пробелом длины 700*4

    def is_unique_ident(self, ident: str) -> bool:
        return not (ident in list(self.labels.keys()) or ident in list(self.consts.keys()) or
                    ident in list(self.vars.keys()) or ident in list(self.functions.keys()) or
                    ident in list(self.procedures.keys()) or ident in list(self.types.keys()) or
                    ident == self.module.name)

    def get_ir_builder(self) -> ir.IRBuilder:
        return self.__ir_builder

    def get_var_by_ident(self, ident: str, search_scopes:list = None):
        ident = ident.lower()
        if search_scopes is None:
            search_scopes = all_scopes

        if Scopes.LABELS in search_scopes:
            res = self.labels.get(ident)
            if res:
                return res
        if Scopes.CONSTS in search_scopes:
            res = self.consts.get(ident)
            if res:
                return res
        if Scopes.VARS in search_scopes:
            res = self.vars.get(ident)
            if res:
                return res
        if Scopes.PROCEDURES in search_scopes:
            res = self.procedures.get(ident)
            if res:
                return res
        if Scopes.FUNCTIONS in search_scopes:
            res = self.functions.get(ident)
            if res:
                return res
        if Scopes.TYPES in search_scopes:
            res = self.types.get(ident)
            if res:
                return res

        return None

    def declare_labels(self, adv_labels: list):
        adv_labels_set = set(adv_labels)
        old_labels_set = set(self.labels.keys())
        if len(adv_labels) != len(adv_labels_set) or old_labels_set.intersection(adv_labels_set):
            raise CompileException(f'Duplicate labels: {self.get_context_name()}')

        for label in adv_labels:
            self.labels[label] = Constructs.Label(label)

    def define_constant(self, const: Constructs.Const):
        is_global = True if self.type() == 'module' else False

        ident = const.ident
        typ = const.typ
        val = const.val
        if not self.is_unique_ident(ident):
            raise CompileException(f"Const identifier \"{ident}\" must be unique")

        """if typ == TypesEnum.INT_LITERAL:
            const.instruct = VarUtils.create__const_int_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)
        elif typ == TypesEnum.REAL_LITERAL:
            const.instruct = VarUtils.create_const_real_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)
        elif typ == TypesEnum.STRING_LITERAL:
            const.instruct = VarUtils.create_const_string_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)
        elif typ == TypesEnum.CHAR_LITERAL:
            const.instruct = VarUtils.create_const_char_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)"""
        if typ == TypesEnum.IDENTIFIER or typ == TypesEnum.SIGNED_IDENTIFIER:
            defined_const:Constructs.Const = self.get_var_by_ident(val, search_scopes=[Scopes.CONSTS])
            if defined_const is None:
                raise CompileException(f"Constant {ident} is not defined")
            val = defined_const.val
            if typ == TypesEnum.SIGNED_IDENTIFIER:
                tmp = defined_const.typ.ident                           # defined_const.typ.typ_val.get_typ()
                if tmp == TypesEnum.INTEGER or tmp == TypesEnum.REAL:
                    v = val.constant
                    val = ir.Constant(typ=defined_const.typ.instruct, constant=v*(-1 if const.sign == '-' else 1))
                else:
                    raise CompileException("String constant must be unsigned")
            const.typ = defined_const.typ
            typ = const.typ
            const.val = val
            const.instruct = VarUtils.create_var_(name=ident, typ=typ, context=self, init_val=val,
                                                  is_const=True, is_global=is_global)
        else:
            const.typ = self.get_var_by_ident(ident=typ.typ_ident, search_scopes=[Scopes.TYPES])
            val = ir.Constant(typ=const.typ.instruct, constant=val)
            const.val = val
            typ = const.typ
            const.instruct = VarUtils.create_var_(name=ident, typ=typ, context=self, init_val=val,
                                                  is_global=is_global, is_const=True)
            # raise CompileException(f"Impossible type of value const: val= {val}; type= {typ}")

        self.consts[ident] = const

    def define_type(self, new_typ: types.CustomType):
        if not self.is_unique_ident(new_typ.ident):
            raise CompileException(f"Identifier of new type \'{new_typ.ident}\' is not unique")
        if new_typ.typ_val.get_type() == EmbeddedTypesEnum.RECORD:
            rec_type = Constructs.Type(ident=new_typ.ident,
                                       typ_val=new_typ.typ_val,
                                       instruct=self.module.context.get_identified_type(new_typ.ident),
                                       default_val=None)
            self.types[new_typ.ident] = rec_type
            new_typ.typ_val.get_instr(self, type_name=new_typ.ident)
            rec_type.default_val = new_typ.typ_val.get_init_val(self)
        else:
            self.types[new_typ.ident] = self.create_type(new_typ)

    def create_type(self, new_typ: types.CustomType) -> Constructs.Type:
        if new_typ.typ_val.get_type() not in EmbeddedTypesEnum:
            raise CompileException(f"Error in type definition: {new_typ.ident}")
        type_instr = new_typ.typ_val.get_instr(self)
        init_val = new_typ.typ_val.get_init_val(self)
        return Constructs.Type(ident=new_typ.ident, typ_val=new_typ.typ_val, instruct=type_instr, default_val=init_val)

    def define_variable(self, var: Constructs.Variable):
        if var.typ.get_type() == EmbeddedTypesEnum.IDENTIFIER:
            var.typ = self.get_var_by_ident(ident=var.typ.typ_ident, search_scopes=[Scopes.TYPES])
        else:
            var.typ = self.create_type(new_typ=types.CustomType(ident=None, typ_val=var.typ))

        if var.typ.typ_val.get_type() == EmbeddedTypesEnum.FUNCTION:
            """self.functions[var.ident] = Constructs.ProcedureOrFunction(
                ident=var.ident, func_typ=var.typ.instruct
            )"""
            pass
        elif var.typ.typ_val.get_type() == EmbeddedTypesEnum.PROCEDURE:
            """self.functions[var.ident] = Constructs.ProcedureOrFunction(
                ident=var.ident, func_typ=var.typ.instruct
            )"""
            pass
        else:
            typ = var.typ
            var.instruct = VarUtils.create_var_(name=var.ident, typ=typ, context=self,
                                                init_val=var.init_val, is_global=True)
            self.vars[var.ident] = var
        # 2) в каждом классе в EmbeddedTypes реализовать функции для записи/получения значения в переменную заданного типа


class ProcedureContext(BaseContext):
    def __init__(self, context_name, module_context: ModuleContext):
        super().__init__(context_name)
        self.module_context: ModuleContext = module_context

    @staticmethod
    def type():
        return 'procedure'

    def get_context_name(self):
        return self.module_context.get_context_name() + '.' + self.context_name

    def is_unique_ident(self, ident: str) -> bool:
        return not (ident in self.labels or ident in self.consts or ident in self.vars or ident == self.get_context_name())

    def get_module(self):
        return self.module_context.get_module()

    def get_ir_builder(self) -> ir.IRBuilder:
        return self.module_context.get_ir_builder()

    def get_var_by_ident(self, ident: str, search_scopes:list = None):
        ident = ident.lower()
        if search_scopes is None:
            search_scopes = all_scopes

        if Scopes.LABELS in search_scopes:
            res = self.labels.get(ident)
            if res:
                return res
        if Scopes.CONSTS in search_scopes:
            res = self.consts.get(ident)
            if res:
                return res
        if Scopes.VARS in search_scopes:
            res = self.vars.get(ident)
            if res:
                return res

        return self.module_context.get_var_by_ident(ident)

    def declare_labels(self, adv_labels: list):
        adv_labels_set = set(adv_labels)
        old_labels_set = set(self.labels.keys())
        if len(adv_labels) != len(adv_labels_set) or old_labels_set.intersection(adv_labels_set):
            raise CompileException(f'Duplicate labels: {self.get_context_name()}')

        for label in adv_labels:
            self.labels[label] = Constructs.Label(label)

    def define_constant(self, const: Constructs.Const):
        is_global = True if self.type() == 'module' else False

        ident = const.ident
        typ = const.typ
        val = const.val
        if not self.is_unique_ident(ident):
            raise CompileException(f"Const identifier \"{ident}\" must be unique")

        """if typ == TypesEnum.INT_LITERAL:
            const.instruct = VarUtils.create__const_int_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)
        elif typ == TypesEnum.REAL_LITERAL:
            const.instruct = VarUtils.create_const_real_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)
        elif typ == TypesEnum.STRING_LITERAL:
            const.instruct = VarUtils.create_const_string_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)
        elif typ == TypesEnum.CHAR_LITERAL:
            const.instruct = VarUtils.create_const_char_var(name=ident, builder=__ir_builder, val=val, is_const=True, is_global=is_global)"""
        if typ == TypesEnum.IDENTIFIER or typ == TypesEnum.SIGNED_IDENTIFIER:
            defined_const:Constructs.Const = self.get_var_by_ident(val, search_scopes=[Scopes.CONSTS])
            if defined_const is None:
                raise CompileException(f"Constant {ident} is not defined")
            val = defined_const.val
            if typ == TypesEnum.SIGNED_IDENTIFIER:
                tmp = defined_const.typ.typ_val.get_typ()
                if tmp == TypesEnum.INTEGER or tmp == TypesEnum.REAL:
                    val *= (-1 if const.sign == '-' else 1)
                else:
                    raise CompileException("String constant must be unsigned")
            const.typ = defined_const.typ
            const.val = val
            typ = const.typ
            const.instruct = VarUtils.create_var_(name=ident, typ=typ, context=self, init_val=val,
                                                  is_const=True, is_global=is_global)
        else:
            const.typ = self.get_var_by_ident(ident=typ.typ_ident, search_scopes=[Scopes.TYPES])
            val = ir.Constant(typ=const.typ.instruct, constant=val)
            typ = const.typ
            const.instruct = VarUtils.create_var_(name=ident, typ=typ, context=self, init_val=val,
                                                  is_global=is_global, is_const=True)
            # raise CompileException(f"Impossible type of value const: val= {val}; type= {typ}")

        self.consts[ident] = const

    def create_type(self, new_typ: types.CustomType):
        return self.module_context.create_type(new_typ=new_typ)

    def define_variable(self, var: Constructs.Variable):
        if var.typ.get_type() == EmbeddedTypesEnum.IDENTIFIER:
            var.typ = self.get_var_by_ident(ident=var.typ.typ_ident, search_scopes=[Scopes.TYPES])
        else:
            var.typ = self.create_type(new_typ=types.CustomType(ident=None, typ_val=var.typ))

        if var.typ.typ_val.get_type() == EmbeddedTypesEnum.FUNCTION:
            pass
            """self.functions[var.ident] = Constructs.ProcedureOrFunction(
                ident=var.ident, func_typ=var.typ.instruct
            )"""
        elif var.typ.typ_val.get_type() == EmbeddedTypesEnum.PROCEDURE:
            pass
            """self.functions[var.ident] = Constructs.ProcedureOrFunction(
                ident=var.ident, func_typ=var.typ.instruct
            )"""
        else:
            typ = var.typ
            self.vars[var.ident] = VarUtils.create_var_(name=var.ident, typ=typ, context=self,
                                                        init_val=var.init_val, is_global=False)
