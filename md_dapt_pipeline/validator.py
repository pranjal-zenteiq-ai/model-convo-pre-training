import re

def normalize(text):
    return re.sub(r'\s+', '', text)

def validate_spans(md_text, transcript):
    norm_md = normalize(md_text)
    for turn in transcript:
        if "anchor_span" in turn:
            span = turn["anchor_span"]
            if normalize(span) not in norm_md:
                print(f"Validation failed on anchor_span: '{span}'")
                return False
        for span in turn.get("evidence_spans", []):
            if normalize(span) not in norm_md:
                print(f"Validation failed on evidence_span: '{span}'")
                return False
    return True
