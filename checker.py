from pathlib import Path

DEFAULT_COMMON_PATH = Path(__file__).with_name("common_passwords.txt")


def load_common_passwords(filepath: Path = DEFAULT_COMMON_PATH) -> set[str]:
    if not filepath.exists():
        return set()
    with filepath.open("r", encoding="utf-8") as handle:
        return {
            line.strip().lower()
            for line in handle
            if line.strip() and not line.lstrip().startswith("#")
        }


def evaluate_password(password: str, common_passwords: set[str] | None = None) -> dict[str, object]:
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password.strip():
        return {
            "rating": "Weak",
            "score": 0,
            "tips": ["Enter a password or passphrase of at least 12 characters."],
        }

    common_set = common_passwords if common_passwords is not None else load_common_passwords()
    normalized = password.strip().lower()
    base_word = normalized.rstrip("0123456789!@#$%^&*()-_=+[]{}:,.?")
    length = len(password)

    if normalized in common_set or base_word in common_set:
        return {
            "rating": "Weak",
            "score": 1,
            "tips": [
                "This matches a commonly leaked or default password—choose something unique.",
                "Aim for 12–16+ characters or a multi-word passphrase.",
            ],
        }

    has_lower = any(ch.islower() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(not ch.isalnum() for ch in password)
    variety_count = sum([has_lower, has_upper, has_digit, has_symbol])

    tips: list[str] = []

    if length < 8:
        score = 1
        tips.append("Increase length to at least 12 characters (12–16+ is much stronger).")
    elif length < 12:
        score = 3
        tips.append("Consider extending to 12–16+ characters for stronger resistance to guessing.")
    elif length < 16:
        score = 5
    else:
        score = 6

    if variety_count >= 3:
        score += 2
    elif variety_count == 2:
        score += 1
    elif length < 14:
        tips.append("Add more character variety (uppercase, lowercase, digits, or symbols) or make it a longer passphrase.")

    if not has_symbol and length < 14:
        tips.append("Adding a symbol or using a 14–16+ character passphrase helps resist brute-force guesses.")

    if score >= 6 and length >= 12:
        rating = "Strong"
    elif score >= 3 and length >= 8:
        rating = "Fair"
    else:
        rating = "Weak"

    if not tips:
        tips.append("Strong length and structure—keep it unique to this account and store it in a password manager.")

    return {"rating": rating, "score": score, "tips": tips}