import sys

from lexer import Lexer
from parser import Parser
from schemebuiltins import *
from schemeobject import BuiltInProcedure

global_env = Environment()


def main(args):
    init_global_environment(global_env)
    if len(args) == 1:
        repl()
    else:
        filename = args[1]
        program = open(filename, 'r')
        value = scan_evaluate(program.read(), global_env)
        scheme_print(value)


def scheme_print(value):
    print(value)


def repl():
    while True:
        try:
            expression = input("-> ")
            value = scan_evaluate(expression, global_env)
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
    # equivalence predicates
    environment.add('eqv?', BuiltInProcedure(scheme_is, arity=2))
    environment.add('eq?', BuiltInProcedure(scheme_is, arity=2))
    environment.add('equal?', BuiltInProcedure(scheme_equal, arity=2))

    # numerical operations
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
    environment.add('remainder', BuiltInProcedure(remainder, arity=2))

    # booleans
    environment.add('not', BuiltInProcedure(scheme_not, arity=1))
    environment.add('boolean?', BuiltInProcedure(is_boolean, arity=1))

    # pairs and lists
    environment.add('pair?', BuiltInProcedure(is_pair, arity=1))
    environment.add('cons', BuiltInProcedure(cons, arity=2))
    environment.add('car', BuiltInProcedure(car, arity=1))
    environment.add('cdr', BuiltInProcedure(cdr, arity=1))
    environment.add('set-car!', BuiltInProcedure(set_car, arity=2))
    environment.add('set-cdr!', BuiltInProcedure(set_cdr, arity=2))
    environment.add('null?', BuiltInProcedure(is_empty_list, arity=1))
    environment.add('list?', BuiltInProcedure(is_list, arity=1))
    environment.add('list', BuiltInProcedure(make_list, variadic=True))
    environment.add('length', BuiltInProcedure(list_length, arity=1))
    environment.add('append', BuiltInProcedure(append_list, variadic=True))
    environment.add('caar', BuiltInProcedure(caar, arity=1))
    environment.add('cadr', BuiltInProcedure(cadr, arity=1))
    environment.add('cdar', BuiltInProcedure(cdar, arity=1))
    environment.add('cddr', BuiltInProcedure(cddr, arity=1))
    environment.add('caaar', BuiltInProcedure(cddr, arity=1))
    environment.add('caadr', BuiltInProcedure(caadr, arity=1))
    environment.add('cadar', BuiltInProcedure(cadar, arity=1))
    environment.add('caddr', BuiltInProcedure(caddr, arity=1))
    environment.add('cdaar', BuiltInProcedure(cdaar, arity=1))
    environment.add('cdadr', BuiltInProcedure(cdadr, arity=1))
    environment.add('cddar', BuiltInProcedure(cddar, arity=1))
    environment.add('cdddr', BuiltInProcedure(cdddr, arity=1))
    environment.add('caaaar', BuiltInProcedure(caaaar, arity=1))
    environment.add('caaadr', BuiltInProcedure(caaadr, arity=1))
    environment.add('caadar', BuiltInProcedure(caadar, arity=1))
    environment.add('caaddr', BuiltInProcedure(caaddr, arity=1))
    environment.add('cadaar', BuiltInProcedure(cadaar, arity=1))
    environment.add('cadadr', BuiltInProcedure(cadadr, arity=1))
    environment.add('caddar', BuiltInProcedure(caddar, arity=1))
    environment.add('cadddr', BuiltInProcedure(cadddr, arity=1))
    environment.add('cdaaar', BuiltInProcedure(cdaaar, arity=1))
    environment.add('cdaadr', BuiltInProcedure(cdaadr, arity=1))
    environment.add('cdadar', BuiltInProcedure(cdadar, arity=1))
    environment.add('cdaddr', BuiltInProcedure(cdaddr, arity=1))
    environment.add('cddaar', BuiltInProcedure(cddaar, arity=1))
    environment.add('cddadr', BuiltInProcedure(cddadr, arity=1))
    environment.add('cdddar', BuiltInProcedure(cdddar, arity=1))
    environment.add('cddddr', BuiltInProcedure(cddddr, arity=1))

    # control features
    environment.add('procedure?', BuiltInProcedure(is_procedure, arity=1))
    environment.add('apply', BuiltInProcedure(apply, variadic=True))
    environment.add('for-each', BuiltInProcedure(scheme_for_each, variadic=True))
    environment.add('map', BuiltInProcedure(scheme_map, variadic=True))
    environment.add('force', BuiltInProcedure(force, arity=1))
    environment.add('make-promise', BuiltInProcedure(make_promise, arity=1))

    # eval
    environment.add('eval', BuiltInProcedure(scheme_eval, arity=2))
    environment.add('scheme-report-environment', BuiltInProcedure(scheme_report_environmnt, arity=1))
    environment.add('null-environment', BuiltInProcedure(null_environment, arity=1))


def scheme_eval(quoted_expression, env):
    text = str(quoted_expression)
    return scan_evaluate(text, env)


@takes_scheme_number
def scheme_report_environmnt(version):
    env = Environment()
    init_global_environment(env)
    return env


@takes_scheme_number
def null_environment(version):
    return Environment()


if __name__ == '__main__':
    main(sys.argv)
