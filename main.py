from password_toolkit.checker import evaluate_password


def run_check(candidate: str) -> None:
    result = evaluate_password(candidate)
    print(f"Rating: {result['rating']}")
    for tip in result["tips"]:
        print(f"- {tip}")


if __name__ == "__main__":
    # Use synthetic sample inputs only; never use real passwords in code or tests.
    run_check("Tr0ub4dor&3!")