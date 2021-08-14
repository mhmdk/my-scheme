import unittest

from interpreter import Environment
from main import init_global_environment, scan_evaluate


class ExpressionTest(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        init_global_environment(self.env)

    def evaluate(self, expression):
        return str(scan_evaluate(expression, self.env))
