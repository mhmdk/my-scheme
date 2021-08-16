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

    def test_recursive_function(self):
        expression = "(define (fact n) ( if (> n 0) (* n (fact (- n 1))) 1) ) (fact 6)"
        expected = "720"
        self.assertEqual(expected, self.evaluate(expression))

    def test_mutation(self):
        expression = "(define (add a b) (set! a 0) (+ a b)) (add 100 2)"
        expected = "2"
        self.assertEqual(expected, self.evaluate(expression))

    def test_dynamic_scope_failure(self):
        expression = "(define (f) a) (define (g a) (f)) (g 1)"
        expected = "variable a not found"
        self.assertIn(expected, self.evaluate(expression))

    def test_top_level_function_scope(self):
        expression = "(define a #t) (define (f) a) (define (g a) (f)) (g 1)"
        expected = "#t"
        self.assertEqual(expected, self.evaluate(expression))
