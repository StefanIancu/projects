from unittest.mock import Mock, MagicMock
from unittest import TestCase
from lib.development import authenticate, send_email, check_email

class TestFunction(TestCase):
    def test_email(self):
        """Testing the inputs of check_email function"""
        check_email = Mock(side_effect=["yes", "no", "y", "n"])
        self.assertEqual(check_email(), "yes")
        self.assertEqual(check_email(), "no")
        self.assertEqual(check_email(), "y")
        self.assertEqual(check_email(), "n")