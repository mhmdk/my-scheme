from itest.test_setup import ExpressionTest


class SchemeBuiltinsTest(ExpressionTest):

    def test_arithmetics(self):
        expression = "(+ 1 2 (- 3) (* 4 5) (/ 6 3 1) )"
        expected = "22.0"
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
        self.assertTrue( self.evaluate("(min )").count("at least 1 argument") > 0)

    def test_max(self):
        self.assertEqual("-1001.6", self.evaluate("(max -1001.6 )"))
        self.assertEqual("8", self.evaluate("(max -2 5 6 7 -100 8)"))
        self.assertTrue( self.evaluate("(max )").count("at least 1 argument") > 0)

    def test_abs(self):
        self.assertEqual("1001.6", self.evaluate("(abs -1001.6 )"))
        self.assertEqual("8", self.evaluate("(abs 8)"))
