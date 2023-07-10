from unittest import TestCase, mock
import io
import builtins
from lib.development import save_json, load_json, reset_json

@mock.patch('lib.development.load_json')
class TestJSON(TestCase):

    def test_load_json(self, open_mock):
        open_mock.load_json = io.StringIO("json loaded.")

    def test_reset_json(self, open_mock):
        open_mock.reset_json = io.StringIO("json reset.")

    # def test_another(self):