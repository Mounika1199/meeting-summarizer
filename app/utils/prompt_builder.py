def build_prompt(query: str, language: str) -> str:
    return (
        "Meeting Transcript:\n" + query + "\n\n"
        "==== TASK ====\n"
        "You are given a transcript of a team meeting (possibly partial).\n\n"
        "Your task is to generate one structured section:\n\n"
        "=== Section 1: Speaker-Wise Summaries ===\n"
        "- Provide a summary of the updates or contributions of each speaker.\n"
        "- Use the format:\n\n[Speaker Name]\n- Point 1\n- Point 2\n\n"
        "- Include all speakers, even if their update was short.\n"
        "=== Section 2: Overall Meeting Summary ===\n"
        "- Summarize the key points discussed in this chunk.\n"
        "- Highlight decisions made.\n"
        "- List any action items assigned.\n\n"
        f"Please give your response in {language}.\n\n"
        "\n\n### Response:\n"
    )
