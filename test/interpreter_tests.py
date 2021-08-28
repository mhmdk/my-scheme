from schemebuiltins import plus
from interpreter import Interpreter, SchemeRuntimeError, Environment, SchemeNumber
from schemeexpression import *
import unittest

from schemeobject import BuiltInProcedure, SchemePair, UserDefinedProcedure, make_scheme_list


def interpreter_with_variables(**kwargs):
    env = Environment()
    for key, value in kwargs.items():
        env.add(key, value)
    return Interpreter(env)


class InterpreterTests(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_number_literal(self):
        number_with_leading_dot = NumberLiteral("+.1")
        number_with_trailing_dot = NumberLiteral("-1.")
        leading_dot_result = self.interpreter.visit_number_literal(number_with_leading_dot)
        trailing_dot_result = self.interpreter.visit_number_literal(number_with_trailing_dot)
        self.assertEqual(0.1, leading_dot_result.value)
        self.assertEqual(-1, trailing_dot_result.value)

    def test_bool_literal(self):
        true_literal = BoolLiteral("#t")
        false_literal = BoolLiteral("#f")
        true_result = self.interpreter.visit_bool_literal(true_literal)
        false_result = self.interpreter.visit_bool_literal(false_literal)
        self.assertEqual(True, true_result.value)
        self.assertEqual(False, false_result.value)

    def test_char_literal(self):
        space_literal = CharLiteral("#\\space")
        newline_literal = CharLiteral("#\\newline")
        t_char_literal = CharLiteral("#\\t")
        space_result = self.interpreter.visit_char_literal(space_literal)
        newline_result = self.interpreter.visit_char_literal(newline_literal)
        t_char_result = self.interpreter.visit_char_literal(t_char_literal)
        self.assertEqual(' ', space_result.value)
        self.assertEqual('\n', newline_result.value)
        self.assertEqual('t', t_char_result.value)

    def test_string_literal(self):
        hello_literal = StringLiteral('"hello"')
        hello_result = self.interpreter.visit_string_literal(hello_literal)
        self.assertEqual('hello', hello_result.value)

    def test_symbol(self):
        hello_symbol = Symbol('hello')
        hello_result = self.interpreter.visit_symbol(hello_symbol)
        self.assertEqual('hello', hello_result.value)

    def test_true_conditional(self):
        conditional = Conditional(NumberLiteral('1'), NumberLiteral('2'), StringLiteral('"hello"'))
        conditional_result = self.interpreter.visit_conditional(conditional)
        self.assertEqual(2, conditional_result.value)

    def test_false_conditional(self):
        conditional = Conditional(BoolLiteral('#f'), NumberLiteral('2'), StringLiteral('"hello"'))
        conditional_result = self.interpreter.visit_conditional(conditional)
        self.assertEqual("hello", conditional_result.value)

    def test_unbound_variable(self):
        variable_reference = VariableReference('x')
        with self.assertRaises(SchemeRuntimeError):
            self.interpreter.visit_variable_reference(variable_reference)

    def test_bound_variable(self):
        variable_reference = VariableReference('x')
        interpreter = interpreter_with_variables(x=SchemeNumber(1))
        value = interpreter.visit_variable_reference(variable_reference)
        self.assertEqual(type(value), SchemeNumber)
        self.assertEqual(value.value, 1)

    def test_builtin_procedure_call(self):
        built_in_procedure = BuiltInProcedure(double_builtin_procedure, arity=1)
        variable_reference = VariableReference('f')
        interpreter = interpreter_with_variables(f=built_in_procedure)
        args = Args()
        args.add(NumberLiteral('2'))
        call = Call(variable_reference, args)
        result = interpreter.visit_call(call)
        self.assertEqual(result, SchemeNumber(4))

    def test_builtin_variadic_procedure_call(self):
        built_in_procedure = BuiltInProcedure(plus, variadic=True)
        result = built_in_procedure.call([make_scheme_list([SchemeNumber(2), SchemeNumber(5)])])
        self.assertEqual(result, SchemeNumber(7))

    def test_user_defined_variadic_procedure_call(self):
        formals = FormalParameters()
        formals.append_parameter("x")
        formals.append_parameter("y")
        scheme_lambda = Lambda(formals, [VariableReference('x'), VariableReference('y')])
        arguments = Args()
        arguments.add(NumberLiteral('1'))
        arguments.add(NumberLiteral('2'))
        call = Call(scheme_lambda, arguments)
        result = self.interpreter.visit_call(call)
        self.assertEqual(result, SchemeNumber(2))

    def test_user_defined_variadic_procedure_call(self):
        formals = FormalParameters()
        formals.set_list_parameter("x")
        scheme_lambda = Lambda(formals, [VariableReference('x')])
        arguments = Args()
        arguments.add(NumberLiteral('1'))
        arguments.add(NumberLiteral('2'))
        call = Call(scheme_lambda, arguments)
        result = self.interpreter.visit_call(call)
        self.assertEqual(type(result), SchemePair)
        self.assertEqual(result.car(), SchemeNumber(1))

    def test_variadic_lambda(self):
        formals = FormalParameters()
        formals.set_list_parameter("x")
        scheme_lambda = Lambda(formals, [NumberLiteral('1')])
        procedure = self.interpreter.visit_lambda(scheme_lambda)
        self.assertEqual(type(procedure), UserDefinedProcedure)
        self.assertEqual(procedure.is_variadic, True)
        self.assertEqual(procedure.parameters, ['x'])

    def test_fixed_parameters_lambda(self):
        formals = FormalParameters()
        formals.append_parameter("x")
        formals.append_parameter("y")
        scheme_lambda = Lambda(formals, [NumberLiteral('1')])
        procedure = self.interpreter.visit_lambda(scheme_lambda)
        self.assertEqual(type(procedure), UserDefinedProcedure)
        self.assertEqual(procedure.arity, 2)
        self.assertEqual(procedure.is_variadic, False)
        self.assertEqual(procedure.parameters, ['x', 'y'])

    def test_definition(self):
        definition = Definition('x', NumberLiteral('1'))
        interpreter = interpreter_with_variables()
        interpreter.visit_definition(definition)
        env = interpreter.environment
        self.assertEqual(env.get('x'), SchemeNumber(1))

    def test_assignment(self):
        assignment = Assignment('x', NumberLiteral('10'))
        interpreter = interpreter_with_variables(x=SchemeNumber(0))
        interpreter.visit_assignment(assignment)
        env = interpreter.environment
        self.assertEqual(env.get('x'), SchemeNumber(10))

    def test_assignment_of_unbound_variable(self):
        assignment = Assignment('x', NumberLiteral('10'))
        interpreter = interpreter_with_variables()
        with self.assertRaises(SchemeRuntimeError) as context:
            interpreter.visit_assignment(assignment)
        self.assertIn(context.exception.message, "variable x not bound")


def double_builtin_procedure(x):
    return SchemeNumber(x.value * 2)


if __name__ == '__main__':
    unittest.main()
