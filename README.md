# Password Toolkit

A local-first Python CLI toolkit for evaluating password strength, generating cryptographically secure passwords and passphrases, and checking known data breaches using the Have I Been Pwned (HIBP) k-anonymity API.

---

## Features

- **Layered Strength Evaluation (`checker.py`)**: Scores passwords across length, character variety, whitespace edge cases, and common password/mutation matching (`common_passwords.txt`).
- **Cryptographic Generation (`generator.py`)**: Uses Python's OS-backed `secrets` module (`secrets.choice`, `secrets.SystemRandom().shuffle`, and `secrets.randbelow`)—never `random`—with guaranteed coverage of every enabled character set.
- **Privacy-Preserving Breach Checks (`breach_check.py`)**: Queries the Have I Been Pwned range API using 5-character SHA-1 hash prefixes so neither plaintext passwords nor full hashes ever leave your machine.
- **In-Memory CLI (`main.py`)**: Masks interactive password input with `getpass` and keeps generated credentials strictly in memory without writing secrets to disk or logs.

---

## Project Architecture

```text
password_toolkit/
├── checker.py            # Local strength scoring and common-password detection
├── generator.py          # Cryptographic password and passphrase generation via secrets
├── breach_check.py       # HIBP k-anonymity range query and local suffix matching
├── main.py               # Interactive CLI menu with masked input (getpass)
├── test_toolkit.py       # Unit test suite covering edge cases and mocked API behavior
├── common_passwords.txt  # Local blocklist of common/default passwords
├── requirements.txt      # External dependencies (requests)
└── README.md             # Project documentation