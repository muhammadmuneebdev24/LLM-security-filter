from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


# -------- CUSTOM RULES -------- #

# API Key detector
apipattern = Pattern(
    name="api_key",
    regex=r"sk-[A-Za-z0-9]+",
    score=0.9
)

api_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[apipattern]
)


# Pakistani phone number detector
phpattern = Pattern(
    name="pk_phone",
    regex=r"\b03[0-9]{9}\b",
    score=0.85
)

phone_recognizer = PatternRecognizer(
    supported_entity="PK_PHONE",
    patterns=[phpattern]
)


# Employee ID detector
emppattern = Pattern(
    name="emp_id",
    regex=r"EMP[0-9]+",
    score=0.85
)

emp_recognizer = PatternRecognizer(
    supported_entity="INTERNAL_ID",
    patterns=[emppattern]
)


# Add recognizers
analyzer.registry.add_recognizer(api_recognizer)
analyzer.registry.add_recognizer(phone_recognizer)
analyzer.registry.add_recognizer(emp_recognizer)


# -------- MAIN FUNCTION -------- #

def mask_pii(text):
    results = analyzer.analyze(text=text, language="en")

    if not results:
        return text

    operators = {
        "API_KEY": OperatorConfig("replace", {"new_value": "<API_KEY>"}),
        "PK_PHONE": OperatorConfig("replace", {"new_value": "<PHONE>"}),
        "INTERNAL_ID": OperatorConfig("replace", {"new_value": "<ID>"})
    }

    masked = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )

    return masked.text