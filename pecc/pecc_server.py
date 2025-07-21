import asyncio
import websockets
import json
from pecc.messages import *

async def handle_secc(websocket, path):
    print(f"SECC connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received from SECC: {data}")
                # Example: echo back the same message as a response
                response = {
                    "type": "response",
                    "kind": data.get("kind", "unknown"),
                    "sequenceNumber": data.get("sequenceNumber", 0),
                    "payload": {"status": "ok"}
                }
                await websocket.send(json.dumps(response))
            except Exception as e:
                print(f"Error processing message: {e}")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("SECC disconnected")

async def main():
    async with websockets.serve(handle_secc, "0.0.0.0", 8765):
        print("PECC server started on port 8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
