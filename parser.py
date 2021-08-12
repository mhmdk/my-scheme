from schemetoken import TokenType, keywords_map
from schemeexpression import *


class SyntaxTree:
    def __init__(self):
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)


class SyntaxTreeVisitor:
    def visit_number_literal(self, number_literal):
        pass

    def visit_bool_literal(self, bool_literal):
        pass

    def visit_char_literal(self, char_literal):
        pass

    def visit_string_literal(self, string_literal):
        pass

    def visit_list(self, scheme_list):
        pass

    def visit_symbol(self, symbol):
        pass

    def visit_conditional(self, symbol):
        pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.number_of_tokens = len(tokens)
        self.syntax_tree = SyntaxTree()
        self.errors = []

    def parse(self):
        while not self.isend():
            expr = self.expression()
            self.syntax_tree.add(expr)
        return self.syntax_tree

    def expression(self):
        current_token = self.current()
        expr = None
        if isliteral(current_token, self.next()):
            expr = self.literal()
        elif current_token.type == TokenType.OPEN_PAREN:
            self.advance()
            current_token = self.current()
            if current_token.type == TokenType.IF:
                expr = self.conditional()
            elif current_token.type == TokenType.LAMBDA:
                expr = Expression()
                self.advance()
            else:
                expr = self.call()
            self.consume(TokenType.CLOSE_PAREN)
        elif current_token.type == TokenType.IDENTIFIER:
            expr = Expression()
            self.advance()
        else:
            self.raise_error(f"unexpected token {current_token.lexeme}", current_token)
        return expr

    def literal(self):
        token = self.current()
        if token.type is TokenType.OPEN_PAREN:
            return self.quote()
        else:
            return self.non_quote_literal()

    def non_quote_literal(self):
        token = self.current()
        expr = None
        if token.type is TokenType.NUMBER:
            expr = NumberLiteral(token.lexeme)
            self.advance()
        elif token.type is TokenType.BOOLEAN:
            expr = BoolLiteral(token.lexeme)
            self.advance()
        elif token.type is TokenType.CHARACTER:
            expr = CharLiteral(token.lexeme)
            self.advance()
        elif token.type is TokenType.STRING:
            expr = StringLiteral(token.lexeme)
            self.advance()
        return expr

    def quote(self):
        self.consume(TokenType.OPEN_PAREN)
        self.consume(TokenType.QUOTE)
        expr = self.datum()
        self.consume(TokenType.CLOSE_PAREN)
        return expr

    def datum(self):
        current_token = self.current()
        if current_token.type is TokenType.OPEN_PAREN:
            return self.list()
        elif is_non_quote_literal(current_token):
            return self.non_quote_literal()
        else:
            return self.symbol()

    def symbol(self):
        current_token = self.current()
        if current_token.type is TokenType.IDENTIFIER or current_token.type in keywords_map.values():
            self.advance()
            return Symbol(current_token.lexeme)
        else:
            # to raise an error, TODO change this when we have error recovery mechanism
            self.expect(TokenType.IDENTIFIER)

    def list(self):
        self.consume(TokenType.OPEN_PAREN)
        scheme_list = QuotedList()
        while not self.is_end_of_list():
            scheme_list.elements.append(self.datum())
        self.consume(TokenType.CLOSE_PAREN)
        return scheme_list

    def conditional(self):
        self.consume(TokenType.IF)
        test = self.expression()
        consequent = self.expression()
        alternate = None
        if not self.is_end_of_list():
            alternate = self.expression()
        return Conditional(test, consequent, alternate)

    def call(self):
        callee = self.expression()
        args = Args()
        while not self.is_end_of_list():
            args.add(self.expression())
        return Call(callee, args)

    def raise_error(self, message, token=None):
        if token is not None:
            enriched_message = f"parse error at {token.lexeme},line {token.line_number}, column {token.column_number}: {message}"
        else:
            enriched_message = message
        self.errors.append(enriched_message)
        self.panic()

    def is_end_of_list(self):
        return self.isend() or self.current().type == TokenType.CLOSE_PAREN

    def haserrors(self):
        return len(self.errors) > 0

    def advance(self):
        self.index = self.index + 1

    def isend(self):
        return self.index >= self.number_of_tokens

    def previous(self):
        return self.tokens[self.index - 1] if self.index - 1 < self.number_of_tokens and self.index > 0 else None

    def current(self):
        return self.tokens[self.index] if self.index < self.number_of_tokens else None

    def next(self):
        return self.tokens[self.index + 1] if self.index + 1 < self.number_of_tokens else None

    def consume(self, token_type):
        self.expect(token_type)
        self.advance()

    def expect(self, token_type):
        if self.isend():
            self.raise_error(f"unexpected end of file, expected token of type {token_type}")
        current_token = self.current()
        if not current_token.type == token_type:
            self.raise_error(f"unexpected token {current_token.lexeme}, expected token of type {token_type}",
                             current_token)

    def panic(self):
        while not self.is_end_of_list():
            self.advance()


def is_non_quote_literal(token):
    return token.type in [TokenType.BOOLEAN, TokenType.NUMBER, TokenType.CHARACTER, TokenType.STRING]


def isliteral(current_token, next_token):
    return is_non_quote_literal(current_token) or \
           current_token.type == TokenType.OPEN_PAREN and next_token is not None and next_token.type == TokenType.QUOTE
