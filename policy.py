def make_decision(text, injection, masked):

    # Step 1: Injection → BLOCK
    if injection:
        return {
            "decision": "BLOCK",
            "reason": "Injection attack detected",
            "output": None
        }

    # Step 2: Masking → MASK
    if masked != text:
        return {
            "decision": "MASK",
            "reason": "Sensitive info was masked",
            "output": masked
        }

    # Step 3: Clean → ALLOW
    return {
        "decision": "ALLOW",
        "reason": "Input is clean",
        "output": text
    }