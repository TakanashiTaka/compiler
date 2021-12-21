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
        self.identdic = {}
        self.constdic = {}
        self.visitres=''
        self.funcdic={}
    
    def visit(self, tree):
        super().visit(tree)
        print(self.visitres)

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
            self.visitres+="define dso_local i32 "
        return None

    def visitFuncdef(self, ctx: programParser.FuncdefContext):
        n = ctx.getChildCount()
        self.visitFuncType(ctx.getChild(0))
        self.visitres+='@'+self.visitIdent(ctx.getChild(1))
        for i in range(2, n-1):
            if (ctx.getChild(i).getText() == '('):
                self.visitres+='('
            elif (ctx.getChild(i).getText() == ')'):
                self.visitres+=')'
            else:
                self.visitFuncfparams(ctx.getChild(i))
        self.visitBlock(ctx.getChild(n-1))
        return None

    def visitFuncfparams(self, ctx: programParser.FuncfparamsContext):
        return super().visitFuncfparams(ctx)

    def visitIdent(self, ctx: programParser.IdentContext):
        return ctx.getText()

    def visitBlock(self, ctx: programParser.BlockContext):
        n = ctx.getChildCount()
        for i in range(n):
            if(ctx.getChild(i).getText() == '{'):
                self.visitres+='{\n'
            elif(ctx.getChild(i).getText() == '}'):
                self.visitres+='}'
            else:
                self.visitBlockitem(ctx.getChild(i))
        return None

    def visitReturnstmt(self, ctx: programParser.ReturnstmtContext):
        res = None
        res = self.visitExp(ctx.getChild(1))
        self.visitres+='ret i32 '+res+'\n'

    def visitExp(self, ctx: programParser.ExpContext):
        return self.visitAddexp(ctx.getChild(0))

    def visitAddexp(self, ctx: programParser.AddexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            return self.visitMulexp(ctx.getChild(0))
        else:
            res1 = self.visitAddexp(ctx.getChild(0))
            res2 = self.visitMulexp(ctx.getChild(2))
            self.maxregnum += 1
            if(ctx.getChild(1).getText() == '+'):
                self.visitres+="%"+str(self.maxregnum)+" = add i32 "+res1+','+res2+'\n'
            else:
                self.visitres+="%"+str(self.maxregnum)+" = sub i32 "+res1+','+res2+'\n'
            return '%'+str(self.maxregnum)

    def visitMulexp(self, ctx: programParser.MulexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            return self.visitUnaryexp(ctx.getChild(0))
        else:
            res1 = self.visitMulexp(ctx.getChild(0))
            res2 = self.visitUnaryexp(ctx.getChild(2))
            self.maxregnum += 1
            if(ctx.getChild(1).getText() == '*'):
                self.visitres+="%"+str(self.maxregnum)+" = mul i32 "+res1+','+res2+'\n'
            elif (ctx.getChild(1).getText() == '/'):
                self.visitres+="%"+str(self.maxregnum)+" = sdiv i32 "+res1+','+res2+'\n'
            else:
                self.visitres+="%"+str(self.maxregnum)+" = srem i32 "+res1+','+res2+'\n'
            return '%'+str(self.maxregnum)

    def visitUnaryexp(self, ctx: programParser.UnaryexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            m = ctx.getChild(0).getChildCount()
            if(m == 3):
                return self.visitBraceexp(ctx.getChild(0))
            else:
                # self.visitres+="rule index is "+str(ctx.getChild(0).getChild(0).getRuleIndex()))
                if(ctx.getChild(0).getChild(0).getRuleIndex() == 18):
                    return self.visitLvalexp(ctx.getChild(0))
                else:
                    return self.visitNumberexp(ctx.getChild(0))
        elif(n == 2):
            if(ctx.getChild(0).getText() == '+'):

                return self.visitUnaryexp(ctx.getChild(1))
            elif(ctx.getChild(0).getText() == '-'):
                res = self.visitUnaryexp(ctx.getChild(1))
                self.maxregnum += 1
                self.visitres+='%'+str(self.maxregnum) + '= sub i32 0 ,'+res+'\n'
                return '%'+str(self.maxregnum)
        else:
            identstr = self.visitIdent(ctx.getChild(0))
            if(identstr == 'getint'):
                self.maxregnum += 1
                if(self.funcdic.get('getint')==None):
                    self.visitres='declare i32 @getint()\n'+self.visitres
                    self.funcdic['getint']=True
                self.visitres+='%'+str(self.maxregnum) + '= call i32 @getint()\n'
                if(ctx.getChildCount() != 3):
                    exit(-1)
            elif(identstr == 'getch'):
                self.maxregnum += 1
                if(self.funcdic.get('getch')==None):
                    self.visitres='declare i32 @getch()\n'+self.visitres
                    self.funcdic['getch']=True
                self.visitres+='%'+str(self.maxregnum) + '= call i32 @getch()\n'
                if(ctx.getChildCount() != 3):
                    exit(-1)
            elif(identstr == 'putint'):
                res = self.visitFuncrparams(ctx.getChild(2))
                if(self.funcdic.get('putint')==None):
                    self.visitres='declare void @putint(i32)\n'+self.visitres
                    self.funcdic['putint']=True
                self.visitres+='call void @putint(i32 '+res+')\n'
                if(ctx.getChild(2).getChildCount() != 1):
                    exit(-1)
            elif(identstr == 'putch'):
                res = self.visitFuncrparams(ctx.getChild(2))
                if(self.funcdic.get('putch')==None):
                    self.visitres='declare void @putch(i32)\n'+self.visitres
                    self.funcdic['putch']=True
                self.visitres+='call void @putch(i32 '+res+')\n'
                if(ctx.getChild(2).getChildCount() != 1):
                    exit(-1)
            return '%'+str(self.maxregnum)

    def visitFuncrparams(self, ctx: programParser.FuncrparamsContext):
        return self.visitExp(ctx.getChild(0))

    def visitBraceexp(self, ctx: programParser.BraceexpContext):
        return self.visitExp(ctx.getChild(1))

    def visitLvalexp(self, ctx: programParser.LvalexpContext):
        # self.visitLval(ctx.getChild(0))
        if(self.identdic.get(self.visitIdent(ctx.getChild(0).getChild(0)))):
            self.maxregnum+=1
            self.visitres+='%'+str(self.maxregnum)+" = load i32, i32* "+self.identdic.get(self.visitIdent(ctx.getChild(0).getChild(0)))+'\n'
            return '%'+str(self.maxregnum)
        elif(self.constdic.get(self.visitIdent(ctx.getChild(0).getChild(0)))):
            return self.constdic.get(self.visitIdent(ctx.getChild(0).getChild(0)))

    def visitLval(self, ctx: programParser.LvalContext):
        n = ctx.getChildCount()
        if(n == 1):
            if(self.identdic.get(self.visitIdent(ctx.getChild(0)))):
                return self.identdic.get(self.visitIdent(ctx.getChild(0)))
            elif(self.constdic.get(self.visitIdent(ctx.getChild(0)))):
                return self.constdic.get(self.visitIdent(ctx.getChild(0)))

        return '0'

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
        # self.visitres+=str(a))
        return str(a)

    # def visitVardecl(self, ctx: programParser.VardeclContext):

    def visitConstdef(self, ctx: programParser.ConstdefContext):
        n = ctx.getChildCount()
        key = self.visitIdent(ctx.getChild(0))
        if(self.constdic.get(key)==None and self.identdic.get(key)==None):
            self.constdic[key] = self.visitConstinitval(ctx.getChild(n-1))
        else:
            exit(-1)

    def visitConstinitval(self, ctx: programParser.ConstinitvalContext):
        return self.visitConstexp(ctx.getChild(0))

    def visitConstexp(self, ctx: programParser.ConstexpContext):
        return self.visitAddexp(ctx.getChild(0))

    def visitAssigndef(self, ctx: programParser.AssigndefContext):
        n = ctx.getChildCount()
        self.maxregnum += 1
        key = self.visitIdent(ctx.getChild(0))
        if(self.constdic.get(key)==None and self.identdic.get(key)==None):
            self.identdic[key] = '%'+str(self.maxregnum)
            self.visitres+='%'+str(self.maxregnum)+'= alloca i32\n'
            res = self.visitInitval(ctx.getChild(n-1))
            self.visitres+='store i32 '+res+', i32* '+self.identdic.get(key)+'\n'
        else:
            exit(-1)

    def visitNoassigndef(self, ctx: programParser.NoassigndefContext):
        n = ctx.getChildCount()
        self.maxregnum += 1
        key = self.visitIdent(ctx.getChild(0))
        if(self.constdic.get(key)==None and self.identdic.get(key)==None):
            self.identdic[key] = '%'+str(self.maxregnum)
            self.visitres+='%'+str(self.maxregnum)+'= alloca i32\n'
        else:
            exit(-1)

    def visitInitval(self, ctx: programParser.InitvalContext):
        return self.visitExp(ctx.getChild(0))

    def visitAssignstmt(self, ctx: programParser.AssignstmtContext):
        res1 = self.visitLval(ctx.getChild(0))
        res2 = self.visitExp(ctx.getChild(2))
        self.visitres+='store i32 '+res2+', i32* '+res1+'\n'
        self.maxregnum += 1
        self.visitres+='%'+str(self.maxregnum)+" = load i32, i32* "+res1+'\n'
