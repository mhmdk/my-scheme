class SchemeObject:
    def to_string(self):
        pass


class SchemeNumber(SchemeObject):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, SchemeNumber) and self.value == other.value


class SchemeChar(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SchemeChar) and self.value == other.value

    def to_string(self):
        return self.value if self.value.isspace() else f"\\#{self.value}"


class SchemeBool(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SchemeBool) and self.value == other.value

    def to_string(self):
        return "#t" if self.value else "#f"


class SchemeString(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SchemeString) and self.value == other.value

    def to_string(self):
        return f'"{self.value}"'


class SchemeSymbol(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SchemeSymbol) and self.value == other.value

    def to_string(self):
        return self.value


class SchemeList(SchemeObject):
    def __init__(self, iterable=None):
        self._elements = []
        if iterable is not None:
            self._elements.extend(iterable)

    def to_string(self):
        return f"( {' '.join(element.to_string() for element in self._elements)} )"

    def __iter__(self):
        return iter(self._elements)


class SchemeProcedure(SchemeObject):
    def __init__(self, kwargs):
        is_variadic = kwargs.get('variadic')
        arity = kwargs.get('arity')
        self.is_variadic = is_variadic if is_variadic is not None else False
        if self.is_variadic:
            self.arity = 1
        else:
            self.arity = arity if arity is not None else 0

    def to_string(self):
        return f"procedure {self}"

    def call(self, args):
        if self.is_variadic:
            return self.docall([SchemeList(args)])
        elif len(args) == self.arity:
            return self.docall(args)
        else:
            raise SchemeRuntimeError(f"procedure expects {self.arity} arguments, {len(args)} given")

    def docall(self, args):
        pass


class BuiltInProcedure(SchemeProcedure):
    def __init__(self, implementation, **kwargs):
        super().__init__(kwargs)
        self.implementation = implementation

    def to_string(self):
        return f"built in procedure {self}"

    def docall(self, args):
        return self.implementation(*args)


class UserDefinedProcedure(SchemeObject):
    def __init__(self, formals, body):
        super().__init__(arity=formals.size)
        self.formals = formals
        self.body = body

    def to_string(self):
        return f"scheme user defined procedure {self}"


class SchemeRuntimeError(Exception):
    def __init__(self, message=""):
        self.message = message
