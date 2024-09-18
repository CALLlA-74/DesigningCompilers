import ir_builder.context
from typing import Union
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
        self.visitChildren(ctx)
        for const in ctx.constantDefinition():
            ctx.parentCtx.customContext.define_constant(const.customContext)
        return True

    def visitConstantDefinition(self, ctx:PascalParser.ConstantDefinitionContext):
        self.visitChildren(ctx)
        constant = ctx.constant().customContext
        ctx.customContext = Constructs.Const(ident=ctx.identifier().customContext,
                                             typ=constant.typ,
                                             val=constant.val,
                                             sign=constant.sign)
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
        elif ctx.getChild(0) == ctx.sign() and ctx.getChild(0) == ctx.unsignedNumber():
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
        ctx.customContext = Constructs.Value(typ=typ, val=s[1:len(s) - 1])
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
        proc = context.define_function(return_type=ir.VoidType(),
                                args=params,
                                name=proc_name)
        ctx.customContext = proc.local_ctx
        # подумать над рекурсивными вызовами: в этом случае контекст функции/процедуры должен заново пересоздаваться
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
        res_type = ctx.resultType().customContext.get_instr(context)
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

    # Visit a parse tree produced by PascalParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:PascalParser.AssignmentStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#variable.
    def visitVariable(self, ctx:PascalParser.VariableContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context
        self.visitChildren(ctx.getChildren())



        return True

    # Visit a parse tree produced by PascalParser#expression.
    def visitExpression(self, ctx:PascalParser.ExpressionContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.simpleExpression())
        if ctx.relationaloperator():
            self.visit(ctx.relationaloperator())
            self.visit(ctx.expression())
        ctx.customContext = ctx.simpleExpression().customContext
        return True

    # Visit a parse tree produced by PascalParser#relationaloperator.
    def visitRelationaloperator(self, ctx:PascalParser.RelationaloperatorContext):
        return self.visitChildren(ctx)

    def visitSimpleExpression(self, ctx:PascalParser.SimpleExpressionContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.term())
        if ctx.additiveoperator():
            self.visit(ctx.additiveoperator())
            self.visit(ctx.simpleExpression())
        ctx.customContext = ctx.term().customContext
        return True

    # Visit a parse tree produced by PascalParser#additiveoperator.
    def visitAdditiveoperator(self, ctx:PascalParser.AdditiveoperatorContext):
        return self.visitChildren(ctx)

    def visitTerm(self, ctx:PascalParser.TermContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.signedFactor())
        if ctx.multiplicativeoperator():
            self.visit(ctx.multiplicativeoperator())
            self.visit(ctx.term())
        ctx.customContext = ctx.signedFactor().customContext
        return True

    # Visit a parse tree produced by PascalParser#multiplicativeoperator.
    def visitMultiplicativeoperator(self, ctx:PascalParser.MultiplicativeoperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#signedFactor.
    def visitSignedFactor(self, ctx:PascalParser.SignedFactorContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visit(ctx.factor())
        if ctx.PLUS():
            pass
        elif ctx.MINUS():
            pass
        ctx.customContext = ctx.factor().customContext
        return True

    def visitFactor(self, ctx:PascalParser.FactorContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        ctx.customContext = context

        self.visitChildren(ctx)
        if ctx.bool_():
            ctx.customContext = ctx.bool_().customContext
            val:Constructs.Value = ctx.customContext
            val.typ = context.create_type(EmbeddedTypes.CustomType(ident=val.typ.typ_ident, typ_val=val.typ))
        elif ctx.NOT():
            ctx.customContext = VarUtils.not_(ctx.factor().customContext, context)    # context.get_ir_builder().not_(ctx.factor().customContext)
        elif ctx.set_():
            ctx.customContext = ctx.set_().customContext
        elif ctx.unsignedConstant():
            ctx.customContext = ctx.unsignedConstant().customContext
        elif ctx.functionDesignator():
            pass
        elif ctx.expression():
            pass
        elif ctx.variable():
            pass
        return True

    def visitUnsignedConstant(self, ctx:PascalParser.UnsignedConstantContext):
        context:Union[ModuleContext, ProcedureContext] = ctx.parentCtx.customContext
        self.visit(ctx.getChild(0))
        if ctx.NIL():
            ctx.customContext = Constructs.Value(typ=None,
                                                 val=None,
                                                 instruct=ir.Constant(ir.IntType(1), None))
        else:
            ctx.customContext = ctx.getChild(0).customContext
            val:Constructs.Value = ctx.customContext
            val.typ = context.create_type(EmbeddedTypes.CustomType(ident=val.typ.typ_ident, typ_val=val.typ))
            #
            v = ir.GlobalVariable(context.module, val.instruct.type, name=EmbeddedTypes.get_unique_ident("literal"))
            v.initializer = val.instruct

            if val.typ.ident == TypesEnum.STRING:
                val.instruct = ir.GlobalVariable(context.module, val.typ.instruct, name=EmbeddedTypes.get_unique_ident("literal_ptr"))
                val.instruct.initializer = ir.Constant(val.typ.instruct, None)
                zero = ir.Constant(ir.IntType(32), 0)
                context.get_ir_builder().store(v.gep(indices=[zero, zero]), val.instruct)
            else:
                val.instruct = v

            val.instruct = context.get_ir_builder().load(val.instruct)     # ??? not sure
        return True

    # Visit a parse tree produced by PascalParser#functionDesignator.
    def visitFunctionDesignator(self, ctx:PascalParser.FunctionDesignatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#parameterList.
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
            params = []
        proc = context.get_var_by_ident(ident=func_name, search_scopes=[Scopes.FUNCTIONS, Scopes.PROCEDURES])
        if not proc:
            raise CompileException(f"No such procedure or function {func_name}")
        context.call_func(proc, params)
        return True

    def visitActualParameter(self, ctx:PascalParser.ActualParameterContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.expression())
        if ctx.parameterwidth():
            for w in ctx.parameterwidth():
                self.visit(w)
        ctx.customContext = ctx.expression().customContext
        return True

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

    # Visit a parse tree produced by PascalParser#empty_.
    def visitEmpty_(self, ctx:PascalParser.Empty_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#structuredStatement.
    def visitStructuredStatement(self, ctx:PascalParser.StructuredStatementContext):
        return self.visitChildren(ctx)

    def visitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        ctx.customContext = ctx.parentCtx.customContext
        self.visit(ctx.getChild(1))
        return True

    def visitStatements(self, ctx:PascalParser.StatementsContext):
        ctx.customContext = ctx.parentCtx.customContext
        for st in ctx.statement():
            self.visit(st)
        return True

    # Visit a parse tree produced by PascalParser#conditionalStatement.
    def visitConditionalStatement(self, ctx:PascalParser.ConditionalStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#ifStatement.
    def visitIfStatement(self, ctx:PascalParser.IfStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#caseStatement.
    def visitCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#caseListElement.
    def visitCaseListElement(self, ctx:PascalParser.CaseListElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#repetetiveStatement.
    def visitRepetetiveStatement(self, ctx:PascalParser.RepetetiveStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#whileStatement.
    def visitWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#repeatStatement.
    def visitRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#forStatement.
    def visitForStatement(self, ctx:PascalParser.ForStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#forList.
    def visitForList(self, ctx:PascalParser.ForListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#initialValue.
    def visitInitialValue(self, ctx:PascalParser.InitialValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#finalValue.
    def visitFinalValue(self, ctx:PascalParser.FinalValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#withStatement.
    def visitWithStatement(self, ctx:PascalParser.WithStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PascalParser#recordVariableList.
    def visitRecordVariableList(self, ctx:PascalParser.RecordVariableListContext):
        return self.visitChildren(ctx)
