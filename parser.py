from schemetoken import TokenType
from schemeexpression import NumberLiteral


class SyntaxTree:
    def __init__(self):
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)


class SyntaxTreeVisitor:
    def visit_number_literal(self, number_literal):
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
                node = NumberLiteral(current_token.lexeme)
                self.syntax_tree.add(node)
            else:
                self.raise_error("unexpected token", current_token)
                # TODO should choose a reasonable place to continue
        return self.syntax_tree

    def raise_error(self, message, token):
        enriched_message = f"parse error at {token.lexeme},line {token.line_number}, column {token.column_number}: {message}"
        self.errors.append(enriched_message)

    def haserrors(self):
        return len(self.errors) > 0
