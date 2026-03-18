import sys
import asyncio
import json
import os
from conversation import run_conversation
from verifier import verify
from validator import validate_spans
from dapt_writer import write_dapt

SEPARATOR = "=" * 70

async def process(md_path):
    print(f"\n{'🚀 DAPT PIPELINE START':=^70}")
    print(f"Input: {md_path}\n")

    md_text = open(md_path).read()
    md_id = md_path.split("/")[-1]

    if len(sys.argv) >= 3:
        transcript_path = sys.argv[2]
        print(f"Loading external transcript from {transcript_path}...")
        if transcript_path.endswith('.json'):
            with open(transcript_path) as f:
                transcript = json.load(f)
        else:
            with open(transcript_path) as f:
                transcript = f.read()
        
        print("\n✅ External transcript loaded successfully")
        
    else:
        # Remove stale cache so we always regenerate
        if os.path.exists("debug_transcript.json"):
            os.remove("debug_transcript.json")
            
        print("📝 Starting multi-turn conversation...\n")
        transcript = await run_conversation(md_text)

        # Always save transcript for debugging
        with open("debug_transcript.json", "w") as f:
            json.dump(transcript, f, indent=2)
        print("\n💾 Transcript saved to debug_transcript.json")

        if not transcript:
            print("\n❌ Transcript generation failed or is empty.")
            return

        # --- Span Validation ---
        print(f"\n{SEPARATOR}")
        print("🔍 STEP 2: Validating evidence spans against source markdown...")
        print(SEPARATOR)

        if isinstance(transcript, list):
            if not validate_spans(md_text, transcript):
                print("\n❌ Span validation failed. Some evidence strings are not in the source.")
                print("   The transcript is saved in debug_transcript.json for inspection.")
                return
            print("✅ All spans validated successfully!")
        else:
            print("✅ Skipping span validation for raw text transcript.")

    # --- Verifier ---
    print(f"\n{SEPARATOR}")
    print("🧪 STEP 3: Running Kimi K2.5 (thinking=true) as VERIFIER...")
    print(SEPARATOR)

    verdict = await verify(md_text, transcript)

    print(f"\n📋 Verifier Verdict: {verdict.get('verdict', 'unknown').upper()}")
    if verdict.get("confidence_score"):
        print(f"   Confidence: {verdict['confidence_score']}")
    if verdict.get("thought_process"):
        print(f"   Reasoning:\n{verdict['thought_process']}\n")
    if verdict.get("invalid_turns"):
        for inv in verdict["invalid_turns"]:
            print(f"   ⚠️  Turn {inv.get('turn_id')}: {inv.get('reason')}")

    if verdict.get("verdict") == "accept":
        write_dapt(md_id, transcript)
        print("\n✅ ACCEPTED! DAPT output appended to dapt_output.txt")
    else:
        print("\n❌ REJECTED by verifier.")

    print(f"\n{'🏁 PIPELINE COMPLETE':=^70}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: uv run python main.py input.md [transcript.md]")
        sys.exit(1)

    asyncio.run(process(sys.argv[1]))
