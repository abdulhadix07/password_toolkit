import hashlib
import requests

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"
DEFAULT_USER_AGENT = "password-toolkit-k-anonymity-check/1.0"


def split_sha1_digest(password: str) -> tuple[str, str]:
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return digest[:5], digest[5:]
def check_pwned_password(
    password: str,
    timeout: float = 5.0,
    user_agent: str = DEFAULT_USER_AGENT,
) -> int:
    if not password:
        raise ValueError("Password must not be empty.")

    prefix, suffix = split_sha1_digest(password)
    url = HIBP_RANGE_URL.format(prefix=prefix)
    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError("Unable to reach the breach-check service.") from exc

    for line in response.text.splitlines():
        parts = line.strip().split(":", maxsplit=1)
        if len(parts) != 2:
            continue
        returned_suffix, raw_count = parts
        if returned_suffix.strip().upper() == suffix:
            try:
                return int(raw_count.strip())
            except ValueError as exc:
                raise RuntimeError("Unexpected breach count format returned.") from exc

    return 0
