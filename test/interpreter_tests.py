from schemebuiltins import plus
from interpreter import Interpreter, SchemeRuntimeError, Environment, SchemeNumber
from schemeexpression import *
import unittest

from schemeobject import BuiltInProcedure


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
        environment = Environment()
        environment.add('x', SchemeNumber(1))
        interpreter = Interpreter(environment)
        value = interpreter.visit_variable_reference(variable_reference)
        self.assertEqual(type(value), SchemeNumber)
        self.assertEqual(value.value, 1)

    def test_builtin_procedure_call(self):
        built_in_procedure = BuiltInProcedure(double_builtin_procedure, arity=1)
        variable_reference = VariableReference('f')
        environment = Environment()
        environment.add('f', built_in_procedure)
        interpreter = Interpreter(environment)
        args = Args()
        args.add(NumberLiteral('2'))
        call = Call(variable_reference, args)
        result = interpreter.visit_call(call)
        self.assertEqual(result, SchemeNumber(4))

    def test_builtin_variadic_procedure_call(self):
        built_in_procedure = BuiltInProcedure(plus, variadic=True)
        result = built_in_procedure.call([SchemeNumber(2), SchemeNumber(5)])
        self.assertEqual(result, SchemeNumber(7))


def double_builtin_procedure(x):
    return SchemeNumber(x.value * 2)


# define a mock python function and call it


if __name__ == '__main__':
    unittest.main()
