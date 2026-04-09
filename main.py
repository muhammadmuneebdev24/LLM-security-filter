from fastapi import FastAPI
from pydantic import BaseModel

from detector import check_injection
from presidio_utils import mask_pii
from policy import make_decision
from evaluate_quan import save_to_csv

app = FastAPI(title="LLM Security Gateway", version="2.0")


class UserInput(BaseModel):
    text: str


@app.post("/process")
def process_input(user_input: UserInput):

    text = user_input.text

    # 🔹 Injection
    is_injection = check_injection(text)
    injection_score = 1 if is_injection else 0

    # 🔹 PII
    masked_text = mask_pii(text)
    pii_count = 0 if masked_text == text else 1

    # 🔹 Decision
    result = make_decision(text, is_injection, masked_text)
    decision = result["decision"]

    # 🔹 Output
    if decision == "BLOCK":
        output = "Request blocked due to injection attack"
    elif decision == "MASK":
        output = masked_text
    else:
        output = text

    # 🔹 Save evaluation
    risk_level = save_to_csv(
        text,
        decision,
        injection_score,
        pii_count
    )

    return {
        "decision": decision,
        "output": output,
        "injection_score": injection_score,
        "pii_count": pii_count,
        "risk_level": risk_level
    }