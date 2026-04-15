import logging
from fastapi import WebSocket
from app.utils.tokenizer_utils import chunk_text
from app.utils.prompt_builder import build_prompt
from app.services.ollama_client import stream_ollama_response
from app.config import MAX_CONTEXT_TOKENS, DEFAULT_MODEL

async def hierarchical_summarization(
    transcript: str,
    language: str,
    websocket: WebSocket,
    model: str = DEFAULT_MODEL
) -> str:
    chunks = chunk_text(transcript, MAX_CONTEXT_TOKENS)
    
    # Single chunk
    if len(chunks) == 1:
        logging.info("Single chunk detected. Skipping hierarchical step.")
        await websocket.send_text("\n\n--- Streaming the Summary ---\n")
        prompt = build_prompt(chunks[0], language)
        return await stream_ollama_response(prompt, websocket, model)

    # Multiple chunks
    partial_summaries = []

    logging.info(f"**Transcript is too long!**\n**Transcript splited into {len(chunks)} chunks!**")
    await websocket.send_text(f"**Transcript is too long!**\n**Transcript splited into {len(chunks)} chunks!**")

    # Summarize each chunk
    for idx, chunk in enumerate(chunks, start=1):
        logging.info(f"Summarizing chunk {idx}/{len(chunks)}...")
        await websocket.send_text(f"\n\n--- Streaming Chunk {idx}/{len(chunks)} Summary ---\n")
        prompt = build_prompt(chunk, language)
        summary = await stream_ollama_response(prompt, websocket, model)
        partial_summaries.append(f"--- Chunk {idx} Summary ---\n{summary}\n")

    combined_text = "\n".join(partial_summaries)

    # Final summary
    final_prompt = (
        "You are given a set of summaries from different chunks of a meeting transcript.\n\n"
        f"{combined_text}\n\n"
        "==== FINAL TASK ====\n"
        "Create a single comprehensive summary of the full meeting:\n\n"
        "=== Section 1: Speaker-Wise Summaries ===\n"
        "- Merge the speaker summaries across all chunks.\n"
        "- Use the format:\n\n[Speaker Name]\n- Point 1\n- Point 2\n\n"
        "- Avoid repetition.\n\n"
        "=== Section 2: Overall Meeting Summary ===\n"
        "- Provide a cohesive narrative.\n"
        "- Highlight key decisions, action items, and major discussions.\n\n"
        f"Please give your response in {language}, and make sure your output follows the input chunks structure, and don't omit any important information.\n\n"
        "### Response:\n"
    )

    await websocket.send_text("\n\n--- Streaming Final Summary ---\n")
    return await stream_ollama_response(final_prompt, websocket, model)
