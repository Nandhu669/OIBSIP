"""Beginner-tier BMI Calculator for the Oasis Infobyte Python internship."""

from __future__ import annotations


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI from positive weight (kg) and height (m)."""
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight_kg / (height_m**2)


def classify_bmi(bmi: float) -> str:
    """Return the standard health category for a BMI value."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def get_positive_number(prompt: str) -> float:
    """Keep prompting until the user enters a positive numeric value."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("Invalid input. Please enter a number, for example: 65.5")
            continue

        if value <= 0:
            print("Please enter a positive value greater than zero.")
            continue
        return value


def run_calculation() -> None:
    """Collect input once and display the rounded BMI result and category."""
    weight = get_positive_number("Enter your weight in kilograms: ")
    height = get_positive_number("Enter your height in metres: ")
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print("\n--- BMI Result ---")
    print(f"Your BMI is: {bmi:.2f}")
    print(f"Category: {category}")


def main() -> None:
    """Run the calculator and optionally let the user calculate again."""
    print("Welcome to the BMI Calculator")
    while True:
        run_calculation()
        again = input("\nCalculate another BMI? (yes/no): ").strip().lower()
        if again not in {"yes", "y"}:
            print("Thank you for using the BMI Calculator.")
            break


if __name__ == "__main__":
    main()
