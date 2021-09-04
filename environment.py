
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
