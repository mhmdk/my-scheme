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

    def test_lambda_with_conditional(self):
        should_return_first_arg = "((lambda (x y) (if (> x 0) x y) ) 10 20)"
        should_return_second_arg = "((lambda (x y) (if (> x 0) x y) ) -10 20)"
        self.assertEqual("10", self.evaluate(should_return_first_arg))
        self.assertEqual("20", self.evaluate(should_return_second_arg))

    def test_lambda_as_return_type(self):
        lambda_as_return_template = """(define (get-callable option) 
                                            (if (= option 1) 
                                                (lambda (x y) (+ x y))
                                                (lambda (x y) (- x y))))
                                        ((get-callable {0}) 2 2)"""
        should_add_args = lambda_as_return_template.format(1)
        should_subtract_args = lambda_as_return_template.format(2)
        self.assertEqual("4", self.evaluate(should_add_args))
        self.assertEqual("0", self.evaluate(should_subtract_args))

    def test_lambda_as_return_type_in_tail_context(self):
        call_option_template = """(define (get-add) (lambda (x y) (+ x y)))
                             (define (get-subtract) (lambda (x y) (- x y)))
                             (define (get-callable option) 
                                (if (= option 1) 
                                       (get-add)
                                       (get-subtract)))
                             (define (call-option option) 
                                ((get-callable option) 2 2))
                             (call-option {0})"""
        should_add_args = call_option_template.format(1)
        should_subtract_args = call_option_template.format(2)
        self.assertEqual("4", self.evaluate(should_add_args))
        self.assertEqual("0", self.evaluate(should_subtract_args))