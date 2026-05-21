def make_decision(
    text,
    rule_score,
    semantic_score,
    masked_text
):

    final_risk = max(
        rule_score,
        semantic_score
    )

    if semantic_score >= 0.60:
        return {
            "decision": "BLOCK",
            "reason": "Semantic injection detected",
            "risk": final_risk,
            "output": None
        }

    if rule_score == 1:
        return {
            "decision": "BLOCK",
            "reason": "Rule-based attack detected",
            "risk": final_risk,
            "output": None
        }

    if masked_text != text:
        return {
            "decision": "MASK",
            "reason": "Sensitive data detected",
            "risk": final_risk,
            "output": masked_text
        }

    return {
        "decision": "ALLOW",
        "reason": "Input is safe",
        "risk": final_risk,
        "output": text
    }