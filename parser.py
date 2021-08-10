from schemetoken import TokenType
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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.number_of_tokens = len(tokens)
        self.syntax_tree = SyntaxTree()
        self.errors = []

    def parse(self):
        for current_token in self.tokens:
            if current_token.type == TokenType.NUMBER:
                self.syntax_tree.add(NumberLiteral(current_token.lexeme))
            elif current_token.type == TokenType.BOOLEAN:
                self.syntax_tree.add(BoolLiteral(current_token.lexeme))
            elif current_token.type == TokenType.CHARACTER:
                self.syntax_tree.add(CharLiteral(current_token.lexeme))
            elif current_token.type == TokenType.STRING:
                self.syntax_tree.add(StringLiteral(current_token.lexeme))
            else:
                self.raise_error(f"unexpected token {current_token.lexeme}", current_token)
                # TODO should choose a reasonable place to continue
        return self.syntax_tree

    def raise_error(self, message, token):
        enriched_message = f"parse error at {token.lexeme},line {token.line_number}, column {token.column_number}: {message}"
        self.errors.append(enriched_message)

    def haserrors(self):
        return len(self.errors) > 0
