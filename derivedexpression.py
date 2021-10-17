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


def make_and(tests):
    if len(tests) == 0:
        return BoolLiteral("#t")
    if len(tests) == 1:
        return tests[0]
    test_result_variable_name = f"{str(len(tests))}_and"
    test_result_variable_reference = VariableReference(test_result_variable_name)
    let_body = [Conditional(test_result_variable_reference, make_and(tests[1:]), test_result_variable_reference)]
    return make_let([LetBinding(test_result_variable_name, tests[0])], let_body)


def make_or(tests):
    if len(tests) == 0:
        return BoolLiteral("#f")
    test_result_variable_name = f"{str(len(tests))}_or"
    test_result_variable_reference = VariableReference(test_result_variable_name)
    let_body = [Conditional(test_result_variable_reference, test_result_variable_reference, make_or(tests[1:]))]
    return make_let([LetBinding(test_result_variable_name, tests[0])], let_body)


def make_delay(exp):
    arguments = Args()
    arguments.add(Lambda(FormalParameters(), [exp]))
    return Call(VariableReference('make-promise'), arguments)


def make_cons_stream(exp1, exp2):
    delayed_exp2 = make_delay(exp2)
    arguments = Args()
    arguments.add(exp1)
    arguments.add(delayed_exp2)
    return Call(VariableReference('cons'), arguments)
