import logging
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from app.services.summarization_pipeline import hierarchical_summarization

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("text", "")
            language = data.get("language", "English")

            if not query.strip():
                await websocket.send_text("Error: Empty transcript received.")
                continue
            preview = query[:300].replace("\n", " ")  # show first 300 chars, flatten newlines
            logging.info(f"Received query (length={len(query)}): {preview}...")
            logging.info(f"Received language: {language}...")
            await hierarchical_summarization(query, language, websocket)

            # ✅ Explicitly close after one request
            await websocket.close(code=1000)
            logging.info("Closed WebSocket after completing summarization.")
            
    except WebSocketDisconnect:
        logging.info("Client disconnected.")
    except Exception as e:
        logging.error(f"Unexpected error in WebSocket: {e}")
