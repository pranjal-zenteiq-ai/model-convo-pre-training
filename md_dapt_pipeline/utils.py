import re
import json

def fix_json_escapes(text: str) -> str:
    """Fix unescaped backslashes in latex/math expressions that break JSON parsing."""
    # Match a single backslash (not preceded by another backslash) 
    # that is NOT followed by a valid JSON escape char
    return re.sub(r'(?<!\\)\\([^"\\/bfnrtu])', r'\\\\\1', text)

def extract_json(text: str) -> dict:
    """Extract and parse JSON from LLM output that might contain markdown formatting."""
    text = text.strip()
    text = fix_json_escapes(text)
    
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
        
    # Look for JSON within markdown code blocks (e.g. ```json ... ```)
    match = re.search(r'```(?:json)?\s*(\{.*\}|\[.*\])\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    # Try finding the first '{' or '[' and last '}' or ']'
    # (naive but sometimes works when model misses markdown tags)
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    raise ValueError("Failed to extract JSON from text")
