from parser import SyntaxTreeVisitor
from schemeobject import *


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

    def add(self, name, value):
        self.dictionary[name] = value

    def set(self, name, value):
        if name in self.dictionary.keys():
            self.dictionary[name] = value
        elif self.parent is not None:
            self.parent.set(name, value)


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
        if value == UnAssigned():
            self.raise_error(f"variable {variable_reference.variable_name} Unassigned")
        return value

    def visit_call(self, call):
        procedure = self.interpret_expression(call.callee)
        if not isinstance(procedure, SchemeProcedure):
            self.raise_error(f"{procedure} is not a procedure")
        arguments_values = [self.interpret_expression(arg) for arg in call.args.args]
        args = self.prepare_args(procedure, arguments_values)
        if isinstance(procedure, BuiltInProcedure):
            return procedure.call(args)
        else:
            return self.interpret_scheme_procedure_call(procedure, args)

    def visit_lambda(self, lambda_expression):
        return UserDefinedProcedure(lambda_expression.formals, lambda_expression.body, self.environment)

    def visit_definition(self, definition):
        self.environment.add(definition.name, self.interpret_expression(definition.expression))

    def visit_assignment(self, assignment):
        old_value = self.environment.get(assignment.name)
        if old_value is None:
            raise SchemeRuntimeError(f"variable {assignment.name} not bound")
        self.environment.set(assignment.name, self.interpret_expression(assignment.expression))

    def interpret_scheme_procedure_call(self, procedure, args):
        call_environment = self.prepare_call_environment(args, procedure)
        old_environment = self.environment
        self.environment = call_environment
        value = None
        for expression in procedure.body:
            value = self.interpret_expression(expression)

        self.environment = old_environment
        return value

    def prepare_call_environment(self, args, procedure):
        call_environment = Environment(procedure.environment)
        for parameter, argument in zip(procedure.parameters, args):
            call_environment.add(parameter, argument)
        return call_environment

    @staticmethod
    def prepare_args(procedure, args):
        if procedure.is_variadic:
            return [SchemeList(args)]
        elif len(args) == procedure.arity:
            return args
        else:
            raise SchemeRuntimeError(
                f"procedure expects {procedure.arity} argument {'s' if procedure.arity > 1 else ''}, {len(args)} given")

    def visit_unassigned(self, unassigned):
        return UnAssigned()

    def raise_error(self, message):
        raise SchemeRuntimeError(message)
