"""Advanced-tier GUI password generator for Oasis Infobyte Python Task 3."""

from __future__ import annotations

import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk


CHARACTER_SETS = {
    "Uppercase letters": string.ascii_uppercase,
    "Lowercase letters": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation,
}
AMBIGUOUS_CHARACTERS = "0Ol1"


def generate_secure_password(
    length: int, selected_sets: list[str], exclude_ambiguous: bool = False
) -> str:
    """Generate a secure password containing every selected type at least once."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")
    if len(selected_sets) < 2:
        raise ValueError("Select at least two character types.")
    if any(name not in CHARACTER_SETS for name in selected_sets):
        raise ValueError("An unsupported character type was selected.")

    character_groups = []
    for name in selected_sets:
        characters = CHARACTER_SETS[name]
        if exclude_ambiguous:
            characters = "".join(char for char in characters if char not in AMBIGUOUS_CHARACTERS)
        if not characters:
            raise ValueError(f"No usable characters remain in {name}.")
        character_groups.append(characters)

    pool = "".join(character_groups)
    password = [secrets.choice(group) for group in character_groups]
    password.extend(secrets.choice(pool) for _ in range(length - len(password)))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def password_strength(length: int, type_count: int) -> tuple[str, int]:
    """Return a user-friendly strength label and a 1–3 progress value."""
    if length >= 14 and type_count >= 3:
        return "Strong", 3
    if length >= 10 and type_count >= 2:
        return "Medium", 2
    return "Weak", 1


class PasswordGeneratorApp(tk.Tk):
    """Tkinter application implementing the Advanced-tier feature checklist."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Secure Password Generator")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        self.length_var = tk.StringVar(value="12")
        self.type_vars = {name: tk.BooleanVar(value=True) for name in CHARACTER_SETS}
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Choose options, then select Generate Password.")
        self.history: list[str] = []

        self._build_interface()

    def _build_interface(self) -> None:
        ttk.Label(self, text="Password length").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(self, from_=8, to=128, textvariable=self.length_var, width=8).grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )

        type_frame = ttk.LabelFrame(self, text="Include character types", padding=10)
        type_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        for row, (name, variable) in enumerate(self.type_vars.items()):
            ttk.Checkbutton(type_frame, text=name, variable=variable).grid(row=row, column=0, sticky="w")
        ttk.Checkbutton(
            type_frame,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.exclude_ambiguous_var,
        ).grid(row=4, column=0, sticky="w", pady=(6, 0))

        ttk.Button(self, text="Generate Password", command=self.generate).grid(
            row=2, column=0, columnspan=2, pady=(15, 8)
        )
        ttk.Entry(self, textvariable=self.password_var, width=42, state="readonly").grid(
            row=3, column=0, sticky="ew"
        )
        ttk.Button(self, text="Copy to Clipboard", command=self.copy_password).grid(
            row=3, column=1, sticky="e", padx=(10, 0)
        )

        ttk.Label(self, text="Password strength").grid(row=4, column=0, sticky="w", pady=(15, 0))
        self.strength_label = ttk.Label(self, text="Not generated")
        self.strength_label.grid(row=4, column=1, sticky="e", pady=(15, 0))
        self.strength_bar = ttk.Progressbar(self, maximum=3, length=320)
        self.strength_bar.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(3, 0))

        ttk.Label(self, text="Last 5 passwords (this session only)").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(15, 2)
        )
        self.history_box = tk.Listbox(self, height=5, width=52)
        self.history_box.grid(row=7, column=0, columnspan=2, sticky="ew")
        ttk.Label(self, textvariable=self.status_var, wraplength=360).grid(
            row=8, column=0, columnspan=2, sticky="w", pady=(12, 0)
        )

    def generate(self) -> None:
        """Validate controls, generate securely, update GUI, and copy the result."""
        try:
            length = int(self.length_var.get())
        except ValueError:
            self._show_error("Password length must be a whole number.")
            return

        selected = [name for name, variable in self.type_vars.items() if variable.get()]
        try:
            password = generate_secure_password(length, selected, self.exclude_ambiguous_var.get())
        except ValueError as error:
            self._show_error(str(error))
            return

        self.password_var.set(password)
        strength, value = password_strength(length, len(selected))
        self.strength_label.config(text=strength)
        self.strength_bar["value"] = value
        self._add_to_history(password)
        self.copy_password(automatic=True)

    def copy_password(self, automatic: bool = False) -> None:
        """Copy the generated password using pyperclip, with an in-app status message."""
        password = self.password_var.get()
        if not password:
            self._show_error("Generate a password before copying it.")
            return
        try:
            import pyperclip

            pyperclip.copy(password)
        except (ImportError, RuntimeError, OSError) as error:
            self.status_var.set(f"Password generated, but clipboard copy failed: {error}")
            return

        action = "generated and copied" if automatic else "copied to the clipboard"
        self.status_var.set(f"Password {action}. It is not saved after this session.")

    def _add_to_history(self, password: str) -> None:
        self.history.insert(0, password)
        self.history = self.history[:5]
        self.history_box.delete(0, tk.END)
        for entry in self.history:
            self.history_box.insert(tk.END, entry)

    def _show_error(self, message: str) -> None:
        self.status_var.set(message)
        messagebox.showerror("Invalid selection", message)


if __name__ == "__main__":
    PasswordGeneratorApp().mainloop()
