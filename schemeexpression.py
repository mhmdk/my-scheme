class Expression:
    def accept(self, syntax_tree_visitor):
        pass


class NumberLiteral(Expression):
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_number_literal(self)


class BoolLiteral(Expression):
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_bool_literal(self)


class CharLiteral(Expression):
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_char_literal(self)


class StringLiteral(Expression):
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_string_literal(self)


class QuotedList(Expression):
    def __init__(self):
        self.elements = []

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_list(self)


class Symbol(Expression):
    def __init__(self, symbol):
        self.symbol = symbol

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_symbol(self)


class Conditional(Expression):
    def __init__(self, test, consequent, alternate=None):
        self.test = test
        self.consequent = consequent
        self.alternate = alternate

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_conditional(self)


class Args():
    def __init__(self):
        self.args = []

    def add(self, arg):
        self.args.append(arg)


class Call(Expression):
    def __init__(self, callee, args=None):
        self.callee = callee
        self.args = args if args is not None else Args()

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_call(self)
