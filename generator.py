import secrets
import string

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}:,.?"


def generate_password(
    length: int = 16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    selected_pools: list[str] = []
    if use_lower:
        selected_pools.append(LOWERCASE)
    if use_upper:
        selected_pools.append(UPPERCASE)
    if use_digits:
        selected_pools.append(DIGITS)
    if use_symbols:
        selected_pools.append(SYMBOLS)

    if not selected_pools:
        raise ValueError("At least one character set must be enabled.")

    min_length = len(selected_pools)
    if length < min_length:
        raise ValueError(f"Length must be at least {min_length} for the selected character sets.")

    rng = secrets.SystemRandom()
    chars: list[str] = [secrets.choice(pool) for pool in selected_pools]

    full_pool = "".join(selected_pools)
    remaining = length - len(chars)
    for _ in range(remaining):
        chars.append(secrets.choice(full_pool))

    rng.shuffle(chars)
    return "".join(chars)


DEFAULT_WORDS = (
    "amber", "basalt", "cedar", "delta", "ember", "falcon",
    "glacier", "harbor", "ivy", "jasper", "kestrel", "lantern",
    "meadow", "nebula", "orbit", "prairie", "quartz", "river",
    "summit", "timber", "umber", "velvet", "willow", "zenith",
)


def generate_passphrase(words_count: int = 4, separator: str = "-") -> str:
    if words_count < 3:
        raise ValueError("Use at least 3 words for a passphrase.")
    picked = [
        DEFAULT_WORDS[secrets.randbelow(len(DEFAULT_WORDS))]
        for _ in range(words_count)
    ]
    return separator.join(picked)