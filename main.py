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
            value = evaluate(expression)
            scheme_print(value)
        except EOFError:
            break


def evaluate(program):
    lexer = Lexer(program)
    tokens = lexer.scan()
    if lexer.haserrors():
        return lexer.errors[0]
    parser = Parser(tokens)
    syntax_tree = parser.parse()
    if parser.haserrors():
        return parser.errors[0]
    return Interpreter().interpret_syntax_tree(syntax_tree)


if __name__ == '__main__':
    main()
