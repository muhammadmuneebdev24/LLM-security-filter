from fastapi import FastAPI
from pydantic import BaseModel

from detector import check_injection
from presidio_utils import mask_pii
from policy import make_decision

app = FastAPI(title="LLM Security Gateway API")


# Input model
class UserMessage(BaseModel):
    text: str


# Root route (just to check API is running)
@app.get("/")
def home():
    return {"message": "LLM Security Gateway API is running"}


# Main API route
@app.post("/check")
def check_message(message: UserMessage):
    user_text = message.text

    # Step 1: Injection detection
    is_injection = check_injection(user_text)

    # Step 2: PII masking
    masked_text = mask_pii(user_text)

    # Step 3: Decision
    result = make_decision(user_text, is_injection, masked_text)

    return result