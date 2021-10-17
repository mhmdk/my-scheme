from itest.test_setup import ExpressionTest
import sys


class TailRecursionTest(ExpressionTest):
    def expect_with_tight_recursion_limits(self, expected, expression):
        old_recursion_limit = sys.getrecursionlimit()
        try:
            sys.setrecursionlimit(100)
            self.assertEqual(expected, self.evaluate(expression))
        except RecursionError as re:
            self.fail(str(re))
        finally:
            sys.setrecursionlimit(old_recursion_limit)

    def test_non_tail_recursive_counter(self):
        expression = """(define (recursive-counter n)
                        (cond ((<= n 0) 0)
                              (else (+ 1 (recursive-counter (- n 1)))
                                       )))
                        (recursive-counter 100)"""
        with self.assertRaises(RecursionError,
                               msg="maximum recursion depth exceeded while calling a Python object"):
            old_recursion_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(100)
            self.evaluate(expression)
            sys.setrecursionlimit(old_recursion_limit)

    def test_tail_recursive_counter(self):
        expression = """(define (recursive-counter-iter n i)
                        (cond ((<= n 0) i)
                              (else (recursive-counter-iter (- n 1) (+ i 1) )
                                       )))
                        (define (recursive-counter n)
                            (recursive-counter-iter n 0))
                        (recursive-counter 100)"""
        expected = "100"
        self.expect_with_tight_recursion_limits(expected, expression)

    def test_tail_recursive_counter_in_and_expression(self):
        expression = """(define (recursive-counter-iter n i)
                        (cond ((<= n 0) i)
                              (else (and #t (recursive-counter-iter (- n 1) (+ i 1) )
                                       ))))
                        (define (recursive-counter n)
                            (recursive-counter-iter n 0))
                        (recursive-counter 100)"""
        expected = "100"
        self.expect_with_tight_recursion_limits(expected, expression)

    def test_tail_recursive_counter_with_scheme_procedure_calls_in_arguments(self):
        expression = """(define ( add a b) (+ a b))
                        (define ( subtract a b) (- a b))
                        
                        (define (recursive-counter-iter n i)
                        (cond ((<= n 0) i)
                              (else (recursive-counter-iter (subtract n 1) (add i 1) )
                                       )))
                        (define (recursive-counter n)
                            (recursive-counter-iter n 0))
                        (recursive-counter 100)"""
        expected = "100"
        self.expect_with_tight_recursion_limits(expected, expression)
