from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def main():
    repl()

def scheme_print(value):
    print(value.to_string())

def repl():
    while True:
        try:
            expression = input("-> ")
            syntax_tree = scan(expression)
            value = evaluate(syntax_tree)
            scheme_print(value)
        except EOFError:
            break
        except ScanException as scan_exception:
            for error in scan_exception.errors:
                print(error)
        except ParseException as parse_exception:
            for error in parse_exception.errors:
                print(error)



def scan(program):
    lexer = Lexer(program)
    tokens = lexer.scan()
    if lexer.haserrors():
        raise ScanException(lexer.errors)
    parser = Parser(tokens)
    syntax_tree = parser.parse()
    if parser.haserrors():
        raise ParseException(parser.errors)
    return syntax_tree


def evaluate(syntax_tree):
    return Interpreter().interpret_syntax_tree(syntax_tree)


class ParseException(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


class ScanException(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

if __name__ == '__main__':
    main()
