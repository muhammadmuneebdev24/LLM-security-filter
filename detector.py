# List of suspicious phrases
bad_pattern = [
    "ignore instructions",
    "you are now",
    "jailbreak",
    "pretend you are",
    "bypass",
    "reveal system prompt",
    "forget your rules",
    "do anything now",
    "hack",
]


def check_injection(text):
    text = text.lower()

    for pattern in bad_pattern:
        if pattern in text:
            return True   # Bad input found

    return False  # Input is clean