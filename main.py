from fastapi import FastAPI
from pydantic import BaseModel

from detector import analyze_prompt
from presidio_utils import mask_pii
from policy import make_decision
from evaluate_quan import save_to_csv

app = FastAPI(
    title="LLM Security Gateway",
    version="3.0"
)

# -----------------------------------
# INPUT MODEL
# -----------------------------------

class UserInput(BaseModel):
    text: str

# -----------------------------------
# MAIN ENDPOINT
# -----------------------------------

@app.post("/process")

def process_input(user_input: UserInput):

    text = user_input.text

    # -----------------------------------
    # STEP 1 — DETECTOR ANALYSIS
    # -----------------------------------

    analysis = analyze_prompt(text)

    language = analysis["language"]

    translated_text = analysis["translated_text"]

    rule_score = analysis["rule_score"]

    semantic_score = analysis["semantic_score"]

    # -----------------------------------
    # STEP 2 — PII MASKING
    # -----------------------------------

    masked_text = mask_pii(
        translated_text
    )

    pii_count = 0 if masked_text == translated_text else 1

    # -----------------------------------
    # STEP 3 — POLICY ENGINE
    # -----------------------------------

    result = make_decision(
        translated_text,
        rule_score,
        semantic_score,
        masked_text
    )

    decision = result["decision"]

    # -----------------------------------
    # STEP 4 — FINAL OUTPUT
    # -----------------------------------

    if decision == "BLOCK":

        output = (
            "Request blocked due to "
            "security policy"
        )

    elif decision == "MASK":

        output = masked_text

    else:

        output = translated_text

    # -----------------------------------
    # STEP 5 — SAVE LOGS
    # -----------------------------------

    risk_level = save_to_csv(
        text,
        translated_text,
        language,
        decision,
        rule_score,
        semantic_score,
        pii_count
    )

    # -----------------------------------
    # FINAL RESPONSE
    # -----------------------------------

    return {

        "original_text": text,

        "translated_text": translated_text,

        "language": language,

        "rule_score": rule_score,

        "semantic_score": semantic_score,

        "pii_count": pii_count,

        "decision": decision,

        "risk_level": risk_level,

        "output": output
    }