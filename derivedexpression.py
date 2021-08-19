from schemeexpression import *


def make_begin(sequence):
    return Call(Lambda(FormalParameters(), sequence))
