from schemeobject import *


def plus(list_of_numbers):
    for scheme_number in list_of_numbers:
        if not isinstance(scheme_number, SchemeNumber):
            raise SchemeRuntimeError(f"argument {scheme_number.to_string()} is of incorrect type ")

    return SchemeNumber(sum(scheme_number.value for scheme_number in list_of_numbers))
