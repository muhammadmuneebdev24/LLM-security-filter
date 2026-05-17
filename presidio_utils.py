from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    Pattern
)

from presidio_anonymizer import AnonymizerEngine

from presidio_anonymizer.entities import (
    OperatorConfig
)

# -----------------------------------
# INITIALIZE PRESIDIO
# -----------------------------------

analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()

# -----------------------------------
# API KEY DETECTOR
# -----------------------------------

api_pattern = Pattern(
    name="api_key",
    regex=r"sk-[A-Za-z0-9]+",
    score=0.95
)

api_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[api_pattern]
)

# -----------------------------------
# CNIC DETECTOR
# -----------------------------------

cnic_pattern = Pattern(
    name="pakistan_cnic",
    regex=r"\b[0-9]{5}-[0-9]{7}-[0-9]{1}\b",
    score=0.95
)

cnic_recognizer = PatternRecognizer(
    supported_entity="PAKISTAN_CNIC",
    patterns=[cnic_pattern]
)

# -----------------------------------
# EMAIL DETECTOR
# -----------------------------------

email_pattern = Pattern(
    name="custom_email",
    regex=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    score=0.90
)

email_recognizer = PatternRecognizer(
    supported_entity="CUSTOM_EMAIL",
    patterns=[email_pattern]
)

# -----------------------------------
# PHONE NUMBER DETECTOR
# -----------------------------------

phone_pattern = Pattern(
    name="pk_phone",
    regex=r"\b03[0-9]{9}\b",
    score=0.85
)

phone_recognizer = PatternRecognizer(
    supported_entity="PK_PHONE",
    patterns=[phone_pattern]
)

# -----------------------------------
# STUDENT ID DETECTOR
# -----------------------------------

student_pattern = Pattern(
    name="student_id",
    regex=r"FA[0-9]{2}-[A-Z]{3}-[0-9]{3}",
    score=0.90
)

student_recognizer = PatternRecognizer(
    supported_entity="STUDENT_ID",
    patterns=[student_pattern]
)

# -----------------------------------
# INTERNAL EMPLOYEE ID
# -----------------------------------

emp_pattern = Pattern(
    name="emp_id",
    regex=r"EMP[0-9]+",
    score=0.85
)

emp_recognizer = PatternRecognizer(
    supported_entity="INTERNAL_ID",
    patterns=[emp_pattern]
)

# -----------------------------------
# ADD ALL RECOGNIZERS
# -----------------------------------

analyzer.registry.add_recognizer(
    api_recognizer
)

analyzer.registry.add_recognizer(
    cnic_recognizer
)

analyzer.registry.add_recognizer(
    email_recognizer
)

analyzer.registry.add_recognizer(
    phone_recognizer
)

analyzer.registry.add_recognizer(
    student_recognizer
)

analyzer.registry.add_recognizer(
    emp_recognizer
)

# -----------------------------------
# MAIN MASK FUNCTION
# -----------------------------------

def mask_pii(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    if not results:
        return text

    operators = {

        "API_KEY": OperatorConfig(
            "replace",
            {"new_value": "<API_KEY>"}
        ),

        "PAKISTAN_CNIC": OperatorConfig(
            "replace",
            {"new_value": "<CNIC>"}
        ),

        "CUSTOM_EMAIL": OperatorConfig(
            "replace",
            {"new_value": "<EMAIL>"}
        ),

        "PK_PHONE": OperatorConfig(
            "replace",
            {"new_value": "<PHONE>"}
        ),

        "STUDENT_ID": OperatorConfig(
            "replace",
            {"new_value": "<STUDENT_ID>"}
        ),

        "INTERNAL_ID": OperatorConfig(
            "replace",
            {"new_value": "<ID>"}
        )
    }

    masked_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )

    return masked_result.text