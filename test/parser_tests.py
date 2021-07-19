import unittest
from schemetoken import Token, TokenType
from parser import Parser
from schemeexpression import NumberLiteral



class ParserTest(unittest.TestCase):
    def test_number_literal(self):
        tokens = [Token("1", TokenType.NUMBER, 0, 0)]
        syntax_tree = Parser(tokens).parse()
        node = syntax_tree.nodes[0]
        self.assertIs(type(node), NumberLiteral)
        self.assertEqual(node.lexeme, "1")


if __name__ == '__main__':
    unittest.main()
