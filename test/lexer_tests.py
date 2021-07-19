import unittest
from lexer import Lexer
from schemetoken import TokenType


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
        self.assertIn("invalid character in number literal:a", lexer.errors[0])

    def test_number_literal_integer(self):
        lexer = Lexer("1")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, '1')

    def test_number_literal_float(self):
        lexer = Lexer("1.2")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, '1.2')

    def test_number_literal_with_leading_dot_and_surrounding_spaces(self):
        lexer = Lexer(" .1 ")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, '.1')

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

    def test_dot_token(self):
        lexer = Lexer(".")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.DOT)

    def test_identifier_beginning_with_dot(self):
        lexer = Lexer(".abc")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, ".abc")

    def test_identifier_ending_with_dot(self):
        lexer = Lexer("abc.")
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "abc.")

    def test_string_literal(self):
        lexer = Lexer('"abc"')
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].lexeme, '"abc"')

    def test_multiline_string_literal(self):
        lexer = Lexer('"abc\ndef"')
        tokens = lexer.scan()
        self.assertIs(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].lexeme, '"abc\ndef"')

    def test_imbalanced_double_quotes(self):
        lexer = Lexer('"abc')
        errors = lexer.scan()
        self.assertTrue(lexer.haserrors())
        self.assertTrue('unbalanced "' in errors[0])

    def test_boolean_literal(self):
        lexer = Lexer('#t')
        tokens = lexer.scan()
        self.assertEqual(TokenType.BOOLEAN, tokens[0].type)
        self.assertEqual('#t', tokens[0].lexeme)

    def test_invalid_boolean_literal(self):
        lexer = Lexer('#abc')
        errors = lexer.scan()
        self.assertTrue(lexer.haserrors())
        self.assertTrue("'t' or 'f'" in errors[0])

    def test_character_literal(self):
        lexer = Lexer('#\\a')
        tokens = lexer.scan()
        self.assertEqual(TokenType.CHARACTER, tokens[0].type)
        self.assertEqual('#\\a', tokens[0].lexeme)

    def test_newline_character_literal(self):
        lexer = Lexer('#\\newline')
        tokens = lexer.scan()
        self.assertEqual(TokenType.CHARACTER, tokens[0].type)
        self.assertEqual('#\\newline', tokens[0].lexeme)

    def test_invalid_character_literal(self):
        lexer = Lexer('#\\ab12.a')
        errors = lexer.scan()
        self.assertTrue(lexer.haserrors())
        self.assertTrue("invalid character name" in errors[0])

    def test_open_close_parenthesis(self):
        lexer = Lexer(' ()')
        tokens = lexer.scan()
        self.assertEqual(TokenType.OPEN_PAREN, tokens[0].type)
        self.assertEqual('(', tokens[0].lexeme)
        self.assertEqual(TokenType.CLOSE_PAREN, tokens[1].type)
        self.assertEqual(')', tokens[1].lexeme)

    def test_comment(self):
        lexer = Lexer(' ;this is a comment\n ')
        tokens = lexer.scan()
        self.assertEqual(TokenType.COMMENT, tokens[0].type)
        self.assertEqual(';this is a comment', tokens[0].lexeme)

    def test_error_should_contain_full_line(self):
        line = 'abc"errorhere ;some comment'
        lexer = Lexer(line)
        lexer.scan()
        self.assertTrue(lexer.haserrors())
        self.assertIn(line, lexer.errors[0])

    def test_acceptance(self):
        program = '( + 9 .2 ) ( f #t #\\newline #\\t \n"44string12.3" -\n'
        lexer = Lexer(program)
        tokens = lexer.scan()
        self.assertFalse(lexer.haserrors())
        tokentypes = [token.type for token in tokens]
        lexemes = [token.lexeme for token in tokens]
        self.assertEqual(tokentypes, [TokenType.OPEN_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                      TokenType.NUMBER, TokenType.CLOSE_PAREN, TokenType.OPEN_PAREN,
                                      TokenType.IDENTIFIER, TokenType.BOOLEAN, TokenType.CHARACTER,
                                      TokenType.CHARACTER, TokenType.STRING, TokenType.IDENTIFIER])
        self.assertEqual(lexemes,
                         ['(', '+', '9', '.2', ')', '(', 'f', '#t', '#\\newline', '#\\t', '"44string12.3"', '-'])


if __name__ == '__main__':
    unittest.main()
