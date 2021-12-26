import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from programLexer import programLexer
from programParser import programParser
from myVisitor import myVisitor
from programVisitor import programVisitor
from myErrorListener import myErrorListener
 
def main(argv):
    input_ = FileStream(argv[1])
    lexer = programLexer(input_)
    stream = CommonTokenStream(lexer)
    # print('lexer ok')
    parser = programParser(stream)
    # print('parser ok')
    parser.removeErrorListeners()
    ErrorListener = myErrorListener()
    parser.addErrorListener(ErrorListener)
    # print('new error added')
    tree = parser.compunit()
    # print('finish')
    v= myVisitor()
    v.visit(tree)
    # print(v.visitres)
    # print(input_)
    # print('visit finish')
    # print(tree.toStringTree(programParser.ruleNames))

if __name__ == '__main__':
    main(sys.argv)
