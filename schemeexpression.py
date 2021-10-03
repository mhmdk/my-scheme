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
    def __init__(self, elements=None):
        self.elements = [] if elements is None else elements

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


class Args:
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


class VariableReference(Expression):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_variable_reference(self)


class FormalParameters:
    def __init__(self):
        self.fixed_parameters = []
        self.has_list_parameter = False
        self.list_parameter_name = ''

    def set_list_parameter(self, name):
        self.has_list_parameter = True
        self.list_parameter_name = name

    def append_parameter(self, name):
        self.fixed_parameters.append(name)


class Lambda(Expression):
    def __init__(self, formals, body):
        self.formals = formals
        self.body = body

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_lambda(self)


class Definition(Expression):
    def __init__(self, variable, expression):
        self.name = variable
        self.expression = expression

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_definition(self)


class Assignment(Expression):
    def __init__(self, variable, expression):
        self.name = variable
        self.expression = expression

    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_assignment(self)


# user has no way to create this in source code, it is created by the parser to implement letrec
class UnAssigned(Expression):
    def accept(self, syntax_tree_visitor):
        return syntax_tree_visitor.visit_unassigned(self)
