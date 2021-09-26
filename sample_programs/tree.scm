
;SICP exercise chapter 2.2

(define (scale-tree tree factor)
  (map (lambda (sub-tree)
         (if (pair? sub-tree)
             (scale-tree sub-tree factor)
             (* sub-tree factor)))
       tree))

;expected:( 10 ( 20 ( 30 40 ) 50 ) ( 60 70 ) )
(scale-tree (list 1
                  (list 2 (list 3 4) 5)
                  (list 6 7))
            10)
