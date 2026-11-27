from checker import evaluate_password
from generator import generate_password, generate_passphrase
from breach_check import check_pwned_password
from generator import generate_passphrase, generate_password


def handle_check() -> None:
    candidate = getpass.getpass("Enter password to evaluate (input hidden): ")
    result = evaluate_password(candidate)
    print(f"\nStrength: {result['rating']} (score: {result['score']}/8)")
    for tip in result["tips"]:
        print(f"  - {tip}")

    if not candidate.strip():
        return

    try:
        breach_count = check_pwned_password(candidate)
        if breach_count > 0:
            print(f"Breach check: Exposed in known breaches ({breach_count:,} times). Do not use it.")
        else:
            print("Breach check: Not found in known breach corpus.")
    except RuntimeError as exc:
        print(f"Breach check skipped: {exc} (Local strength check above still completed.)")


def handle_generate_password() -> None:
    raw_len = input("Length [16]: ").strip()
    length = int(raw_len) if raw_len else 16
    use_symbols = input("Include symbols? [Y/n]: ").strip().lower() != "n"
    try:
        pwd = generate_password(length=length, use_symbols=use_symbols)
        print(f"\nGenerated password (in memory only): {pwd}")
    except ValueError as exc:
        print(f"Invalid option: {exc}")


def handle_generate_passphrase() -> None:
    raw_words = input("Word count [4]: ").strip()
    words = int(raw_words) if raw_words else 4
    try:
        phrase = generate_passphrase(words_count=words)
        print(f"\nGenerated passphrase (in memory only): {phrase}")
    except ValueError as exc:
        print(f"Invalid option: {exc}")


def main() -> None:
    actions = {
        "1": handle_check,
        "2": handle_generate_password,
        "3": handle_generate_passphrase,
    }
    while True:
        print("\n=== Password Toolkit ===")
        print("1. Check password strength & breach status")
        print("2. Generate cryptographic password")
        print("3. Generate cryptographic passphrase")
        print("4. Exit")
        choice = input("Select an option [1-4]: ").strip()
        if choice == "4":
            print("Exiting. No secrets were saved to disk.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()