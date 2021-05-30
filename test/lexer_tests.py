import unittest
from lexer import Lexer, TokenType


class LexerTest(unittest.TestCase):
    def test_scan_keyword(self):
        tokens = Lexer("   else  ").scan()
        self.assertIs(tokens[0].type, TokenType.ELSE)

    def test_scan_identifier(self):
        variablename = "!abcDe23w-9+2.x"
        lexer = Lexer(variablename)
        tokens = lexer.scan()
        self.assertFalse(lexer.haserrors())
        self.assertIs(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, variablename)

    def test_peculiar_identifier(self):
        tokens = Lexer("+").scan()
        self.assertIs(tokens[0].type, TokenType.IDENTIFIER)

    def test_identifier_cannot_start_with_plus(self):
        lexer = Lexer("+abc")
        errors = lexer.scan()
        self.assertTrue(lexer.haserrors())
        self.assertIn("invalid character in number literal:b", lexer.errors[0])


    def test_number_with_sign(self):
        lexer = Lexer("+123")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.NUMBER)

    def test_floating_point_number(self):
        lexer = Lexer(".123")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.NUMBER)

    def test_number_with_multiple_dots(self):
        lexer = Lexer(".123.")
        tokens = lexer.scan()
        self.assertTrue(lexer.haserrors())

    def test_error_should_contain_full_line(self):
        line = 'abc"errorhere ;some comment'
        lexer = Lexer(line)
        errors = lexer.scan()
        self.assertTrue(lexer.haserrors())
        self.assertIn(line, lexer.errors[0])


if __name__ == '__main__':
    unittest.main()
