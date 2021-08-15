from itest.test_setup import ExpressionTest


class DefinitionTests(ExpressionTest):
    def test_variable_definition(self):
        expression = "(define x 1) x"
        expected = "1"
        self.assertEqual(expected, self.evaluate(expression))

    def test_variable_bound_to_lambda(self):
        expression = "(define add (lambda (a b) (+ a b))) (add 1 2)"
        expected = "3"
        self.assertEqual(expected, self.evaluate(expression))

    def test_procedure_definition(self):
        expression = "(define (add a b) (+ a b)) (add 1 2)"
        expected = "3"
        self.assertEqual(expected, self.evaluate(expression))

    def test_mutation(self):
        expression = "(define (add a b) (set! a 0) (+ a b)) (add 100 2)"
        expected = "2"
        self.assertEqual(expected, self.evaluate(expression))
