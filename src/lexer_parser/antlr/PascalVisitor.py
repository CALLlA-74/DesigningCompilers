# Generated from Pascal.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PascalParser import PascalParser
else:
    from PascalParser import PascalParser

# This class defines a complete generic visitor for a parse tree produced by PascalParser.

class PascalVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PascalParser#program.
    def visitProgram(self, ctx:PascalParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#programHeading.
    def visitProgramHeading(self, ctx:PascalParser.ProgramHeadingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#identifier.
    def visitIdentifier(self, ctx:PascalParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#block.
    def visitBlock(self, ctx:PascalParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#usesUnitsPart.
    def visitUsesUnitsPart(self, ctx:PascalParser.UsesUnitsPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#labelDeclarationPart.
    def visitLabelDeclarationPart(self, ctx:PascalParser.LabelDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#label.
    def visitLabel(self, ctx:PascalParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constantDefinitionPart.
    def visitConstantDefinitionPart(self, ctx:PascalParser.ConstantDefinitionPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constantDefinition.
    def visitConstantDefinition(self, ctx:PascalParser.ConstantDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constantChr.
    def visitConstantChr(self, ctx:PascalParser.ConstantChrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constant.
    def visitConstant(self, ctx:PascalParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unsignedNumber.
    def visitUnsignedNumber(self, ctx:PascalParser.UnsignedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unsignedInteger.
    def visitUnsignedInteger(self, ctx:PascalParser.UnsignedIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unsignedReal.
    def visitUnsignedReal(self, ctx:PascalParser.UnsignedRealContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#sign.
    def visitSign(self, ctx:PascalParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#bool_.
    def visitBool_(self, ctx:PascalParser.Bool_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#string.
    def visitString(self, ctx:PascalParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeDefinitionPart.
    def visitTypeDefinitionPart(self, ctx:PascalParser.TypeDefinitionPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeDefinition.
    def visitTypeDefinition(self, ctx:PascalParser.TypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionType.
    def visitFunctionType(self, ctx:PascalParser.FunctionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureType.
    def visitProcedureType(self, ctx:PascalParser.ProcedureTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#type_.
    def visitType_(self, ctx:PascalParser.Type_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#simpleType.
    def visitSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#scalarType.
    def visitScalarType(self, ctx:PascalParser.ScalarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#subrangeType.
    def visitSubrangeType(self, ctx:PascalParser.SubrangeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:PascalParser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#structuredType.
    def visitStructuredType(self, ctx:PascalParser.StructuredTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unpackedStructuredType.
    def visitUnpackedStructuredType(self, ctx:PascalParser.UnpackedStructuredTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#stringtype.
    def visitStringtype(self, ctx:PascalParser.StringtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayType.
    def visitArrayType(self, ctx:PascalParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeList.
    def visitTypeList(self, ctx:PascalParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#indexType.
    def visitIndexType(self, ctx:PascalParser.IndexTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#componentType.
    def visitComponentType(self, ctx:PascalParser.ComponentTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#recordType.
    def visitRecordType(self, ctx:PascalParser.RecordTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#fieldList.
    def visitFieldList(self, ctx:PascalParser.FieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#fixedPart.
    def visitFixedPart(self, ctx:PascalParser.FixedPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#recordSection.
    def visitRecordSection(self, ctx:PascalParser.RecordSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variantPart.
    def visitVariantPart(self, ctx:PascalParser.VariantPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#tag.
    def visitTag(self, ctx:PascalParser.TagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variant.
    def visitVariant(self, ctx:PascalParser.VariantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#setType.
    def visitSetType(self, ctx:PascalParser.SetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#baseType.
    def visitBaseType(self, ctx:PascalParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#fileType.
    def visitFileType(self, ctx:PascalParser.FileTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#pointerType.
    def visitPointerType(self, ctx:PascalParser.PointerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variableDeclarationPart.
    def visitVariableDeclarationPart(self, ctx:PascalParser.VariableDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:PascalParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureAndFunctionDeclarationPart.
    def visitProcedureAndFunctionDeclarationPart(self, ctx:PascalParser.ProcedureAndFunctionDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureOrFunctionDeclaration.
    def visitProcedureOrFunctionDeclaration(self, ctx:PascalParser.ProcedureOrFunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureDeclaration.
    def visitProcedureDeclaration(self, ctx:PascalParser.ProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#formalParameterList.
    def visitFormalParameterList(self, ctx:PascalParser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#formalParameterSection.
    def visitFormalParameterSection(self, ctx:PascalParser.FormalParameterSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#parameterGroup.
    def visitParameterGroup(self, ctx:PascalParser.ParameterGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#identifierList.
    def visitIdentifierList(self, ctx:PascalParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constList.
    def visitConstList(self, ctx:PascalParser.ConstListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:PascalParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#resultType.
    def visitResultType(self, ctx:PascalParser.ResultTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#statement.
    def visitStatement(self, ctx:PascalParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unlabelledStatement.
    def visitUnlabelledStatement(self, ctx:PascalParser.UnlabelledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#simpleStatement.
    def visitSimpleStatement(self, ctx:PascalParser.SimpleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:PascalParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variable.
    def visitVariable(self, ctx:PascalParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#expression.
    def visitExpression(self, ctx:PascalParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#relationaloperator.
    def visitRelationaloperator(self, ctx:PascalParser.RelationaloperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#simpleExpression.
    def visitSimpleExpression(self, ctx:PascalParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#additiveoperator.
    def visitAdditiveoperator(self, ctx:PascalParser.AdditiveoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#term.
    def visitTerm(self, ctx:PascalParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#multiplicativeoperator.
    def visitMultiplicativeoperator(self, ctx:PascalParser.MultiplicativeoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#signedFactor.
    def visitSignedFactor(self, ctx:PascalParser.SignedFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#factor.
    def visitFactor(self, ctx:PascalParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unsignedConstant.
    def visitUnsignedConstant(self, ctx:PascalParser.UnsignedConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionDesignator.
    def visitFunctionDesignator(self, ctx:PascalParser.FunctionDesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#parameterList.
    def visitParameterList(self, ctx:PascalParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#set_.
    def visitSet_(self, ctx:PascalParser.Set_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#elementList.
    def visitElementList(self, ctx:PascalParser.ElementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#element.
    def visitElement(self, ctx:PascalParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureStatement.
    def visitProcedureStatement(self, ctx:PascalParser.ProcedureStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#actualParameter.
    def visitActualParameter(self, ctx:PascalParser.ActualParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#parameterwidth.
    def visitParameterwidth(self, ctx:PascalParser.ParameterwidthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#gotoStatement.
    def visitGotoStatement(self, ctx:PascalParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#emptyStatement_.
    def visitEmptyStatement_(self, ctx:PascalParser.EmptyStatement_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#empty_.
    def visitEmpty_(self, ctx:PascalParser.Empty_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#structuredStatement.
    def visitStructuredStatement(self, ctx:PascalParser.StructuredStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#compoundStatement.
    def visitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#statements.
    def visitStatements(self, ctx:PascalParser.StatementsContext):
        return self.visitChildren(ctx)


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



del PascalParser