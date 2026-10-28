"""Password Generator (CodSoft Python Internship - Task 3).

Asks for a password length and which character types to include,
then generates a random password and prints it.
"""

import secrets
import string


def ask_yes_no(prompt, default=True):
    suffix = " [Y/n]: " if default else " [y/N]: "
    answer = input(prompt + suffix).strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def ask_length():
    while True:
        raw = input("Password length (minimum 4): ").strip()
        try:
            length = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if length < 4:
            print("Length must be at least 4.")
            continue
        return length


def build_character_pool():
    pool = ""
    required = []

    if ask_yes_no("Include lowercase letters?"):
        pool += string.ascii_lowercase
        required.append(string.ascii_lowercase)
    if ask_yes_no("Include uppercase letters?"):
        pool += string.ascii_uppercase
        required.append(string.ascii_uppercase)
    if ask_yes_no("Include digits?"):
        pool += string.digits
        required.append(string.digits)
    if ask_yes_no("Include symbols?", default=False):
        pool += string.punctuation
        required.append(string.punctuation)

    if not pool:
        print("No character types selected. Using lowercase and digits.")
        pool = string.ascii_lowercase + string.digits
        required = [string.ascii_lowercase, string.digits]

    return pool, required


def generate_password(length, pool, required):
    """Build a password of the given length.

    One character from each selected group is guaranteed, so the
    password always satisfies the chosen complexity rules.
    """
    if length < len(required):
        raise ValueError("Length is too short for the selected character types.")

    chars = [secrets.choice(group) for group in required]
    chars += [secrets.choice(pool) for _ in range(length - len(chars))]
    # Shuffle so the guaranteed characters are not always at the start.
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main():
    print("========== PASSWORD GENERATOR ==========")
    length = ask_length()
    pool, required = build_character_pool()

    if length < len(required):
        print(f"Length must be at least {len(required)} for these options.")
        length = len(required)

    password = generate_password(length, pool, required)
    print(f"\nYour pasword: {password}\n")


if __name__ == "__main__":
    main()
