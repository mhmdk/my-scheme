from schemeexpression import *


def make_begin(sequence):
    return Call(Lambda(FormalParameters(), sequence))


class CondClause:
    def __init__(self, expressions, condition=None):
        self.sequence = expressions
        self.condition = condition
        self.is_else = condition is None


def make_cond(clauses):
    number_of_clauses = len(clauses)
    expression = BoolLiteral("#f")

    for index in range(number_of_clauses - 1, -1, -1):
        clause = clauses[index]
        if clause.is_else:
            expression = make_begin(clause.sequence)
        else:
            expression = Conditional(clause.condition,
                                     make_begin(clause.sequence) if len(clause.sequence) > 0 else clause.condition,
                                     expression)

    return expression
