import argparse

from pylox.debug_print import DebugAstPrinter, DebugRpnPrinter


from . import PyLoxInterpreter
from .asts import BinaryExpression, GroupingExpression, LiteralExpression, UnaryExpression
from .error import had_error
from .scanner import Token, TokenType

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('script', nargs='?', default=None)
    arg_parser.add_argument('--debug-expression', action='store_true')
    arg_parser.add_argument('--debug-rpn', action='store_true')
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
    elif args.debug_rpn:
        expression = BinaryExpression(
            BinaryExpression(
                LiteralExpression(1),
                Token(TokenType.PLUS, '+', None, 1),
                LiteralExpression(2)
            ),
            Token(TokenType.STAR, '*', None, 1),
            BinaryExpression(
                LiteralExpression(4),
                Token(TokenType.MINUS, '-', None, 1),
                LiteralExpression(3)
            )
        )
        print(DebugRpnPrinter().print(expression))
    elif args.script is not None:
        interpreter = PyLoxInterpreter()
        interpreter.run_file(args.script)
        if had_error:
            print('Errors found.')
    else:
        interpreter = PyLoxInterpreter()
        interpreter.run_prompt()

if __name__ == '__main__':
    main()