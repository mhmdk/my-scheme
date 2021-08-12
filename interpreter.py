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
        return f'"{self.value}"'


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


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.dictionary = {}

    def get(self, name):
        if name in self.dictionary.keys():
            return self.dictionary[name]
        if self.parent is not None:
            return self.parent.get(name)
        return None

    def add(self, name, value=None):
        self.dictionary[name] = value


class SchemeRuntimeError(Exception):
    def __init__(self, message=""):
        self.message = message


class Interpreter(SyntaxTreeVisitor):
    def __init__(self, environment=None):
        self.environment = Environment() if environment is None else environment

    def interpret_syntax_tree(self, syntax_tree):
        result = None
        try:
            for expression in syntax_tree.nodes:
                result = self.interpret_expression(expression)
            # return the result of last expression
            return result
        except SchemeRuntimeError as error:
            return SchemeString(error.message)

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
        return SchemeList(self.interpret_expression(element) for element in quoted_list.elements)

    def visit_symbol(self, symbol):
        return SchemeSymbol(symbol.symbol)

    def visit_conditional(self, conditional):
        conditional_value = self.interpret_expression(conditional.test)
        if isinstance(conditional_value, SchemeBool) and not conditional_value.value:
            return self.interpret_expression(
                conditional.alternate) if conditional.alternate is not None else SchemeList()
        return self.interpret_expression(conditional.consequent)

    def visit_variable_reference(self, variable_reference):
        value = self.environment.get(variable_reference.variable_name)
        if value is None:
            self.raise_error(f"variable {variable_reference.variable_name} not found")
        return value

    def raise_error(self, message):
        raise SchemeRuntimeError(message)
