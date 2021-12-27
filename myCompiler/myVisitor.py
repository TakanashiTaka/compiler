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
        self.identdic = {}
        self.constdic = {}
        self.visitres = ''
        self.funcdic = {}
        self.labeldic = {}
        self.nowblock = '0'
        self.nowif='0'
        self.scopehisdic={0:-1}
        self.scopeidentdic={0:[{},{}]}
        self.nowscope=0
        self.maxscope=0

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
        return None

    def visitFuncdef(self, ctx: programParser.FuncdefContext):
        
        n = ctx.getChildCount()
        self.visitFuncType(ctx.getChild(0))
        self.visitres += '@'+self.visitIdent(ctx.getChild(1))
        for i in range(2, n-1):
            if (ctx.getChild(i).getText() == '('):
                self.visitres += '('
            elif (ctx.getChild(i).getText() == ')'):
                self.visitres += ')'
            else:
                self.visitFuncfparams(ctx.getChild(i))
        self.visitres+='{\n'
        self.visitBlock(ctx.getChild(n-1))
        self.visitres+='}'
        return None

    def visitFuncfparams(self, ctx: programParser.FuncfparamsContext):
        return super().visitFuncfparams(ctx)

    def visitIdent(self, ctx: programParser.IdentContext):
        return ctx.getText()

    def visitBlock(self, ctx: programParser.BlockContext):
        n = ctx.getChildCount()
        for i in range(n):
            if(ctx.getChild(i).getText() == '{'):
                self.maxscope+=1
                self.scopehisdic[self.maxscope]=self.nowscope
                self.nowscope=self.maxscope
                copyold=copy.deepcopy(self.scopeidentdic.get(self.scopehisdic.get(self.nowscope)))
                self.scopeidentdic[self.nowscope]=copyold
                # print(self.scopeidentdic)
            elif(ctx.getChild(i).getText() == '}'):
                self.nowscope=self.scopehisdic.get(self.nowscope)
            else:
                self.visitBlockitem(ctx.getChild(i))
        return None

    def visitReturnstmt(self, ctx: programParser.ReturnstmtContext):
        res = None
        res = self.visitExp(ctx.getChild(1))
        self.visitres += 'ret i32 '+res+'\n'

    def visitExp(self, ctx: programParser.ExpContext):
        return self.visitAddexp(ctx.getChild(0))

    def visitAddexp(self, ctx: programParser.AddexpContext):
        n = ctx.getChildCount()
        if(self.nowscope==0):
            if(n==1):
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
                        str(self.maxregnum)+" = add i32 "+res1+','+res2+'\n'
                else:
                    self.visitres += "%g" + \
                        str(self.maxregnum)+" = sub i32 "+res1+','+res2+'\n'
                return '%g'+str(self.maxregnum)

    def visitMulexp(self, ctx: programParser.MulexpContext):
        n = ctx.getChildCount()
        if(self.nowscope==0):
            if(n==1):
                return self.visitUnaryexp(ctx.getChild(0))
            else:
                return self.visitMulexp(ctx.getChild(0))*self.visitUnaryexp(ctx.getChild(2))
        else:
            if(n == 1):
                return self.visitUnaryexp(ctx.getChild(0))
            else:
                res1 = self.visitMulexp(ctx.getChild(0))
                res2 = self.visitUnaryexp(ctx.getChild(2))
                self.maxregnum += 1
                if(ctx.getChild(1).getText() == '*'):
                    self.visitres += "%g" +   str(self.maxregnum)+" = mul i32 "+res1+','+res2+'\n'
                elif (ctx.getChild(1).getText() == '/'):
                    self.visitres += "%g" +  str(self.maxregnum)+" = sdiv i32 "+res1+','+res2+'\n'
                else:
                    self.visitres += "%g" + str(self.maxregnum)+" = srem i32 "+res1+','+res2+'\n'
                return '%g'+str(self.maxregnum)

    def visitUnaryexp(self, ctx: programParser.UnaryexpContext):
        n = ctx.getChildCount()
        if(self.nowscope==0):
            if(n==1):
                m=ctx.getChild(0).getChildCount()
                if(m==3):
                    return self.visitBraceexp(ctx.getChild(0))
                else:
                    if(ctx.getChild(0).getChild(0).getRuleIndex() == programParser.RULE_lval):
                        return self.visitLvalexp(ctx.getChild(0))
                    else:
                        # return ''
                        return self.visitNumberexp(ctx.getChild(0))
            elif(n==2):
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
                    # self.visitres+="rule index is "+str(ctx.getChild(0).getChild(0).getRuleIndex())+'\n'
                    if(ctx.getChild(0).getChild(0).getRuleIndex() == programParser.RULE_lval):
                        return self.visitLvalexp(ctx.getChild(0))
                    else:
                        # return ''
                        return self.visitNumberexp(ctx.getChild(0))
            elif(n == 2):
                if(ctx.getChild(0).getText() == '+'):
                    return self.visitUnaryexp(ctx.getChild(1))
                elif(ctx.getChild(0).getText() == '-'):
                    res = self.visitUnaryexp(ctx.getChild(1))
                    self.maxregnum += 1
                    self.visitres += '%g' + \
                        str(self.maxregnum) + '= sub i32 0 ,'+res+'\n'
                    return '%g'+str(self.maxregnum)
                else:
                    res = self.visitUnaryexp(ctx.getChild(1))
                    self.maxregnum += 1
                    self.visitres += '%g' + \
                        str(self.maxregnum) + '= icmp eq i32 '+res+', 0\n'
                    self.maxregnum += 1
                    self.visitres += '%g' + \
                        str(self.maxregnum) + '= zext i1 %g' + \
                            str(self.maxregnum-1)+' to i32\n'
                    return '%g'+str(self.maxregnum)
            else:
                identstr = self.visitIdent(ctx.getChild(0))
                if(identstr == 'getint'):
                    self.maxregnum += 1
                    if(self.funcdic.get('getint') == None):
                        self.visitres = 'declare i32 @getint()\n'+self.visitres
                        self.funcdic['getint'] = True
                    self.visitres += '%g' + \
                        str(self.maxregnum) + '= call i32 @getint()\n'
                    if(ctx.getChildCount() != 3):
                        exit(-1)
                elif(identstr == 'getch'):
                    self.maxregnum += 1
                    if(self.funcdic.get('getch') == None):
                        self.visitres = 'declare i32 @getch()\n'+self.visitres
                        self.funcdic['getch'] = True
                    self.visitres += '%g' + \
                        str(self.maxregnum) + '= call i32 @getch()\n'
                    if(ctx.getChildCount() != 3):
                        exit(-1)
                elif(identstr == 'putint'):
                    res = self.visitFuncrparams(ctx.getChild(2))
                    if(self.funcdic.get('putint') == None):
                        self.visitres = 'declare void @putint(i32)\n'+self.visitres
                        self.funcdic['putint'] = True
                    self.visitres += 'call void @putint(i32 '+res+')\n'
                    if(ctx.getChild(2).getChildCount() != 1):
                        exit(-1)
                elif(identstr == 'putch'):
                    res = self.visitFuncrparams(ctx.getChild(2))
                    if(self.funcdic.get('putch') == None):
                        self.visitres = 'declare void @putch(i32)\n'+self.visitres
                        self.funcdic['putch'] = True
                    self.visitres += 'call void @putch(i32 '+res+')\n'
                    if(ctx.getChild(2).getChildCount() != 1):
                        exit(-1)
                return '%g'+str(self.maxregnum)

    def visitFuncrparams(self, ctx: programParser.FuncrparamsContext):
        return self.visitExp(ctx.getChild(0))

    def visitBraceexp(self, ctx: programParser.BraceexpContext):
        return self.visitExp(ctx.getChild(1))

    def visitLvalexp(self, ctx: programParser.LvalexpContext):
        # self.visitLval(ctx.getChild(0))
        # print(self.scopeidentdic)
        if(self.nowscope==0):
            a=self.scopeidentdic.get(0)
            # print('a is'+str(a))
            if(a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))):
                
                res=a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))
                
                return res
            else:
                print('cannot use var to def')
                exit(-1)
                
        else:
            a=self.scopeidentdic.get(self.nowscope)
            if(a[0].get(self.visitIdent(ctx.getChild(0).getChild(0)))):
                self.maxregnum += 1
                self.visitres += '%g'+str(self.maxregnum)+" = load i32, i32* "+a[0].get(
                    self.visitIdent(ctx.getChild(0).getChild(0)))+'\n'
                return '%g'+str(self.maxregnum)
            elif(a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))):
                return a[1].get(self.visitIdent(ctx.getChild(0).getChild(0)))
            else:
                print('not defined '+self.visitIdent(ctx.getChild(0).getChild(0)))
                exit(-1)

    def visitLval(self, ctx: programParser.LvalContext):
        n = ctx.getChildCount()
        if(n == 1):
            a=self.scopeidentdic.get(self.nowscope)
            print('a is '+str(a))
            if(a[0].get(self.visitIdent(ctx.getChild(0)))):
                print(a[0].get(self.visitIdent(ctx.getChild(0))))
                return a[0].get(self.visitIdent(ctx.getChild(0)))
            elif(a[1].get(self.visitIdent(ctx.getChild(0)))):
                return a[1].get(self.visitIdent(ctx.getChild(0)))
            else:
                print('not defined '+self.visitIdent(ctx.getChild(0)) )
                exit(-1)

        return '0'

    def visitNumberexp(self, ctx: programParser.NumberexpContext):
        numstr = ctx.getText()
        # print(numstr)
        # return ''
        a = None
        if(numstr[0] == '0'):
            if (len(numstr) > 1 and (numstr[1] == 'x' or numstr[1] == 'X')):
                a = int(numstr, 16)
            else:
                a = int(numstr, 8)
        else:
            a = int(numstr, 10)
        # self.visitres+=str(a))
        if(self.nowscope==0):
            return a
        else:
            return str(a) or ''

    # def visitVardecl(self, ctx: programParser.VardeclContext):

    def visitConstdef(self, ctx: programParser.ConstdefContext):
        n = ctx.getChildCount()
        key = self.visitIdent(ctx.getChild(0))
        nowscopedecl=self.scopeidentdic.get(self.nowscope)
        # print(self.scopeidentdic)
        if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
            nowidentdic=nowscopedecl[1]
            nowidentdic[key] = self.visitConstinitval(ctx.getChild(n-1))
            nowscopedecl[1]=nowidentdic
        else:
            lastscope=self.scopehisdic.get(self.nowscope)
            outident=self.scopeidentdic.get(lastscope)
            inident=self.scopeidentdic.get(self.nowscope)
            regout=outident[0].get(key) or outident[1].get(key)
            regin = inident[0].get(key) or inident[1].get(key)
            
            if( regout == regin ):
                nowidentdic=nowscopedecl[1]
                nowidentdic[key] = self.visitConstinitval(ctx.getChild(n-1))
                nowscopedecl[1]=nowidentdic
            else:
                print('same dane~')
                exit(-1)
        
        # print(self.scopeidentdic)

    def visitConstinitval(self, ctx: programParser.ConstinitvalContext):
        return self.visitConstexp(ctx.getChild(0))

    def visitConstexp(self, ctx: programParser.ConstexpContext):
        return self.visitAddexp(ctx.getChild(0))

    def visitAssigndef(self, ctx: programParser.AssigndefContext):
        if(self.nowscope==0):
            n = ctx.getChildCount()
            key = self.visitIdent(ctx.getChild(0))
            nowscopedecl=self.scopeidentdic.get(self.nowscope)
            if(nowscopedecl[0].get(key)==None and nowscopedecl[1].get(key)==None):
                nowidentdic=nowscopedecl[0]
                nowidentdic[key]='@'+key
                nowscopedecl[0]=nowidentdic
                self.scopeidentdic[self.nowscope]=nowscopedecl
                res = self.visitInitval(ctx.getChild(n-1))
                self.visitres += '@'+key+'= dso_local global i32 '+str(res)+'\n'
            else:
                print('same dane~')
                exit(-1)

        else:
            n = ctx.getChildCount()
            self.maxregnum += 1
            key = self.visitIdent(ctx.getChild(0))
            nowscopedecl=self.scopeidentdic.get(self.nowscope)
            # print(self.scopeidentdic)
            if(nowscopedecl[0].get(key) == None and nowscopedecl[1].get(key) == None):
                nowidentdic=nowscopedecl[0]
                nowidentdic[key] = '%g'+str(self.maxregnum)
                nowscopedecl[0]=nowidentdic
                self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'                
                res = self.visitInitval(ctx.getChild(n-1))
                self.visitres += 'store i32 ' +res+ ', i32* '+nowscopedecl[0].get(key)+'\n'
            else:
                lastscope=self.scopehisdic.get(self.nowscope)
                outident=self.scopeidentdic.get(lastscope)
                inident=self.scopeidentdic.get(self.nowscope)
                regout=outident[0].get(key) or outident[1].get(key)
                regin = inident[0].get(key) or inident[1].get(key)
                # print('in is'+str(regin)+ ' out is '+ str(regout))
                if(regin == regout):
                    nowidentdic=nowscopedecl[0]
                    nowidentdic[key]='%g'+str(self.maxregnum)
                    nowscopedecl[0]=nowidentdic
                    self.scopeidentdic[self.nowscope]=nowscopedecl
                    self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'
                    res = self.visitInitval(ctx.getChild(n-1))
                    self.visitres += 'store i32 ' +res+ ', i32* '+nowscopedecl[0].get(key)+'\n'
                else:
                    print('same dane~')
                    exit(-1)
            
    def visitNoassigndef(self, ctx: programParser.NoassigndefContext):
       
        if(self.nowscope==0):
            key = self.visitIdent(ctx.getChild(0))
            nowscopedecl=self.scopeidentdic.get(self.nowscope)
            if(nowscopedecl[0].get(key)==None and nowscopedecl[1].get(key)==None):
                nowidentdic=nowscopedecl[0]
                nowidentdic[key]='@'+key
                nowscopedecl[0]=nowidentdic
                self.scopeidentdic[self.nowscope]=nowscopedecl
                self.visitres += '@'+key+'= dso_local global i32 0\n'
            else:
                print('same dane~')
                exit(-1)

        # print(nowscopedecl)
        # print('nowscope is'+str(self.nowscope))
        else:
            n = ctx.getChildCount()
            self.maxregnum += 1
            key = self.visitIdent(ctx.getChild(0))
            nowscopedecl=self.scopeidentdic.get(self.nowscope)
            if(nowscopedecl[0].get(key)==None and nowscopedecl[1].get(key)==None):
                nowidentdic=nowscopedecl[0]
                nowidentdic[key]='%g'+str(self.maxregnum)
                nowscopedecl[0]=nowidentdic
                self.scopeidentdic[self.nowscope]=nowscopedecl
                self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'
                # print(self.scopeidentdic)
            # if(self.constdic.get(key) == None and self.identdic.get(key) == None):
            #     self.identdic[key] = '%g'+str(self.maxregnum)
            #     self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'
            else:
                lastscope=self.scopehisdic.get(self.nowscope)
                outident=self.scopeidentdic.get(lastscope)
                inident=self.scopeidentdic.get(self.nowscope)
                regout=outident[0].get(key) or outident[1].get(key)
                regin = inident[0].get(key) or inident[1].get(key)
                # print('in is'+str(regin)+ ' out is '+ str(regout))
                if(regin == regout):
                    nowidentdic=nowscopedecl[0]
                    nowidentdic[key]='%g'+str(self.maxregnum)
                    nowscopedecl[0]=nowidentdic
                    self.scopeidentdic[self.nowscope]=nowscopedecl
                    self.visitres += '%g'+str(self.maxregnum)+'= alloca i32\n'
                    # print(self.scopeidentdic)
                else:
                    print('same dane~')
                    exit(-1)

    def visitInitval(self, ctx: programParser.InitvalContext):
        return self.visitExp(ctx.getChild(0))

    def visitAssignstmt(self, ctx: programParser.AssignstmtContext):
        
        res1 = self.visitLval(ctx.getChild(0))
        res2 = self.visitExp(ctx.getChild(2))
        self.visitres += 'store i32 '+res2+', i32* '+res1+'\n'
        self.maxregnum += 1
        self.visitres += '%g'+str(self.maxregnum)+" = load i32, i32* "+res1+'\n'

    def visitIfstmt(self, ctx: programParser.IfstmtContext):
        n=ctx.getChildCount()
        self.maxregnum+=1
        self.nowblock=str(self.maxregnum)
        self.nowif=self.nowblock
        self.visitres+='br label %g'+self.nowblock+'\n'
        ifblock=self.nowblock
        self.maxregnum+=3
        self.labeldic[ifblock]=['%g'+str(self.maxregnum-2),'%g'+str(self.maxregnum-1),'%g'+str(self.maxregnum)]
        ifblockbr=[str(self.maxregnum-2),str(self.maxregnum-1),str(self.maxregnum)]
        # print(self.labeldic)
        res=self.visitCond(ctx.getChild(2))
        # print(self.labeldic)
        self.visitres+='g'+ifblockbr[0]+':\n'
        self.visitStmt(ctx.getChild(4))
        self.visitres+='br label %g'+ifblockbr[2]+'\n'
        
        self.visitres+='g'+ifblockbr[1]+':\n'
        if(n>5):
            self.visitStmt(ctx.getChild(6))
        self.visitres+='br label %g'+ifblockbr[2]+'\n'
        
        self.visitres+='g'+ifblockbr[2]+':\n'
        # self.nowblock=self.labeldic.get(ifblock)[2][1:]
    
    def visitCond(self, ctx: programParser.CondContext):
        return self.visitLOrexp(ctx.getChild(0))

    def visitLOrexp(self, ctx: programParser.LOrexpContext):
        n = ctx.getChildCount()
        if(n == 1):
            res1 = self.visitLandexp(ctx.getChild(0))
            # self.visitres+=self.nowblock+':\n'
            # self.visitres += 'br i1 '+res1+' , label '+self.labeldic.get(self.nowblock)[0]+' , label '+self.labeldic.get(self.nowblock)[1]+'\n'
            return res1

        else:
            lastblock=self.nowblock
            self.maxregnum+=1
            self.nowblock=str(self.maxregnum)
            self.labeldic[self.nowblock]=self.labeldic.get(lastblock)
            self.labeldic[lastblock]=[self.labeldic.get(self.nowblock)[0],'%g'+self.nowblock,self.labeldic.get(self.nowblock)[2]]
            res2=self.visitLandexp(ctx.getChild(2))
            # self.visitres+=self.nowblock+':\n'
            # self.visitres += 'br i1 '+res2+' , label '+self.labeldic.get(self.nowblock)[0]+' , label '+self.labeldic.get(self.nowblock)[1]+'\n'
            self.nowblock=lastblock
            
            res1=self.visitLOrexp(ctx.getChild(0))
            return '%g'+str(self.maxregnum-1)

    def visitLandexp(self, ctx: programParser.LandexpContext):
        n=ctx.getChildCount()
        if(n==1):
            # print(self.labeldic)
            
            self.visitres+='g'+self.nowblock+':\n'
            res1=self.visitEqexp(ctx.getChild(0))
            # self.visitres+='br label %g'+self.nowblock+'\n'
            self.maxregnum+=1
            
            self.visitres+='%g'+str(self.maxregnum)+'= icmp ne i32 '+res1+', 0\n'
            self.visitres += 'br i1 %g'+str(self.maxregnum)+' , label '+self.labeldic.get(self.nowblock)[0]+' , label '+self.labeldic.get(self.nowblock)[1]+'\n'
            return '%g'+str(self.maxregnum)
        else:
            lastblock=self.nowblock
            self.maxregnum+=1
            self.nowblock=str(self.maxregnum)
            self.labeldic[self.nowblock]=self.labeldic.get(lastblock)
            self.labeldic[lastblock]=['%g'+self.nowblock,self.labeldic.get(self.nowblock)[1],self.labeldic.get(self.nowblock)[2]]
            
            self.visitres+='g'+self.nowblock+':\n' 
            res2=self.visitEqexp(ctx.getChild(2))
            
            # self.visitres+='br label %g'+self.nowblock+'\n'
            self.maxregnum+=1
            self.visitres+='%g'+str(self.maxregnum)+'= icmp ne i32 '+res2+' , 0\n'
            self.visitres += 'br i1 %g'+str(self.maxregnum)+' , label '+self.labeldic.get(self.nowblock)[0]+' , label '+self.labeldic.get(self.nowblock)[1]+'\n'
            
            self.nowblock=lastblock
            
            res1=self.visitLandexp(ctx.getChild(0))
            return '%g'+str(self.maxregnum-1)


    def visitEqexp(self, ctx: programParser.EqexpContext):
        n=ctx.getChildCount()
        if(n==1):
            return self.visitRelexp(ctx.getChild(0))
        else:
            res1=self.visitEqexp(ctx.getChild(0))
            res2=self.visitRelexp(ctx.getChild(2))
            cmpsign=ctx.getChild(1).getText()
            self.maxregnum+=1
            if(cmpsign=="=="):
                self.visitres+='%g'+str(self.maxregnum)+' = icmp eq i32 '+res1+' ,'+res2+'\n'
            else:
                self.visitres+='%g'+str(self.maxregnum)+' = icmp ne i32 '+res1+' ,'+res2+'\n'
            self.maxregnum+=1
            self.visitres+='%g'+str(self.maxregnum)+' = zext i1 %g'+str(self.maxregnum-1)+' to i32\n'
            return '%g'+str(self.maxregnum)
    
    def visitRelexp(self, ctx: programParser.RelexpContext):
        n=ctx.getChildCount()
        if(n==1):
            return self.visitAddexp(ctx.getChild(0))
        else:
            res1=self.visitRelexp(ctx.getChild(0))
            res2=self.visitAddexp(ctx.getChild(2))
            cmpsign=ctx.getChild(1).getText()
            self.maxregnum+=1
            if(cmpsign=="<"):
                self.visitres+='%g'+str(self.maxregnum)+' = icmp slt i32 '+res1+' ,'+res2+'\n'
            elif(cmpsign==">"):
                self.visitres+='%g'+str(self.maxregnum)+' = icmp sgt i32 '+res1+' ,'+res2+'\n'
            elif(cmpsign=="<="):
                self.visitres+='%g'+str(self.maxregnum)+' = icmp sle i32 '+res1+' ,'+res2+'\n'
            elif(cmpsign==">="):
                self.visitres+='%g'+str(self.maxregnum)+' = icmp sge i32 '+res1+' ,'+res2+'\n'
            self.maxregnum+=1
            self.visitres+='%g'+str(self.maxregnum)+' = zext i1 %g'+str(self.maxregnum-1)+' to i32\n'
            return '%g'+str(self.maxregnum)
    
