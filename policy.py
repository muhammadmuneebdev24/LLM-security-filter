def make_decision(
    text,
    rule_score,
    semantic_score,
    masked_text
):

    # -----------------------------
    # FINAL RISK CALCULATION
    # -----------------------------

    final_risk = max(
        rule_score,
        semantic_score
    )

    # -----------------------------
    # BLOCK CONDITIONS
    # -----------------------------

    # Strong semantic attack
    if semantic_score >= 0.75:
        return {
            "decision": "BLOCK",
            "reason": "Semantic injection detected",
            "risk": final_risk,
            "output": None
        }

    # Strong rule attack
    if rule_score == 1:
        return {
            "decision": "BLOCK",
            "reason": "Rule-based attack detected",
            "risk": final_risk,
            "output": None
        }

    # -----------------------------
    # MASK CONDITIONS
    # -----------------------------

    if masked_text != text:
        return {
            "decision": "MASK",
            "reason": "Sensitive data detected",
            "risk": final_risk,
            "output": masked_text
        }

    # -----------------------------
    # SAFE INPUT
    # -----------------------------

    return {
        "decision": "ALLOW",
        "reason": "Input is safe",
        "risk": final_risk,
        "output": text
    }