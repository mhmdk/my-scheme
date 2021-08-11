from parser import SyntaxTreeVisitor


class SchemeObject:
    def to_string(self):
        pass


class SchemeNumber(SchemeObject):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return str(self.value)


class SchemeChar(SchemeObject):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return self.value if self.value.isspace() else f"\\#{self.value}"


class SchemeBool(SchemeObject):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "#t" if self.value else "#f"


class SchemeString(SchemeObject):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return self.value


class SchemeSymbol(SchemeObject):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return self.value


class SchemeList(SchemeObject):
    def __init__(self, elements=None):
        self.elements = elements if elements is not None else []

    def to_string(self):
        return f"( {' '.join(element.to_string() for element in self.elements)} )"


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
        value = float(literal) if '.' in literal else int(literal)
        return SchemeNumber(value)

    def visit_bool_literal(self, bool_literal):
        literal = bool_literal.lexeme[1:]
        value = True if literal == 't' else False
        return SchemeBool(value)

    def visit_char_literal(self, char_literal):
        literal = char_literal.lexeme[2:]
        value = literal
        if literal == "newline":
            value = "\n"
        if literal == "space":
            value = ' '
        return SchemeChar(value)

    def visit_string_literal(self, string_literal):
        literal = string_literal.lexeme[1:len(string_literal.lexeme) - 1]
        return SchemeString(literal)

    def visit_list(self, quoted_list):
        return SchemeList(element.accept(self) for element in quoted_list.elements)

    def visit_symbol(self, symbol):
        return SchemeSymbol(symbol.symbol)
