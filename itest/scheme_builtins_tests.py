from itest.test_setup import ExpressionTest


class SchemeBuiltinsTest(ExpressionTest):

    def test_arithmetics(self):
        expression = "(+ 1 2 (- 3) (* 4 5) (/ 6 3 1) )"
        expected = "22.0"
        self.assertEqual(expected, self.evaluate(expression))

    def test_subtract_two_numbers(self):
        expression = "(- 6 1)"
        expected = "5"
        self.assertEqual(expected, self.evaluate(expression))

    def test_minus_with_one_arg(self):
        expression = "(- 1)"
        expected = "-1"
        self.assertEqual(expected, self.evaluate(expression))

    def test_divide_two_numbers(self):
        expression = "(/ 6 2)"
        expected = "3.0"
        self.assertEqual(expected, self.evaluate(expression))

    def test_division_with_one_arg(self):
        expression = "(/ 2)"
        expected = "0.5"
        self.assertEqual(expected, self.evaluate(expression))

    def test_number_comparison(self):
        self.assertEqual("#t", self.evaluate("(< 1 2 3.2 6 )"))
        self.assertEqual("#f", self.evaluate("(<= 2 1)"))
        self.assertEqual("#f", self.evaluate("(> 2 1 6 )"))
        self.assertEqual("#t", self.evaluate("(>= 1 1 0.5 0.1 )"))
        self.assertEqual("#t", self.evaluate("(= 1 1 1 )"))

    def test_number_type_predicates(self):
        self.assertEqual("#t", self.evaluate("(number? 1 )"))
        self.assertEqual("#f", self.evaluate("(number? #\\a)"))
        self.assertEqual("#t", self.evaluate("(integer? 4 )"))
        self.assertEqual("#f", self.evaluate("(integer? 6.7  )"))

    def test_number_sign_predicates(self):
        self.assertEqual("#t", self.evaluate("(positive? 1 )"))
        self.assertEqual("#f", self.evaluate("(positive? -1)"))
        self.assertEqual("#t", self.evaluate("(zero? 0 )"))
        self.assertEqual("#f", self.evaluate("(zero? 6.7  )"))
        self.assertEqual("#f", self.evaluate("(negative? 0 )"))
        self.assertEqual("#t", self.evaluate("(negative? -100001  )"))

    def test_min(self):
        self.assertEqual("1", self.evaluate("(min 1 )"))
        self.assertEqual("-100", self.evaluate("(min -2 5 6 7 -100 8)"))
        self.assertTrue(self.evaluate("(min )").count("at least 1 argument") > 0)

    def test_max(self):
        self.assertEqual("-1001.6", self.evaluate("(max -1001.6 )"))
        self.assertEqual("8", self.evaluate("(max -2 5 6 7 -100 8)"))
        self.assertTrue(self.evaluate("(max )").count("at least 1 argument") > 0)

    def test_abs(self):
        self.assertEqual("1001.6", self.evaluate("(abs -1001.6 )"))
        self.assertEqual("8", self.evaluate("(abs 8)"))

    # booleans

    def test_not(self):
        self.assertEqual("#f", self.evaluate("(not 0)"))
        self.assertEqual("#f", self.evaluate("(not 1)"))
        self.assertEqual("#t", self.evaluate("(not #f)"))
        self.assertEqual("#f", self.evaluate("(not #t)"))
        self.assertEqual("#f", self.evaluate("(not (quote ()))"))
        self.assertEqual("#f", self.evaluate("(not (quote (1 2)))"))

    def test_is_boolean(self):
        self.assertEqual("#t", self.evaluate("(boolean? #f)"))
        self.assertEqual("#f", self.evaluate("(boolean? (quote (1)) )"))
        self.assertEqual("#f", self.evaluate("(boolean? 2)"))

    # pairs and lists

    def test_is_pair(self):
        self.assertEqual("#t", self.evaluate("(pair? (cons 1 2))"))
        self.assertEqual("#t", self.evaluate("(pair? (quote (1 2 3)))"))
        self.assertEqual("#f", self.evaluate("(pair? (lambda () 2))"))
        self.assertEqual("#f", self.evaluate("(pair? #t)"))

    def test_cons(self):
        self.assertEqual("( 1 . 2 )", self.evaluate("(cons 1 2)"))

    def test_car(self):
        self.assertEqual("1", self.evaluate("(car (cons 1 2))"))
        self.assertEqual("#f", self.evaluate("(car (car (cons (cons #f 2) 2)))"))
        self.assertEqual("1", self.evaluate("(car (quote (1 2 3)))"))

    def test_cdr(self):
        self.assertEqual("2", self.evaluate("(cdr (cons 1 2))"))
        self.assertEqual("( 3 )", self.evaluate("(cdr (cdr (quote (1 2 3))))"))

    def test_set_car(self):
        self.assertEqual("1", self.evaluate("( (lambda (p) (set-car! p 1) (car p)) (cons #t #t))"))

    def test_set_cdr(self):
        self.assertEqual("1", self.evaluate("( (lambda (p) (set-cdr! p 1) (cdr p)) (quote (#t #t) ))"))

    def test_is_null(self):
        self.assertEqual("#f", self.evaluate("(null? (cons 1 2))"))
        self.assertEqual("#f", self.evaluate("(null? 0)"))
        self.assertEqual("#f", self.evaluate("(null? #f)"))
        self.assertEqual("#f", self.evaluate("(null? (quote (1 2 3)))"))
        self.assertEqual("#t", self.evaluate("(null? (quote ()))"))

    def test_is_list(self):
        self.assertEqual("#f", self.evaluate("(list? (cons 1 2))"))
        self.assertEqual("#f", self.evaluate("(list? #t)"))
        self.assertEqual("#t", self.evaluate("(list? (quote (1 2 3)))"))
        self.assertEqual("#t", self.evaluate("(list? (quote ()))"))

    def test_length(self):
        self.assertIn("incorrect type", self.evaluate("(length (cons 1 2))"))
        self.assertEqual("2", self.evaluate("(length (quote ( 1 2)))"))
        self.assertEqual("1", self.evaluate("(length (cons 2 (quote ()) ))"))

    def test_list(self):
        self.assertEqual("( 1 2 #t )", self.evaluate("(list 1 2 #t)"))
        self.assertEqual("( 3 #t ( a b ) )", self.evaluate("(list (+ 1 2) (not #f) (quote (a b)))"))
        self.assertEqual("()", self.evaluate("(list )"))

    def test_append(self):
        self.assertEqual("()", self.evaluate("(append (quote ()) )"))
        self.assertEqual("1", self.evaluate("(append (quote ()) 1 )"))
        self.assertEqual("( 1 2 )", self.evaluate("(append (quote (1 2)) (quote ()) )"))
        self.assertEqual("( 1 2 3 4 5 )", self.evaluate("(append (list 1 2 3) (list 4 5) )"))
        self.assertEqual("( 1 . ( 2 . ( 3 . ( 4 . ( 5 . ( 6 . 7 ) ) ) ) ) )",
                         self.evaluate("(append (list 1 2 3) (list 4 5) (cons 6 7) )"))
