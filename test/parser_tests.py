import unittest
from schemetoken import Token, TokenType
from parser import Parser
from schemeexpression import *


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


if __name__ == '__main__':
    unittest.main()
