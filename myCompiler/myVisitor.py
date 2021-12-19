from antlr4 import *
from programVisitor import programVisitor
from programLexer import programLexer
if __name__ is not None and "." in __name__:
    from .programParser import programParser
else:
    from programParser import programParser


class myVisitor(programVisitor):
    def __init__(self):
        self.regnum = 0
        self.maxregnum = 0

    # def visitChildren(self, node):
    #     retres = 0
    #     retreg = self.maxregnum
    #     n = node.getChildCount()
    #     for i in range(n):
    #         c = node.getChild(i)

    #         retres,retreg=self.visit(c)

    #     return retres,retreg

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
            if(ctx.getChild(i).getText() == '{'):
                print('{')
            elif(ctx.getChild(i).getText() == '}'):
                print('}')
            else:
                self.visit(ctx.getChild(i))
        return None

    def visitReturnstmt(self, ctx: programParser.ReturnstmtContext):
        n = ctx.getChildCount()
        retreg = 0
        res = None
        for i in range(1, n-1):
            retreg, res = self.visitExp(ctx.getChild(i))
        if(retreg == 0):
            print('ret i32 '+str(res))
        else:
            print('ret i32 %'+str(retreg))

    def visitExp(self, ctx: programParser.ExpContext):
        return self.visitAddexp(ctx.getChild(0))

    def visitAddexp(self, ctx: programParser.AddexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            return self.visitMulexp(ctx.getChild(0))
        else:
            reg1,res1=self.visitAddexp(ctx.getChild(0))
            reg2,res2=self.visitMulexp(ctx.getChild(2))
            self.maxregnum+=1
            fstr=''
            sstr=''
            if(reg1==0):
                fstr=str(res1)
            else:
                fstr='%'+str(reg1)
            if(reg2==0):
                sstr=str(res2)
            else:
                sstr='%'+str(reg2)
            res=0
            if(ctx.getChild(1).getText()=='+'):
                print("%"+str(self.maxregnum)+" = add i32 "+fstr+','+sstr)
                res=res1+res2
            else:
                print("%"+str(self.maxregnum)+" = sub i32 "+fstr+','+sstr)
                res=res1-res2
            return self.maxregnum,res


    def visitMulexp(self, ctx: programParser.MulexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            return self.visitUnaryexp(ctx.getChild(0))
        else:
            reg1,res1 = self.visitMulexp(ctx.getChild(0))
            reg2,res2 = self.visitUnaryexp(ctx.getChild(2))
            self.maxregnum+=1
            fstr=''
            sstr=''
            if(reg1==0):
                fstr=str(res1)
            else:
                fstr='%'+str(reg1)
            if(reg2==0):
                sstr=str(res2)
            else:
                sstr='%'+str(reg2)
            res=0
            if(ctx.getChild(1).getText()=='*'):
                print("%"+str(self.maxregnum)+" = mul i32 "+fstr+','+sstr)
                res=res1*res2
            elif (ctx.getChild(1).getText()=='/'):
                print("%"+str(self.maxregnum)+" = sdiv i32 "+fstr+','+sstr)
                res=int(res1/res2)
            else:
                print("%"+str(self.maxregnum)+" = srem i32 "+fstr+','+sstr)
                res=res1%res2
            return self.maxregnum,res

    def visitUnaryexp(self, ctx: programParser.UnaryexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            m = ctx.getChild(0).getChildCount()
            if(m == 3):
                return self.visitBraceexp(ctx.getChild(0))
            else:
                # print("rule index is "+str(ctx.getChild(0).getChild(0).getRuleIndex()))
                if(ctx.getChild(0).getChild(0).getRuleIndex() == 18):
                    return self.visitLval(ctx.getChild(0))
                else:
                    return self.visitNumberexp(ctx.getChild(0))
        elif(n == 2):
            if(ctx.getChild(0).getText() == '+'):
                
                return self.visitUnaryexp(ctx.getChild(1))
            elif(ctx.getChild(0).getText() == '-'):
                reg,res=self.visitUnaryexp(ctx.getChild(1))
                self.maxregnum+=1
                print('%'+str(self.maxregnum) + '= sub i32 0 ,'+str(res))
                
                return self.maxregnum, res

    def visitBraceexp(self, ctx: programParser.BraceexpContext):
        return self.visitExp(ctx.getChild(1))

    def visitLval(self, ctx: programParser.LvalContext):
        return 0,0

    def visitNumberexp(self, ctx: programParser.NumberexpContext):
        numstr = ctx.getText()
        a = None
        if(numstr[0] == '0'):
            if (len(numstr) > 1 and (numstr[1] == 'x' or numstr[1] == 'X')):
                a = int(numstr, 16)
            else:
                a = int(numstr, 8)
        else:
            a = int(numstr, 10)
        # print(str(a))
        return 0,a
