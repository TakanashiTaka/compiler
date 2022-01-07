from typing import List
from antlr4 import *
from programVisitor import programVisitor
from programLexer import programLexer
if __name__ is not None and "." in __name__:
    from .programParser import programParser
else:
    from programParser import programParser
import copy


class myVisitor(programVisitor):
    def __init__(self):
        self.regnum = 0
        self.maxregnum = 0
        self.visitres = 'declare void @memset(i32*, i32, i32)\ndeclare i32 @getint()\ndeclare i32 @getch()\ndeclare void @putint(i32)\ndeclare void @putch(i32)\ndeclare i32 @getarray(i32*)\ndeclare void @putarray(i32, i32*)\n'
        self.funcdic = {}
        self.labeldic = {}
        self.nowblock = '0'
        self.scopehisdic = {0: -1}
        self.scopeidentdic = {0: [{}, {}]}
        self.arraydic = {}
        self.nowscope = 0
        self.maxscope = 0
        self.nowwhilecond = '0'
        self.nowwhileout = '0'
        self.nowconst = False
        self.myfuncdic = {
            'memset': ['void', ['i32*', 'i32', 'i32']],
            'getint': ['int', []],
            'getch': ['int', []],
            'putint': ['void', ['i32']],
            'putch': ['void', ['i32']],
            'getarray': ['int', ['i32*']],
            'putarray': ['void', ['i32', 'i32*']]
        }
        self.nowfuncparams = {}

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
            self.visitres += "define dso_local i32 "
        elif(ctx.getText() == 'void'):
            self.visitres += "define dso_local void "
        return ctx.getText()

    def visitFuncdef(self, ctx: programParser.FuncdefContext):
        statelist = []
        n = ctx.getChildCount()
        functype = self.visitFuncType(ctx.getChild(0))
        statelist.append(functype)
        funcname = self.visitIdent(ctx.getChild(1))
        self.visitres += '@'+funcname
        paramlist = []
        for i in range(2, n-1):
            if (ctx.getChild(i).getText() == '('):
                self.visitres += '('
            elif (ctx.getChild(i).getText() == ')'):
                self.visitres += ')'
            else:
                paramlist = self.visitFuncfparams(ctx.getChild(i))
        statelist.append(paramlist)
        self.myfuncdic[funcname] = statelist
        self.visitres += '{\n'
        self.visitBlock(ctx.getChild(n-1))
        self.visitres += '}\n'

    def visitFuncfparams(self, ctx: programParser.FuncfparamsContext):
        n = ctx.getChildCount()
        paramlist = []
        for i in range(0, n, 2):
            paramlist.append(self.visitFuncfparam(ctx.getChild(i)))
            if(i < n-1):
                self.visitres += ','
        return paramlist

    def visitFuncfparam(self, ctx: programParser.FuncfparamContext):
        n = ctx.getChildCount()
        if(n == 2):
            self.maxregnum += 1
            self.visitres += 'i32 %g'+str(self.maxregnum)
            ident = self.visitIdent(ctx.getChild(1))
            self.nowfuncparams[ident] = ['%g'+str(self.maxregnum), 'i32']
            return 'i32'
        else:
            self.maxregnum += 1
            self.visitres += 'i32* %g'+str(self.maxregnum)
            lens = [-1]
            totlen = 1
            ident = self.visitIdent(ctx.getChild(1))
            for i in range(2, n):
                text = ctx.getChild(i).getText()
                if(text != '[' and text != ']'):
                    res = self.visitExp(ctx.getChild(i))
                    totlen *= int(res)
                    lens.append(int(res))
            self.nowfuncparams[ident] = ['%g'+str(self.maxregnum), 'i32*']
            self.arraydic[ident+'+'+str(self.maxscope+1)] = lens
            return 'i32*'

    def visitIdent(self, ctx: programParser.IdentContext):
        return ctx.getText()

    def visitBlock(self, ctx: programParser.BlockContext):
        n = ctx.getChildCount()
        for i in range(n):
            if(ctx.getChild(i).getText() == '{'):
                oldscope = self.nowscope
                self.maxscope += 1
                self.scopehisdic[self.maxscope] = self.nowscope
                self.nowscope = self.maxscope
                copyold = copy.deepcopy(self.scopeidentdic.get(
                    self.scopehisdic.get(self.nowscope)))
                if(oldscope==0):
                    for i in self.nowfuncparams.keys():
                        value = self.nowfuncparams.get(i)
                        if(value[1] == 'i32'):

                            self.maxregnum += 1
                            self.visitres += '%g' + \
                                str(self.maxregnum)+'= alloca i32\n'
                            self.visitres += 'store i32 ' + \
                                str(value[0])+', i32* %g'+str(self.maxregnum)+'\n'
                            copyold[0][i] = '%g'+str(self.maxregnum)
                        elif(value[1] == 'i32*'):
                            copyold[0][i] = value[0]

                self.scopeidentdic[self.nowscope] = copyold
                oldarray = []
                for i in self.arraydic.keys():
                    spl = i.split('+')
                    oldarray.append(spl)
                for i in range(len(oldarray)):
                    if(oldarray[i][1] == str(oldscope)):
                        self.arraydic[oldarray[i][0]+'+'+str(self.nowscope)] = self.arraydic.get(
                            oldarray[i][0]+'+'+str(oldscope))

            elif(ctx.getChild(i).getText() == '}'):
                self.nowscope = self.scopehisdic.get(self.nowscope)
                self.nowfuncparams.clear()
            else:
                self.visitBlockitem(ctx.getChild(i))
        return None

    def visitReturnstmt(self, ctx: programParser.ReturnstmtContext):
        res = None
        res = self.visitExp(ctx.getChild(1))
        self.visitres += 'ret i32 '+str(res)+'\n'

    def visitExp(self, ctx: programParser.ExpContext):
        return self.visitAddexp(ctx.getChild(0))

    def visitAddexp(self, ctx: programParser.AddexpContext):
        n = ctx.getChildCount()
        if(self.nowscope == 0):
            if(n == 1):
                return self.visitMulexp(ctx.getChild(0))
            else:
                return self.visitAddexp(ctx.getChild(0))+self.visitMulexp(ctx.getChild(2))
        else:
            if(self.nowconst == True):
                if(n == 1):
                    return self.visitMulexp(ctx.getChild(0))
                else:
                    return self.visitAddexp(ctx.getChild(0))+self.visitMulexp(ctx.getChild(2))
            else:
                if(n == 1):
                    return self.visitMulexp(ctx.getChild(0))
                else:
                    res1 = self.visitAddexp(ctx.getChild(0))
                    res2 = self.visitMulexp(ctx.getChild(2))
                    self.maxregnum += 1
                    if(ctx.getChild(1).getText() == '+'):
                        self.visitres += "%g" + \
                            str(self.maxregnum) + \
                            " = add i32 "+str(res1)+','+str(res2)+'\n'
                    else:
                        self.visitres += "%g" + \
                            str(self.maxregnum) + \
                            " = sub i32 "+str(res1)+','+str(res2)+'\n'
                    return '%g'+str(self.maxregnum)

    def visitMulexp(self, ctx: programParser.MulexpContext):
        n = ctx.getChildCount()
        if(self.nowscope == 0):
            if(n == 1):
                return self.visitUnaryexp(ctx.getChild(0))
            else:
                if(ctx.getChild(1).getText() == '*'):
                    return int(self.visitMulexp(ctx.getChild(0))*self.visitUnaryexp(ctx.getChild(2)))
                elif (ctx.getChild(1).getText() == '/'):
                    return int(self.visitMulexp(ctx.getChild(0))/self.visitUnaryexp(ctx.getChild(2)))
                else:
                    return int(self.visitMulexp(ctx.getChild(0)) % self.visitUnaryexp(ctx.getChild(2)))
        else:
            if(self.nowconst == True):
                if(n == 1):
                    return self.visitUnaryexp(ctx.getChild(0))
                else:
                    if(ctx.getChild(1).getText() == '*'):
                        return int(self.visitMulexp(ctx.getChild(0))*self.visitUnaryexp(ctx.getChild(2)))
                    elif (ctx.getChild(1).getText() == '/'):
                        return int(self.visitMulexp(ctx.getChild(0))/self.visitUnaryexp(ctx.getChild(2)))
                    else:
                        return int(self.visitMulexp(ctx.getChild(0)) % self.visitUnaryexp(ctx.getChild(2)))
            else:
                if(n == 1):
                    return self.visitUnaryexp(ctx.getChild(0))
                else:
                    res1 = self.visitMulexp(ctx.getChild(0))
                    res2 = self.visitUnaryexp(ctx.getChild(2))
                    self.maxregnum += 1
                    if(ctx.getChild(1).getText() == '*'):
                        self.visitres += "%g" + \
                            str(self.maxregnum) + \
                            " = mul i32 "+str(res1)+','+str(res2)+'\n'
                    elif (ctx.getChild(1).getText() == '/'):
                        self.visitres += "%g" + \
                            str(self.maxregnum) + \
                            " = sdiv i32 "+str(res1)+','+str(res2)+'\n'
                    else:
                        self.visitres += "%g" + \
                            str(self.maxregnum) + \
                            " = srem i32 "+str(res1)+','+str(res2)+'\n'
                    return '%g'+str(self.maxregnum)

    def visitUnaryexp(self, ctx: programParser.UnaryexpContext):
        n = ctx.getChildCount()
        if(self.nowscope == 0):
            if(n == 1):
                m = ctx.getChild(0).getChildCount()
                if(m == 3):
                    return self.visitBraceexp(ctx.getChild(0))
                else:
                    if(ctx.getChild(0).getChild(0).getRuleIndex() == programParser.RULE_lval):
                        return self.visitLvalexp(ctx.getChild(0))
                    else:
                        return self.visitNumberexp(ctx.getChild(0))
            elif(n == 2):
                if(ctx.getChild(0).getText() == '+'):
                    return self.visitUnaryexp(ctx.getChild(1))
                elif(ctx.getChild(0).getText() == '-'):
                    return -self.visitUnaryexp(ctx.getChild(1))

        else:
            if(self.nowconst == True):
                if(n == 1):
                    m = ctx.getChild(0).getChildCount()
                    if(m == 3):
                        return self.visitBraceexp(ctx.getChild(0))
                    else:
                        if(ctx.getChild(0).getChild(0).getRuleIndex() == programParser.RULE_lval):
                            return self.visitLvalexp(ctx.getChild(0))
                        else:
                            return self.visitNumberexp(ctx.getChild(0))
                elif(n == 2):
                    if(ctx.getChild(0).getText() == '+'):
                        return self.visitUnaryexp(ctx.getChild(1))
                    elif(ctx.getChild(0).getText() == '-'):
                        return -self.visitUnaryexp(ctx.getChild(1))
            else:
                if(n == 1):
                    m = ctx.getChild(0).getChildCount()
                    if(m == 3):
                        return self.visitBraceexp(ctx.getChild(0))
                    else:
                        if(ctx.getChild(0).getChild(0).getRuleIndex() == programParser.RULE_lval):

                            return self.visitLvalexp(ctx.getChild(0))

                        else:
                            return self.visitNumberexp(ctx.getChild(0))
                elif(n == 2):
                    if(ctx.getChild(0).getText() == '+'):
                        return self.visitUnaryexp(ctx.getChild(1))
                    elif(ctx.getChild(0).getText() == '-'):
                        res = self.visitUnaryexp(ctx.getChild(1))
                        self.maxregnum += 1
                        self.visitres += '%g' + \
                            str(self.maxregnum) + '= sub i32 0 ,'+str(res)+'\n'
                        return '%g'+str(self.maxregnum)
                    else:
                        res = self.visitUnaryexp(ctx.getChild(1))
                        self.maxregnum += 1
                        self.visitres += '%g' + \
                            str(self.maxregnum) + \
                            '= icmp eq i32 '+str(res)+', 0\n'
                        self.maxregnum += 1
                        self.visitres += '%g' + \
                            str(self.maxregnum) + '= zext i1 %g' + \
                            str(self.maxregnum-1)+' to i32\n'
                        return '%g'+str(self.maxregnum)
                else:
                    identstr = self.visitIdent(ctx.getChild(0))
                    func = self.myfuncdic.get(identstr)
                    if(func):
                        if(func[0] == 'int'):
                            if(n == 3):
                                self.maxregnum += 1
                                self.visitres += '%g' + \
                                    str(self.maxregnum) + \
                                    '= call i32 @'+identstr+'()\n'
                            elif(n == 4):
                                res = self.visitFuncrparams(
                                    ctx.getChild(2))
                                self.maxregnum += 1
                                parastr = ''
                                for i in range(len(res)):
                                    parastr += self.myfuncdic.get(
                                        identstr)[1][i]+' '+str(res[i])
                                    if(i < len(res)-1):
                                        parastr += ', '
                                self.visitres += '%g' + \
                                    str(self.maxregnum)+'= call i32 @' + \
                                    identstr+'('+parastr+')\n'
                        elif(func[0] == 'void'):
                            if(n == 3):
                                self.visitres += 'call void @'+identstr+'()\n'
                            elif(n == 4):
                                res = self.visitFuncrparams(
                                    ctx.getChild(2))
                                parastr = ''
                                for i in range(len(res)):
                                    parastr += self.myfuncdic.get(
                                        identstr)[1][i]+' '+str(res[i])
                                    if(i < len(res)-1):
                                        parastr += ', '
                                self.visitres += 'call void @' + \
                                    identstr+'('+parastr+')\n'
                    else:
                        exit(-1)
                    return '%g'+str(self.maxregnum)

    def visitFuncrparams(self, ctx: programParser.FuncrparamsContext):
        n = ctx.getChildCount()
        resreg = []
        for i in range(0, n, 2):
            resreg.append(self.visitExp(ctx.getChild(i)))
        return resreg

    def visitBraceexp(self, ctx: programParser.BraceexpContext):
        return self.visitExp(ctx.getChild(1))

    def visitLvalexp(self, ctx: programParser.LvalexpContext):
        if(self.nowscope == 0):
            a = self.scopeidentdic.get(0)
            if(a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))):

                res = a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))

                return res
            else:
                exit(-1)

        else:
            a = self.scopeidentdic.get(self.nowscope)
            if(self.nowconst == True):
                if(a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))):

                    res = a[1].get(self.visitIdent(
                        ctx.getChild(0).getChild(0)))

                    return res
                else:
                    exit(-1)
            else:
                if(a[0].get(self.visitIdent(ctx.getChild(0).getChild(0)))):
                    m = ctx.getChild(0).getChildCount()
                    if(m == 1):
                        if(self.arraydic.get(self.visitIdent(ctx.getChild(0).getChild(0))+'+'+str(self.nowscope))):
                            
                            totlen = 1
                            lens = self.arraydic.get(self.visitIdent(
                                ctx.getChild(0).getChild(0))+'+'+str(self.nowscope))
                            for i in range(len(lens)):
                                totlen *= int(lens[i])
                            if(totlen>0):
                                self.maxregnum += 1
                                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr ['+str(totlen)+' x i32], [' +\
                                    str(totlen)+' x i32]* '+a[0].get(self.visitIdent(ctx.getChild(0).getChild(0))) +\
                                    ', i32 0,i32 0\n'
                            else:
                                return self.scopeidentdic.get(self.nowscope)[0].get(self.visitIdent(ctx.getChild(0).getChild(0)))
                            
                        else:
                            self.maxregnum += 1
                            self.visitres += '%g'+str(self.maxregnum)+" = load i32, i32* "+a[0].get(
                                self.visitIdent(ctx.getChild(0).getChild(0)))+'\n'
                        return '%g'+str(self.maxregnum)
                    else:
                        pos = []
                        key = self.visitIdent(ctx.getChild(0).getChild(0))
                        for i in range(2, m, 3):
                            pos.append(self.visitExp(
                                ctx.getChild(0).getChild(i)))
                        ###
                        linepos = self.getpos(
                            pos, self.arraydic.get(key+'+'+str(self.nowscope)))

                        lens = self.arraydic.get(key+'+'+str(self.nowscope))
                        
                        totlen = 1
                        for i in range(len(lens)):
                            totlen *= int(lens[i])
                        if(totlen > 0):
                            self.maxregnum += 1
                            self.visitres += '%g'+str(self.maxregnum)+' = getelementptr ['+str(totlen)+' x i32],' \
                                + '['+str(totlen)+' x i32]* ' + \
                                a[0].get(key)+', i32 0, i32 0\n'
                            self.maxregnum += 1
                            self.visitres += '%g'+str(self.maxregnum)+" = getelementptr i32, i32* %g"+str(
                                self.maxregnum-1)+', i32 '+str(linepos)+'\n'
                            self.maxregnum += 1
                            self.visitres += '%g' + \
                                str(self.maxregnum)+" = load i32, i32* %g" + \
                                str(self.maxregnum-1)+'\n'
                        else:
                            self.maxregnum += 1
                            self.visitres += '%g' + \
                                str(self.maxregnum)+" = getelementptr i32, i32* " + \
                                a[0].get(key)+', i32 '+str(linepos)+'\n'
                            self.maxregnum += 1
                            self.visitres += '%g' + \
                                str(self.maxregnum)+" = load i32, i32* %g" + \
                                str(self.maxregnum-1)+'\n'

                        return '%g'+str(self.maxregnum)

                elif(a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))):
                    m = ctx.getChild(0).getChildCount()
                    if(m == 1):
                        return str(a[1].get(self.visitIdent(ctx.getChild(0).getChild(0))))
                    else:
                        pos = []
                        key = self.visitIdent(ctx.getChild(0).getChild(0))
                        array = a[1].get(key)
                        res = copy.deepcopy(array)
                        for i in range(2, m, 3):
                            res = res[int(self.visitExp(
                                ctx.getChild(0).getChild(i)))]
                        return res

                else:
                    exit(-1)

    def visitLval(self, ctx: programParser.LvalContext):
        n = ctx.getChildCount()
        if(n == 1):
            a = self.scopeidentdic.get(self.nowscope)
            if(a[0].get(self.visitIdent(ctx.getChild(0)))):
                return a[0].get(self.visitIdent(ctx.getChild(0)))
            elif(a[1].get(self.visitIdent(ctx.getChild(0)))):
                return a[1].get(self.visitIdent(ctx.getChild(0)))
            else:
                exit(-1)
        else:
            res = []
            key = self.visitIdent(ctx.getChild(0))
            for i in range(2, n, 3):
                res.append(self.visitExp(ctx.getChild(i)))
            pos = self.getpos(res, self.arraydic.get(
                key+'+'+str(self.nowscope)))

            lens = self.arraydic.get(key+'+'+str(self.nowscope))
            totlen = 1
            for i in range(len(lens)):
                totlen *= int(lens[i])
            if(totlen > 0):
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr ['+str(totlen)+' x i32],' \
                    + '['+str(totlen)+' x i32]* '+self.scopeidentdic.get(self.nowscope)[0].get(
                    key)+', i32 0, i32 0\n'
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr i32 ,i32* %g' + \
                    str(self.maxregnum-1)+', i32 '+str(pos)+'\n'
            else:
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr i32 ,i32* ' + \
                    self.scopeidentdic.get(self.nowscope)[0].get(
                        key)+', i32 '+str(pos)+'\n'
            return '%g'+str(self.maxregnum)

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
        if(self.nowscope == 0):
            return a
        else:
            if(self.nowconst == True):
                return a
            else:
                return str(a) or ''

    # def visitVardecl(self, ctx: programParser.VardeclContext):

    def visitConstdef(self, ctx: programParser.ConstdefContext):
        n = ctx.getChildCount()
        if(n == 3):
            key = self.visitIdent(ctx.getChild(0))
            nowscopedecl = self.scopeidentdic.get(self.nowscope)
            if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                nowidentdic = nowscopedecl[1]
                nowidentdic[key] = self.visitConstinitval(ctx.getChild(n-1))
                nowscopedecl[1] = nowidentdic
            else:
                lastscope = self.scopehisdic.get(self.nowscope)
                outident = self.scopeidentdic.get(lastscope)
                inident = self.scopeidentdic.get(self.nowscope)
                regout = outident[0].get(key) or outident[1].get(key)
                regin0 = inident[0].get(key)
                regin1 = inident[1].get(key)

                if(regin1 == regout):
                    nowidentdic = nowscopedecl[1]
                    nowidentdic[key] = self.visitConstinitval(
                        ctx.getChild(n-1))
                    nowscopedecl[1] = nowidentdic
                elif(regin0 == regout):
                    nowidentdic = nowscopedecl[1]
                    nowidentdic[key] = self.visitConstinitval(
                        ctx.getChild(n-1))
                    nowscopedecl[1] = nowidentdic
                    todelidentdic = nowscopedecl[0]
                    todelidentdic.pop(key)
                    nowscopedecl[0] = todelidentdic
                else:
                    exit(-1)
        else:
            key = self.visitIdent(ctx.getChild(0))
            lens = []
            for i in range(2, n-1, 3):
                lens.append(self.visitConstexp(ctx.getChild(i)))
            self.arraydic[key+'+'+str(self.nowscope)] = lens
            nowscopedecl = self.scopeidentdic.get(self.nowscope)
            totlen = 1
            for i in range(0, len(lens)):
                totlen *= int(lens[i])
            if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                nowidentdic = nowscopedecl[1]
                nowidentdic[key] = self.visitConstinitval(ctx.getChild(n-1))
                nowscopedecl[1] = nowidentdic
                self.scopeidentdic[self.nowscope] = nowscopedecl

            else:
                lastscope = self.scopehisdic.get(self.nowscope)
                outident = self.scopeidentdic.get(lastscope)
                inident = self.scopeidentdic.get(self.nowscope)
                regout = outident[0].get(key) or outident[1].get(key)
                regin0 = inident[0].get(key)
                regin1 = inident[1].get(key)
                if(regin1 == regout):
                    nowidentdic = nowscopedecl[1]
                    nowidentdic[key] = self.visitConstinitval(
                        ctx.getChild(n-1))
                    nowscopedecl[1] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl

                elif(regin0 == regout):
                    nowidentdic = nowscopedecl[1]
                    nowidentdic[key] = self.visitConstinitval(
                        ctx.getChild(n-1))
                    nowscopedecl[1] = nowidentdic
                    todelidentdic = nowscopedecl[0]
                    todelidentdic.pop(key)
                    nowscopedecl[0] = todelidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                else:
                    exit(-1)

    def visitConstinitval(self, ctx: programParser.ConstinitvalContext):
        n = ctx.getChildCount()
        self.nowconst = True
        if(n == 1):
            res = self.visitConstexp(ctx.getChild(0))
        else:
            res = []
            for i in range(1, n, 2):
                res.append(self.visitConstinitval(ctx.getChild(i)))
            return res
        self.nowconst = False
        return res

    def visitConstexp(self, ctx: programParser.ConstexpContext):
        res = self.visitAddexp(ctx.getChild(0))

        return res

    def getpos(self, pos, lens):
        # if(len(pos) != len(lens)):
        #     print('cannot compute')
        #     exit(-1)
        lena = len(pos)
        # for i in range(lena):
        #     lenb = int(pos[i])
        #     if(i < lena-1):
        #         for m in range(i+1, lena):
        #             lenb *= int(lens[m])
        #         res += lenb
        #     else:
        #         res += int(pos[i])

        if(lena == 1):
            return str(pos[0])
        lastreg = 0
        for i in range(lena):
            if(i < lena-1):
                for m in range(i+1, lena):
                    self.maxregnum += 1
                    if(m == i+1):
                        self.visitres += '%g' + \
                            str(self.maxregnum)+' = mul i32 ' + \
                            str(pos[i])+' ,'+str(lens[m])+'\n'
                    else:
                        self.visitres += '%g' + \
                            str(self.maxregnum)+' = mul i32 %g' + \
                            str(self.maxregnum-1)+' ,'+str(lens[m])+'\n'
                if(i == 0):
                    lastreg = self.maxregnum
                else:
                    self.maxregnum += 1
                    self.visitres += '%g' + \
                        str(self.maxregnum)+'= add i32 %g' + \
                        str(self.maxregnum-1)+', %g'+str(lastreg)+'\n'
                    lastreg = self.maxregnum
            else:
                self.maxregnum += 1
                self.visitres += '%g' + \
                    str(self.maxregnum)+'= add i32 %g' + \
                    str(self.maxregnum-1)+','+str(pos[i])+'\n'

        return '%g'+str(self.maxregnum)

    def compileArray(self, nums, pos: list, key, deep):
        if(type(nums) == list):
            m = len(nums)
            for i in range(m):
                pos1 = copy.deepcopy(pos)
                pos1.append(i)
                self.compileArray(nums[i], pos1, key, deep+1)
        else:
            respos = self.getpos(pos, self.arraydic.get(
                key+'+'+str(self.nowscope)))

            lens = self.arraydic.get(key+'+'+str(self.nowscope))
            totlen = 1
            for i in range(len(lens)):
                totlen *= int(lens[i])
            if(totlen > 0):
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr ['+str(totlen)+' x i32],' \
                    + '['+str(totlen)+' x i32]* '+self.scopeidentdic.get(self.nowscope)[0].get(
                    key)+', i32 0, i32 0\n'
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr i32 ,i32* %g' + \
                    str(self.maxregnum-1)+', i32 '+str(respos)+'\n'
                self.visitres += 'store i32 '+nums + \
                    ',i32* %g'+str(self.maxregnum)+'\n'
            else:
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+' = getelementptr i32, i32* ' +\
                    self.scopeidentdic.get(self.nowscope)[0].get(
                        key)+', i32 '+str(respos)+'\n'
                self.visitres += 'store i32 '+nums + \
                    ',i32* %g'+str(self.maxregnum)+'\n'

    def getInitPos(self, nums, pos: list, key, deep, allpos: dict):
        if(type(nums) == list):
            m = len(nums)
            for i in range(m):
                pos1 = copy.deepcopy(pos)
                pos1.append(i)
                self.getInitPos(nums[i], pos1, key, deep+1, allpos)
        else:
            respos = self.getnumpos(
                pos, self.arraydic.get(key+'+'+str(self.nowscope)))
            allpos[respos] = nums

    def getnumpos(self, pos, lens):
        if(len(pos) != len(lens)):
            print('cannot compute')
            exit(-1)
        lena = len(pos)
        res = 0
        for i in range(lena):
            lenb = int(pos[i])
            if(i < lena-1):
                for m in range(i+1, lena):
                    lenb *= int(lens[m])
                res += lenb
            else:
                res += int(pos[i])
        return res

    def compileGlobalArray(self, totlen, allpos: dict):
        resstr = '['
        for i in range(totlen):
            if(allpos.get(i)):
                resstr += 'i32 '+str(allpos.get(i))
            else:
                resstr += 'i32 0'
            if(i < totlen-1):
                resstr += ','
            else:
                resstr += ']'
        return resstr

    def visitAssigndef(self, ctx: programParser.AssigndefContext):
        if(self.nowscope == 0):

            n = ctx.getChildCount()
            if(n == 3):
                key = self.visitIdent(ctx.getChild(0))
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '@'+key
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    res = self.visitInitval(ctx.getChild(n-1))
                    self.visitres += '@'+key + \
                        '= dso_local global i32 '+str(res)+'\n'
                else:
                    exit(-1)
            else:
                key = self.visitIdent(ctx.getChild(0))
                lens = []
                for i in range(2, n-1, 3):
                    lens.append(self.visitConstexp(ctx.getChild(i)))
                self.arraydic[key+'+'+str(self.nowscope)] = lens
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                totlen = 1
                for i in range(0, len(lens)):
                    totlen *= int(lens[i])
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '@'+key
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    res = self.visitInitval(ctx.getChild(n-1))
                    allpos = {}
                    self.getInitPos(res, [], key, 0, allpos)
                    initstr = self.compileGlobalArray(totlen, allpos)
                    self.visitres += '@'+key + \
                        '= dso_local global [' + \
                        str(totlen)+' x i32] '+initstr+'\n'
                else:
                    exit(-1)

        else:
            n = ctx.getChildCount()
            if(n == 3):
                self.maxregnum += 1
                key = self.visitIdent(ctx.getChild(0))
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '%g'+str(self.maxregnum)
                    nowscopedecl[0] = nowidentdic
                    self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'
                    res = self.visitInitval(ctx.getChild(n-1))
                    self.visitres += 'store i32 ' + res + \
                        ', i32* '+nowscopedecl[0].get(key)+'\n'
                else:
                    lastscope = self.scopehisdic.get(self.nowscope)
                    outident = self.scopeidentdic.get(lastscope)
                    inident = self.scopeidentdic.get(self.nowscope)
                    regout = outident[0].get(key) or outident[1].get(key)
                    regin0 = inident[0].get(key)
                    regin1 = inident[1].get(key)
                    if(regin0 == regout):
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.visitres += '%g' + \
                            str(self.maxregnum)+'= alloca i32\n'
                        res = self.visitInitval(ctx.getChild(n-1))
                        self.visitres += 'store i32 ' + res + \
                            ', i32* '+nowscopedecl[0].get(key)+'\n'
                    elif(regin1 == regout):
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        todelidentdic = nowscopedecl[1]
                        todelidentdic.pop(key)
                        nowscopedecl[1] = todelidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.visitres += '%g' + \
                            str(self.maxregnum)+'= alloca i32\n'
                        res = self.visitInitval(ctx.getChild(n-1))
                        self.visitres += 'store i32 ' + res + \
                            ', i32* '+nowscopedecl[0].get(key)+'\n'

                    else:

                        exit(-1)
            else:
                self.maxregnum += 1
                key = self.visitIdent(ctx.getChild(0))
                lens = []
                oldscope = self.nowscope
                self.nowscope = 0
                for i in range(2, n-1, 3):
                    dim = self.visitConstexp(ctx.getChild(i))
                    if(int(dim) < 0):
                        print('minus define')
                        exit(-1)
                    lens.append(dim)
                self.nowscope = oldscope
                self.arraydic[key+'+'+str(self.nowscope)] = lens
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                totlen = 1
                for i in range(0, len(lens)):
                    totlen *= int(lens[i])
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):

                    self.visitres += '%g' + \
                        str(self.maxregnum) + \
                        '= alloca ['+str(totlen) + ' x i32] \n'
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '%g'+str(self.maxregnum)
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    self.maxregnum += 1
                    self.visitres += '%g'+str(self.maxregnum)+'= getelementptr ['+str(
                        totlen)+' x i32], '+'['+str(totlen)+' x i32]* %g'+str(self.maxregnum-1)+', i32 0, i32 0\n'

                    self.visitres += 'call void @memset(i32* %g'+str(
                        self.maxregnum)+', i32 0, i32 '+str(totlen*4)+')\n'
                    res = self.visitInitval(ctx.getChild(n-1))
                    self.compileArray(res, [], key, 0)
                else:
                    lastscope = self.scopehisdic.get(self.nowscope)
                    outident = self.scopeidentdic.get(lastscope)
                    inident = self.scopeidentdic.get(self.nowscope)
                    regout = outident[0].get(key) or outident[1].get(key)
                    regin0 = inident[0].get(key)
                    regin1 = inident[1].get(key)
                    if(regin0 == regout):
                        self.visitres += '%g' + \
                            str(self.maxregnum) + \
                            '= alloca ['+str(totlen) + ' x i32] \n'
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.maxregnum += 1
                        self.visitres += '%g'+str(self.maxregnum)+'= getelementptr ['+str(
                            totlen)+' x i32], '+'['+str(totlen)+' x i32]* %g'+str(self.maxregnum-1)+', i32 0, i32 0\n'

                        self.visitres += 'call void @memset(i32* %g'+str(
                            self.maxregnum)+', i32 0, i32 '+str(totlen*4)+')\n'
                        res = self.visitInitval(ctx.getChild(n-1))
                        self.compileArray(res, [], key, 0)
                    elif(regin1 == regout):

                        self.visitres += '%g' + \
                            str(self.maxregnum) + \
                            '= alloca ['+str(totlen) + ' x i32] \n'
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        todelidentdic = nowscopedecl[1]
                        todelidentdic.pop(key)
                        nowscopedecl[1] = todelidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.maxregnum += 1
                        self.visitres += '%g'+str(self.maxregnum)+'= getelementptr ['+str(
                            totlen)+' x i32], '+'['+str(totlen)+' x i32]* %g'+str(self.maxregnum-1)+', i32 0, i32 0\n'

                        self.visitres += 'call void @memset(i32* %g'+str(
                            self.maxregnum)+', i32 0, i32 '+str(totlen*4)+')\n'
                        res = self.visitInitval(ctx.getChild(n-1))
                        self.compileArray(res, [], key, 0)
                    else:
                        exit(-1)

    def visitNoassigndef(self, ctx: programParser.NoassigndefContext):
        if(self.nowscope == 0):  # 全局
            n = ctx.getChildCount()
            if(n == 1):
                key = self.visitIdent(ctx.getChild(0))
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '@'+key
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    self.visitres += '@'+key+'= dso_local global i32 0\n'
                else:
                    exit(-1)
            else:
                key = self.visitIdent(ctx.getChild(0))
                lens = []
                for i in range(2, n+1, 3):
                    lens.append(self.visitConstexp(ctx.getChild(i)))
                self.arraydic[key+'+'+str(self.nowscope)] = lens
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                totlen = 1
                for i in range(0, len(lens)):
                    totlen *= int(lens[i])
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '@'+key
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    self.visitres += '@'+key + \
                        '= dso_local global [' + \
                        str(totlen)+' x i32] zeroinitializer\n'

                else:
                    exit(-1)
        else:  # 非全局
            n = ctx.getChildCount()
            if(n == 1):  # int
                self.maxregnum += 1
                key = self.visitIdent(ctx.getChild(0))
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '%g'+str(self.maxregnum)
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'
                else:
                    lastscope = self.scopehisdic.get(self.nowscope)
                    outident = self.scopeidentdic.get(lastscope)
                    inident = self.scopeidentdic.get(self.nowscope)
                    regout = outident[0].get(key) or outident[1].get(key)
                    regin0 = inident[0].get(key)
                    regin1 = inident[1].get(key)
                    if(regin0 == regout):
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.visitres += '%g' + \
                            str(self.maxregnum)+'= alloca i32\n'
                    elif(regin1 == regout):
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        todelidentdic = nowscopedecl[1]
                        todelidentdic.pop(key)
                        nowscopedecl[1] = todelidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.visitres += '%g' + \
                            str(self.maxregnum)+'= alloca i32\n'
                    else:
                        exit(-1)
            else:  # array
                self.maxregnum += 1
                key = self.visitIdent(ctx.getChild(0))
                lens = []
                oldscope = self.nowscope
                self.nowscope = 0
                for i in range(2, n+1, 3):
                    dim = self.visitConstexp(ctx.getChild(i))
                    if(int(dim) < 0):
                        print('minus define')
                        exit(-1)
                    lens.append(dim)
                self.nowscope = oldscope
                self.arraydic[key+'+'+str(self.nowscope)] = lens
                nowscopedecl = self.scopeidentdic.get(self.nowscope)
                totlen = 1
                for i in range(0, len(lens)):
                    totlen *= int(lens[i])
                if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                    self.visitres += '%g' + \
                        str(self.maxregnum) + \
                        '= alloca ['+str(totlen) + ' x i32] \n'
                    nowidentdic = nowscopedecl[0]
                    nowidentdic[key] = '%g'+str(self.maxregnum)
                    nowscopedecl[0] = nowidentdic
                    self.scopeidentdic[self.nowscope] = nowscopedecl
                    self.maxregnum += 1
                    self.visitres += '%g'+str(self.maxregnum)+'= getelementptr ['+str(
                        totlen)+' x i32], '+'['+str(totlen)+' x i32]* %g'+str(self.maxregnum-1)+', i32 0, i32 0\n'

                    self.visitres += 'call void @memset(i32* %g'+str(
                        self.maxregnum)+', i32 0, i32 '+str(totlen*4)+')\n'
                else:
                    lastscope = self.scopehisdic.get(self.nowscope)
                    outident = self.scopeidentdic.get(lastscope)
                    inident = self.scopeidentdic.get(self.nowscope)
                    regout = outident[0].get(key) or outident[1].get(key)
                    regin0 = inident[0].get(key)
                    regin1 = inident[1].get(key)
                    if(regin0 == regout):
                        self.visitres += '%g' + \
                            str(self.maxregnum) + \
                            '= alloca ['+str(totlen) + ' x i32] \n'
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.maxregnum += 1
                        self.visitres += '%g'+str(self.maxregnum)+'= getelementptr ['+str(
                            totlen)+' x i32], '+'['+str(totlen)+' x i32]* %g'+str(self.maxregnum-1)+', i32 0, i32 0\n'

                        self.visitres += 'call void @memset(i32* %g'+str(
                            self.maxregnum)+', i32 0, i32 '+str(totlen*4)+')\n'
                    elif(regin1 == regout):
                        self.visitres += '%g' + \
                            str(self.maxregnum) + \
                            '= alloca ['+str(totlen) + ' x i32] \n'
                        nowidentdic = nowscopedecl[0]
                        nowidentdic[key] = '%g'+str(self.maxregnum)
                        nowscopedecl[0] = nowidentdic
                        todelidentdic = nowscopedecl[1]
                        todelidentdic.pop(key)
                        nowscopedecl[1] = todelidentdic
                        self.scopeidentdic[self.nowscope] = nowscopedecl
                        self.maxregnum += 1
                        self.visitres += '%g'+str(self.maxregnum)+'= getelementptr ['+str(
                            totlen)+' x i32], '+'['+str(totlen)+' x i32]* %g'+str(self.maxregnum-1)+', i32 0, i32 0\n'

                        self.visitres += 'call void @memset(i32* %g'+str(
                            self.maxregnum)+', i32 0, i32 '+str(totlen*4)+')\n'
                    else:
                        exit(-1)

    def visitInitval(self, ctx: programParser.InitvalContext):
        n = ctx.getChildCount()
        if(n == 1):
            return str(self.visitExp(ctx.getChild(0)))
        else:
            res = []
            for i in range(1, n, 2):
                res.append(self.visitInitval(ctx.getChild(i)))
            return res

    def visitAssignstmt(self, ctx: programParser.AssignstmtContext):

        res1 = self.visitLval(ctx.getChild(0))
        res2 = self.visitExp(ctx.getChild(2))
        self.visitres += 'store i32 '+str(res2)+', i32* '+str(res1)+'\n'
        self.maxregnum += 1
        self.visitres += '%g'+str(self.maxregnum) + \
            " = load i32, i32* "+str(res1)+'\n'

    def visitWhilestmt(self, ctx: programParser.WhilestmtContext):
        oldout = self.nowwhileout
        oldcond = self.nowwhilecond
        self.maxregnum += 1
        self.nowblock = str(self.maxregnum)
        self.visitres += 'br label %g'+self.nowblock+'\n'
        whileblock = self.nowblock
        self.nowwhilecond = self.nowblock
        self.maxregnum += 2
        self.nowwhileout = str(self.maxregnum)
        self.labeldic[whileblock] = [
            '%g'+str(self.maxregnum-1), '%g'+str(self.maxregnum), '%g'+str(self.maxregnum)]
        whileblockbr = [str(self.maxregnum-1),
                        str(self.maxregnum), str(self.maxregnum-2)]
        res = self.visitCond(ctx.getChild(2))
        self.visitres += 'g'+whileblockbr[0]+':\n'
        self.visitStmt(ctx.getChild(4))
        self.visitres += 'br label %g'+whileblockbr[2]+'\n'
        self.visitres += 'g'+whileblockbr[1]+':\n'
        self.nowwhileout = oldout
        self.nowwhilecond = oldcond

    def visitContinuestmt(self, ctx: programParser.ContinuestmtContext):
        self.visitres += 'br label %g'+self.nowwhilecond+'\n'

    def visitBreakstmt(self, ctx: programParser.BreakstmtContext):
        self.visitres += 'br label %g'+self.nowwhileout+'\n'

    def visitIfstmt(self, ctx: programParser.IfstmtContext):
        n = ctx.getChildCount()
        self.maxregnum += 1
        self.nowblock = str(self.maxregnum)
        self.visitres += 'br label %g'+self.nowblock+'\n'
        ifblock = self.nowblock
        self.maxregnum += 3
        self.labeldic[ifblock] = [
            '%g'+str(self.maxregnum-2), '%g'+str(self.maxregnum-1), '%g'+str(self.maxregnum)]
        ifblockbr = [str(self.maxregnum-2),
                     str(self.maxregnum-1), str(self.maxregnum)]
        res = self.visitCond(ctx.getChild(2))
        self.visitres += 'g'+ifblockbr[0]+':\n'
        self.visitStmt(ctx.getChild(4))
        self.visitres += 'br label %g'+ifblockbr[2]+'\n'

        self.visitres += 'g'+ifblockbr[1]+':\n'
        if(n > 5):
            self.visitStmt(ctx.getChild(6))
        self.visitres += 'br label %g'+ifblockbr[2]+'\n'

        self.visitres += 'g'+ifblockbr[2]+':\n'

    def visitCond(self, ctx: programParser.CondContext):
        return self.visitLOrexp(ctx.getChild(0))

    def visitLOrexp(self, ctx: programParser.LOrexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            res1 = self.visitLandexp(ctx.getChild(0))
            return res1

        else:
            lastblock = self.nowblock
            self.maxregnum += 1
            self.nowblock = str(self.maxregnum)
            self.labeldic[self.nowblock] = self.labeldic.get(lastblock)
            self.labeldic[lastblock] = [self.labeldic.get(
                self.nowblock)[0], '%g'+self.nowblock, self.labeldic.get(self.nowblock)[2]]
            res2 = self.visitLandexp(ctx.getChild(2))
            self.nowblock = lastblock

            res1 = self.visitLOrexp(ctx.getChild(0))
            return '%g'+str(self.maxregnum-1)

    def visitLandexp(self, ctx: programParser.LandexpContext):
        n = ctx.getChildCount()
        if(n == 1):

            self.visitres += 'g'+self.nowblock+':\n'
            res1 = self.visitEqexp(ctx.getChild(0))
            self.maxregnum += 1

            self.visitres += '%g'+str(self.maxregnum) + \
                '= icmp ne i32 '+str(res1)+', 0\n'
            self.visitres += 'br i1 %g'+str(self.maxregnum)+' , label '+self.labeldic.get(
                self.nowblock)[0]+' , label '+self.labeldic.get(self.nowblock)[1]+'\n'
            return '%g'+str(self.maxregnum)
        else:
            lastblock = self.nowblock
            self.maxregnum += 1
            self.nowblock = str(self.maxregnum)
            self.labeldic[self.nowblock] = self.labeldic.get(lastblock)
            self.labeldic[lastblock] = [
                '%g'+self.nowblock, self.labeldic.get(self.nowblock)[1], self.labeldic.get(self.nowblock)[2]]

            self.visitres += 'g'+self.nowblock+':\n'
            res2 = self.visitEqexp(ctx.getChild(2))

            # self.visitres+='br label %g'+self.nowblock+'\n'
            self.maxregnum += 1
            self.visitres += '%g'+str(self.maxregnum) + \
                '= icmp ne i32 '+str(res2)+' , 0\n'
            self.visitres += 'br i1 %g'+str(self.maxregnum)+' , label '+self.labeldic.get(
                self.nowblock)[0]+' , label '+self.labeldic.get(self.nowblock)[1]+'\n'

            self.nowblock = lastblock

            res1 = self.visitLandexp(ctx.getChild(0))
            return '%g'+str(self.maxregnum-1)

    def visitEqexp(self, ctx: programParser.EqexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            return self.visitRelexp(ctx.getChild(0))
        else:
            res1 = self.visitEqexp(ctx.getChild(0))
            res2 = self.visitRelexp(ctx.getChild(2))
            cmpsign = ctx.getChild(1).getText()
            self.maxregnum += 1
            if(cmpsign == "=="):
                self.visitres += '%g' + \
                    str(self.maxregnum)+' = icmp eq i32 ' + \
                    str(res1)+' ,'+str(res2)+'\n'
            else:
                self.visitres += '%g' + \
                    str(self.maxregnum)+' = icmp ne i32 ' + \
                    str(res1)+' ,'+str(res2)+'\n'
            self.maxregnum += 1
            self.visitres += '%g' + \
                str(self.maxregnum)+' = zext i1 %g' + \
                str(self.maxregnum-1)+' to i32\n'
            return '%g'+str(self.maxregnum)

    def visitRelexp(self, ctx: programParser.RelexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            return self.visitAddexp(ctx.getChild(0))
        else:
            res1 = self.visitRelexp(ctx.getChild(0))
            res2 = self.visitAddexp(ctx.getChild(2))
            cmpsign = ctx.getChild(1).getText()
            self.maxregnum += 1
            if(cmpsign == "<"):
                self.visitres += '%g' + \
                    str(self.maxregnum)+' = icmp slt i32 ' + \
                    str(res1)+' ,'+str(res2)+'\n'
            elif(cmpsign == ">"):
                self.visitres += '%g' + \
                    str(self.maxregnum)+' = icmp sgt i32 ' + \
                    str(res1)+' ,'+str(res2)+'\n'
            elif(cmpsign == "<="):
                self.visitres += '%g' + \
                    str(self.maxregnum)+' = icmp sle i32 ' + \
                    str(res1)+' ,'+str(res2)+'\n'
            elif(cmpsign == ">="):
                self.visitres += '%g' + \
                    str(self.maxregnum)+' = icmp sge i32 ' + \
                    str(res1)+' ,'+str(res2)+'\n'
            self.maxregnum += 1
            self.visitres += '%g' + \
                str(self.maxregnum)+' = zext i1 %g' + \
                str(self.maxregnum-1)+' to i32\n'
            return '%g'+str(self.maxregnum)
