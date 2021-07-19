from lexer import Lexer
from parser import Parser


def main():
    repl()


def repl():
    while True:
        try:
            expression = input("-> ")
            value = evaluate(expression)
            print(value)
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


if __name__ == '__main__':
    main()
