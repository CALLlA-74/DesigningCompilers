import ir_builder.context
from typing import Union
import typing
from lexer_parser.antlr.PascalVisitor import PascalVisitor
from lexer_parser.antlr.PascalParser import PascalParser
from ir_builder.context.Context import ModuleContext, ProcedureContext
from ir_builder.exceptions.CompileException import CompileException
from ir_builder.utils import VarUtils
from ir_builder.context import Constructs, EmbeddedTypes, TypesEnum, Scopes
from llvmlite import ir


class ParserVisitor(PascalVisitor):
    def __init__(self):
        self.context: ModuleContext = None

    def visitProgram(self, ctx:PascalParser.ProgramContext):
        if ctx.getChildCount() == 4:
            self.visit(ctx.programHeading())
            ctx.customContext = ModuleContext(ctx.programHeading().customContext)
            self.context = ctx.customContext
            self.visit(ctx.block())
        else:
            # self.visit(ctx.getChild(0))
            # self.visit(ctx.getChild(2))
            raise CompileException(f"Syntax error. {ctx.INTERFACE()}...")
        return self.context

    def visitProgramHeading(self, ctx:PascalParser.ProgramHeadingContext):
        self.visit(ctx.identifier())
        if ctx.getChildCount() == 3 and ctx.getChild(0) == ctx.PROGRAM():
            ctx.customContext = ctx.identifier().customContext
        else:
            raise CompileException(f'Syntax error:{ctx.start.line}:{ctx.start.column}. {ctx.UNIT()}...')
        return True

    def visitIdentifier(self, ctx:PascalParser.IdentifierContext):
        ctx.customContext = ctx.IDENT().symbol.text.lower()
        return True

    def visitBlock(self, ctx:PascalParser.BlockContext):
        # 1) ПРИ ОБЪЯВЛЕНИИ ПЕРЕМЕННЫХ/ФУНКЦИЙ/ПРОЦЕДУР ИХ ИДЕНТИФИКАТОРЫ = id_модуля + id_в_коде
        # если переменная создана внутри функиции/процедуры, то идентификатор = id_модуля + id_функции + id_в_коде

        # 2) Labels можно юзать только, объявленные в этом блоке. То есть глобальные метки недоступны внутри функции
        # 3) Имена любых идентификаторов должны быть уникальны: в рамках одного блока не должно быть VAR c и CONST c (например)
        # или VAR и PROCEDURE (и т.п.). Имя модуля тоже является идентификатором и тоже уникально!
        # 4) По умолчанию идет обращение к локальному полю (вне зависимости от того CONST это или VAR).
        # 5) Для обращения именно к глобальному полю надо писать ModuleName.{имя поля}
        # 6) функций и процедур внутри функций и процедур быть не может
        # 7) функция или процедура не может быть вызвана (из другой функции/процедуры) до ее описания
        # 8) в контекстах процедур/функций RECORD описывать нельзя (скорее всего так сделаю???)
        # 9) в контекстах процедуры/функции имена локальных переменных и их параметров не должны совпадать с именем самой процедуры/функции
        ctx.customContext = ctx.parentCtx.customContext
        context:ModuleContext = ctx.customContext
        for i in range(ctx.getChildCount()):
            if ctx.customContext.type() != 'module':
                if ctx.getChild(i) == ctx.procedureAndFunctionDeclarationPart():
                    raise CompileException("Procedure or function declaration inside of function or procedure context is not expected")
                if ctx.getChild(i) == ctx.typeDefinitionPart():
                    raise CompileException("Type definition inside of function or procedure context is not expected")
            if ctx.compoundStatement():
                if ctx.getChild(i) == ctx.compoundStatement() and context.type() == "module":
                    context.define_main()
                    self.visit(ctx.getChild(i))
                    context.finish_main()
                    break
            self.visit(ctx.getChild(i))
            if ctx.compoundStatement():
                if ctx.getChild(i) == ctx.compoundStatement() and context.type() == "procedure":
                    context.finish_func()

            """
            остались: 
            1) compoundStatement"""
        return True

    def visitUsesUnitsPart(self, ctx:PascalParser.UsesUnitsPartContext):
        return False

    def visitLabelDeclarationPart(self, ctx:PascalParser.LabelDeclarationPartContext):
        ctx.customContext = []
        for label in ctx.label():
            ctx.customContext.append(label.start.text)
        ctx.parentCtx.customContext.declare_labels(ctx.customContext)
        return True

    def visitLabel(self, ctx:PascalParser.LabelContext):
        return True

    def visitConstantDefinitionPart(self, ctx:PascalParser.ConstantDefinitionPartContext):
        ctx.customContext = ctx.parentCtx.customContext
        for const in ctx.constantDefinition():
            self.visit(const)
            ctx.parentCtx.customContext.define_constant(const.customContext)
        return True

    def visitConstantDefinition(self, ctx:PascalParser.ConstantDefinitionContext):
        self.visit(ctx.identifier())
        tmp = ctx.identifier().customContext
        self.visit(ctx.constant())
        const = ctx.constant().customContext
        ctx.customContext = Constructs.Const(ident=ctx.identifier().customContext, typ=const.typ, val=const.val, sign=const.sign)
        return True

    def visitConstantChr(self, ctx:PascalParser.ConstantChrContext):
        self.visit(ctx.unsignedInteger())
        code = ctx.unsignedInteger().customContext.val
        typ = EmbeddedTypes.TypeIdentifier(typ_ident=TypesEnum.CHAR)
        ctx.customContext = Constructs.Value(typ=typ, val=chr(code))
        ctx.customContext.instruct = ir.Constant(ir.IntType(8), bytearray(ctx.customContext.val, 'utf-8'))
        return True

    def visitConstant(self, ctx:PascalParser.ConstantContext):
        self.visitChildren(ctx)
        if ctx.getChild(0) == ctx.unsignedNumber():
            ctx.customContext = ctx.unsignedNumber().customContext
        elif ctx.getChild(0) == ctx.sign() and ctx.getChild(1) == ctx.unsignedNumber():
            ctx.customContext = ctx.unsignedNumber().customContext
            ctx.customContext.val *= (-1 if ctx.sign().customContext == '-' else 1)
        elif ctx.string():
            ctx.customContext = ctx.string().customContext
        elif ctx.constantChr():
            ctx.customContext = ctx.constantChr().customContext
        elif ctx.sign() and ctx.identifier():
            ctx.customContext = Constructs.Value(typ=TypesEnum.SIGNED_IDENTIFIER,
                                                 val=ctx.identifier().customContext,
                                                 sign=ctx.sign().customContext)
        elif ctx.identifier():
            ctx.customContext = Constructs.Value(typ=TypesEnum.IDENTIFIER, val=ctx.identifier().customContext)
        return True

    def visitUnsignedNumber(self, ctx:PascalParser.UnsignedNumberContext):
        self.visit(ctx.getChild(0))
        ctx.customContext = ctx.children[0].customContext
        return True

    def visitUnsignedInteger(self, ctx:PascalParser.UnsignedIntegerContext):
        typ = EmbeddedTypes.TypeIdentifier(typ_ident=TypesEnum.INTEGER)
        ctx.customContext = Constructs.Value(typ=typ, val=VarUtils.parse_int(ctx.NUM_INT().symbol.text))
        ctx.customContext.instruct = ir.Constant(ir.IntType(64), ctx.customContext.val)
        return True

    def visitUnsignedReal(self, ctx:PascalParser.UnsignedRealContext):
        typ = EmbeddedTypes.TypeIdentifier(typ_ident=TypesEnum.REAL)
        ctx.customContext = Constructs.Value(typ=typ, val=VarUtils.parse_real(ctx.NUM_REAL().symbol.text))
        ctx.customContext.instruct = ir.Constant(ir.DoubleType(), ctx.customContext.val)
        return True

    def visitSign(self, ctx:PascalParser.SignContext):
        ctx.customContext = ctx.getChild(0).symbol.text
        return True

    def visitBool_(self, ctx:PascalParser.Bool_Context):
        typ = EmbeddedTypes.TypeIdentifier(typ_ident=TypesEnum.BOOLEAN)
        ctx.customContext = Constructs.Value(typ=typ, val=ctx.getChild(0).symbol.text.lower())
        val = ctx.customContext.val
        ctx.customContext.instruct = ir.Constant(ir.IntType(1), 1 if val == "true" else 0)
        return True

    def visitString(self, ctx:PascalParser.StringContext):
        s = ctx.STRING_LITERAL().symbol.text
        typ = EmbeddedTypes.TypeIdentifier(typ_ident=TypesEnum.STRING)
        ctx.customContext = Constructs.Value(typ=typ, val=s[1:len(s) - 1] + "\0")
        string = ctx.customContext.val
        ctx.customContext.instruct = ir.Constant(ir.ArrayType(ir.IntType(8), len(string)), bytearray(string, "utf-8"))
        return True

    def visitTypeDefinitionPart(self, ctx:PascalParser.TypeDefinitionPartContext):
        self.visitChildren(ctx)
        for define in ctx.typeDefinition():
            ctx.parentCtx.customContext.define_type(define.customContext)
        return True

    def visitTypeDefinition(self, ctx:PascalParser.TypeDefinitionContext):
        self.visit(ctx.identifier())
        self.visit(ctx.getChild(2))
        ctx.customContext = EmbeddedTypes.CustomType(ident=ctx.identifier().customContext,
                                                     typ_val=ctx.getChild(2).customContext)
        return True

    def visitFunctionType(self, ctx:PascalParser.FunctionTypeContext):
        """if ctx.formalParameterList():
            self.visit(ctx.formalParameterList())
            arg_list = ctx.formalParameterList().customContext
        else:
            arg_list = []
        self.visit(ctx.resultType())
        ctx.customContext = EmbeddedTypes.FunctionType(arg_list=arg_list,
                                                       ret_type=ctx.resultType().customContext)
        return True"""
        raise CompileException("Invalid syntax")

    def visitProcedureType(self, ctx:PascalParser.ProcedureTypeContext):
        """self.visit(ctx.formalParameterList())
        ctx.customContext = EmbeddedTypes.ProcedureType(arg_list=ctx.formalParameterList().customContext)
        return True"""
        raise CompileException("Invalid syntax")

    def visitType_(self, ctx:PascalParser.Type_Context):
        self.visit(ctx.getChild(0))
        ctx.customContext = ctx.getChild(0).customContext
        return True

    def visitSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        self.visitChildren(ctx)
        ctx.customContext = ctx.children[0].customContext
        return True

    def visitScalarType(self, ctx:PascalParser.ScalarTypeContext):
        raise CompileException("Unsupportable type")

    def visitSubrangeType(self, ctx:PascalParser.SubrangeTypeContext):
        self.visitChildren(ctx)
        l, r = ctx.constant()[0].customContext, ctx.constant()[1].customContext
        ctx.customContext = EmbeddedTypes.SubRangeType(left=l, right=r)
        return True

    def visitTypeIdentifier(self, ctx:PascalParser.TypeIdentifierContext):
        self.visitChildren(ctx)
        if ctx.identifier():
            ctx.customContext = EmbeddedTypes.TypeIdentifier(typ_ident=ctx.identifier().customContext)
        elif ctx.CHAR():
            ctx.customContext = EmbeddedTypes.TypeIdentifier(typ_ident=ir_builder.context.TypesEnum.CHAR)
        elif ctx.BOOLEAN():
            ctx.customContext = EmbeddedTypes.TypeIdentifier(typ_ident=ir_builder.context.TypesEnum.BOOLEAN)
        elif ctx.INTEGER():
            ctx.customContext = EmbeddedTypes.TypeIdentifier(typ_ident=ir_builder.context.TypesEnum.INTEGER)
        elif ctx.REAL():
            ctx.customContext = EmbeddedTypes.TypeIdentifier(typ_ident=ir_builder.context.TypesEnum.REAL)
        elif ctx.STRING():
            ctx.customContext = EmbeddedTypes.TypeIdentifier(typ_ident=ir_builder.context.TypesEnum.STRING)
        return True

    def visitStructuredType(self, ctx:PascalParser.StructuredTypeContext):
        self.visit(ctx.unpackedStructuredType())
        ctx.customContext = ctx.unpackedStructuredType().customContext
        return True

    def visitUnpackedStructuredType(self, ctx:PascalParser.UnpackedStructuredTypeContext):
        self.visit(ctx.getChild(0))
        if ctx.arrayType():
            ctx.customContext = ctx.arrayType().customContext
        elif ctx.recordType():
            ctx.customContext = ctx.recordType().customContext
        return True

    def visitStringtype(self, ctx:PascalParser.StringtypeContext):
        self.visit(ctx.getChild(2))
        ctx.customContext = EmbeddedTypes.StringType(length=ctx.getChild(2).customContext)
        return True

    def visitArrayType(self, ctx:PascalParser.ArrayTypeContext):
        self.visit(ctx.typeList())
        self.visit(ctx.componentType())
        ctx.customContext = EmbeddedTypes.ArrayType(subranges=ctx.typeList().customContext,
                                                    typ_val=ctx.componentType().customContext)
        return True

    def visitTypeList(self, ctx:PascalParser.TypeListContext):
        self.visitChildren(ctx)
        ctx.customContext = []
        for typ in ctx.indexType():
            ctx.customContext.append(typ.customContext)
        return True

    def visitIndexType(self, ctx:PascalParser.IndexTypeContext):
        self.visit(ctx.simpleType())
        ctx.customContext = ctx.simpleType().customContext
        if ctx.customContext.get_type() != ir_builder.context.EmbeddedTypesEnum.SUBRANGE:
            raise CompileException(f"Invalid index type: {ir_builder.context.EmbeddedTypesEnum.SUBRANGE} expected but {ctx.customContext.get_type()} got")
        return True

    def visitComponentType(self, ctx:PascalParser.ComponentTypeContext):
        self.visitChildren(ctx)
        ctx.customContext = ctx.type_().customContext
        return True

    def visitRecordType(self, ctx:PascalParser.RecordTypeContext):
        if ctx.fieldList():
            self.visit(ctx.fieldList())
            ctx.customContext = EmbeddedTypes.RecordType(field_list=ctx.fieldList().customContext)
        else:
            ctx.customContext = EmbeddedTypes.RecordType()
        return True

    def visitFieldList(self, ctx:PascalParser.FieldListContext):
        self.visit(ctx.fixedPart())
        ctx.customContext = ctx.fixedPart().customContext
        return True

    def visitFixedPart(self, ctx:PascalParser.FixedPartContext):
        ctx.customContext = []
        for section in ctx.recordSection():
            self.visit(section)
            ctx.customContext += section.customContext
        return True

    def visitRecordSection(self, ctx:PascalParser.RecordSectionContext):
        self.visit(ctx.identifierList())
        self.visit(ctx.type_())

        ctx.customContext = []
        type_ = ctx.type_().customContext
        for ident in ctx.identifierList().customContext:
            ctx.customContext.append(Constructs.Variable(ident=ident, typ=type_))
        return True

    def visitVariantPart(self, ctx:PascalParser.VariantPartContext):
        raise CompileException("Invalid syntax")

    def visitTag(self, ctx:PascalParser.TagContext):
        raise CompileException("Invalid syntax")

    def visitVariant(self, ctx:PascalParser.VariantContext):
        raise CompileException("Invalid syntax")

    def visitSetType(self, ctx:PascalParser.SetTypeContext):
        raise CompileException("Invalid syntax")

    def visitBaseType(self, ctx:PascalParser.BaseTypeContext):
        self.visitChildren(ctx)
        ctx.customContext = ctx.simpleType().customContext
        return True

    def visitFileType(self, ctx:PascalParser.FileTypeContext):
        raise CompileException("Invalid syntax")

    def visitPointerType(self, ctx:PascalParser.PointerTypeContext):
        self.visit(ctx.typeIdentifier())
        ctx.customContext = EmbeddedTypes.PointerType(type_ident=ctx.typeIdentifier().customContext)
        return True

    def visitVariableDeclarationPart(self, ctx:PascalParser.VariableDeclarationPartContext):
        self.visitChildren(ctx)
        for variables in ctx.variableDeclaration():
            for var in variables.customContext:
                ctx.parentCtx.customContext.define_variable(var)
        return True

    def visitVariableDeclaration(self, ctx:PascalParser.VariableDeclarationContext):
        self.visit(ctx.identifierList())
        self.visit(ctx.type_())
        ident_list = ctx.identifierList().customContext
        type_ = ctx.type_().customContext
        ctx.customContext = []
        for ident in ident_list:
            ctx.customContext.append(Constructs.Variable(ident=ident, typ=type_))
        return True

    # Visit a parse tree produced by PascalParser#procedureAndFunctionDeclarationPart.
    def visitProcedureAndFunctionDeclarationPart(self, ctx:PascalParser.ProcedureAndFunctionDeclarationPartContext):
        ctx.customContext = ctx.parentCtx.customContext
        for fop in ctx.children:
            self.visit(fop)
        return True

    # Visit a parse tree produced by PascalParser#procedureOrFunctionDeclaration.
    def visitProcedureOrFunctionDeclaration(self, ctx:PascalParser.ProcedureOrFunctionDeclarationContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visitChildren(ctx)
        return True

    def visitProcedureDeclaration(self, ctx:PascalParser.ProcedureDeclarationContext):
        context:ModuleContext = ctx.parentCtx.customContext
        self.visit(ctx.identifier())
        proc_name = ctx.identifier().customContext
        if ctx.formalParameterList():
            self.visitFormalParameterList(ctx.formalParameterList())
            params = ctx.formalParameterList().customContext
        else:
            params = []
        proc = context.define_procedure(args=params,
                                        name=proc_name)
        ctx.customContext = proc.local_ctx
        self.visitBlock(ctx.block())
        return True

    def visitFormalParameterList(self, ctx:PascalParser.FormalParameterListContext):
        ctx.customContext = []
        for section in ctx.formalParameterSection():
            self.visit(section)
            ctx.customContext += section.customContext
        return True

    def visitFormalParameterSection(self, ctx:PascalParser.FormalParameterSectionContext):
        if ctx.getChildCount() > 1:
            raise CompileException("Invalid syntax")
        self.visit(ctx.parameterGroup())
        ctx.customContext = ctx.parameterGroup().customContext
        return True

    def visitParameterGroup(self, ctx:PascalParser.ParameterGroupContext):
        self.visit(ctx.identifierList())
        self.visit(ctx.typeIdentifier())
        ctx.customContext = []
        type_ = ctx.typeIdentifier().customContext
        tmp = ctx.identifierList()
        for ident in ctx.identifierList().customContext:
            ctx.customContext.append(Constructs.Variable(ident=ident, typ=type_))
        return True

    def visitIdentifierList(self, ctx:PascalParser.IdentifierListContext):
        self.visitChildren(ctx)
        ctx.customContext = []
        for ident in ctx.identifier():
            ctx.customContext.append(ident.customContext)
        return True

    # Visit a parse tree produced by PascalParser#constList.
    def visitConstList(self, ctx:PascalParser.ConstListContext):
        return self.visitChildren(ctx)

    def visitFunctionDeclaration(self, ctx:PascalParser.FunctionDeclarationContext):
        context:ModuleContext = ctx.parentCtx.customContext
        self.visit(ctx.identifier())
        proc_name = ctx.identifier().customContext
        if ctx.formalParameterList():
            self.visitFormalParameterList(ctx.formalParameterList())
            params = ctx.formalParameterList().customContext
        else:
            params = []
        self.visitResultType(ctx.resultType())
        res_type = ctx.resultType().customContext   # .get_instr(context)
        func = context.define_function(return_type=res_type,
                                       args=params,
                                       name=proc_name)
        ctx.customContext = func.local_ctx
        self.visitBlock(ctx.block())
        return True

    def visitResultType(self, ctx:PascalParser.ResultTypeContext):
        self.visit(ctx.typeIdentifier())
        ctx.customContext = ctx.typeIdentifier().customContext
        return True

    def visitStatement(self, ctx:PascalParser.StatementContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.unlabelledStatement())
        if ctx.label():
            pass                    # добавить label в модуль!!!
        return True

    def visitUnlabelledStatement(self, ctx:PascalParser.UnlabelledStatementContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.getChild(0))
        return True

    def visitSimpleStatement(self, ctx:PascalParser.SimpleStatementContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.getChild(0))
        return True

    def visitAssignmentStatement(self, ctx:PascalParser.AssignmentStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.variable())
        self.visit(ctx.expression())
        var:Constructs.Value = ctx.variable().customContext
        val:Constructs.Value = ctx.expression().customContext
        if var.instruct.type != val.instruct.type:
            if var.instruct.type == ir.IntType(64) and val.instruct.type == ir.DoubleType():
                val.instruct = context.get_ir_builder().fptosi(val.instruct, ir.IntType(64))
            elif val.instruct.type == ir.IntType(64) and var.instruct.type == ir.DoubleType():
                val.instruct = context.get_ir_builder().sitofp(val.instruct, ir.DoubleType())
            else:
                val.instruct = context.get_ir_builder().bitcast(val.instruct, var.instruct.type)

        context.get_ir_builder().store(val.instruct, var.parent_instruct)
        return True

    def visitVariable(self, ctx:PascalParser.VariableContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visitChildren(ctx)
        zero = ir.Constant(ir.IntType(32), 0)
        indices = []
        var = None
        typ_val = None
        try:
            idx = 0
            while idx < ctx.getChildCount():
                if ctx.getChild(idx) in ctx.identifier():
                    indices += [zero]
                    var:Constructs.Const = context.get_var_by_ident(ident=ctx.getChild(idx).customContext,
                                                                    search_scopes=[Scopes.VARS, Scopes.CONSTS])
                    if not var:
                        func:Constructs.ProcedureOrFunction = context.get_var_by_ident(ident=ctx.getChild(idx).customContext,
                                                                                      search_scopes=[Scopes.FUNCTIONS])
                        ctx.customContext = context.call_func(func, params=[])
                        return True
                    typ_val:typing.Type[EmbeddedTypes.AbstractType] = var.typ.typ_val
                    parent_alloca_instruct = var.instruct
                elif ctx.getChild(idx) in ctx.DOT():
                    idx += 1
                    ident = ctx.getChild(idx).customContext
                    indices.append(ir.Constant(ir.IntType(32), typ_val.field_indexes[ident]))
                    typ_val = typ_val.fields[ident].typ.typ_val
                elif ctx.getChild(idx) in ctx.POINTER():
                    ptr = context.get_ir_builder().gep(var.instruct, indices)
                    var = Constructs.Value(typ=None, val=None, instruct=context.get_ir_builder().load(ptr))
                    typ_val = context.get_var_by_ident(typ_val.typ.typ_ident, search_scopes=[Scopes.TYPES]).typ_val
                    indices = [zero]
                elif ctx.getChild(idx) in ctx.LBRACK() or ctx.getChild(idx) in ctx.LBRACK2():
                    index = 0
                    idx += 1
                    while ctx.getChild(idx + 1) in ctx.COMMA() \
                            or ctx.getChild(idx + 2) in ctx.LBRACK() \
                            or ctx.getChild(idx + 2) in ctx.LBRACK2():
                        v = ctx.getChild(idx).customContext
                        index_val = context.get_ir_builder().sub(v.instruct, typ_val.subranges[index].load_dim_val(context))        # load(context)
                        indices.append(index_val)    # v.load(context)
                        if ctx.getChild(idx + 1) in ctx.COMMA():
                            idx += 2
                        else:
                            idx += 3
                        if index >= len(typ_val.subranges):
                            typ_val = typ_val.typ.typ_val
                            index = 0
                        else:
                            index += 1
                    v = ctx.getChild(idx).customContext
                    index_val = context.get_ir_builder().sub(v.instruct, typ_val.subranges[index].load_dim_val(context))    # load(context)
                    indices.append(index_val)       # v.load(context)
                idx += 1
            ctx.customContext = Constructs.Value(typ=None, val=None,
                                                 instruct=context.get_ir_builder().gep(ptr=var.instruct, indices=indices))
            ctx.customContext.parent_instruct = ctx.customContext.instruct
            ctx.customContext.parent_alloca_instruct = parent_alloca_instruct
            if not ctx.AT():
               ctx.customContext.instruct = context.get_ir_builder().load(ctx.customContext.instruct)     # ctx.customContext.is_ptr = True
        except Exception as e:
            print(e)
            print(e.args)
            raise CompileException(f"Variable getting error")
        return True

    def visitExpression(self, ctx:PascalParser.ExpressionContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.simpleExpression())
        if ctx.relationaloperator():
            self.visit(ctx.relationaloperator())
            self.visit(ctx.expression())
            op1 = ctx.simpleExpression().customContext
            op2 = ctx.expression().customContext
            operator = ctx.relationaloperator().customContext
            ctx.customContext = VarUtils.relOperCalc(op1, op2, operator, context)
        else:
            ctx.customContext = ctx.simpleExpression().customContext
        return True

    def visitRelationaloperator(self, ctx:PascalParser.RelationaloperatorContext):
        self.visit(ctx.getChild(0))
        ctx.customContext = ctx.getChild(0).symbol.text
        return True

    def visitSimpleExpression(self, ctx:PascalParser.SimpleExpressionContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.term())
        if ctx.additiveoperator():
            self.visit(ctx.additiveoperator())
            self.visit(ctx.simpleExpression())
            op1 = ctx.term().customContext
            op2 = ctx.simpleExpression().customContext
            operator = ctx.additiveoperator().customContext
            ctx.customContext = VarUtils.addOperCalc(op1, op2, operator, context)
        else:
            ctx.customContext = ctx.term().customContext
        return True

    def visitAdditiveoperator(self, ctx:PascalParser.AdditiveoperatorContext):
        self.visit(ctx.getChild(0))
        ctx.customContext = ctx.getChild(0).symbol.text
        return True

    def visitTerm(self, ctx:PascalParser.TermContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.signedFactor())
        if ctx.multiplicativeoperator():
            self.visit(ctx.multiplicativeoperator())
            self.visit(ctx.term())
            op1 = ctx.signedFactor().customContext
            op2 = ctx.term().customContext
            operator = ctx.multiplicativeoperator().customContext
            ctx.customContext = VarUtils.mulOperCalc(op1, op2, operator, context)
        else:
            ctx.customContext = ctx.signedFactor().customContext
        return True

    def visitMultiplicativeoperator(self, ctx:PascalParser.MultiplicativeoperatorContext):
        self.visit(ctx.getChild(0))
        ctx.customContext = ctx.getChild(0).symbol.text
        return True

    def visitSignedFactor(self, ctx:PascalParser.SignedFactorContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.factor())
        ctx.customContext = ctx.factor().customContext
        if ctx.PLUS():
            pass
        elif ctx.MINUS():
            ctx.customContext = VarUtils.inverse(ctx.customContext, context)
        return True

    # set_ not AC
    def visitFactor(self, ctx:PascalParser.FactorContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visitChildren(ctx)
        if ctx.bool_():
            ctx.customContext = ctx.bool_().customContext
            val:Constructs.Value = ctx.customContext
            val.typ = context.create_type(EmbeddedTypes.CustomType(ident=val.typ.typ_ident, typ_val=val.typ))
            v = ir.GlobalVariable(context.get_module(), val.instruct.type, name=EmbeddedTypes.get_unique_ident("literal"))
            v.initializer = val.instruct
            val.instruct = v
            val.instruct = context.get_ir_builder().load(val.instruct)
        elif ctx.NOT():
            ctx.customContext = VarUtils.not_(ctx.factor().customContext, context)
        elif ctx.set_():
            ctx.customContext = ctx.set_().customContext
        elif ctx.unsignedConstant():
            ctx.customContext = ctx.unsignedConstant().customContext
        elif ctx.functionDesignator():
            ctx.customContext = ctx.functionDesignator().customContext
        elif ctx.expression():
            ctx.customContext = ctx.expression().customContext
        elif ctx.variable():
            ctx.customContext = ctx.variable().customContext
        return True

    def visitUnsignedConstant(self, ctx:PascalParser.UnsignedConstantContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        self.visit(ctx.getChild(0))
        if ctx.NIL():
            ctx.customContext = Constructs.Value(typ=None,
                                                 val=None,
                                                 instruct=ir.Constant(ir.PointerType(ir.IntType(1)), None))
        else:
            ctx.customContext = ctx.getChild(0).customContext
            val:Constructs.Value = ctx.customContext
            val.typ = context.create_type(EmbeddedTypes.CustomType(ident=val.typ.typ_ident, typ_val=val.typ))

            if val.typ.ident == TypesEnum.STRING:
                v = ir.GlobalVariable(context.get_module(), val.instruct.type, name=EmbeddedTypes.get_unique_ident("literal"))
                v.initializer = val.instruct

                val.instruct = ir.GlobalVariable(context.get_module(), val.typ.instruct, name=EmbeddedTypes.get_unique_ident("literal_ptr"))
                val.instruct.initializer = ir.Constant(val.typ.instruct, None)
                zero = ir.Constant(ir.IntType(32), 0)
                context.get_ir_builder().store(v.gep(indices=[zero, zero]), val.instruct)

                val.instruct = context.get_ir_builder().load(val.instruct)
        return True

    def visitFunctionDesignator(self, ctx:PascalParser.FunctionDesignatorContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.identifier())
        self.visit(ctx.parameterList())
        params = ctx.parameterList().customContext
        func_name:str = ctx.identifier().customContext
        func = context.get_var_by_ident(ident=func_name, search_scopes=[Scopes.FUNCTIONS])
        if not func:
            raise CompileException(f"No such function {func_name}")
        ctx.customContext = context.call_func(func, params)
        return True

    def visitParameterList(self, ctx:PascalParser.ParameterListContext):
        ctx.customContext = ctx.parentCtx.customContext
        params = []
        for param in ctx.actualParameter():
            self.visit(param)
            params.append(param.customContext)
        ctx.customContext = params
        return True

    # Visit a parse tree produced by PascalParser#set_.
    def visitSet_(self, ctx:PascalParser.Set_Context):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.elementList())
        ctx.customContext = ctx.elementList().customContext
        return True

    # Visit a parse tree produced by PascalParser#elementList.
    def visitElementList(self, ctx:PascalParser.ElementListContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        elems = []
        for elem in ctx.element():
            self.visit(elem)
            elems.append(elem.customContext)
        ctx.customContext = elems
        return True

    # Visit a parse tree produced by PascalParser#element.
    def visitElement(self, ctx:PascalParser.ElementContext):
        if ctx.DOTDOT():
            raise CompileException(f"Element of array have to be literal or const")
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.expression())
        ctx.customContext = ctx.expression().customContext
        return True

    def visitProcedureStatement(self, ctx:PascalParser.ProcedureStatementContext):
        ctx.customContext = ctx.parentCtx.customContext
        context:Union[ModuleContext, ProcedureContext] = ctx.customContext
        self.visit(ctx.identifier())
        func_name:str = ctx.identifier().customContext
        if ctx.parameterList():
            self.visit(ctx.parameterList())
            params = ctx.parameterList().customContext
        else:
            if func_name == "exit":
                if context.type() == "procedure":
                    context.finish_func()
                else:
                    context.finish_main()
                return True
            params = []
        proc = context.get_var_by_ident(ident=func_name, search_scopes=[Scopes.FUNCTIONS, Scopes.PROCEDURES])
        if not proc:
            raise CompileException(f"No such procedure or function {func_name}")
        context.call_func(proc, params)
        return True

    # ???
    def visitActualParameter(self, ctx:PascalParser.ActualParameterContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.expression())
        if ctx.parameterwidth():
            for w in ctx.parameterwidth():
                self.visit(w)
        ctx.customContext = ctx.expression().customContext
        return True

    # ???
    def visitParameterwidth(self, ctx:PascalParser.ParameterwidthContext):
        ctx.customContext = ctx.parentCtx.customContext
        if ctx.expression():
            self.visit(ctx.expression())
        return True

    # Visit a parse tree produced by PascalParser#gotoStatement.
    def visitGotoStatement(self, ctx:PascalParser.GotoStatementContext):
        return self.visitChildren(ctx)

    def visitEmptyStatement_(self, ctx:PascalParser.EmptyStatement_Context):
        return True

    def visitEmpty_(self, ctx:PascalParser.Empty_Context):
        return True

    def visitStructuredStatement(self, ctx:PascalParser.StructuredStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.getChild(0))
        return True

    def visitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.getChild(1))
        return True

    def visitStatements(self, ctx:PascalParser.StatementsContext):
        ctx.customContext = ctx.parentCtx.customContext
        for st in ctx.statement():
            self.visit(st)
        return True

    def visitConditionalStatement(self, ctx:PascalParser.ConditionalStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.getChild(0))
        return True

    def visitIfStatement(self, ctx:PascalParser.IfStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.expression())
        pred = ctx.expression().customContext.instruct

        if ctx.ELSE():
            with context.get_ir_builder().if_else(pred) as (then, otherwise):
                with then:
                    self.visit(ctx.statement()[0])
                with otherwise:
                    self.visit(ctx.statement()[1])
        else:
            with context.get_ir_builder().if_then(pred):
                self.visit(ctx.statement()[0])

        return True

    # Visit a parse tree produced by PascalParser#caseStatement.
    def visitCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#caseListElement.
    def visitCaseListElement(self, ctx:PascalParser.CaseListElementContext):
        return self.visitChildren(ctx)

    def visitRepetetiveStatement(self, ctx:PascalParser.RepetetiveStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.getChild(0))
        return True

    def visitWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        bbcond = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('cond'))
        bbwhile = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('while'))
        bbafter = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('after'))

        context.get_ir_builder().branch(bbcond)
        context.get_ir_builder().position_at_start(bbcond)
        self.visit(ctx.expression())
        pred = ctx.expression().customContext.instruct
        context.get_ir_builder().cbranch(pred, bbwhile, bbafter)

        context.get_ir_builder().position_at_start(bbwhile)
        self.visit(ctx.statement())
        context.get_ir_builder().branch(bbcond)
        context.get_ir_builder().position_at_start(bbafter)
        return True

    # Visit a parse tree produced by PascalParser#repeatStatement.
    def visitRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        bbrepeat = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('repeat'))
        bbuntil = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('until'))
        bbafter = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('after'))

        context.get_ir_builder().branch(bbrepeat)
        context.get_ir_builder().position_at_start(bbrepeat)
        self.visit(ctx.statements())

        context.get_ir_builder().branch(bbuntil)
        context.get_ir_builder().position_at_start(bbuntil)
        self.visit(ctx.expression())
        pred = VarUtils.not_(ctx.expression().customContext, context).instruct
        context.get_ir_builder().cbranch(pred, bbrepeat, bbafter)
        context.get_ir_builder().position_at_start(bbafter)
        return True

    # Visit a parse tree produced by PascalParser#forStatement.
    def visitForStatement(self, ctx:PascalParser.ForStatementContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        bbprepare = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('prepare_for'))
        bbcond = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('cond'))
        bbfor = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('for'))
        bbafter = context.get_ir_builder().append_basic_block(name=EmbeddedTypes.get_unique_ident('after'))

        context.get_ir_builder().branch(bbprepare)
        context.get_ir_builder().position_at_start(bbprepare)
        self.visit(ctx.identifier())
        ident = ctx.identifier().customContext
        var_iterator = context.get_var_by_ident(ident=ident, search_scopes=[Scopes.VARS])
        v = Constructs.Value(typ=None, val=None)
        v.parent_instruct = var_iterator.instruct
        backup, var_iterator = var_iterator, v

        self.visit(ctx.forList())
        init_val:Constructs.Value = ctx.forList().customContext[0]
        final_val:Constructs.Value = ctx.forList().customContext[1]
        step:Constructs.Value = ctx.forList().customContext[2]
        zero_val = Constructs.Value(typ=None, val=None, instruct=ir.Constant(ir.IntType(64), 0))
        #context.vars.pop(ident)     # удаляем переменную, выбранною в качестве счетчика перед циклом
        context.get_ir_builder().store(init_val.instruct, var_iterator.parent_instruct)

        v1 = VarUtils.lt_le_gt_ge(init_val, final_val, '<=', context)
        v2 = VarUtils.lt_le_gt_ge(step, zero_val, '>', context)
        v3 = VarUtils.lt_le_gt_ge(init_val, final_val, '>=', context)
        v4 = VarUtils.lt_le_gt_ge(step, zero_val, '<', context)
        v5 = VarUtils.and_(v1, v2, context)
        v6 = VarUtils.and_(v3, v4, context)
        prep_cond = VarUtils.or_(v5, v6, context)
        context.get_ir_builder().cbranch(prep_cond.instruct, bbcond, bbafter)

        context.get_ir_builder().position_at_start(bbcond)
        var_iterator.instruct = context.get_ir_builder().load(var_iterator.parent_instruct)
        cond = VarUtils.lt_le_gt_ge(var_iterator, final_val, '<=', context)
        context.get_ir_builder().cbranch(cond.instruct, bbfor, bbafter)

        context.get_ir_builder().position_at_start(bbfor)
        self.visit(ctx.statement())
        new_val_iter = VarUtils.plus(var_iterator, step, context)
        context.get_ir_builder().store(new_val_iter.instruct, var_iterator.parent_instruct)
        context.get_ir_builder().branch(bbcond)

        context.get_ir_builder().position_at_start(bbafter)
        #context.vars[ident] = backup     # возвращаем переменную-счетчик обратно после выхода из цикла
        return True

    def visitForList(self, ctx:PascalParser.ForListContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.initialValue())
        self.visit(ctx.finalValue())
        step = 1 if ctx.TO() else -1
        step = ir.Constant(ir.IntType(64), step)
        step = Constructs.Value(typ=None, val=None, instruct=step)
        ctx.customContext = [ctx.initialValue().customContext, ctx.finalValue().customContext, step]
        return True

    def visitInitialValue(self, ctx:PascalParser.InitialValueContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.expression())
        ctx.customContext = ctx.expression().customContext
        return True

    def visitFinalValue(self, ctx:PascalParser.FinalValueContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visit(ctx.expression())
        ctx.customContext = ctx.expression().customContext
        return True

    # Visit a parse tree produced by PascalParser#withStatement.
    def visitWithStatement(self, ctx:PascalParser.WithStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#recordVariableList.
    def visitRecordVariableList(self, ctx:PascalParser.RecordVariableListContext):
        return self.visitChildren(ctx)
