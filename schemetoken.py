from enum import Enum, auto


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
    LETSTAR = auto()
    LETREC = auto()

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
    "set!": TokenType.SET,
    "begin": TokenType.BEGIN,
    "cond": TokenType.COND,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "case": TokenType.CASE,
    "let": TokenType.LET,
    "let*": TokenType.LETSTAR,
    "letrec": TokenType.LETREC
}


class Token:
    def __init__(self, lexeme, typ, line_number, column_number):
        self.lexeme = lexeme
        self.type = typ
        self.line_number = line_number
        self.column_number = column_number
