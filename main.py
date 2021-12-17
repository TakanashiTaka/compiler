import sys
from .antlr4 import *
from .antlr4.error.ErrorListener import ErrorListener
from programLexer import programLexer
from programParser import programParser
from myVisitor import myVisitor
from programVisitor import programVisitor
from myErrorListener import myErrorListener
 
def main(argv):
    input_ = FileStream(argv[1])
    lexer = programLexer(input_)
    stream = CommonTokenStream(lexer)
    parser = programParser(stream)
    parser.removeErrorListeners()
    ErrorListener = myErrorListener()
    parser.addErrorListener(ErrorListener)
    tree = parser.compunit()
    v= myVisitor()
    v.visit(tree)
    # print(tree.toStringTree())
 
if __name__ == '__main__':
    main(sys.argv)