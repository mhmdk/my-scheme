from enum import Enum, auto


# ##Lexical Grammar:##
# reduced version of https://schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-10.html#%_sec_7.1.1
#
# token -> keyword | identifier | number | string | boolean | character | ( | ) | .
# comment -> ; all characters until line break
# keyword -> else | define | quote | lambda | if | set! | begin | cond | and | or | case | let
# identifier -> initial subsequent* | + | -
# initial -> alpha | ! | $ | % | & | * | / | : | < | = | > | ? | ^ | _ | ~
# subsequent -> initial | digit | + | - | .
# number -> sign? (digit*.digit+ | digit+.digit*)
# string -> "any character except "*"
# character -> #\any character | #\newline | #\space
# boolean -> #t | #f
# alpha -> a | b | ... | Z
# digit -> 0 | 1 | ... | 9
#
# see also:
# https://www.scheme.com/tspl2d/grammar.html
# https://www.scheme.com/tspl4/grammar.html
# https://docs.microsoft.com/en-us/cpp/c-language/lexical-grammar?view=msvc-160


class TokenType(Enum):
    # keyword:
    ELSE = auto()
    DEFINE = auto()
    QUOTE = auto()
    LAMBDA = auto()
    IF = auto()
    SET = auto()
    BEGIN = auto()
    COND = auto()
    AND = auto()
    OR = auto()
    CASE = auto()
    LET = auto()

    # identifier
    IDENTIFIER = auto()

    # literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    CHARACTER = auto()

    # delimiters
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    DOT = auto()

    COMMENT = auto()


keywords_map = {
    "else": TokenType.ELSE,
    "define": TokenType.DEFINE,
    "quote": TokenType.QUOTE,
    "lambda": TokenType.LAMBDA,
    "if": TokenType.IF,
    "set": TokenType.SET,
    "begin": TokenType.BEGIN,
    "cond": TokenType.COND,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "case": TokenType.CASE,
    "let": TokenType.LET
}


class Token:
    # TODO add column, and add it to token construction and error reporting
    def __init__(self, lexeme, typ, line_number):
        self.lexeme = lexeme
        self.type = typ
        self.line_number = line_number


class Lexer:
    def __init__(self, text):
        self.text = text
        self.text_length = len(text)
        self.current_index = 0
        self.current_line = 1
        self.current_column = 1
        self.current_line_begin = 0
        self.current_line_end = self.text.find('\n', self.current_line_begin)
        if self.current_line_end == -1:
            self.current_line_end = len(self.text)
        self.errors = []

    def scan(self):
        tokens = []
        while not self.isend():
            while not self.isend() and self.iswhitespace():
                self.advance()
            if not self.isend():
                tokens.append(self.token())
        if self.haserrors():
            return self.errors
        return tokens

    def token(self):
        current_char = self.text[self.current_index]
        if self.isinitial():
            return self.identifier()
        elif self.ispeculiaridentifier():
            return self.peculiaridentifier()
        elif self.issign() or self.isdigit() or current_char == '.': # be careful, . is an independent token as well
            return self.number()
        else:
            self.raiseerror(f"unexpected character {current_char}")
            self.advance()

    def identifier(self):
        lexeme = self.text[self.current_index]
        self.advance()
        while not self.isend() and self.issubsequent():
            lexeme += self.text[self.current_index]
            self.advance()
        if not self.checkdelimiter():
            self.raiseerror(f"expected delimiter after identifier name {lexeme}, got {self.text[self.current_index]}")
        if lexeme in keywords_map:
            return Token(lexeme, keywords_map[lexeme], self.current_line)
        else:
            return Token(lexeme, TokenType.IDENTIFIER, self.current_line)

    def peculiaridentifier(self):
        token = Token(self.text[self.current_index], TokenType.IDENTIFIER, self.current_line)
        self.advance()
        if not self.checkdelimiter():
            self.raiseerror(
                f"expected delimiter after identifier name {token.lexeme}, got {self.text[self.current_index]}")
        return token

    def number(self):
        dotreached = False
        error=False

        def checkdot():
            nonlocal dotreached
            nonlocal error
            if self.text[self.current_index] == '.':
                if dotreached:
                    self.raiseerror(f"multiple decimal points in number literal:{self.text[self.current_index]}")
                    error=True
                else:

                    dotreached = True

        lexeme = self.text[self.current_index]
        checkdot()
        self.advance()

        while not self.isend() and self.text[self.current_index].isdigit():
            lexeme += self.text[self.current_index]
            self.advance()

        if not self.isend():
            checkdot()
            self.advance()

            if not error:
                while not self.isend() and self.text[self.current_index].isdigit():
                    lexeme += self.text[self.current_index]

                if not self.checkdelimiter():
                    self.raiseerror(f"invalid character in number literal:{self.text[self.current_index]}")

        return Token(lexeme, TokenType.NUMBER, self.current_line)



    def advance(self):

        if self.text[self.current_index] == '\n':
            self.current_line += 1
            self.current_column = 1
            self.current_line_begin = self.current_index
            self.current_line_end = self.text.find('\n', self.current_line_begin)
            if self.current_line_end == -1:
                self.current_line_end = len(self.text)
        else:
            self.current_column += 1
        self.current_index += 1

    def iswhitespace(self):
        return self.text[self.current_index].isspace()

    def isend(self):
        return self.current_index >= self.text_length

    def raiseerror(self, message):
        line = self.text[self.current_line_begin:self.current_line_end]
        self.errors.append(f"line {self.current_line}: {line}\n{message}")

    def isinitial(self):
        return self.text[self.current_index].isalpha() or \
               self.text[self.current_index] in ['!', '$', '%', '&', '*', '/', ':', '<', '=', '>', '?', '^', '_', '~']

    def issubsequent(self):
        current_char = self.text[self.current_index]
        return current_char.isalpha() or current_char.isdigit() or current_char in ['+', '-', '.']

    def ispeculiaridentifier(self):
        return self.text[self.current_index] in ['+', '-'] and self.isnextdelimiter()

    def haserrors(self):
        return len(self.errors) > 0

    def checkdelimiter(self):
        return self.isdelimiter(self.current_index)

    def isnextdelimiter(self):
        return self.isdelimiter(self.current_index + 1)

    def isdelimiter(self, index):
        return index >= self.text_length or self.text[index].isspace() or self.text[index] in ['(', ')', ';']

    def issign(self):
        return self.text[self.current_index] in ['+', '-']

    def isdigit(self):
        self.text[self.current_index].isdigit()
