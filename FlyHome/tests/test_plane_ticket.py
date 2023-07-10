from unittest import TestCase, mock
from lib.development import PlaneTicket


class TestConstructor(TestCase):

    def test_attributes(self):
        ticket = PlaneTicket(1, "Andrew Jackson", "33RK", 2, "rome", "BR120", 5)

        self.assertIsInstance(ticket.current_number, int)
        self.assertIsInstance(ticket.name, str)
        self.assertIsInstance(ticket.seat, str)
        self.assertIsInstance(ticket.date, int)
        self.assertIsInstance(ticket.destination, str)
        self.assertIsInstance(ticket.flight_number, str)
        self.assertIsInstance(ticket.gate, int)
        self.assertEqual(ticket.current_price, 0)

