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

    def visit_variable_reference(self, variable_reference):
        pass

    def visit_call(self, call):
        pass

    def visit_lambda(self, lambda_expression):
        pass

    def visit_definition(self, definition):
        pass

    def visit_assignment(self, assignment):
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
            if self.is_definition():
                expr = self.definition()
            else:
                expr = self.expression()
            self.syntax_tree.add(expr)
        return self.syntax_tree

    def expression(self):
        if self.isend():
            self.raise_error(f"expected expression")
        expr = None
        if self.is_literal():
            expr = self.literal()
        elif self.current_token_has_type(TokenType.OPEN_PAREN):
            self.advance()
            if self.current_token_has_type(TokenType.IF):
                expr = self.conditional()
            elif self.current_token_has_type(TokenType.LAMBDA):
                expr = self.scheme_lambda()
            elif self.current_token_has_type(TokenType.SET):
                expr = self.assignment()
            else:
                expr = self.call()
            self.consume(TokenType.CLOSE_PAREN)
        elif self.current_token_has_type(TokenType.IDENTIFIER):
            expr = self.variable_reference()
        else:
            current_token = self.current()
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
        if self.current_token_has_type(TokenType.OPEN_PAREN):
            return self.list()
        elif self.is_non_quote_literal():
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
        quoted_list = QuotedList()
        while not self.is_end_of_list():
            quoted_list.elements.append(self.datum())
        self.consume(TokenType.CLOSE_PAREN)
        return quoted_list

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

    def variable_reference(self):
        identifier = self.consume(TokenType.IDENTIFIER)
        return VariableReference(identifier.lexeme)

    def scheme_lambda(self):
        self.consume(TokenType.LAMBDA)
        formals = self.formals()
        body = self.lambda_body()
        return Lambda(formals, body)

    def formals(self):
        formal_parameters = FormalParameters()
        if self.current_token_has_type(TokenType.OPEN_PAREN):
            self.fixed_number_parameters(formal_parameters)
        else:
            parameter = self.consume(TokenType.IDENTIFIER)
            formal_parameters.set_list_parameter(parameter.lexeme)
        return formal_parameters

    def fixed_number_parameters(self, formal_parameters):
        self.consume(TokenType.OPEN_PAREN)
        while not self.is_end_of_list():
            parameter = self.consume(TokenType.IDENTIFIER)
            formal_parameters.append_parameter(parameter.lexeme)
        self.consume(TokenType.CLOSE_PAREN)

    def lambda_body(self):
        expressions = []
        while not self.is_end_of_list():
            expressions.append(self.expression())
        if len(expressions) == 0:
            self.raise_error(f"lambda has empty body", self.previous())
        return expressions

    def definition(self):
        self.consume(TokenType.OPEN_PAREN)
        self.consume(TokenType.DEFINE)
        if self.current_token_has_type(TokenType.OPEN_PAREN):
            definition = self.procedure_definition()
        else:
            definition = self.variable_definition()
        self.consume(TokenType.CLOSE_PAREN)
        return definition

    def variable_definition(self):
        name = self.consume(TokenType.IDENTIFIER).lexeme
        expression = self.expression()
        return Definition(name, expression)

    def procedure_definition(self):
        self.consume(TokenType.OPEN_PAREN)
        name = self.consume(TokenType.IDENTIFIER).lexeme
        formals = FormalParameters()
        while not self.is_end_of_list():
            parameter = self.consume(TokenType.IDENTIFIER)
            formals.append_parameter(parameter.lexeme)
        self.consume(TokenType.CLOSE_PAREN)
        body = self.lambda_body()
        return Definition(name, Lambda(formals, body))

    def assignment(self):
        self.consume(TokenType.SET)
        name = self.consume(TokenType.IDENTIFIER).lexeme
        expression = self.expression()
        return Assignment(name, expression)

    def raise_error(self, message, token=None):
        if token is not None:
            enriched_message = f"parse error at {token.lexeme},line {token.line_number}, column {token.column_number}: {message}"
        else:
            enriched_message = message
        self.errors.append(enriched_message)
        self.panic()

    def current_token_has_type(self, *token_types):
        return not self.isend() and self.current().type in token_types

    def is_end_of_list(self):
        return self.isend() or self.current().type == TokenType.CLOSE_PAREN

    def haserrors(self):
        return len(self.errors) > 0

    def advance(self):
        self.index = self.index + 1

    def isend(self):
        return self.index >= self.number_of_tokens

    def get_at(self, index):
        return self.tokens[index] if self.number_of_tokens > index >= 0 else None

    def previous(self):
        return self.get_at(self.index - 1)

    def current(self):
        return self.get_at(self.index)

    def next(self):
        return self.get_at(self.index + 1)

    def consume(self, token_type):
        self.expect(token_type)
        token = self.current()
        self.advance()
        return token

    def expect(self, token_type):
        if self.isend():
            self.raise_error(f"unexpected end of file, expected token of type {token_type}")
        else:
            current_token = self.current()
            if not current_token.type == token_type:
                self.raise_error(f"unexpected token {current_token.lexeme}, expected token of type {token_type}",
                                 current_token)

    def panic(self):
        while not self.is_end_of_list():
            self.advance()

    def is_literal(self):
        return self.is_non_quote_literal() or self.is_quote()

    def is_non_quote_literal(self):
        return self.current_token_has_type(TokenType.BOOLEAN, TokenType.NUMBER, TokenType.CHARACTER,
                                           TokenType.STRING)

    def is_quote(self):
        return self.next_two_tokens_have_types(TokenType.OPEN_PAREN, TokenType.QUOTE)

    def is_definition(self):
        return self.next_two_tokens_have_types(TokenType.OPEN_PAREN, TokenType.DEFINE)

    def next_two_tokens_have_types(self, current_token_type, next_token_type):
        next_token = self.next()
        current_token = self.current()
        if current_token is None or next_token is None:
            return False
        return current_token.type is current_token_type and next_token.type is next_token_type

