import asyncio
import websockets
import json
import sys
from pathlib import Path
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


async def test(file_path: str, language: str):
    # Read meeting transcript from a text file
    transcript = Path(file_path).read_text(encoding="utf-8")

    uri = "ws://localhost:8009/ws"
    async with websockets.connect(uri) as websocket:
        # Send the meeting transcript + target language
        message = {
            "text": transcript,
            "language": language
        }
        await websocket.send(json.dumps(message))

        #print(f"Responding in {language}:")
        try:
            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=40)
                print(response, end="", flush=True)
        except asyncio.TimeoutError:
            print("\n⏳ No new messages for 20s — closing connection.")
        except ConnectionClosedOK:
            print("\n✅ Connection closed cleanly by server.")
        except ConnectionClosedError as e:
            print(f"\n⚠️ Connection closed with error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            # Ensure the websocket is closed gracefully
            if not websocket.close:
                await websocket.close()
                print("🔒 Client closed the connection.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test.py <meeting_file.txt> <language>")
        sys.exit(1)

    file_path = sys.argv[1]
    language = sys.argv[2]
    asyncio.run(test(file_path, language))
