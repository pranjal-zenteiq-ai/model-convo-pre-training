from config import VERIFIER_MODEL, VERIFIER_TEMP
from llm_client import call_llm
from prompts import verifier_prompt
from utils import extract_json

async def verify(md_text, transcript):
    prompt = verifier_prompt(md_text, transcript)
    
    print("\n========== VERIFIER INPUT PROMPT ==========")
    print(prompt)
    print("===========================================\n")
    
    raw = await call_llm(VERIFIER_MODEL, prompt, VERIFIER_TEMP, thinking=True)

    print("\n========== VERIFIER RAW OUTPUT ==========")
    print(raw)
    print("=========================================\n")

    try:
        return extract_json(raw)
    except Exception as e:
        print(f"Failed to parse verifier output JSON. Error: {e}")
        return {"verdict": "reject"}
