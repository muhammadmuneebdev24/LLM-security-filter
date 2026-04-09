import csv
import os

CSV_FILE = "evaluation_log.csv"


def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Input Text",
                "Decision",
                "Injection Score",
                "PII Count",
                "Risk Level"
            ])


def get_risk(injection_score, pii_count):
    if injection_score == 1:
        return "HIGH"
    elif pii_count == 1:
        return "MEDIUM"
    return "LOW"


def save_to_csv(text, decision, injection_score, pii_count):
    init_csv()
    risk = get_risk(injection_score, pii_count)

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            text,
            decision,
            injection_score,
            pii_count,
            risk
        ])

    return risk