; SICP exercise 1.32

(define (accumulate combiner null-value term a next b)
    (if (> a b) null-value
        (combiner (term a) (accumulate combiner null-value term (next a) next b))))

(define (sum term a next b) (accumulate + 0 term a next b))

(define (inc n) (+ n 1))

(define (identity x) x)

(define (sum-integers a b)
  (sum identity a inc b))

;expected: 55
(sum-integers 1 10)
