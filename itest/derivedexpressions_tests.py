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
