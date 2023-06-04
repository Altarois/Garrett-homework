import unittest
from datetime import datetime
from phone_calculation import compute_minute_types

# testing the calculation of different types of minutes


class TestPhoneCalculation(unittest.TestCase):
    def test_compute_minute_types(self):
        # Test case 1: Call starts and ends during the normal tarification
        start = datetime(2023, 6, 1, 6, 15)
        end = datetime(2023, 6, 1, 6, 30)
        night_minutes, day_minutes, bonus_minutes = compute_minute_types(start, end)
        self.assertEqual(night_minutes, 5)
        self.assertEqual(day_minutes, 0)
        self.assertEqual(bonus_minutes, 9)

        # Test case 2: Call starts during the reduced tarification and ends during the normal tarification
        start = datetime(2023, 6, 1, 7, 57)
        end = datetime(2023, 6, 1, 8, 27)
        night_minutes, day_minutes, bonus_minutes = compute_minute_types(start, end)
        self.assertEqual(night_minutes, 3)
        self.assertEqual(day_minutes, 2)
        self.assertEqual(bonus_minutes, 24)

        # Test case 2: Call starts during the normal tarification and ends during the reduced tarification
        start = datetime(2023, 6, 1, 15, 58)
        end = datetime(2023, 6, 1, 16, 2)
        night_minutes, day_minutes, bonus_minutes = compute_minute_types(start, end)
        self.assertEqual(night_minutes, 1)
        self.assertEqual(day_minutes, 2)
        self.assertEqual(bonus_minutes, 0)


if __name__ == "__main__":
    unittest.main()
