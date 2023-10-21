"""
Sample test file
"""

from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """
    Sample test class
    """

    def test_add_numbers(self):
        """
        Sample test method
        """
        self.assertEqual(calc.add(3, 8), 11)

    def test_subtract_numbers(self):
        """
        Sample test method
        """
        self.assertEqual(calc.subtract(5, 11), 6)