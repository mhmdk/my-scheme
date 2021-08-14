import functools
import itertools
import operator

from schemeobject import *


def return_scheme_boolean(function):
    def wrapper(*args, **kwargs):
        return SchemeBool(function(*args, **kwargs))

    return wrapper


def return_scheme_number(function):
    def wrapper(*args, **kwargs):
        return SchemeNumber(function(*args, **kwargs))

    return wrapper


def takes_scheme_number(function):
    def wrapper(*args, **kwargs):
        check_all_are_numbers(args)
        return function(*args, **kwargs)

    return wrapper


def takes_scheme_numbers(function_name="", minimum_number_of_args=0):
    def decorated_wrapper(function):
        def wrapper(*args, **kwargs):
            check_all_are_numbers(*args)
            scheme_list = args[0]
            if scheme_list.size() < minimum_number_of_args:
                raise SchemeRuntimeError(
                    f"procedure {function_name} requires at least {minimum_number_of_args} argument{'' if minimum_number_of_args == 1 else 's'} ")
            return function(*args, **kwargs)

        return wrapper

    return decorated_wrapper


@return_scheme_boolean
def is_number(scheme_object):
    return isinstance(scheme_object, SchemeNumber)


@return_scheme_boolean
def is_integer(scheme_object):
    return is_number(scheme_object) and isinstance(scheme_object.value, int)


@return_scheme_boolean
@takes_scheme_numbers()
def numbers_equal(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] == values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_numbers()
def numbers_less(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] < values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_numbers()
def numbers_greater(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] > values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_numbers()
def numbers_less_or_equal(list_of_numbers):
    values = [number.value for number in list_of_numbers]
    if len(values) == 0:
        return True
    return all(values[i] <= values[i + 1] for i in range(0, len(values) - 1))


@return_scheme_boolean
@takes_scheme_numbers()
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
    if not is_integer(scheme_object):
        raise SchemeRuntimeError(f"procedure odd? requires an integer")
    return scheme_object.value % 2 == 1


@return_scheme_boolean
@takes_scheme_number
def is_even(scheme_object):
    if not is_integer(scheme_object):
        raise SchemeRuntimeError(f"procedure even? requires an integer")
    return scheme_object.value % 2 == 0


@return_scheme_number
@takes_scheme_numbers('max', 1)
def numbers_max(list_of_numbers):
    return max([number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_numbers('min', 1)
def numbers_min(list_of_numbers):
    return min([number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_numbers()
def plus(list_of_numbers):
    return sum(scheme_number.value for scheme_number in list_of_numbers)


@return_scheme_number
@takes_scheme_numbers()
def minus(list_of_numbers):
    return functools.reduce(operator.sub, [number.value for number in list_of_numbers], 0)


@return_scheme_number
@takes_scheme_numbers()
def multiply(list_of_numbers):
    return functools.reduce(operator.mul, [number.value for number in list_of_numbers], 1)


@return_scheme_number
@takes_scheme_numbers('/', 1)
def divide(list_of_numbers):
    return functools.reduce(operator.truediv, [number.value for number in list_of_numbers])


@return_scheme_number
@takes_scheme_number
def absolute_value(scheme_object):
    return abs(scheme_object.value)


def check_all_are_numbers(list_of_arguments):
    for scheme_object in list_of_arguments:
        check_argument_is_number(scheme_object)


def check_argument_is_number(scheme_object):
    if not is_number(scheme_object):
        raise SchemeRuntimeError(f"argument {scheme_object} is of incorrect type ")
