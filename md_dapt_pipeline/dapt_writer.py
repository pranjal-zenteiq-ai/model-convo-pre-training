def write_dapt(md_id, transcript):
    block = f"<|DAPT_DOC| md_id={md_id}>\n\n"

    if isinstance(transcript, str):
        block += transcript + "\n\n"
    else:
        for turn in transcript:
            block += f"{turn['role']}: {turn['content']}\n\n"

    block += "<|END_DOC|>\n"

    with open("dapt_output.txt", "a") as f:
        f.write(block)
