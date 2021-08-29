import functools
import operator

from interpreter import Interpreter
from schemeobject import *


def return_scheme_boolean(function):
    def wrapper(*args, **kwargs):
        return SchemeBool(function(*args, **kwargs))

    return wrapper


def return_scheme_number(function):
    def wrapper(*args, **kwargs):
        return SchemeNumber(function(*args, **kwargs))

    return wrapper


def check_argument_type(scheme_object, check_function):
    if not check_function(scheme_object):
        raise SchemeRuntimeError(f"argument {scheme_object} is of incorrect type ")


def make_check_and_call_function(function_to_call, check_type_function):
    def wrapper(*args, **kwargs):
        check_argument_type(args[0], check_type_function)
        return function_to_call(*args, **kwargs)

    return wrapper


def takes_scheme_pair(function):
    return make_check_and_call_function(function, is_pair)


def takes_scheme_number(function):
    return make_check_and_call_function(function, is_number)


def takes_scheme_list(function):
    return make_check_and_call_function(function, is_list)


def minimum_required_args(function_name, minimum_number_of_args):
    def decorated_wrapper(function):
        def wrapper(*args, **kwargs):
            scheme_list = args[0]
            if scheme_list.size() < minimum_number_of_args:
                raise SchemeRuntimeError(
                    f"procedure {function_name} requires at least {minimum_number_of_args} argument{'' if minimum_number_of_args == 1 else 's'} ")
            return function(*args, **kwargs)

        return wrapper

    return decorated_wrapper


def takes_scheme_list_of_numbers(function):
    def wrapper(*args, **kwargs):
        scheme_list = args[0]
        for scheme_object in scheme_list:
            check_argument_type(scheme_object, is_number)
        return function(*args, **kwargs)

    return wrapper


# equivalence predicates

@return_scheme_boolean
def scheme_is(object1, object2):
    if type(object1) in [SchemeNumber, SchemeChar]:
        return object1 == object2
    else:
        return object1 is object2


@return_scheme_boolean
def scheme_equal(object1, object2):
    return object1 == object2


# numerical operations

@return_scheme_boolean
def is_number(scheme_object):
    return isinstance(scheme_object, SchemeNumber)


@return_scheme_boolean
def is_integer(scheme_object):
    return is_number(scheme_object) and isinstance(scheme_object.value, int)


@return_scheme_boolean
@takes_scheme_list_of_numbers
def numbers_equal(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] == values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_list_of_numbers
def numbers_less(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] < values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_list_of_numbers
def numbers_greater(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] > values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_list_of_numbers
def numbers_less_or_equal(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] <= values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_list_of_numbers
def numbers_greater_or_equal(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] >= values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_number
def is_zero(scheme_object):
    return scheme_object.value == 0


@return_scheme_boolean
@takes_scheme_number
def is_positive(scheme_object):
    return scheme_object.value > 0


@return_scheme_boolean
@takes_scheme_number
def is_negative(scheme_object):
    return scheme_object.value < 0


@return_scheme_boolean
@takes_scheme_number
def is_odd(scheme_object):
    return scheme_object.value % 2 == 1


@return_scheme_boolean
@takes_scheme_number
def is_even(scheme_object):
    return scheme_object.value % 2 == 0


@return_scheme_number
@takes_scheme_list_of_numbers
@minimum_required_args('max', 1)
def numbers_max(list_of_numbers):
    return max([number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_list_of_numbers
@minimum_required_args('min', 1)
def numbers_min(list_of_numbers):
    return min([number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_list_of_numbers
def plus(list_of_numbers):
    return sum(scheme_number.value for scheme_number in list_of_numbers)


@return_scheme_number
@takes_scheme_list_of_numbers
@minimum_required_args('-', 1)
def minus(list_of_numbers):
    if list_of_numbers.size() == 1:
        return - list_of_numbers.car().value
    return functools.reduce(operator.sub, [number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_list_of_numbers
def multiply(list_of_numbers):
    return functools.reduce(operator.mul, [number.value for number in list_of_numbers], 1)


@return_scheme_number
@takes_scheme_list_of_numbers
@minimum_required_args('/', 1)
def divide(list_of_numbers):
    if list_of_numbers.size() == 1:
        return 1 / list_of_numbers.car().value
    return functools.reduce(operator.truediv, [number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_number
def absolute_value(scheme_object):
    return abs(scheme_object.value)


# booleans
@return_scheme_boolean
def scheme_not(scheme_object):
    return not Interpreter.truth(scheme_object)


@return_scheme_boolean
def is_boolean(scheme_object):
    return isinstance(scheme_object, SchemeBool)


# lists

@return_scheme_boolean
def is_pair(scheme_object):
    return isinstance(scheme_object, SchemePair)


def cons(first, second):
    return SchemePair(first, second)


@takes_scheme_pair
def car(scheme_pair):
    return scheme_pair.car()


@takes_scheme_pair
def cdr(scheme_pair):
    return scheme_pair.cdr()


@takes_scheme_pair
def set_car(scheme_pair, value):
    scheme_pair.set_car(value)


@takes_scheme_pair
def set_cdr(scheme_pair, value):
    scheme_pair.set_cdr(value)


@return_scheme_boolean
def is_empty_list(scheme_object):
    return scheme_object == SchemeEmptyList()


@return_scheme_boolean
def is_list(scheme_object):
    return is_scheme_list(scheme_object)


def make_list(scheme_objects):
    return scheme_objects


@return_scheme_number
@takes_scheme_list
def list_length(scheme_list):
    return scheme_list_length(scheme_list)


@takes_scheme_list
@minimum_required_args('append', 1)
def append_list(scheme_objects):
    check_append_args(scheme_objects)
    while scheme_objects.cdr() is not SchemeEmptyList() and scheme_objects.car() is SchemeEmptyList():
        scheme_objects = scheme_objects.cdr()
    first_non_empty_list_or_last_element = scheme_objects.car()
    while scheme_objects.cdr() is not SchemeEmptyList():
        current = scheme_list_tail(scheme_objects.car())
        next_arg = scheme_objects.cdr()
        current.set_cdr(next_arg.car() if is_list(next_arg) else next_arg)
        scheme_objects = scheme_objects.cdr()
    return first_non_empty_list_or_last_element


def check_append_args(args):
    while args.cdr() is not SchemeEmptyList():
        check_argument_type(args.car(), is_list)
        args = args.cdr()


# control features
@return_scheme_boolean
def is_procedure(scheme_object):
    return isinstance(scheme_object, SchemeProcedure)


def check_map_args(args):
    check_argument_type(args[0], is_procedure)
    for arg in args[1:len(args)]:
        check_argument_type(arg, is_list)


def check_apply_args(args):
    check_argument_type(args[0], is_procedure)
    check_argument_type(args[len(args) - 1], is_list)


def apply_impl(procedure, args):
    # TODO add tests in combination with closures
    return Interpreter().do_apply(procedure, args)


@minimum_required_args('apply', 2)
def apply(scheme_objects):
    args = list(scheme_objects)
    check_apply_args(args)
    number_of_args = len(args)
    procedure = args[0]
    final_argument = args[number_of_args - 1]
    args_to_pass = args[1:number_of_args - 1]
    args_to_pass.extend(final_argument)
    return apply_impl(procedure, args_to_pass)


@minimum_required_args('for-each', 2)
def scheme_for_each(scheme_objects):
    scheme_map(scheme_objects)
    return SchemeSymbol('ok')


@minimum_required_args('map', 2)
def scheme_map(scheme_objects):
    args = list(scheme_objects)
    check_map_args(args)
    number_of_args = len(args)
    procedure = args[0]
    lists = [list(arg) for arg in args[1:number_of_args]]
    results = []
    for tuple_of_args_to_pass in zip(*lists):
        args_to_pass = list(tuple_of_args_to_pass)
        result = apply_impl(procedure, args_to_pass)
        results.append(result)
    return make_scheme_list(results)


def force(promise):
    pass


def make_promise(proc):
    pass
