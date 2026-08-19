"""Beginner-tier random password generator for Oasis Infobyte Python Task 3."""

from __future__ import annotations

import random
import string


CHARACTER_SETS = {
    "uppercase letters": string.ascii_uppercase,
    "lowercase letters": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": string.punctuation,
}


def generate_password(length: int, selected_sets: list[str]) -> str:
    """Generate a password containing every selected character type at least once."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")
    if len(selected_sets) < 2:
        raise ValueError("Select at least two character types.")
    if any(item not in CHARACTER_SETS for item in selected_sets):
        raise ValueError("One or more character types are not supported.")
    if length < len(selected_sets):
        raise ValueError("Password length is too short for the selected character types.")

    pool = "".join(CHARACTER_SETS[item] for item in selected_sets)
    password = [random.choice(CHARACTER_SETS[item]) for item in selected_sets]
    password.extend(random.choice(pool) for _ in range(length - len(password)))
    random.shuffle(password)
    return "".join(password)


def get_length() -> int:
    """Prompt until a valid password length of eight or greater is entered."""
    while True:
        raw_value = input("Enter password length (minimum 8): ").strip()
        try:
            length = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number, for example: 12.")
            continue

        if length < 8:
            print("Password length must be at least 8 characters.")
            continue
        return length


def ask_yes_no(label: str) -> bool:
    """Prompt for a yes/no response and return True for yes."""
    while True:
        answer = input(f"Include {label}? (yes/no): ").strip().lower()
        if answer in {"yes", "y"}:
            return True
        if answer in {"no", "n"}:
            return False
        print("Please answer yes or no.")


def get_character_types() -> list[str]:
    """Collect at least two character types from the user."""
    while True:
        selected = [
            label for label in CHARACTER_SETS if ask_yes_no(label)
        ]
        if len(selected) >= 2:
            return selected
        print("Please select at least two character types for a stronger password.\n")


def main() -> None:
    """Run the interactive password generator."""
    print("Welcome to the Random Password Generator")
    while True:
        length = get_length()
        selected_sets = get_character_types()
        password = generate_password(length, selected_sets)
        print(f"\nGenerated password: {password}")

        again = input("\nGenerate another password? (yes/no): ").strip().lower()
        if again not in {"yes", "y"}:
            print("Keep your passwords private. Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
