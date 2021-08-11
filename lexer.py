from schemetoken import Token, TokenType, keywords_map

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
                next_token = self.token()
                if next_token is not None:
                    tokens.append(next_token)
        if self.haserrors():
            return self.errors
        return tokens

    def token(self):
        current_char = self.text[self.current_index]

        if self.isinitial():
            return self.identifier()

        elif self.ispeculiaridentifier():
            return self.peculiaridentifier()

        elif current_char == '.':
            if self.next() is not None and self.next().isdigit():
                return self.number()
            elif self.isnextdelimiter():
                return self.dot()
            else:
                return self.identifier()

        elif self.issign() or self.isdigit():
            return self.number()

        elif current_char == '"':
            return self.string()

        elif current_char == '#':
            if self.next() is not None and self.next() == "\\":
                return self.character()
            else:
                return self.boolean()
        elif current_char == '(':
            return self.openparenthesis()

        elif current_char == ')':
            return self.closeparenthesis()

        elif current_char == ';':
             self.comment()

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
            return self.maketoken(lexeme, keywords_map[lexeme])
        else:
            return self.maketoken(lexeme, TokenType.IDENTIFIER)

    def peculiaridentifier(self):
        token = self.maketoken(self.text[self.current_index], TokenType.IDENTIFIER)
        self.advance()
        if not self.checkdelimiter():
            self.raiseerror(
                f"expected delimiter after identifier name {token.lexeme}, got {self.text[self.current_index]}")
        return token

    def number(self):
        dotcount = 0

        def checkdot():
            nonlocal dotcount
            if self.text[self.current_index] == '.':
                dotcount += 1
                if dotcount > 1:
                    self.raiseerror(f"multiple decimal points in number literal:{self.text[self.current_index]}")

        lexeme = self.text[self.current_index]
        checkdot()
        self.advance()

        while not self.isend() and self.text[self.current_index].isdigit():
            lexeme += self.text[self.current_index]
            self.advance()

        if not self.isend():
            checkdot()

            if self.text[self.current_index] == '.':
                lexeme += self.text[self.current_index]
                self.advance()
                while not self.isend() and self.text[self.current_index].isdigit():
                    lexeme += self.text[self.current_index]
                    self.advance()

        if not self.checkdelimiter():
            self.raiseerror(f"invalid character in number literal:{self.text[self.current_index]}")

        return self.maketoken(lexeme, TokenType.NUMBER)

    def dot(self):
        self.advance()
        return self.maketoken(".", TokenType.DOT)

    def string(self):
        lexeme = self.text[self.current_index]
        self.advance()
        while not self.isend() and not self.text[self.current_index] == '"':
            lexeme += self.text[self.current_index]
            self.advance()
        if self.isend():
            self.raiseerror('unbalanced "')
        else:
            lexeme += self.text[self.current_index]
            self.advance()
            return self.maketoken(lexeme, TokenType.STRING)

    def boolean(self):
        lexeme = self.text[self.current_index]
        self.advance()
        if self.isend():
            self.raiseerror("expected boolean literal")
        if self.text[self.current_index] not in {'t', 'f'}:
            self.raiseerror("boolean literal should be either 't' or 'f'")
        lexeme += self.text[self.current_index]
        self.advance()
        return self.maketoken(lexeme, TokenType.BOOLEAN)

    def character(self):
        lexeme = self.text[self.current_index:self.current_index + 2]
        self.advance()
        self.advance()

        while not self.isend() and not self.checkdelimiter():
            lexeme += self.text[self.current_index]
            self.advance()
        if len(lexeme) > 3 and lexeme not in {'#\\space', '#\\newline'}:
            self.raiseerror(f"invalid character name {lexeme}")
        return self.maketoken(lexeme, TokenType.CHARACTER)

    def openparenthesis(self):
        self.advance()
        return self.maketoken('(', TokenType.OPEN_PAREN)

    def closeparenthesis(self):
        self.advance()
        return self.maketoken(')', TokenType.CLOSE_PAREN)

    def comment(self):
        lexeme = self.text[self.current_index]
        self.advance()

        while not self.isend() and not self.text[self.current_index] == '\n':
            lexeme += self.text[self.current_index]
            self.advance()

        return self.maketoken(lexeme, TokenType.COMMENT)

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
        return self.text[self.current_index].isdigit()

    def next(self):
        if self.current_index + 1 < self.text_length:
            return self.text[self.current_index + 1]
        else:
            return None

    def maketoken(self, lexeme, tokentype):
        return Token(lexeme, tokentype, self.current_line, self.current_column)
