import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from lib.development import BookFlight, WhereToGo, UTILS, PlaneTicket, DESTINATIONS_AND_PRICES

data = Mock()

class TestConstructor(TestCase):

    def test_attributes(self):

        book = BookFlight("bookflight")

        self.assertIsInstance(book.title, str)
        self.assertIsInstance(book.current_price, int)

class TestMethods(TestCase):

    def test_name_with_string(self):

        # testing the method name with a string input
        book1 = BookFlight("bookflight1")
        book1.get_user_name = MagicMock()
        book1.get_user_name(str)
        book1.get_user_name.assert_called_with(str)
    

    def test_name_with_others(self):

        # testing the method with other inputs - will fail
        book1 = BookFlight("bookflight1")
        book1.get_user_name = Mock(side_effect=ValueError())
        with self.assertRaises(ValueError):
            book1.get_user_name()

        
    def test_destination(self):

        sample_function = Mock(side_effect=["timisoara", "budapest", "bratislava",
                                            "sofia", "prague", "berlin",
                                            "rome", "paris", "basel", "tokyo"])
        self.assertEqual(sample_function(), "timisoara")
        self.assertEqual(sample_function(), "budapest")
        self.assertEqual(sample_function(), "bratislava")
        self.assertEqual(sample_function(), "sofia")
        self.assertEqual(sample_function(), "prague")
        self.assertEqual(sample_function(), "berlin")
        self.assertEqual(sample_function(), "rome")
        self.assertEqual(sample_function(), "paris")
        self.assertEqual(sample_function(), "basel")
        self.assertEqual(sample_function(), "tokyo")

    def test_user_seat(self):

        book1 = BookFlight("bookflight1")
        book1.get_user_seat = Mock()
        book1.get_user_seat("yes" or "no")
        book1.get_user_seat.assert_called_with("yes" or "no")
        seat_function = Mock(side_effect=["yes", "no", "y", "n"])
        self.assertEqual(seat_function(), "yes")
        self.assertEqual(seat_function(), "no")
        self.assertEqual(seat_function(), "y")
        self.assertEqual(seat_function(), "n")

    def test_user_luggage(self):

        book1 = BookFlight("bookflight1")
        book1.get_user_seat = Mock()
        book1.get_user_seat("yes" or "no")
        book1.get_user_seat.assert_called_with("yes" or "no")
        luggage_function = Mock(side_effect=["yes", "no", "y", "n"])
        self.assertEqual(luggage_function(), "yes")
        self.assertEqual(luggage_function(), "no")
        self.assertEqual(luggage_function(), "y")
        self.assertEqual(luggage_function(), "n")

    def test_user_date(self):

        #test for the date method - it only allows an int between 0-31
        book1 = BookFlight("bookflight1")
        book1.get_user_date = Mock()
        book1.get_user_date(range(31))
        book1.get_user_date.assert_called_with(range(31))
