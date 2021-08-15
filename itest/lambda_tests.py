from itest.test_setup import ExpressionTest


class LambdaTests(ExpressionTest):
    def test_simple_lambda(self):
        expression = "((lambda () 1))"
        expected = "1"
        self.assertEqual(expected, self.evaluate(expression))

    def test_argument_number_mismatch(self):
        expression = "((lambda () 1) 1)"
        self.assertIn("expects 0 argument", self.evaluate(expression))

    def test_variadic_lambda(self):
        expression = "((lambda x x) 1 2 3 4)"
        self.assertEqual("( 1 2 3 4 )", self.evaluate(expression))

    def test_lambda_with_fixed_parameters(self):
        expression = "((lambda (x y) (+ x y 1)) 10 20)"
        self.assertEqual("31", self.evaluate(expression))

    def test_lambda_with_multiple_expressions(self):
        expression = "((lambda (x y) (+ x y 1) #t) 10 20)"
        self.assertEqual("#t", self.evaluate(expression))
