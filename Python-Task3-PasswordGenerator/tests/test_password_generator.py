import string
import unittest

from password_generator import generate_password
from advanced_password_generator import generate_secure_password, password_strength


class GeneratePasswordTests(unittest.TestCase):
    def test_password_has_required_length_and_selected_types(self) -> None:
        password = generate_password(
            16,
            ["uppercase letters", "lowercase letters", "numbers", "symbols"],
        )
        self.assertEqual(len(password), 16)
        self.assertTrue(any(character in string.ascii_uppercase for character in password))
        self.assertTrue(any(character in string.ascii_lowercase for character in password))
        self.assertTrue(any(character in string.digits for character in password))
        self.assertTrue(any(character in string.punctuation for character in password))

    def test_password_uses_only_selected_types(self) -> None:
        password = generate_password(10, ["uppercase letters", "numbers"])
        self.assertTrue(all(character in string.ascii_uppercase + string.digits for character in password))

    def test_rejects_invalid_length_and_insufficient_types(self) -> None:
        with self.assertRaises(ValueError):
            generate_password(7, ["uppercase letters", "numbers"])
        with self.assertRaises(ValueError):
            generate_password(10, ["uppercase letters"])


class AdvancedGeneratorTests(unittest.TestCase):
    def test_secure_password_includes_selected_groups_and_excludes_ambiguous_characters(self) -> None:
        password = generate_secure_password(
            20,
            ["Uppercase letters", "Lowercase letters", "Numbers", "Symbols"],
            exclude_ambiguous=True,
        )
        self.assertEqual(len(password), 20)
        self.assertTrue(any(char in string.ascii_uppercase for char in password))
        self.assertTrue(any(char in string.ascii_lowercase for char in password))
        self.assertTrue(any(char in string.digits for char in password))
        self.assertTrue(any(char in string.punctuation for char in password))
        self.assertFalse(any(char in "0Ol1" for char in password))

    def test_strength_levels(self) -> None:
        self.assertEqual(password_strength(8, 2), ("Weak", 1))
        self.assertEqual(password_strength(12, 2), ("Medium", 2))
        self.assertEqual(password_strength(16, 4), ("Strong", 3))


if __name__ == "__main__":
    unittest.main()
