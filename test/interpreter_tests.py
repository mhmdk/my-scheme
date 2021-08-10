from interpreter import Interpreter
from schemeexpression import *
import unittest


class InterpreterTests(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_number_literal(self):
        number_with_leading_dot = NumberLiteral("+.1")
        number_with_trailing_dot = NumberLiteral("-1.")
        leading_dot_result = self.interpreter.visit_number_literal(number_with_leading_dot)
        trailing_dot_result = self.interpreter.visit_number_literal(number_with_trailing_dot)
        self.assertEqual(0.1, leading_dot_result)
        self.assertEqual(-1, trailing_dot_result)

    def test_bool_literal(self):
        true_literal = BoolLiteral("#t")
        false_literal = BoolLiteral("#f")
        true_result = self.interpreter.visit_bool_literal(true_literal)
        false_result = self.interpreter.visit_bool_literal(false_literal)
        self.assertEqual(True, true_result)
        self.assertEqual(False, false_result)

    def test_char_literal(self):
        space_literal = CharLiteral("#\\space")
        newline_literal = CharLiteral("#\\newline")
        t_char_literal = CharLiteral("#\\t")
        space_result = self.interpreter.visit_char_literal(space_literal)
        newline_result = self.interpreter.visit_char_literal(newline_literal)
        t_char_result = self.interpreter.visit_char_literal(t_char_literal)
        self.assertEqual(' ', space_result)
        self.assertEqual('\n', newline_result)
        self.assertEqual('t', t_char_result)

    def test_string_literal(self):
        hello_literal = StringLiteral('"hello"')
        hello_result = self.interpreter.visit_string_literal(hello_literal)
        self.assertEqual('hello', hello_result)


if __name__ == '__main__':
    unittest.main()
