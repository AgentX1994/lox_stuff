import argparse
from dataclasses import dataclass
from enum import auto, StrEnum
import sys
from typing import Any, Iterator, Optional

# TODO: Better error reporting
had_error = False

def error(line: int, message: str) -> None:
    # TODO: improve error reporting
    report(line, '', message)

def report(line: int, where: str, message: str) -> None:
    global had_error
    print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
    had_error = True

class TokenType(StrEnum):
    # Single Character Tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    EOF = auto()

KEYWORDS = {
    'and': TokenType.AND,
    'class': TokenType.CLASS,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'super': TokenType.SUPER,
    'this': TokenType.THIS,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE,
}

def is_valid_identifier_start(c: str) -> bool:
    return c.isalpha() or c in ['-', '_']

def is_valid_identifier_char(c: str) -> bool:
    return c.isdigit() or is_valid_identifier_start(c)

@dataclass(frozen=True)
class Token:
    typ: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self) -> str:
        return f'{self.typ:>13} {self.lexeme:>10} {self.literal}'

class Scanner:
    def __init__(self, source: str) -> None:
        self._source = source
        self._start = 0
        self._current = 0
        self._line = 1

    def is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def get_start(self) -> int:
        return self._start

    def get_current(self) -> int:
        return self._current

    def get_lines(self) -> int:
        return self._line

    def tokens(self) -> Iterator[Token]:
        while not self.is_at_end():
            self._start = self._current
            token = self._scan_token()
            if token is not None:
                yield token
        # TODO what about remaining tokens after hitting end?
        yield Token(TokenType.EOF, '', None, self._line)

    def _advance(self) -> str:
        temp = self._source[self._current]
        self._current += 1
        return temp

    def _match(self, expected: str) -> bool:
        if self.is_at_end(): return False
        if self._source[self._current] != expected: return False
        self._current += 1
        return True

    def _peek(self) -> str:
        if self.is_at_end():
            return '\0'
        else:
            return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return '\0'
        else:
            return self._source[self._current + 1]

    def _make_token(self, typ: TokenType, literal: Any = None) -> Token:
        lexeme = self._source[self._start:self._current]
        return Token(typ, lexeme, literal, self._line)

    def _string(self) -> Optional[Token]:
        while self._peek() != '"' and not self.is_at_end():
            if self._peek() == '\n':
                self._line += 1
            self._advance()
        
        if self.is_at_end():
            error(self._line, 'Unterminated string')
            return None
        
        self._advance()
        
        value = self._source[self._start+1:self._current-1]
        return self._make_token(TokenType.STRING, value)

    def _number(self) -> Optional[Token]:
        while self._peek().isdigit():
            self._advance()
        
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        
        value = self._source[self._start:self._current]
        return self._make_token(TokenType.NUMBER, float(value))

    def _identifier(self) -> Optional[Token]:
        while is_valid_identifier_char(self._peek()):
            self._advance()
        
        value = self._source[self._start:self._current]
        typ = KEYWORDS.get(value, TokenType.IDENTIFIER)
        return self._make_token(typ)

    def _scan_token(self) -> Optional[Token]:
        c = self._advance()
        if c == '(':
            return self._make_token(TokenType.LEFT_PAREN)
        if c == ')':
            return self._make_token(TokenType.RIGHT_PAREN)
        if c == '{':
            return self._make_token(TokenType.LEFT_BRACE)
        if c == '}':
            return self._make_token(TokenType.RIGHT_BRACE)
        if c == ',':
            return self._make_token(TokenType.COMMA)
        if c == '.':
            return self._make_token(TokenType.DOT)
        if c == '-':
            return self._make_token(TokenType.MINUS)
        if c == '+':
            return self._make_token(TokenType.PLUS)
        if c == ';':
            return self._make_token(TokenType.SEMICOLON)
        if c == '*':
            return self._make_token(TokenType.STAR)
        if c == '!':
            if self._match('='):
                return self._make_token(TokenType.BANG_EQUAL)
            else:
                return self._make_token(TokenType.BANG)
        if c == '=':
            if self._match('='):
                return self._make_token(TokenType.EQUAL_EQUAL)
            else:
                return self._make_token(TokenType.EQUAL)
        if c == '<':
            if self._match('='):
                return self._make_token(TokenType.LESS_EQUAL)
            else:
                return self._make_token(TokenType.LESS)
        if c == '>':
            if self._match('='):
                return self._make_token(TokenType.GREATER_EQUAL)
            else:
                return self._make_token(TokenType.GREATER)
        if c == '/':
            if self._match('/'):
                # Comment
                while (self._peek() != '\n' and not self.is_at_end()):
                    self._advance()
                return None
            elif self._match('*'):
                # multiline comment
                num_levels = 1
                while num_levels > 0:
                    if self.is_at_end():
                        error(self._line, 'Unterminated multiline comment')
                        return None
                    if self._peek() == '*' and self._peek_next() == '/':
                        # End of comment
                        self._advance()
                        self._advance()
                        num_levels -= 1
                    elif self._peek() == '/' and self._peek_next() == '*':
                        # Nested comment
                        self._advance()
                        self._advance()
                        num_levels += 1
                    else:
                        if self._peek() == '\n':
                            self._line += 1
                        self._advance()
                return None
            else:
                return self._make_token(TokenType.SLASH)
        if c in [' ', '\r', '\t']:
            return None
        if c == '\n':
            self._line += 1
            return None
        if c == '"':
            return self._string()
        if c.isdigit():
            return self._number()
        if is_valid_identifier_start(c):
            return self._identifier()
        error(self._line, f'Unexpected character: {c}')
        

class PyLoxInterpreter:
    def __init__(self) -> None:
        ...

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.tokens()
        for token in tokens:
            print(token)
        print('Debug Stats:')
        print(f'\tTotal Length: {len(source)}')
        print(f'\tFinal start value: {scanner.get_start()}')
        print(f'\tFinal current value: {scanner.get_current()}')
        print(f'\tTotal Lines: {scanner.get_lines()}')

    def run_file(self, script: str) -> bool:
        with open(script, 'r', encoding='utf-8') as script_fh:
            source = script_fh.read()
        self.run(source)
        return not had_error

    def run_prompt(self) -> None:
        global had_error
        while True:
            # TODO: Do this better
            line = input('> ')
            if not line: break
            self.run(line)
            had_error = False

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('script')
    args = arg_parser.parse_args()
    interpreter = PyLoxInterpreter()
    interpreter.run_file(args.script)
    if had_error:
        print('Errors found.')

if __name__ == '__main__':
    main()