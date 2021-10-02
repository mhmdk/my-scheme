import unittest
from schemetoken import Token, TokenType
from parser import Parser
from schemeexpression import *


def build_simple_quote(token):
    open_paren = Token("(", TokenType.OPEN_PAREN, 0, 0)
    quote_token = Token("quote", TokenType.QUOTE, 0, 0)
    close_paren = Token(")", TokenType.CLOSE_PAREN, 0, 0)
    return [open_paren, quote_token, token, close_paren]


def build_quoted_list(literals):
    open_paren = Token("(", TokenType.OPEN_PAREN, 0, 0)
    quote_token = Token("quote", TokenType.QUOTE, 0, 0)
    close_paren = Token(")", TokenType.CLOSE_PAREN, 0, 0)
    tokens = build_tokens_of_types(literals)
    quoted_list = [open_paren, quote_token, open_paren]
    quoted_list.extend(tokens)
    quoted_list.extend([close_paren, close_paren])
    return quoted_list


def build_lambda(parameter_tokens, body_tokens):
    tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.LAMBDA]) + parameter_tokens + body_tokens + \
             build_tokens_of_types([TokenType.CLOSE_PAREN])
    return tokens


def build_tokens_of_types(token_types):
    return [Token("", token_type, 0, 0) for token_type in token_types]


def build_variable_definition(name, expression_tokens):
    return [Token("(", TokenType.OPEN_PAREN, 0, 0), Token("", TokenType.DEFINE, 0, 0),
            Token(name, TokenType.IDENTIFIER, 0, 0)] + expression_tokens + [Token(")", TokenType.CLOSE_PAREN, 0, 0)]


def build_procedure_definition(name, parameters, expression_tokens):
    return [Token("(", TokenType.OPEN_PAREN, 0, 0), Token("", TokenType.DEFINE, 0, 0),
            Token("(", TokenType.OPEN_PAREN, 0, 0),
            Token(name, TokenType.IDENTIFIER, 0, 0)] + [Token(parameter, TokenType.IDENTIFIER, 0, 0) for parameter in
                                                        parameters] + [
               Token(")", TokenType.CLOSE_PAREN, 0, 0)] + expression_tokens + [
               Token(")", TokenType.CLOSE_PAREN, 0, 0)]


def types(objects):
    return [type(arg) for arg in objects]


class ParserTest(unittest.TestCase):

    def test_number_literal(self):
        tokens = [Token("1", TokenType.NUMBER, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), NumberLiteral)
        self.assertEqual(node.lexeme, "1")

    def test_bool_literal(self):
        tokens = [Token("#f", TokenType.BOOLEAN, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), BoolLiteral)
        self.assertEqual(node.lexeme, "#f")

    def test_char_literal(self):
        tokens = [Token("#\\f", TokenType.CHARACTER, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), CharLiteral)
        self.assertEqual(node.lexeme, "#\\f")

    def test_string_literal(self):
        tokens = [Token('"f"', TokenType.STRING, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), StringLiteral)
        self.assertEqual(node.lexeme, '"f"')

    def test_quoted_string_literal(self):
        string_token = Token('"f"', TokenType.STRING, 0, 0)
        tokens = build_simple_quote(string_token)
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), StringLiteral)
        self.assertEqual(node.lexeme, '"f"')

    def test_quoted_bool_literal(self):
        string_token = Token('#t', TokenType.BOOLEAN, 0, 0)
        tokens = build_simple_quote(string_token)
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), BoolLiteral)
        self.assertEqual(node.lexeme, "#t")

    def test_quoted_char_literal(self):
        char_token = Token("#\\f", TokenType.CHARACTER, 0, 0)
        tokens = build_simple_quote(char_token)
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), CharLiteral)
        self.assertEqual(node.lexeme, "#\\f")

    def test_quoted_number_literal(self):
        number_token = Token("1", TokenType.NUMBER, 0, 0)
        tokens = build_simple_quote(number_token)
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), NumberLiteral)
        self.assertEqual(node.lexeme, '1')

    def test_quoted_symbol(self):
        number_token = Token("quote", TokenType.IDENTIFIER, 0, 0)
        tokens = build_simple_quote(number_token)
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), Symbol)
        self.assertEqual(node.symbol, 'quote')

    def test_quoted_list(self):
        literals = [TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.ELSE,
                    TokenType.IDENTIFIER, TokenType.BOOLEAN, TokenType.STRING,
                    TokenType.CHARACTER]
        tokens = build_quoted_list(literals)
        syntax_tree = Parser(tokens).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertIs(type(quoted_list), QuotedList)
        types = [type(node) for node in quoted_list.elements]
        self.assertEqual(types, [NumberLiteral, Symbol, Symbol, Symbol, BoolLiteral, StringLiteral, CharLiteral])

    def test_nested_quoted_lists(self):
        literals = [TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.OPEN_PAREN,
                    TokenType.STRING, TokenType.CLOSE_PAREN]
        outer_list = build_quoted_list(literals)
        syntax_tree = Parser(outer_list).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertIs(type(quoted_list), QuotedList)
        types = [type(node) for node in quoted_list.elements]
        self.assertEqual(types, [NumberLiteral, Symbol, QuotedList])

    def test_quoted_symbol_with_single_quotation(self):
        tokens = [TokenType.SINGLE_QUOTE, TokenType.OPEN_PAREN, TokenType.IDENTIFIER,
                  TokenType.STRING, TokenType.CLOSE_PAREN]
        quoted_list = build_tokens_of_types(tokens)
        syntax_tree = Parser(quoted_list).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertIs(type(quoted_list), QuotedList)
        types = [type(node) for node in quoted_list.elements]
        self.assertEqual(types, [Symbol, StringLiteral])

    def test_quoted_list_with_single_quotation(self):
        tokens = [Token("'", TokenType.SINGLE_QUOTE, 0, 0), Token("This-is-a-symbol", TokenType.IDENTIFIER, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        symbol = syntax_tree.nodes[0]
        self.assertIs(type(symbol), Symbol)
        self.assertEqual(symbol.symbol, "This-is-a-symbol")

    def test_nested_single_quote(self):
        tokens = [Token("'", TokenType.SINGLE_QUOTE, 0, 0), Token("'", TokenType.SINGLE_QUOTE, 0, 0),
                  Token("a", TokenType.IDENTIFIER, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertEqual(type(quoted_list), QuotedList)
        self.assertEqual(type(quoted_list.elements[0]), Symbol)
        self.assertEqual(quoted_list.elements[0].symbol, 'quote')
        self.assertEqual(type(quoted_list.elements[1]), Symbol)
        self.assertEqual(quoted_list.elements[1].symbol, 'a')

    def test_nested_single_quote_in_list(self):
        tokens = [Token("'", TokenType.SINGLE_QUOTE, 0, 0), Token("(", TokenType.OPEN_PAREN, 0, 0),
                  Token("a", TokenType.IDENTIFIER, 0, 0), Token("'", TokenType.SINGLE_QUOTE, 0, 0),
                  Token("1", TokenType.NUMBER, 0, 0), Token("#t", TokenType.BOOLEAN, 0, 0),
                  Token(")", TokenType.CLOSE_PAREN, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertEqual(type(quoted_list), QuotedList)
        types = [type(node) for node in quoted_list.elements]
        self.assertEqual(types, [Symbol, QuotedList, BoolLiteral])
        inner_quote = quoted_list.elements[1]
        quote_as_symbol = inner_quote.elements[0]
        inner_quote_datum = inner_quote.elements[1]
        self.assertEqual(type(quote_as_symbol), Symbol)
        self.assertEqual(quote_as_symbol.symbol, 'quote')
        self.assertEqual(type(inner_quote_datum), NumberLiteral)
        self.assertEqual(inner_quote_datum.lexeme, '1')

    def test_conditional(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.IF, TokenType.BOOLEAN,
                                        TokenType.STRING, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        conditional = syntax_tree.nodes[0]
        self.assertIs(type(conditional), Conditional)
        self.assertIs(type(conditional.test), BoolLiteral)
        self.assertIs(type(conditional.consequent), StringLiteral)
        self.assertIs(conditional.alternate, None)

    def test_conditional_with_alternate(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.IF, TokenType.NUMBER,
                                        TokenType.NUMBER, TokenType.OPEN_PAREN, TokenType.QUOTE,
                                        TokenType.IDENTIFIER, TokenType.CLOSE_PAREN, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        conditional = syntax_tree.nodes[0]
        self.assertIs(type(conditional), Conditional)
        self.assertIs(type(conditional.test), NumberLiteral)
        self.assertIs(type(conditional.consequent), NumberLiteral)
        self.assertIs(type(conditional.alternate), Symbol)

    def test_conditional_with_more_args(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.IF, TokenType.NUMBER,
                                        TokenType.NUMBER, TokenType.NUMBER, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN])
        parser = Parser(tokens)
        parser.parse()
        self.assertTrue(parser.haserrors())

    def test_function_call(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        call = syntax_tree.nodes[0]
        self.assertIs(type(call), Call)
        self.assertIs(type(call.callee), VariableReference)
        self.assertIs(type(call.args), Args)
        self.assertTrue(object_type is Expression for object_type in types(call.args.args))

    def test_variable_reference(self):
        token = Token("x", TokenType.IDENTIFIER, 0, 0)
        syntax_tree = Parser([token]).parse()
        variable_reference = syntax_tree.nodes[0]
        self.assertIs(type(variable_reference), VariableReference)
        self.assertEqual(variable_reference.variable_name, "x")

    def test_lambda(self):
        tokens = build_lambda(
            parameter_tokens=[Token("(", TokenType.OPEN_PAREN, 0, 0), Token("x", TokenType.IDENTIFIER, 0, 0),
                              Token(")", TokenType.CLOSE_PAREN, 0, 0)],
            body_tokens=[Token("2", TokenType.NUMBER, 0, 0)])
        syntax_tree = Parser(tokens).parse()
        procedure = syntax_tree.nodes[0]
        self.assertIs(type(procedure), Lambda)
        self.assertEqual(procedure.formals.fixed_parameters, ["x"])
        self.assertFalse(procedure.formals.has_list_parameter)
        self.assertEqual(len(procedure.body), 1)
        self.assertEqual(type(procedure.body[0]), NumberLiteral)

    def test_lambda_with_variadic_parameter(self):
        tokens = build_lambda(
            parameter_tokens=[Token("x", TokenType.IDENTIFIER, 0, 0)],
            body_tokens=[Token("2", TokenType.NUMBER, 0, 0), Token("2", TokenType.NUMBER, 0, 0),
                         Token("#\\y", TokenType.CHARACTER, 0, 0)])
        syntax_tree = Parser(tokens).parse()
        procedure = syntax_tree.nodes[0]
        self.assertIs(type(procedure), Lambda)
        self.assertEqual(procedure.formals.fixed_parameters, [])
        self.assertTrue(procedure.formals.has_list_parameter)
        self.assertEqual(procedure.formals.list_parameter_name, "x")
        self.assertEqual(len(procedure.body), 3)

    def test_lambda_with_empty_body(self):
        tokens = build_lambda(parameter_tokens=[Token("x", TokenType.IDENTIFIER, 0, 0)], body_tokens=[])
        parser = Parser(tokens)
        parser.parse()
        self.assertTrue(parser.haserrors())
        self.assertIn("empty body", parser.errors[0])

    def test_variable_definition(self):
        tokens = build_variable_definition('x', [Token('1', TokenType.NUMBER, 0, 0)])
        syntax_tree = Parser(tokens).parse()
        definition = syntax_tree.nodes[0]
        self.assertIs(type(definition), Definition)
        self.assertEqual(definition.name, 'x')
        self.assertEqual(type(definition.expression), NumberLiteral)

    def test_procedure_definition(self):
        tokens = build_procedure_definition('x', ['a', 'b'], [Token('1', TokenType.NUMBER, 0, 0)])
        syntax_tree = Parser(tokens).parse()
        definition = syntax_tree.nodes[0]
        self.assertIs(type(definition), Definition)
        self.assertEqual(definition.name, 'x')
        self.assertEqual(type(definition.expression), Lambda)
        self.assertEqual(type(definition.expression.body[0]), NumberLiteral)
        self.assertEqual(definition.expression.formals.fixed_parameters, ['a', 'b'])

    def test_internal_definition(self):
        internal_definition = build_variable_definition('c', [Token('1', TokenType.NUMBER, 0, 0)])
        tokens = build_procedure_definition('x', ['a', 'b'], internal_definition + [Token('1', TokenType.NUMBER, 0, 0)])
        syntax_tree = Parser(tokens).parse()
        definition = syntax_tree.nodes[0]
        self.assertIs(type(definition), Definition)
        self.assertEqual(definition.name, 'x')
        self.assertEqual(type(definition.expression), Lambda)
        self.assertEqual(definition.expression.formals.fixed_parameters, ['a', 'b'])
        outer_let = definition.expression.body[0]
        self.assertEqual(type(outer_let), Call)
        inner_let = outer_let.callee.body[0]
        self.assertEqual(type(inner_let), Call)
        self.assertEqual(type(inner_let.callee.body[0]), Assignment)
        self.assertEqual(type(inner_let.callee.body[1]), NumberLiteral)

    def test_assignment(self):
        tokens = [Token('(', TokenType.OPEN_PAREN, 0, 0), Token('set!', TokenType.SET, 0, 0),
                  Token('x', TokenType.IDENTIFIER, 0, 0), Token('1', TokenType.NUMBER, 0, 0),
                  Token(')', TokenType.CLOSE_PAREN, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        assignment = syntax_tree.nodes[0]
        self.assertIs(type(assignment), Assignment)
        self.assertEqual(assignment.name, 'x')
        self.assertEqual(type(assignment.expression), NumberLiteral)

    def test_begin(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.BEGIN,
                                        TokenType.NUMBER,
                                        TokenType.IDENTIFIER,
                                        TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.CLOSE_PAREN,
                                        TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        begin = syntax_tree.nodes[0]
        self.assertIs(type(begin), Call)
        lambda_of_begin = begin.callee
        self.assertEqual(types(lambda_of_begin.body), [NumberLiteral, VariableReference, Call])
        self.assertEqual(type(lambda_of_begin.formals), FormalParameters)
        self.assertEqual(lambda_of_begin.formals.fixed_parameters, [])

    def test_cond(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.COND,
                                        TokenType.OPEN_PAREN,
                                        TokenType.BOOLEAN, TokenType.IDENTIFIER,
                                        TokenType.CLOSE_PAREN,
                                        TokenType.OPEN_PAREN,
                                        TokenType.BOOLEAN, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN,
                                        TokenType.OPEN_PAREN,
                                        TokenType.ELSE, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN,
                                        TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        conditional = syntax_tree.nodes[0]
        self.assertIs(type(conditional), Conditional)
        self.assertIs(type(conditional.test), BoolLiteral)
        # a begin which is transformed to lambda
        self.assertIs(type(conditional.consequent), Call)

        self.assertIs(type(conditional.alternate), Conditional)
        else_clause = conditional.alternate.alternate
        self.assertIs(type(else_clause), Call)

    def test_let(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN,
                                        TokenType.LET, TokenType.OPEN_PAREN,
                                        TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN, TokenType.CLOSE_PAREN,
                                        TokenType.IDENTIFIER, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        let = syntax_tree.nodes[0]
        self.assertIs(type(let), Call)
        self.assertIs(type(let.callee), Lambda)
        self.assertEqual(len(let.callee.formals.fixed_parameters), 1)
        self.assertEqual(len(let.args.args), 1)
        self.assertIs(type(let.callee.body[0]), VariableReference)

    def test_letstar(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN,
                                        TokenType.LETSTAR, TokenType.OPEN_PAREN,
                                        TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN,
                                        TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.STRING,
                                        TokenType.CLOSE_PAREN, TokenType.CLOSE_PAREN,
                                        TokenType.IDENTIFIER, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        letstar = syntax_tree.nodes[0]
        self.assertIs(type(letstar), Call)
        self.assertIs(type(letstar.callee), Lambda)
        self.assertEqual(len(letstar.callee.formals.fixed_parameters), 1)
        self.assertEqual(len(letstar.args.args), 1)
        self.assertIs(type(letstar.callee.body[0]), Call)
        self.assertIs(type(letstar.callee.body[0].callee), Lambda)
        self.assertIs(type(letstar.callee.body[0].callee.body[0]), VariableReference)

    def test_letrec(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN,
                                        TokenType.LETREC, TokenType.OPEN_PAREN,
                                        TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                        TokenType.CLOSE_PAREN,
                                        TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.STRING,
                                        TokenType.CLOSE_PAREN, TokenType.CLOSE_PAREN,
                                        TokenType.IDENTIFIER, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        letrec = syntax_tree.nodes[0]
        self.assertIs(type(letrec), Call)
        outer_let = letrec
        self.assertIs(type(outer_let.callee), Lambda)
        self.assertEqual(len(outer_let.callee.formals.fixed_parameters), 2)
        self.assertEqual(len(outer_let.args.args), 2)
        inner_let = outer_let.callee.body[0]
        self.assertIs(type(inner_let), Call)
        self.assertIs(type(inner_let.callee.body[0]), Assignment)
        self.assertIs(type(inner_let.callee.body[1]), Assignment)

    def test_and(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.AND, TokenType.NUMBER,
                                        TokenType.IDENTIFIER, TokenType.STRING, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        and_expression = syntax_tree.nodes[0]
        self.assertIs(type(and_expression), Call)
        self.assertIs(len(and_expression.args.args), 1)
        self.assertIs(type(and_expression.callee.body[0]), Conditional)

    def test_or(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.OR, TokenType.NUMBER,
                                        TokenType.IDENTIFIER, TokenType.STRING, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        or_expression = syntax_tree.nodes[0]
        self.assertIs(type(or_expression), Call)
        self.assertIs(len(or_expression.args.args), 1)
        self.assertIs(type(or_expression.callee.body[0]), Conditional)

    def test_delay(self):
        tokens = build_tokens_of_types([TokenType.OPEN_PAREN, TokenType.DELAY, TokenType.NUMBER, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        delay_expression = syntax_tree.nodes[0]
        self.assertIs(type(delay_expression), Call)
        self.assertIs(len(delay_expression.args.args), 1)
        self.assertIs(type(delay_expression.callee), VariableReference)
        self.assertEqual(delay_expression.callee.variable_name, 'make-promise')

    def test_cons_stream(self):
        tokens = build_tokens_of_types(
            [TokenType.OPEN_PAREN, TokenType.CONS_STREAM, TokenType.NUMBER, TokenType.NUMBER, TokenType.CLOSE_PAREN])
        syntax_tree = Parser(tokens).parse()
        cons_stream_call = syntax_tree.nodes[0]
        self.assertIs(type(cons_stream_call), Call)
        self.assertIs(len(cons_stream_call.args.args), 2)
        self.assertIs(type(cons_stream_call.callee), VariableReference)
        self.assertEqual(cons_stream_call.callee.variable_name, 'cons')
        self.assertIs(type(cons_stream_call.args.args[1]), Call)
        self.assertIs(type(cons_stream_call.args.args[1].callee), VariableReference)
        self.assertEqual(cons_stream_call.args.args[1].callee.variable_name, 'make-promise')


if __name__ == '__main__':
    unittest.main()
