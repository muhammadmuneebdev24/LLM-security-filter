from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from detector import check_injection
from presidio_utils import mask_pii
from policy import make_decision

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Input model
class UserMessage(BaseModel):
    text: str

# Frontend route (opens HTML page)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("frontend.html", {"request": request})

# Backend API route
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