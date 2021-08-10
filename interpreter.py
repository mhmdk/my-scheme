from parser import SyntaxTreeVisitor


class Interpreter(SyntaxTreeVisitor):
    def interpret_syntax_tree(self, syntax_tree):
        result = None
        for expression in syntax_tree.nodes:
            result = self.interpret_expression(expression)
        # return the result of last expression
        return result

    def interpret_expression(self, expression):
        return expression.accept(self)

    def visit_number_literal(self, number_literal):
        literal = number_literal.lexeme
        return float(literal) if '.' in literal else int(literal)

    def visit_bool_literal(self, bool_literal):
        literal = bool_literal.lexeme[1:]
        return True if literal == 't' else False

    def visit_char_literal(self, char_literal):
        literal = char_literal.lexeme[2:]
        if literal == "newline":
            return "\n"
        if literal == "space":
            return ' '
        return literal

    def visit_string_literal(self, string_literal):
        literal = string_literal.lexeme[1:len(string_literal.lexeme) - 1]
        return literal
