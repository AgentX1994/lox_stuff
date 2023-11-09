

from .error import had_error
from .debug_print import DebugAstPrinter
from .parser import Parser
from .scanner import Scanner

class PyLoxInterpreter:
    def __init__(self) -> None:
        ...

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens_iter = scanner.tokens()
        tokens = list(tokens_iter)
        for token in tokens:
            print(token)

        print('Debug Stats:')
        print(f'\tTotal Length: {len(source)}')
        print(f'\tFinal start value: {scanner.get_start()}')
        print(f'\tFinal current value: {scanner.get_current()}')
        print(f'\tTotal Lines: {scanner.get_lines()}')

        parser = Parser(tokens)
        expression = parser.parse()
        if expression is not None:
            print(DebugAstPrinter().print(expression))
        else:
            print("Had parse error!")

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