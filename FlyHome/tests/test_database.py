from unittest import TestCase
from lib.development import Database, DB_PATH
import sqlite3
from pathlib import Path

class TestConstructor(TestCase):

    def test_constructor(self):
        """Testing constructor attributes."""
        d1 = Database(DB_PATH)

        self.assertIsInstance(DB_PATH, Path)
        self.assertTrue(d1.connection, sqlite3.connect(DB_PATH))
        self.assertTrue(d1.cursor, d1.connection.cursor())


class TestDatabase(TestCase):

    def test_database_readability(self):
        """Testing the efficiency of a query."""
        # expected = works at the time of testing. when new entries will be added to DB, needs to be updated
        d1 = Database(DB_PATH)
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("""SELECT "destination" FROM flights""")
        result = cursor.fetchall()
        expected = [("Rome", ), ('Tokyo',),('Rome',),('Tokyo',),('Paris',),('Tokyo',),('Rome',),('Budapest',),('Timisoara',),('Tokyo',),('Berlin',),('Tokyo',),('Prague',),('Sofia',),('Budapest',),('Tokyo',),('Paris',),('Paris',),('Tokyo',),('Prague',),('Bratislava',)]
        self.assertEqual(result, expected)
        connection.close()
