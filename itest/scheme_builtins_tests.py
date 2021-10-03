from itest.test_setup import ExpressionTest


class SchemeBuiltinsTest(ExpressionTest):

    # equivalence predicates
    def test_eqv(self):
        self.assertEqual("#t", self.evaluate("(eqv? #t #t)"))
        self.assertEqual("#f", self.evaluate("(eqv? #t #f)"))
        self.assertEqual("#t", self.evaluate("(eqv? (quote abc) (quote abc))"))
        self.assertEqual("#f", self.evaluate("(eqv? (quote abc) (quote def))"))
        self.assertEqual("#t", self.evaluate("(eqv? 1 (+ 1 0) )"))
        self.assertEqual("#f", self.evaluate("(eqv? 1 1.0 )"))
        self.assertEqual("#t", self.evaluate("(define a #\\a) (eqv? #\\a a)"))
        self.assertEqual("#f", self.evaluate("(eqv? #\\b #\\a )"))
        self.assertEqual("#t", self.evaluate("(eqv? (quote ()) (list))"))
        self.assertEqual("#f", self.evaluate("(eqv? (quote (1)) (list 1))"))
        self.assertEqual("#f", self.evaluate('(eqv?  "abc" "def")'))
        self.assertEqual("#f", self.evaluate('(define a "abc") (define b "abc") (eqv? a b)'))
        self.assertEqual("#t", self.evaluate("(define (f x) x) (define g f) (eqv? f g)"))
        self.assertEqual("#f", self.evaluate("(define (f x) x) (define (g x) (+ x 1)) (eqv? f g)"))

    def test_equal(self):
        self.assertEqual("#t", self.evaluate("(equal? #t #t)"))
        self.assertEqual("#f", self.evaluate("(equal? #t #f)"))
        self.assertEqual("#t", self.evaluate("(equal? (quote abc) (quote abc))"))
        self.assertEqual("#f", self.evaluate("(equal? (quote abc) (quote def))"))
        self.assertEqual("#t", self.evaluate("(equal? 1 (+ 1 0) )"))
        self.assertEqual("#f", self.evaluate("(equal? 1 1.0 )"))
        self.assertEqual("#t", self.evaluate("(define a #\\a) (equal? #\\a a)"))
        self.assertEqual("#f", self.evaluate("(equal? #\\b #\\a )"))
        self.assertEqual("#t", self.evaluate("(equal? (quote ()) (list))"))
        self.assertEqual("#t", self.evaluate("(equal? (quote (1)) (list 1))"))
        self.assertEqual("#f", self.evaluate('(equal?  "abc" "def")'))
        self.assertEqual("#t", self.evaluate('(define a "abc") (define b "abc") (equal? a b)'))
        self.assertEqual("#t", self.evaluate("(define (f x) x) (define g f) (equal? f g)"))
        self.assertEqual("#f", self.evaluate("(define (f x) x) (define (g x) (+ x 1)) (equal? f g)"))

    # numeric operations
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

    def test_remainder(self):
        self.assertEqual("0", self.evaluate("(remainder 4 2 )"))
        self.assertEqual("1", self.evaluate("(remainder 4 3 )"))

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

    def test_caddar(self):
        self.assertEqual("( 3 4 )", self.evaluate("""(caddar
         (list 
         (cons 1 
         (cons 2 
         (cons (list 3 4) 5
         )))
         6) 
         )"""))

    # control features
    def test_is_procedure(self):
        self.assertEqual("#f", self.evaluate("(procedure? #t)"))
        self.assertEqual("#t", self.evaluate("(procedure? (lambda () 1) )"))

    def test_apply(self):
        self.assertEqual("3", self.evaluate("(apply + (list 1 2))"))
        self.assertEqual("3", self.evaluate("(apply + 0 0 0 (list 1 2))"))
        self.assertEqual("4", self.evaluate("(define (square x) (* x x)) (apply square (quote (2)))"))
        self.assertIn("incorrect type", self.evaluate("(define (square x) (* x x)) (apply square 2)"))
        self.assertEqual("( 200 )", self.evaluate('''
            (define compose
                (lambda (f g)
                    (lambda args
                        (f (apply g args)))))

            ((compose list *) 10 20)'''))

    def test_apply_with_closures(self):
        self.assertEqual("6", self.evaluate("""
            (define (make-adder x)
                (lambda (y) (+ x y)))
            (define one-adder (make-adder 1))
            (apply one-adder '(5))
            """))

    def test_for_each(self):
        self.assertEqual("( ( 0 . 1 ) ( 0 . 1 ) ( 0 . 1 ) ( 0 . 1 ) ( 0 . 1 ) )", self.evaluate('''
                (define l (list (cons 2 2) (cons 2 2) (cons 2 2) (cons 2 2) (cons 2 2)))
                (for-each 
                    (lambda (pair-to-modify ) 
                        (set-car! pair-to-modify 0) 
                        (set-cdr! pair-to-modify 1)) 
                    l )
                l'''))
        self.assertEqual("2", self.evaluate('''
            (let ((count 0))
                (for-each 
                    (lambda (ignored) (set! count (+ count 1)))
                    (quote (a b)) )
                count)'''))

    def test_map(self):
        self.assertEqual("( 1 4 9 16 25 )", self.evaluate('''
                (map (lambda (n) (* n n))
                    (quote (1 2 3 4 5)) ) '''))
        self.assertEqual("( 5 7 9 )", self.evaluate('''
                (map +
                    (quote ( 1 2 3 )) (quote ( 4 5 6 ))) '''))

    def test_eval(self):
        report_env = "(scheme-report-environment 5)"
        null_env = "(null-environment 5)"
        self.assertIn("variable + not found", self.evaluate(f'(eval (quote (+ 1 1)) {null_env})'))
        self.assertEqual("2", self.evaluate(f'(eval (quote (+ 1 1)) {report_env})'))
        self.assertEqual("( 1 2 3 )", self.evaluate(f"""(eval 
        (quote 
            (append (quote (1 2)) (quote (3)) )
        )
        {report_env})"""))

        self.assertEqual("( 2 9 )", self.evaluate(f"""(eval 
        (quote 
            (map 
                (lambda (f x) (f x x))
                (list + *) (list 1 3) 
        ))
        {report_env})"""))

        self.assertEqual("( + 1 2 )", self.evaluate(f"""(eval 
             ''(+ 1 2) 
        {report_env})"""))

        self.assertIn("not a procedure", self.evaluate(f"""(eval 
            '( '+ 1 2)
        {report_env})"""))

    def test_make_promise_force(self):
        self.assertEqual("11", self.evaluate(f"""
        (let ((x 0))
        (define pr (make-promise (lambda () (+ x 1))))
        (set! x 10)
        (force pr))"""))
