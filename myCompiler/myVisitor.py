from antlr4 import *
from programVisitor import programVisitor
from programLexer import programLexer
if __name__ is not None and "." in __name__:
    from .programParser import programParser
else:
    from programParser import programParser


class myVisitor(programVisitor):
    def visitFuncType(self, ctx: programParser.BTypeContext):
        if(ctx.getText() == 'int'):
            print("define dso_local i32 ", end='')
            return self.visitChildren(ctx)

    def visitFuncdef(self, ctx: programParser.FuncdefContext):
        n = ctx.getChildCount()
        for i in range(n):
            if (ctx.getChild(i).getText() == '('):
                print('(', end='')
            elif (ctx.getChild(i).getText() == ')'):
                print(')', end='')
            else:
                self.visit(ctx.getChild(i))
        return None

    def visitFuncfparams(self, ctx: programParser.FuncfparamsContext):
        return super().visitFuncfparams(ctx)

    def visitIdent(self, ctx: programParser.IdentContext):
        print('@'+ctx.getText(), end='')
        return self.visitChildren(ctx)

    def visitBlock(self, ctx: programParser.BlockContext):
        n = ctx.getChildCount()
        for i in range(n):
            if( ctx.getChild(i).getText()=='{'):
                print('{')
            elif(ctx.getChild(i).getText()=='}'):
                print('}')
            else:
                self.visit(ctx.getChild(i))
        return None

    def visitReturnstmt(self, ctx: programParser.ReturnstmtContext):
        n=ctx.getChildCount()
        for i in range(n):
            if(ctx.getChild(i).getText()=='return'):
                print('ret ',end='')
            else:
                self.visit(ctx.getChild(i))
    
    def visitNumberexp(self, ctx: programParser.NumberexpContext):
        numstr = ctx.getText()
        a=None
        if(numstr[0]=='0'):
            if (numstr[1]=='x' or numstr[1]=='X'):
                a=int(numstr,16)
            else:
                a=int(numstr,8)
        else:
            a=int(numstr,10)
        print("i32 "+str(a))