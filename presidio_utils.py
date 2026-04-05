from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Create the analyzer and anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

#  detect API keys 
apipattern = Pattern(name="api_key",
                             regex=r"sk-[A-Za-z0-9]+",
                             score=0.9)
api_recognizer = PatternRecognizer(supported_entity="API_KEY",
                                        patterns=[apipattern ])

# Custom rule 2: detect Pakistani phone numbers like 03001234567
phonepattern = Pattern(name="pk_phone",
                            regex=r"\b03[0-9]{9}\b",
                              score=0.85)
phone_recognizer = PatternRecognizer(supported_entity="PK_PHONE",
                                         patterns=[phonepattern])

# Custom rule 3: detect employee IDs like EMP-1234
empidpattern = Pattern(name="emp_id",
                          regex=r"EMP[0-9]+",
                            score=0.85)
empid_recognizer = PatternRecognizer(supported_entity="INTERNAL_ID", patterns=[empidpattern])

# Add all custom rules
analyzer.registry.add_recognizer(api_recognizer)
analyzer.registry.add_recognizer(phone_recognizer)
analyzer.registry.add_recognizer(empid_recognizer)

def mask_pii(text):
    # Find sensitive info in the text
    results = analyzer.analyze(text=text, language="en")
    
    # If nothing found, return text as is
    if not results:
        return text
    operators = {
        "API_KEY": OperatorConfig("replace", {"new_value": "<API_KEY>"}),
        "PK_PHONE": OperatorConfig("replace", {"new_value": "<PHONE>"}),
        "INTERNAL_ID": OperatorConfig("replace", {"new_value": "<ID>"})
    }
    # Replace sensitive info with <masked>
    masked = anonymizer.anonymize(text=text,
                                   analyzer_results=results,
                                    operators=operators)
    return masked.text