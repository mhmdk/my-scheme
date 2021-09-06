;SICP 1.2.1

(define (factorial n)
  (if (= n 1)
      1
      (* n (factorial (- n 1)))))

;expected: 3628800
(factorial 10)