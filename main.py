import sys

from interpreter import Interpreter, Environment
from lexer import Lexer
from parser import Parser
from schemebuiltins import *
from schemeobject import BuiltInProcedure

global_env = Environment()


def main():
    init_global_environment(global_env)
    args = sys.argv
    if len(args) == 1:
        repl()
    else:
        filename = args[1]
        program = open(filename, 'r')
        scan_evaluate(program.read(), global_env)


def scheme_print(value):
    print(value)


def repl():
    while True:
        try:
            expression = input("-> ")
            value = scan_evaluate(expression, global_env)
            if value is not None:
                scheme_print(value)
        except EOFError:
            break


def scan_evaluate(expression, environment):
    try:
        syntax_tree = scan(expression)
        return evaluate(syntax_tree, environment)

    except (ScanException, ParseException) as scan_exception:
        return '\n'.join(scan_exception.errors)


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


def evaluate(syntax_tree, environment):
    interpreter = Interpreter(environment)
    return interpreter.interpret_syntax_tree(syntax_tree)


class ParseException(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


class ScanException(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


def init_global_environment(environment):
    environment.add('number?', BuiltInProcedure(is_number, arity=1))
    environment.add('integer?', BuiltInProcedure(is_integer, arity=1))
    environment.add('<', BuiltInProcedure(numbers_less, variadic=True))
    environment.add('<=', BuiltInProcedure(numbers_less_or_equal, variadic=True))
    environment.add('>', BuiltInProcedure(numbers_greater, variadic=True))
    environment.add('>=', BuiltInProcedure(numbers_greater_or_equal, variadic=True))
    environment.add('=', BuiltInProcedure(numbers_equal, variadic=True))
    environment.add('zero?', BuiltInProcedure(is_zero, arity=1))
    environment.add('positive?', BuiltInProcedure(is_positive, arity=1))
    environment.add('negative?', BuiltInProcedure(is_negative, arity=1))
    environment.add('odd?', BuiltInProcedure(is_odd, arity=1))
    environment.add('even?', BuiltInProcedure(is_even, arity=1))
    environment.add('max', BuiltInProcedure(numbers_max, variadic=True))
    environment.add('min', BuiltInProcedure(numbers_min, variadic=True))
    environment.add('+', BuiltInProcedure(plus, variadic=True))
    environment.add('-', BuiltInProcedure(minus, variadic=True))
    environment.add('*', BuiltInProcedure(multiply, variadic=True))
    environment.add('/', BuiltInProcedure(divide, variadic=True))
    environment.add('abs', BuiltInProcedure(absolute_value, arity=1))



if __name__ == '__main__':
    main()
