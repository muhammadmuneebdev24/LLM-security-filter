import csv
import os
from datetime import datetime

CSV_FILE = "evaluation_log.csv"


def init_csv():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Original Text",
                "Translated Text",
                "Language",
                "Decision",
                "Rule Score",
                "Semantic Score",
                "PII Count",
                "Risk Level"
            ])

def get_risk(rule_score, semantic_score, pii_count):

    if semantic_score >= 0.75 or rule_score == 1:
        return "HIGH"

    elif pii_count > 0:
        return "MEDIUM"

    return "LOW"


def save_to_csv(
    original_text,
    translated_text,
    language,
    decision,
    rule_score,
    semantic_score,
    pii_count
):

    init_csv()

    risk = get_risk(
        rule_score,
        semantic_score,
        pii_count
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        CSV_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            original_text,
            translated_text,
            language,
            decision,
            rule_score,
            semantic_score,
            pii_count,
            risk
        ])

    return risk