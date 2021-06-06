
## Lexical Grammar:
reduced version of https://schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-10.html#%_sec_7.1.1  

token -> keyword | identifier | number | string | boolean | character | ( | ) | .  
comment -> ; all characters until line break  
keyword -> else | define | quote | lambda | if | set! | begin | cond | and | or | case | let  
identifier -> initial subsequent* | peculiaridentifier  
initial -> alpha | ! | $ | % | & | * | / | : | < | = | > | ? | ^ | _ | ~  
subsequent -> initial | digit | + | - | .  
peculiaridentifier -> + | -  
number -> sign? (digit*.digit+ | digit+.digit*)  
string -> "any character except "*"    
character -> #\any character | #\newline | #\space  
boolean -> #t | #f  
alpha -> a | b | ... | Z  
digit -> 0 | 1 | ... | 9  

see also:  
https://www.scheme.com/tspl2d/grammar.html  
https://www.scheme.com/tspl4/grammar.html  
https://docs.microsoft.com/en-us/cpp/c-language/lexical-grammar?view=msvc-160  


## Syntax Grammar: 
Subset of https://schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-10.html#%_sec_7.1.3  

expression -> variable | literal | call | lambda | conditional  
literal -> quotation | self-evaluating  
self-evaluating -> boolean | character | number | string  
quotation -> (quote datum)  
datum -> boolean | character | number | string | identifier | list  
list -> (datum*)   
call -> (operator operand*)  
operator -> expression  
operand -> expression  
lambda -> ("lambda" formals body)  
formals -> identifier | (identifier*)   
body -> expression+  
conditional -> ("if" test consequent alternate?)  
test -> expression  
consequent -> expression  
alternate -> expression  

to consider adding:  
top level definitions, internal definitions in body, assignment, some derived expressions(ex :cond, let),   
dot notation for pairs, including pairs in quoted expressions and formal parameters.  


see also:  
https://schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-10.html#%_sec_7.1.3  
https://schemers.org/Documents/Standards/R5RS/HTML/ chapters 4 & 5  
