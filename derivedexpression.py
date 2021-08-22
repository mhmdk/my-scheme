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


class LetBinding:
    def __init__(self, variable, init):
        self.variable = variable
        self.init = init


def make_let(bindings, body):
    parameters = FormalParameters()
    arguments = Args()
    for binding in bindings:
        parameters.append_parameter(binding.variable)
        arguments.add(binding.init)
    lambda_expression = Lambda(parameters, body)
    return Call(lambda_expression, arguments)


def make_letstar(bindings, body):
    if len(bindings) <= 1:
        return make_let(bindings, body)
    else:
        return make_let(bindings[:1], [make_letstar(bindings[1:], body)])


def make_letrec(bindings, body):
    generated_variables = [str(i) for i in range(len(bindings))]
    internal_let_bindings = [LetBinding(generated_variable, binding.init) for generated_variable, binding in
                             zip(generated_variables, bindings)]
    initialization_expressions = [Assignment(binding.variable, VariableReference(generated_variable)) for
                                  generated_variable, binding in
                                  zip(generated_variables, bindings)]
    internal_let_body = initialization_expressions + body
    outer_let_bindings = [LetBinding(binding.variable, UnAssigned()) for binding in bindings]
    outer_let_body = [make_let(internal_let_bindings, internal_let_body)]
    return make_let(outer_let_bindings, outer_let_body)


def make_lambda_body_with_internal_definitions(definitions, body):
    bindings = [LetBinding(definition.name, definition.expression) for definition in definitions]
    return [make_letrec(bindings, body)]
