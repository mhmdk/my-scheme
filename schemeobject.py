class SchemeObject:
    pass


class SchemeNumber(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, SchemeNumber) and type(self.value) == type(other.value) and self.value == other.value


class SchemeChar(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SchemeChar) and self.value == other.value

    def __str__(self):
        return self.value if self.value.isspace() else f"\\#{self.value}"


class SchemeBool(SchemeObject):
    scheme_true = None
    scheme_false = None

    def __new__(cls, value):
        if value:
            if cls.scheme_true is None:
                cls.scheme_true = super().__new__(cls)
                cls.scheme_true.value = True
            return cls.scheme_true
        else:
            if cls.scheme_false is None:
                cls.scheme_false = super().__new__(cls)
                cls.scheme_false.value = False
            return cls.scheme_false

    def __eq__(self, other):
        return isinstance(other, SchemeBool) and self.value == other.value

    def __str__(self):
        return "#t" if self.value else "#f"

    def __bool__(self):
        return self.value


class SchemeString(SchemeObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SchemeString) and self.value == other.value

    def __str__(self):
        return f'"{self.value}"'


class SchemeSymbol(SchemeObject):
    instances = {}

    def __new__(cls, value):
        if value not in cls.instances:
            instance = super().__new__(cls)
            instance.value = value
            cls.instances[value] = instance
        else:
            instance = cls.instances[value]
        return instance

    def __eq__(self, other):
        return isinstance(other, SchemeSymbol) and self.value == other.value

    def __str__(self):
        return self.value


class SchemeEmptyList:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __iter__(self):
        return iter([])

    def __str__(self):
        return "()"

    def size(self):
        return 0

    def is_list(self):
        return True


class SchemePair(SchemeObject):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        if self.is_list():
            return f"( {' '.join(str(element) for element in self)} )"
        else:
            return f"( {self.first} . {self.second} )"

    def __iter__(self):
        if not self.is_list():
            raise Exception("trying to iterate a non list pair")
        return SchemeListIterator(self)

    def __eq__(self, other):
        return isinstance(other, SchemePair) and self.car() == other.car() and self.cdr() == other.cdr()

    def size(self):
        if not self.is_list():
            raise Exception("trying to iterate a non list pair")
        return scheme_list_length(self)

    def car(self):
        return self.first

    def cdr(self):
        return self.second

    def set_car(self, value):
        self.first = value

    def set_cdr(self, value):
        self.second = value

    def is_list(self):
        return isinstance(self.cdr(), SchemePair) and self.cdr().is_list() or self.cdr() == SchemeEmptyList()


class SchemeListIterator:
    def __init__(self, pair):
        self.current = pair

    def __next__(self):
        if self.current is SchemeEmptyList():
            raise StopIteration
        element = self.current.first
        self.current = self.current.cdr()
        return element


def is_scheme_list(scheme_object):
    return scheme_object is SchemeEmptyList() or isinstance(scheme_object, SchemePair) and scheme_object.is_list()


def make_scheme_list(elements):
    if len(elements) == 0:
        return SchemeEmptyList()
    return SchemePair(elements[0], make_scheme_list(elements[1:]))


def scheme_list_length(scheme_list):
    if scheme_list is SchemeEmptyList():
        return 0
    return 1 + scheme_list_length(scheme_list.cdr())


def scheme_list_tail(scheme_list):
    if scheme_list is SchemeEmptyList():
        return scheme_list
    while scheme_list.cdr() is not SchemeEmptyList():
        scheme_list = scheme_list.cdr()
    return scheme_list


class SchemeProcedure(SchemeObject):
    def __init__(self, **kwargs):
        is_variadic = kwargs.get('variadic')
        arity = kwargs.get('arity')
        self.is_variadic = is_variadic if is_variadic is not None else False
        if self.is_variadic:
            self.arity = 1
        else:
            self.arity = arity if arity is not None else 0

    def __str__(self):
        return f"procedure {self}"


class BuiltInProcedure(SchemeProcedure):
    def __init__(self, implementation, **kwargs):
        super().__init__(**kwargs)
        self.implementation = implementation

    def __str__(self):
        return f"built in procedure"

    def call(self, args):
        return self.implementation(*args)


class UserDefinedProcedure(SchemeProcedure):
    def __init__(self, formal_parameters, body, surrounding_environment):
        super().__init__(arity=len(formal_parameters.fixed_parameters), variadic=formal_parameters.has_list_parameter)
        self.parameters = formal_parameters.fixed_parameters if not formal_parameters.has_list_parameter else [
            formal_parameters.list_parameter_name]
        self.body = body
        self.environment = surrounding_environment

    def __str__(self):
        return f"scheme user defined procedure"


class UnAssigned(SchemeObject):
    def __eq__(self, other):
        return isinstance(other, UnAssigned)


class SchemeRuntimeError(Exception):
    def __init__(self, message=""):
        self.message = message
