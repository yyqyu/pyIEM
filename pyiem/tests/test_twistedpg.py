import unittest
from pyiem import twistedpg
from psycopg2.extras import RealDictCursor


class TestTWPG(unittest.TestCase):

    def test_connect(self):
        conn = twistedpg.connect(database='postgis', host='iemdb')
        cursor = conn.cursor()
        self.assertTrue(isinstance(cursor, RealDictCursor))