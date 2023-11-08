import sys

# TODO: Better error reporting
had_error = False

def error(line: int, message: str) -> None:
    # TODO: improve error reporting
    report(line, '', message)

def report(line: int, where: str, message: str) -> None:
    global had_error
    print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
    had_error = True