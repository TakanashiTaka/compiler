from antlr4.error.ErrorListener import ConsoleErrorListener
import sys
class myErrorListener(ConsoleErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        sys.exit(-1)