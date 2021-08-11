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
    tokens = []
    for literal in literals:
        lexeme = literal[0]
        token_type = literal[1]
        tokens.append(Token(lexeme, token_type, 0, 0))
    quoted_list = [open_paren, quote_token, open_paren]
    quoted_list.extend(tokens)
    quoted_list.extend([close_paren, close_paren])
    return quoted_list


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
        literals = [['1', TokenType.NUMBER], ['quote', TokenType.IDENTIFIER], ['else', TokenType.ELSE],
                    ['else', TokenType.IDENTIFIER], ['#f', TokenType.BOOLEAN], ['"quote"', TokenType.STRING],
                    ['#\\r', TokenType.CHARACTER]]
        tokens = build_quoted_list(literals)
        syntax_tree = Parser(tokens).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertIs(type(quoted_list), QuotedList)
        types = [type(node) for node in quoted_list.elements]
        self.assertEqual(types, [NumberLiteral, Symbol, Symbol, Symbol, BoolLiteral, StringLiteral, CharLiteral])

    def test_nested_quoted_lists(self):
        literals = [['1', TokenType.NUMBER], ['i', TokenType.IDENTIFIER], ['(', TokenType.OPEN_PAREN],
                    ['"abc"', TokenType.STRING], [')', TokenType.CLOSE_PAREN]]
        outer_list = build_quoted_list(literals)
        syntax_tree = Parser(outer_list).parse()
        quoted_list = syntax_tree.nodes[0]
        self.assertIs(type(quoted_list), QuotedList)
        types = [type(node) for node in quoted_list.elements]
        self.assertEqual(types, [NumberLiteral, Symbol, QuotedList])


if __name__ == '__main__':
    unittest.main()
