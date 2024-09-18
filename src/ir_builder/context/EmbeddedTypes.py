import abc
from typing import Union, List, Type, Any

from ir_builder.exceptions import CompileException
from llvmlite import ir

from ir_builder.context import Scopes, TypesEnum, EmbeddedTypesEnum  # , Context as Context
import ir_builder.context.Constructs as Constructs


def get_unique_ident(head: str) -> str:
    if not hasattr(get_unique_ident, "ident"):
        get_unique_ident.ident = 0
    get_unique_ident.ident += 1
    return f".{head}_{get_unique_ident.ident}"


class AbstractType(abc.ABC):
    @abc.abstractmethod
    def get_type(self): pass

    @abc.abstractmethod
    def get_instr(self, context): pass  # :Union[Context.ModuleContext, Context.ProcedureContext]

    @abc.abstractmethod
    def get_init_val(self, context): pass    # :Union[Context.ModuleContext, Context.ProcedureContext]

    def abstract_type_to_type(self, context, abstr_typ) -> Constructs.Type:
        if abstr_typ.get_type() == EmbeddedTypesEnum.IDENTIFIER:
            return context.get_var_by_ident(ident=abstr_typ.typ_ident, search_scopes=[Scopes.TYPES])
        else:
            return context.create_type(new_typ=CustomType(ident=None, typ_val=abstr_typ))


class TypeIdentifier(AbstractType):
    def __init__(self, typ_ident: Union[TypesEnum, str]):
        self.typ_ident = typ_ident
        self.embedded_typ = EmbeddedTypesEnum.IDENTIFIER

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):       # :Union[Context.ModuleContext, Context.ProcedureContext]
        return context.get_var_by_ident(ident=self.typ_ident, search_scopes=[Scopes.TYPES]).instruct

    def get_init_val(self, context):
        t:Constructs.Type = context.get_var_by_ident(ident=self.typ_ident, search_scopes=[Scopes.TYPES])
        return ir.Constant(t.instruct, t.default_val)


class ProcedureType(AbstractType):
    def __init__(self, arg_list:List[Constructs.Variable]):
        self.embedded_typ = EmbeddedTypesEnum.PROCEDURE
        self.arg_list = arg_list

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):       # :Union[Context.ModuleContext, Context.ProcedureContext]
        arg_types = []
        for arg in self.arg_list:
            arg_types.append(arg.typ.get_instr(context))
        return ir.FunctionType(return_type=ir.VoidType(), args=arg_types)

    def get_init_val(self, context):
        return None


class FunctionType(AbstractType):
    def __init__(self, arg_list:List[Constructs.Variable], ret_type: TypeIdentifier):
        self.embedded_typ = EmbeddedTypesEnum.FUNCTION
        self.arg_list = arg_list
        self.ret_type = ret_type

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):       # :Union[Context.ModuleContext, Context.ProcedureContext]
        arg_types = []
        for arg in self.arg_list:
            arg_types.append(arg.typ.get_instr())
        return ir.FunctionType(return_type=self.ret_type.get_instr(context), args=arg_types)

    def get_init_val(self, context):
        return None


class SubRangeType(AbstractType):
    def __init__(self, left:Union[Constructs.Value, int], right:Union[Constructs.Value, int]):
        self.left = left
        self.right = right
        self.embedded_typ = EmbeddedTypesEnum.SUBRANGE
        self.length = -1
        self.dim = -1

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):       # :Union[Context.ModuleContext, Context.ProcedureContext]
        if self.length <= -1:
            self.left = self.left.get_val(context, search_scopes=[Scopes.CONSTS])
            self.right = self.right.get_val(context, search_scopes=[Scopes.CONSTS])

            if isinstance(self.left, ir.Constant):
                self.left = self.left.constant
            if isinstance(self.right, ir.Constant):
                self.right = self.right.constant

            if not isinstance(self.left, int) or not isinstance(self.right, int):
                raise CompileException(f"Subrange limits l, r error: got type of l: {type(self.left)}; "
                                       f"type of r: {type(self.right)}, but expected int")
            if self.left > self.right:
                raise CompileException(f"Subrange limits error: {self.left} > {self.right}")
            self.length = self.right - self.left + 1
            self.dim = self.left
        return None

    def get_init_val(self, context):
        return None


class ArrayType(AbstractType):
    def __init__(self, subranges:List[SubRangeType], typ_val:Constructs.Type):
        self.subranges = subranges
        self.embedded_typ = EmbeddedTypesEnum.ARRAY
        if isinstance(typ_val, SubRangeType or FunctionType or ProcedureType):
            raise CompileException(f"Invalid component array type: {type(typ_val).__name__}")
        if len(subranges) <= 0:
            raise CompileException(f"Invalid array length: {len(subranges)}")
        self.typ = typ_val

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):                   # :Union[Context.ModuleContext, Context.ProcedureContext]
        self.typ = self.abstract_type_to_type(context, self.typ)
        instr = self.typ.instruct
        for subr in reversed(self.subranges):
            subr.get_instr(context)
            instr = ir.ArrayType(instr, subr.length)
        return instr

    def get_init_val(self, context):
        instr = self.typ.instruct
        init_val = self.typ.default_val
        for subr in reversed(self.subranges):
            subr.get_instr(context)
            instr = ir.ArrayType(instr, subr.length)
            init_val = [init_val]*subr.length
        return ir.Constant(instr, init_val)


class StringType(AbstractType):
    def __init__(self, length: Any):
        self.length = length
        self.embedded_typ = EmbeddedTypesEnum.FIXEDSTRING

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):               # :Union[Context.ModuleContext, Context.ProcedureContext]
        if isinstance(self.length, Constructs.Value):
            if isinstance(self.length.val, int):
                if self.length.val < 0:
                    raise CompileException(f"String length cannot less than 0")
                elif isinstance(self.length.val, float):
                    raise CompileException(f"String length cannot be type REAL")
        else:
            var_const = context.get_var_by_ident(ident=self.length, search_scopes=[Scopes.CONSTS])
            self.length = var_const.val
        return ir.PointerType(ir.IntType(8))    # ir.ArrayType(ir.IntType(8), self.length)

    def get_init_val(self, context):
        ir.Constant(ir.ArrayType(ir.IntType(8), self.length), bytearray('', 'utf-8'))


class RecordType(AbstractType):

    def __init__(self, field_list:List[Constructs.Variable] = [], packed:bool = False):
        self.embedded_typ = EmbeddedTypesEnum.RECORD
        self.field_list = field_list
        self.field_indexes = {}
        self.packed = packed
        self.__typ = None

        for idx, field in enumerate(self.field_list):
            self.field_indexes[field.ident] = idx

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context, type_name=""):                           # :Union[Context.ModuleContext, Context.ProcedureContext]
        if type_name and len(type_name) > 0:
            record_instruct = context.get_var_by_ident(ident=type_name, search_scopes=[Scopes.TYPES]).instruct
        else:
            module:ir.Module = context.get_module()
            record_instruct = module.context.get_identified_type(get_unique_ident("rec"))

        self.__typ = record_instruct
        if not record_instruct.is_opaque:   # если тело декларировано, то возвращаемся
            return record_instruct

        elems = []
        for field in self.field_list:
            field.typ = self.abstract_type_to_type(context, field.typ)
            elems.append(field.typ.instruct)
        record_instruct.set_body(*elems)
        return record_instruct  # ir.LiteralStructType(elems=elems, packed=self.packed)

    def get_init_val(self, context):
        vals = []
        for field in self.field_list:
            vals.append(field.typ.default_val)
        return ir.Constant(typ=self.__typ, constant=vals)


class PointerType(AbstractType):
    def __init__(self, type_ident: Union[EmbeddedTypesEnum, str]):
        self.embedded_typ = EmbeddedTypesEnum.POINTER
        self.typ = type_ident

    def get_type(self):
        return self.embedded_typ

    def get_instr(self, context):                           # :Union[Context.ModuleContext, Context.ProcedureContext]
        return ir.PointerType(context.get_var_by_ident(ident=self.typ.typ_ident, search_scopes=[Scopes.TYPES]).instruct)

    def get_init_val(self, context):                        # :Union[Context.ModuleContext, Context.ProcedureContext]
        return ir.Constant(self.get_instr(context), None)


class CustomType:
    def __init__(self, ident:str, typ_val:Type[AbstractType]):
        self.ident = ident
        self.typ_val = typ_val
