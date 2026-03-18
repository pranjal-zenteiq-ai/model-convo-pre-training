from config import GEN_MODEL_A, GEN_MODEL_B, GEN_TEMP_A, GEN_TEMP_B, MAX_TURNS
from llm_client import call_llm
from prompts import explorer_prompt, elaborator_prompt
from utils import extract_json

SEPARATOR = "=" * 70

async def run_conversation(md_text):
    transcript = []

    for turn_id in range(1, MAX_TURNS + 1):
        if turn_id % 2 == 1:
            prompt = explorer_prompt(md_text, transcript)
            model = GEN_MODEL_A
            temp = GEN_TEMP_A
            role_label = "EXPLORER"
        else:
            prompt = elaborator_prompt(md_text, transcript)
            model = GEN_MODEL_B
            temp = GEN_TEMP_B
            role_label = "ELABORATOR"

        print(f"\n{SEPARATOR}")
        print(f"Turn {turn_id}/{MAX_TURNS} | {role_label} | model={model} | temp={temp}")
        print(SEPARATOR)

        try:
            raw = await call_llm(model, prompt, temp)
            parsed = extract_json(raw)
            transcript.append(parsed)

            # Print the actual conversation content
            print(f"\n💬 {parsed.get('role', role_label)}:")
            print(f"   {parsed.get('content', '(no content)')}")
            if parsed.get('anchor_span'):
                print(f"\n   📌 Anchor: \"{parsed['anchor_span'][:120]}...\"")
            if parsed.get('evidence_spans'):
                for i, span in enumerate(parsed['evidence_spans'], 1):
                    print(f"   📎 Evidence {i}: \"{span[:120]}...\"")
            if parsed.get('thought_process'):
                print(f"\n   🧠 Thought: {parsed['thought_process'][:200]}...")
            print(f"   hypothesis={parsed.get('hypothesis', False)}")

        except Exception as e:
            print(f"\n❌ Turn {turn_id} failed: {e}")
            break

        if len(transcript) >= 2:
            if transcript[-1].get("hypothesis") and transcript[-2].get("hypothesis"):
                print("\n⚠️  Two consecutive hypotheses detected. Stopping early.")
                break

    print(f"\n{SEPARATOR}")
    print(f"Conversation completed: {len(transcript)} turns generated.")
    print(SEPARATOR)
    return transcript
