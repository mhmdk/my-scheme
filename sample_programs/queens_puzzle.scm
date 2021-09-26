
;SICP exercise 2.42

(define nil '())

(define (filter predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (filter predicate (cdr sequence))))
        (else (filter predicate (cdr sequence)))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (flatmap proc seq)
  (accumulate append nil (map proc seq)))

(define (enumerate-interval low high)
  (if (> low high)
      nil
      (cons low (enumerate-interval (+ low 1) high))))

(define empty-board nil)

 (define (adjoin-position new-row k rest-of-queens)
   (cons (list new-row k) rest-of-queens))

 (define (queen-in-k k positions)
   (cond ((null? positions) nil)
         ((= (cadar positions) k)
          (car positions))
         (else (queen-in-k k (cdr positions)))))

 (define (queens-not-k k positions)
   (cond ((null? positions) nil)
         ((= (cadar positions) k)
          (cdr positions))
         (else (cons (car positions)
                     (queens-not-k k (cdr positions))))))

 (define (safe? k positions)
   (let ((queen-k (queen-in-k k positions))
         (o-queens (queens-not-k k positions)))
     (null? (filter (lambda (o-q)
                      (or (= (car o-q) (car queen-k))
                          (= (- (car o-q) (cadr o-q))
                             (- (car queen-k) (cadr queen-k)))
                          (= (+ (car o-q) (cadr o-q))
                             (+ (car queen-k) (cadr queen-k)))))
                    o-queens))))

(define (queens board-size)
  (define (queen-cols k)
    (if (= k 0)
        (list empty-board)
        (filter
         (lambda (positions) (safe? k positions))
         (flatmap
          (lambda (rest-of-queens)
            (map (lambda (new-row)
                   (adjoin-position new-row k rest-of-queens))
                 (enumerate-interval 1 board-size)))
          (queen-cols (- k 1))))))
  (queen-cols board-size))

;expected:( ( ( 3 4 ) ( 1 3 ) ( 4 2 ) ( 2 1 ) ) ( ( 2 4 ) ( 4 3 ) ( 1 2 ) ( 3 1 ) ) )
(queens 4)