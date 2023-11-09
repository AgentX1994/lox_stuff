from typing import Optional
from .error import report
from .asts import BinaryExpression, Expression, GroupingExpression, LiteralExpression, UnaryExpression
from .scanner import Token, TokenType

class ParseError(RuntimeError):
    ...


def parse_error(token: Token, error_message: str) -> ParseError:
    if token.typ == TokenType.EOF:
        report(token.line, ' at end', error_message)
    else:
        report(token.line, f' at "{token.lexeme}"', error_message)
    return ParseError()


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Optional[Expression]:
        try:
            return self._expression()
        except ParseError:
            return None

    def is_at_end(self) -> bool:
        return self._peek().typ == TokenType.EOF
    
    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current-1]

    def _check(self, expected: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self._peek().typ == expected

    def _advance(self) -> Token:
        if not self.is_at_end():
            self._current += 1
        return self._previous()

    def _match(self, *expected_types: TokenType) -> bool:
        for expected in expected_types:
            if self._check(expected):
                self._advance()
                return True
        return False

    def _consume(self, expected: TokenType, error_message: str) -> Token:
        if self._check(expected):
            return self._advance()
        
        raise parse_error(self._peek(), error_message)

    def _expression(self) -> Expression:
        return self._equality()

    def _equality(self) -> Expression:
        expression = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _comparison(self) -> Expression:
        expression = self._term()

        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _term(self) -> Expression:
        expression = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _factor(self) -> Expression:
        expression = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _unary(self) -> Expression:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return UnaryExpression(operator, right)

        return self._primary()

    def _primary(self) -> Expression:
        if self._match(TokenType.FALSE):
            return LiteralExpression(False)
        if self._match(TokenType.TRUE):
            return LiteralExpression(True)
        if self._match(TokenType.NIL):
            return LiteralExpression(None)
        
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpression(self._previous().literal)
        
        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, 'Expected ) after expression')
            return GroupingExpression(expression)
        
        raise parse_error(self._peek(), 'Expected an expression')
