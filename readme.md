
##Lexical Grammar:##
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