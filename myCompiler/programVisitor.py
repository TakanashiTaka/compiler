# Generated from program.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .programParser import programParser
else:
    from programParser import programParser

# This class defines a complete generic visitor for a parse tree produced by programParser.

class programVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by programParser#compunit.
    def visitCompunit(self, ctx:programParser.CompunitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#decl.
    def visitDecl(self, ctx:programParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#constdecl.
    def visitConstdecl(self, ctx:programParser.ConstdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#bType.
    def visitBType(self, ctx:programParser.BTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#constdef.
    def visitConstdef(self, ctx:programParser.ConstdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#constinitval.
    def visitConstinitval(self, ctx:programParser.ConstinitvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#vardecl.
    def visitVardecl(self, ctx:programParser.VardeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#noassigndef.
    def visitNoassigndef(self, ctx:programParser.NoassigndefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#assigndef.
    def visitAssigndef(self, ctx:programParser.AssigndefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#initval.
    def visitInitval(self, ctx:programParser.InitvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#funcdef.
    def visitFuncdef(self, ctx:programParser.FuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#funcType.
    def visitFuncType(self, ctx:programParser.FuncTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#funcfparams.
    def visitFuncfparams(self, ctx:programParser.FuncfparamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#funcfparam.
    def visitFuncfparam(self, ctx:programParser.FuncfparamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#block.
    def visitBlock(self, ctx:programParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#blockitem.
    def visitBlockitem(self, ctx:programParser.BlockitemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#assignstmt.
    def visitAssignstmt(self, ctx:programParser.AssignstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#normalstmt.
    def visitNormalstmt(self, ctx:programParser.NormalstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#blockstmt.
    def visitBlockstmt(self, ctx:programParser.BlockstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#ifstmt.
    def visitIfstmt(self, ctx:programParser.IfstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#whilestmt.
    def visitWhilestmt(self, ctx:programParser.WhilestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#breakstmt.
    def visitBreakstmt(self, ctx:programParser.BreakstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#continuestmt.
    def visitContinuestmt(self, ctx:programParser.ContinuestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#returnstmt.
    def visitReturnstmt(self, ctx:programParser.ReturnstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#exp.
    def visitExp(self, ctx:programParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#cond.
    def visitCond(self, ctx:programParser.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#lval.
    def visitLval(self, ctx:programParser.LvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#braceexp.
    def visitBraceexp(self, ctx:programParser.BraceexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#lvalexp.
    def visitLvalexp(self, ctx:programParser.LvalexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#numberexp.
    def visitNumberexp(self, ctx:programParser.NumberexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#unaryexp.
    def visitUnaryexp(self, ctx:programParser.UnaryexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#unaryOp.
    def visitUnaryOp(self, ctx:programParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#funcrparams.
    def visitFuncrparams(self, ctx:programParser.FuncrparamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#mulexp.
    def visitMulexp(self, ctx:programParser.MulexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#addexp.
    def visitAddexp(self, ctx:programParser.AddexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#relexp.
    def visitRelexp(self, ctx:programParser.RelexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#eqexp.
    def visitEqexp(self, ctx:programParser.EqexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#landexp.
    def visitLandexp(self, ctx:programParser.LandexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#lOrexp.
    def visitLOrexp(self, ctx:programParser.LOrexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#constexp.
    def visitConstexp(self, ctx:programParser.ConstexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by programParser#ident.
    def visitIdent(self, ctx:programParser.IdentContext):
        return self.visitChildren(ctx)



del programParser