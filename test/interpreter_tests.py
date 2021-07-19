from interpreter import Interpreter
from parser import NumberLiteral
import unittest


class InterpreterTests(unittest.TestCase):
    def test_number_literal(self):
        number_with_leading_dot = NumberLiteral("+.1")
        number_with_trailing_dot = NumberLiteral("-1.")
        leading_dot_result = Interpreter().visit_number_literal(number_with_leading_dot)
        trailing_dot_result = Interpreter().visit_number_literal(number_with_trailing_dot)
        self.assertEqual(0.1, leading_dot_result)
        self.assertEqual(-1, trailing_dot_result)

if __name__ == '__main__':
    unittest.main()