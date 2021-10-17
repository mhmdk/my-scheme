from environment import Environment
from parser import SyntaxTreeVisitor
from schemeobject import *


class TailCall:
    def __init__(self, procedure, arguments_values):
        self.procedure = procedure
        self.arguments_values = arguments_values


class Interpreter(SyntaxTreeVisitor):
    def __init__(self, environment=None):
        self.environment = Environment() if environment is None else environment
        self.tail_context = False

    def interpret_syntax_tree(self, syntax_tree):
        result = None
        try:
            for expression in syntax_tree.nodes:
                result = self.interpret_expression(expression)
            return result
        except SchemeRuntimeError as error:
            return SchemeString(error.message)

    def interpret_expression(self, expression):
        value = expression.accept(self)
        old_tail_context = self.tail_context
        self.tail_context = False
        value = self.trampoline(value)
        self.tail_context = old_tail_context
        return value

    def interpret_expression_tail(self, expression):
        value = expression.accept(self)
        return self.trampoline(value)

    def trampoline(self, value):
        while not self.tail_context and isinstance(value, TailCall):
            value = self.do_apply(value.procedure, value.arguments_values)
        return value

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
        return make_scheme_list([self.interpret_expression(element) for element in quoted_list.elements])

    def visit_symbol(self, symbol):
        return SchemeSymbol(symbol.symbol)

    def visit_conditional(self, conditional):
        conditional_value = self.interpret_expression(conditional.test)
        if self.truth(conditional_value):
            return self.interpret_expression_tail(conditional.consequent)
        return self.interpret_expression_tail(
            conditional.alternate) if conditional.alternate is not None else SchemeEmptyList()

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
        return self.do_apply(procedure, arguments_values)

    def do_apply(self, procedure, arguments_values):
        if self.tail_context:
            return TailCall(procedure, arguments_values)
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
        for expression in procedure.body[:len(procedure.body) - 1]:
            self.interpret_expression(expression)

        last_expression = procedure.body[len(procedure.body) - 1]
        self.tail_context = True
        value = self.interpret_expression_tail(last_expression)
        self.tail_context = False
        self.environment = old_environment

        return value

    @staticmethod
    def prepare_call_environment(args, procedure):
        call_environment = Environment(procedure.environment)
        for parameter, argument in zip(procedure.parameters, args):
            call_environment.add(parameter, argument)
        return call_environment

    @staticmethod
    def prepare_args(procedure, args):
        if procedure.is_variadic:
            return [make_scheme_list(args)]
        elif len(args) == procedure.arity:
            return args
        else:
            raise SchemeRuntimeError(
                f"procedure expects {procedure.arity} argument {'s' if procedure.arity > 1 else ''}, {len(args)} given")

    def visit_unassigned(self, unassigned):
        return UnAssigned()

    @staticmethod
    def truth(scheme_object):
        return not (isinstance(scheme_object, SchemeBool) and not scheme_object.value)

    def raise_error(self, message):
        raise SchemeRuntimeError(message)
