from itest.test_setup import ExpressionTest


class QuotesTest(ExpressionTest):
    def test_consecutive_single_quotes(self):
        expression = "''''a"
        expected = "( quote ( quote ( quote a ) ) )"
        self.assertEqual(expected, self.evaluate(expression))

    def test_quotes_in_list(self):
        expression = "(quote (quote 1 (quote a) ''a 'b ) )"
        expected = "( quote 1 ( quote a ) ( quote ( quote a ) ) ( quote b ) )"
        self.assertEqual(expected, self.evaluate(expression))
