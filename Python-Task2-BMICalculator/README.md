# BMI Calculator — Beginner Tier

A command-line Body Mass Index (BMI) calculator built for Oasis Infobyte Python Programming Task 2.

## Features

- Accepts weight in kilograms and height in metres.
- Calculates BMI using `weight / (height²)`.
- Rounds BMI to two decimal places.
- Classifies BMI using the required categories:
  - Underweight: below 18.5
  - Normal: 18.5 to 24.9
  - Overweight: 25 to 29.9
  - Obese: 30 and above
- Rejects non-numeric, zero, and negative values with helpful messages.
- Lets the user calculate again without restarting the program.

## Requirements

- Python 3.10 or newer
- No external packages are required.

## Run the program

```bash
python bmi_calculator.py
```

## Example

```text
Enter your weight in kilograms: 70
Enter your height in metres: 1.75

--- BMI Result ---
Your BMI is: 22.86
Category: Normal
```

## Test the calculation logic

```bash
python -m unittest discover -s tests -v
```
