import sync as syncron
from unittest import TestCase

class TestInput(TestCase):

    def test_program_input(self):
        source = "path/to/folder"
        replica = "path/to/replicafolder"
        self.assertIsInstance(source, str)
        self.assertIsInstance(replica, str)

    def test_a_function(self):
        msg = "show a message"
        self.assertIsInstance(msg, str)
