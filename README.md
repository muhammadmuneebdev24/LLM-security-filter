LLM Security Gateway (FastAPI)

 Project Overview:
This project implements a Security Gateway for LLM Applications that protects systems from:

Prompt Injection / Jailbreak attacks
Sensitive data exposure (PII leakage)
Unsafe or malicious user inputs

 Features:
Detects prompt injection attacks using rule-based patterns
Masks sensitive data (PII) using Microsoft Presidio
Policy-based decision system:
BLOCK → malicious input
MASK → sensitive data detected
ALLOW → safe input
Saves evaluation logs in CSV
FastAPI backend for API handling

⚙️ Installation & Setup
Step 1: Clone Repository
git clone <your-repo-link>
cd <repo-name>
Step 2: Create Virtual Environment
python -m venv venv

Activate it:
venv\Scripts\activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Run the Server
uvicorn main:app --reload

Server will start
Open in browser:
Endpoint
POST /process
