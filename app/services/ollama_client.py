import json
import httpx
import logging
from fastapi import WebSocket
from app.config import OLLAMA_HOST, DEFAULT_MODEL

async def stream_ollama_response(prompt: str, websocket: WebSocket, model: str = DEFAULT_MODEL) -> str:
    logging.info(f"Sending prompt to Ollama (model={model})...")

    full_output = ""
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(600.0, read=None)) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"top_p": 0.9, "top_k": 50, "num_predict": 2048},
                },
            ) as response:
                logging.info(f"Ollama response status: {response.status_code}")
                if response.status_code != 200:
                    err_text = await response.aread()
                    logging.error(f"Ollama error: {err_text.decode()}")
                    await websocket.send_text(f"[Error from Ollama: {err_text.decode()}]")
                    return ""

                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            full_output += token
                            try:
                                await websocket.send_text(token)
                            except Exception as ws_err:
                                logging.error(f"WebSocket send failed: {ws_err}")
                                break
                    except json.JSONDecodeError as e:
                        logging.warning(f"JSON parse error: {e}")
                        continue
    except Exception as e:
        logging.error(f"Stream error: {e}")

    return full_output