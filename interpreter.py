from parser import SyntaxTree, SyntaxTreeVisitor


class Interpreter(SyntaxTreeVisitor):
    def interpret_syntax_tree(self, syntax_tree):
        for node in syntax_tree.nodes:
            self.interpret_expression(node)

    def interpret_expression(self, expression):
        expression.accept(self)

    def visit_number_literal(self, number_literal):
        literal = number_literal.lexeme
        return float(literal) if '.' in literal else int(literal)
