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
