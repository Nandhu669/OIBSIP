# Random Password Generator — Beginner and Advanced Tiers

A password generator built for Oasis Infobyte Python Programming Task 3. The original Beginner command-line application remains available, and the Advanced implementation adds a secure Tkinter GUI.

## Beginner features

- Prompts for a password length and enforces a minimum of 8 characters.
- Lets the user include uppercase letters, lowercase letters, numbers, and symbols.
- Requires at least two selected character types.
- Generates a password that includes at least one character from every selected type.
- Handles invalid lengths and invalid yes/no answers with clear messages.
- Allows another password to be generated without restarting the program.

## Advanced features

- Tkinter GUI with a length spinbox and character-type checkboxes.
- Uses Python's `secrets` module for cryptographically secure generation.
- Shows a Weak / Medium / Strong strength indicator.
- Guarantees at least one character from every selected type.
- Automatically copies every generated password to the clipboard and includes a Copy button.
- Can exclude ambiguous characters: `0`, `O`, `l`, and `1`.
- Shows only the five most recently generated passwords for the current session.
- Does not save generated passwords to a file or database.

## Requirements

- Python 3.10 or newer
- Beginner version: no external packages are needed.
- Advanced version: install clipboard support with `pip install -r requirements.txt`.

## Run the Beginner version

```bash
python beginner_password_generator.py
```

## Run the Advanced version

```bash
pip install -r requirements.txt
python advanced_password_generator.py
```

## Example

```text
Enter password length (minimum 8): 12
Include uppercase letters? (yes/no): yes
Include lowercase letters? (yes/no): yes
Include numbers? (yes/no): yes
Include symbols? (yes/no): no

Generated password: qJ3aM5Zp7xRt
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Note

The Beginner version follows the task’s required `random` module stack. The Advanced GUI uses `secrets` as required for secure password generation. For important accounts, prefer a trusted password manager.
