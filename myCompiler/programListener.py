# Generated from program.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .programParser import programParser
else:
    from programParser import programParser

# This class defines a complete listener for a parse tree produced by programParser.
class programListener(ParseTreeListener):

    # Enter a parse tree produced by programParser#compunit.
    def enterCompunit(self, ctx:programParser.CompunitContext):
        pass

    # Exit a parse tree produced by programParser#compunit.
    def exitCompunit(self, ctx:programParser.CompunitContext):
        pass


    # Enter a parse tree produced by programParser#decl.
    def enterDecl(self, ctx:programParser.DeclContext):
        pass

    # Exit a parse tree produced by programParser#decl.
    def exitDecl(self, ctx:programParser.DeclContext):
        pass


    # Enter a parse tree produced by programParser#constdecl.
    def enterConstdecl(self, ctx:programParser.ConstdeclContext):
        pass

    # Exit a parse tree produced by programParser#constdecl.
    def exitConstdecl(self, ctx:programParser.ConstdeclContext):
        pass


    # Enter a parse tree produced by programParser#bType.
    def enterBType(self, ctx:programParser.BTypeContext):
        pass

    # Exit a parse tree produced by programParser#bType.
    def exitBType(self, ctx:programParser.BTypeContext):
        pass


    # Enter a parse tree produced by programParser#constdef.
    def enterConstdef(self, ctx:programParser.ConstdefContext):
        pass

    # Exit a parse tree produced by programParser#constdef.
    def exitConstdef(self, ctx:programParser.ConstdefContext):
        pass


    # Enter a parse tree produced by programParser#constinitval.
    def enterConstinitval(self, ctx:programParser.ConstinitvalContext):
        pass

    # Exit a parse tree produced by programParser#constinitval.
    def exitConstinitval(self, ctx:programParser.ConstinitvalContext):
        pass


    # Enter a parse tree produced by programParser#vardecl.
    def enterVardecl(self, ctx:programParser.VardeclContext):
        pass

    # Exit a parse tree produced by programParser#vardecl.
    def exitVardecl(self, ctx:programParser.VardeclContext):
        pass


    # Enter a parse tree produced by programParser#noassigndef.
    def enterNoassigndef(self, ctx:programParser.NoassigndefContext):
        pass

    # Exit a parse tree produced by programParser#noassigndef.
    def exitNoassigndef(self, ctx:programParser.NoassigndefContext):
        pass


    # Enter a parse tree produced by programParser#assigndef.
    def enterAssigndef(self, ctx:programParser.AssigndefContext):
        pass

    # Exit a parse tree produced by programParser#assigndef.
    def exitAssigndef(self, ctx:programParser.AssigndefContext):
        pass


    # Enter a parse tree produced by programParser#initval.
    def enterInitval(self, ctx:programParser.InitvalContext):
        pass

    # Exit a parse tree produced by programParser#initval.
    def exitInitval(self, ctx:programParser.InitvalContext):
        pass


    # Enter a parse tree produced by programParser#funcdef.
    def enterFuncdef(self, ctx:programParser.FuncdefContext):
        pass

    # Exit a parse tree produced by programParser#funcdef.
    def exitFuncdef(self, ctx:programParser.FuncdefContext):
        pass


    # Enter a parse tree produced by programParser#funcType.
    def enterFuncType(self, ctx:programParser.FuncTypeContext):
        pass

    # Exit a parse tree produced by programParser#funcType.
    def exitFuncType(self, ctx:programParser.FuncTypeContext):
        pass


    # Enter a parse tree produced by programParser#funcfparams.
    def enterFuncfparams(self, ctx:programParser.FuncfparamsContext):
        pass

    # Exit a parse tree produced by programParser#funcfparams.
    def exitFuncfparams(self, ctx:programParser.FuncfparamsContext):
        pass


    # Enter a parse tree produced by programParser#funcfparam.
    def enterFuncfparam(self, ctx:programParser.FuncfparamContext):
        pass

    # Exit a parse tree produced by programParser#funcfparam.
    def exitFuncfparam(self, ctx:programParser.FuncfparamContext):
        pass


    # Enter a parse tree produced by programParser#block.
    def enterBlock(self, ctx:programParser.BlockContext):
        pass

    # Exit a parse tree produced by programParser#block.
    def exitBlock(self, ctx:programParser.BlockContext):
        pass


    # Enter a parse tree produced by programParser#blockitem.
    def enterBlockitem(self, ctx:programParser.BlockitemContext):
        pass

    # Exit a parse tree produced by programParser#blockitem.
    def exitBlockitem(self, ctx:programParser.BlockitemContext):
        pass


    # Enter a parse tree produced by programParser#stmt.
    def enterStmt(self, ctx:programParser.StmtContext):
        pass

    # Exit a parse tree produced by programParser#stmt.
    def exitStmt(self, ctx:programParser.StmtContext):
        pass


    # Enter a parse tree produced by programParser#assignstmt.
    def enterAssignstmt(self, ctx:programParser.AssignstmtContext):
        pass

    # Exit a parse tree produced by programParser#assignstmt.
    def exitAssignstmt(self, ctx:programParser.AssignstmtContext):
        pass


    # Enter a parse tree produced by programParser#normalstmt.
    def enterNormalstmt(self, ctx:programParser.NormalstmtContext):
        pass

    # Exit a parse tree produced by programParser#normalstmt.
    def exitNormalstmt(self, ctx:programParser.NormalstmtContext):
        pass


    # Enter a parse tree produced by programParser#blockstmt.
    def enterBlockstmt(self, ctx:programParser.BlockstmtContext):
        pass

    # Exit a parse tree produced by programParser#blockstmt.
    def exitBlockstmt(self, ctx:programParser.BlockstmtContext):
        pass


    # Enter a parse tree produced by programParser#ifstmt.
    def enterIfstmt(self, ctx:programParser.IfstmtContext):
        pass

    # Exit a parse tree produced by programParser#ifstmt.
    def exitIfstmt(self, ctx:programParser.IfstmtContext):
        pass


    # Enter a parse tree produced by programParser#whilestmt.
    def enterWhilestmt(self, ctx:programParser.WhilestmtContext):
        pass

    # Exit a parse tree produced by programParser#whilestmt.
    def exitWhilestmt(self, ctx:programParser.WhilestmtContext):
        pass


    # Enter a parse tree produced by programParser#breakstmt.
    def enterBreakstmt(self, ctx:programParser.BreakstmtContext):
        pass

    # Exit a parse tree produced by programParser#breakstmt.
    def exitBreakstmt(self, ctx:programParser.BreakstmtContext):
        pass


    # Enter a parse tree produced by programParser#continuestmt.
    def enterContinuestmt(self, ctx:programParser.ContinuestmtContext):
        pass

    # Exit a parse tree produced by programParser#continuestmt.
    def exitContinuestmt(self, ctx:programParser.ContinuestmtContext):
        pass


    # Enter a parse tree produced by programParser#returnstmt.
    def enterReturnstmt(self, ctx:programParser.ReturnstmtContext):
        pass

    # Exit a parse tree produced by programParser#returnstmt.
    def exitReturnstmt(self, ctx:programParser.ReturnstmtContext):
        pass


    # Enter a parse tree produced by programParser#exp.
    def enterExp(self, ctx:programParser.ExpContext):
        pass

    # Exit a parse tree produced by programParser#exp.
    def exitExp(self, ctx:programParser.ExpContext):
        pass


    # Enter a parse tree produced by programParser#cond.
    def enterCond(self, ctx:programParser.CondContext):
        pass

    # Exit a parse tree produced by programParser#cond.
    def exitCond(self, ctx:programParser.CondContext):
        pass


    # Enter a parse tree produced by programParser#lval.
    def enterLval(self, ctx:programParser.LvalContext):
        pass

    # Exit a parse tree produced by programParser#lval.
    def exitLval(self, ctx:programParser.LvalContext):
        pass


    # Enter a parse tree produced by programParser#braceexp.
    def enterBraceexp(self, ctx:programParser.BraceexpContext):
        pass

    # Exit a parse tree produced by programParser#braceexp.
    def exitBraceexp(self, ctx:programParser.BraceexpContext):
        pass


    # Enter a parse tree produced by programParser#lvalexp.
    def enterLvalexp(self, ctx:programParser.LvalexpContext):
        pass

    # Exit a parse tree produced by programParser#lvalexp.
    def exitLvalexp(self, ctx:programParser.LvalexpContext):
        pass


    # Enter a parse tree produced by programParser#numberexp.
    def enterNumberexp(self, ctx:programParser.NumberexpContext):
        pass

    # Exit a parse tree produced by programParser#numberexp.
    def exitNumberexp(self, ctx:programParser.NumberexpContext):
        pass


    # Enter a parse tree produced by programParser#unaryexp.
    def enterUnaryexp(self, ctx:programParser.UnaryexpContext):
        pass

    # Exit a parse tree produced by programParser#unaryexp.
    def exitUnaryexp(self, ctx:programParser.UnaryexpContext):
        pass


    # Enter a parse tree produced by programParser#unaryOp.
    def enterUnaryOp(self, ctx:programParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by programParser#unaryOp.
    def exitUnaryOp(self, ctx:programParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by programParser#funcrparams.
    def enterFuncrparams(self, ctx:programParser.FuncrparamsContext):
        pass

    # Exit a parse tree produced by programParser#funcrparams.
    def exitFuncrparams(self, ctx:programParser.FuncrparamsContext):
        pass


    # Enter a parse tree produced by programParser#mulexp.
    def enterMulexp(self, ctx:programParser.MulexpContext):
        pass

    # Exit a parse tree produced by programParser#mulexp.
    def exitMulexp(self, ctx:programParser.MulexpContext):
        pass


    # Enter a parse tree produced by programParser#addexp.
    def enterAddexp(self, ctx:programParser.AddexpContext):
        pass

    # Exit a parse tree produced by programParser#addexp.
    def exitAddexp(self, ctx:programParser.AddexpContext):
        pass


    # Enter a parse tree produced by programParser#relexp.
    def enterRelexp(self, ctx:programParser.RelexpContext):
        pass

    # Exit a parse tree produced by programParser#relexp.
    def exitRelexp(self, ctx:programParser.RelexpContext):
        pass


    # Enter a parse tree produced by programParser#eqexp.
    def enterEqexp(self, ctx:programParser.EqexpContext):
        pass

    # Exit a parse tree produced by programParser#eqexp.
    def exitEqexp(self, ctx:programParser.EqexpContext):
        pass


    # Enter a parse tree produced by programParser#landexp.
    def enterLandexp(self, ctx:programParser.LandexpContext):
        pass

    # Exit a parse tree produced by programParser#landexp.
    def exitLandexp(self, ctx:programParser.LandexpContext):
        pass


    # Enter a parse tree produced by programParser#lOrexp.
    def enterLOrexp(self, ctx:programParser.LOrexpContext):
        pass

    # Exit a parse tree produced by programParser#lOrexp.
    def exitLOrexp(self, ctx:programParser.LOrexpContext):
        pass


    # Enter a parse tree produced by programParser#constexp.
    def enterConstexp(self, ctx:programParser.ConstexpContext):
        pass

    # Exit a parse tree produced by programParser#constexp.
    def exitConstexp(self, ctx:programParser.ConstexpContext):
        pass


    # Enter a parse tree produced by programParser#number.
    def enterNumber(self, ctx:programParser.NumberContext):
        pass

    # Exit a parse tree produced by programParser#number.
    def exitNumber(self, ctx:programParser.NumberContext):
        pass


    # Enter a parse tree produced by programParser#ident.
    def enterIdent(self, ctx:programParser.IdentContext):
        pass

    # Exit a parse tree produced by programParser#ident.
    def exitIdent(self, ctx:programParser.IdentContext):
        pass



del programParser