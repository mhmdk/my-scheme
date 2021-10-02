from itest.test_setup import ExpressionTest


class DerivedExpressionsTest(ExpressionTest):
    def test_begin(self):
        expression = "(begin 1 #t (if #t (+ 5 6) 2) )"
        expected = "11"
        self.assertEqual(expected, self.evaluate(expression))

    def test_cond(self):
        expression = "(cond (#f 1) (#f 5) (#t 10) (else 20))"
        expected = "10"
        self.assertEqual(expected, self.evaluate(expression))

    def test_let(self):
        expression = "(let ((x 2) (y 5)) (* x y))"
        expected = "10"
        self.assertEqual(expected, self.evaluate(expression))

    def test_letstar(self):
        expression = "(let* ( (x 2) (y (+ x 1)) ) (* x y))"
        expected = "6"
        self.assertEqual(expected, self.evaluate(expression))

    def test_letrec_unassigned_variable_used(self):
        expression = "(letrec ( (x 2) (y (+ x 1)) ) (* x y))"
        expected = "variable x Unassigned"
        self.assertIn(expected, self.evaluate(expression))

    def test_letrec(self):
        expression = '''(letrec 
        ((even? (lambda (n) (if (zero? n) #t (odd? (- n 1)))))
        (odd? (lambda (n) (if (zero? n) #f (even? (- n 1))))))
        (even? 88))'''
        expected = "#t"
        self.assertEqual(expected, self.evaluate(expression))

    def test_internal_definition(self):
        expression = '''( define (f x)
        (define even? (lambda (n) (if (zero? n) #t (odd? (- n 1)))))
        (define odd? (lambda (n) (if (zero? n) #f (even? (- n 1)))))
        (even? x))
        (f 88)'''
        expected = "#t"
        self.assertEqual(expected, self.evaluate(expression))

    def test_interdependent_internal_definition(self):
        expression = '''(let ((a 1))
        (define (f x)
        (define b (+ a x))
        (define a 5)
        (+ a b))
        (f 10))'''
        expected = "variable a Unassigned"
        self.assertIn(expected, self.evaluate(expression))

    def test_and(self):
        expression = "(and #t (+ 1 2) (zero? 0) )"
        expected = "#t"
        self.assertEqual(expected, self.evaluate(expression))

    def test_or(self):
        expression = "(or #f (+ 1 2) (undefined_function 1 2) )"
        expected = "3"
        self.assertEqual(expected, self.evaluate(expression))

    def test_delay(self):
        expression = """
        (define x 1)
        (define lazy (delay (+ 1 x)))
        (define eager  (+ 1 x))
        (set! x 10)
        (cons (force lazy) eager)"""
        expected = "( 11 . 2 )"
        self.assertEqual(expected, self.evaluate(expression))

    def test_promise_should_be_evaluated_only_once(self):
        expression = """
        (define count 0)
        (define p
          (delay (begin (set! count (+ count 1))
                        (if (> count x)
                            count
                            (force p)))))
        (define x 5)
        (force p)                     ;;===>  6
        (begin (set! x 10)
        (force p))             ;;===>  6"""

        expected = "6"
        self.assertEqual(expected, self.evaluate(expression))

    def test_promise_should_be_evaluated_only_once_when_referring_to_itself(self):
        expression = """
        (define count 0)
        (define p
          (delay (begin (set! count (+ count 1))
                        (if (> count x)
                            count
                            (+ (force p) 1) ))))
        (define x 5)
        (force p)"""

        expected = "6"
        self.assertEqual(expected, self.evaluate(expression))
