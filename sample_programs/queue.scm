;;SICP 3.3.2

(define (front-ptr queue) (car queue))
(define (rear-ptr queue) (cdr queue))
(define (set-front-ptr! queue item) (set-car! queue item))
(define (set-rear-ptr! queue item) (set-cdr! queue item))

(define (empty-queue? queue) (null? (front-ptr queue)))
(define (make-queue) (cons '() '()))

(define (front-queue queue)
  (if (empty-queue? queue)
      (error "FRONT called with an empty queue" queue)
      (car (front-ptr queue))))

(define (insert-queue! queue item)
  (let ((new-pair (cons item '())))
    (cond ((empty-queue? queue)
           (set-front-ptr! queue new-pair)
           (set-rear-ptr! queue new-pair)
           queue)
          (else
           (set-cdr! (rear-ptr queue) new-pair)
           (set-rear-ptr! queue new-pair)
           queue))))

(define (delete-queue! queue)
  (cond ((empty-queue? queue)
         (error "DELETE! called with an empty queue" queue))
        (else
         (set-front-ptr! queue (cdr (front-ptr queue)))
         queue)))

;;SICP Exercise 3.21
(define q1 (make-queue))

;expected: ( ( a b ) ( a b ) ( b ) () )
(insert-queue! q1 'a)
(define s1 (front-ptr q1))

(insert-queue! q1 'b)
(define s2 (front-ptr q1))

(delete-queue! q1)
(define s3 (front-ptr q1))

(delete-queue! q1)
(define s4 (front-ptr q1))

(list s1 s2 s3 s4)

