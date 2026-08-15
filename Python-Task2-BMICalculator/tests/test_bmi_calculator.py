import unittest

from bmi_calculator import calculate_bmi, classify_bmi


class CalculateBmiTests(unittest.TestCase):
    def test_calculates_bmi(self) -> None:
        self.assertAlmostEqual(calculate_bmi(70, 1.75), 22.8571428571)

    def test_rejects_zero_or_negative_measurements(self) -> None:
        with self.assertRaises(ValueError):
            calculate_bmi(0, 1.75)
        with self.assertRaises(ValueError):
            calculate_bmi(70, -1.75)


class ClassifyBmiTests(unittest.TestCase):
    def test_standard_categories_and_boundaries(self) -> None:
        self.assertEqual(classify_bmi(18.49), "Underweight")
        self.assertEqual(classify_bmi(18.5), "Normal")
        self.assertEqual(classify_bmi(24.9), "Normal")
        self.assertEqual(classify_bmi(25), "Overweight")
        self.assertEqual(classify_bmi(29.9), "Overweight")
        self.assertEqual(classify_bmi(30), "Obese")


if __name__ == "__main__":
    unittest.main()
