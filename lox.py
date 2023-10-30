import logging
import os
import sys

from ast_printer import AstPrinter
from error import clear_error, had_error
from parser import Parser
from scanner import Scanner


def run_file(path):
    f = open(path, 'r')
    run(f.read())
    f.close()


def run_prompt():
    while True:
        print(">> ", end="")

        try:
            line = input()
        except EOFError:
            break

        run(line)
        clear_error()


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    expr = parser.parse()

    if had_error():
        return

    ast_printer = AstPrinter()
    print(ast_printer.print(expr))


if __name__ == '__main__':
    LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
    logging.basicConfig(level=LOGLEVEL)
    logging.debug(f"ENV ARGS: {sys.argv}")

    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

    if had_error():
        sys.exit(1)
