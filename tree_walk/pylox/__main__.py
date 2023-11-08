import argparse

from pylox.debug_print import DebugAstPrinter


from . import PyLoxInterpreter
from .asts import BinaryExpression, GroupingExpression, LiteralExpression, UnaryExpression
from .error import had_error
from .scanner import Token, TokenType

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('script')
    arg_parser.add_argument('--debug-expression', action='store_true')
    args = arg_parser.parse_args()
    if args.debug_expression:
        expression = BinaryExpression(
            UnaryExpression(
                Token(TokenType.MINUS, '-', None, 1),
                LiteralExpression(123)
            ),
            Token(TokenType.STAR, '*', None, 1),
            GroupingExpression(LiteralExpression(45.67))
        )
        print(DebugAstPrinter().print(expression))
    else:
        interpreter = PyLoxInterpreter()
        interpreter.run_file(args.script)
        if had_error:
            print('Errors found.')

if __name__ == '__main__':
    main()