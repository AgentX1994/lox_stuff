

from .scanner import Scanner
from .error import had_error

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