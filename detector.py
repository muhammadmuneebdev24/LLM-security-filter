import re

# List of suspicious phrases
BAD_PATTERNS = [
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
    for pattern in BAD_PATTERNS:
        if pattern in text:
            return True   # Bad input found
    return False          # Input is clean