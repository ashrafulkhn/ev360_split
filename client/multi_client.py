"""
Multi-client script to connect to PECC server, send JSON messages, and disconnect.
"""
import asyncio
import websockets
import json

NUM_CLIENTS = 3
SERVER_URI = "ws://localhost:8765"

async def client_task(client_id):
    uri = f"{SERVER_URI}/client{client_id}"
    async with websockets.connect(uri) as ws:
        msg = {
            "type": "request",
            "client_id": client_id,
            "action": "connect",
            "payload": {"message": f"Hello from client {client_id}"}
        }
        await ws.send(json.dumps(msg))
        # Optionally, wait for a response
        # response = await ws.recv()
        # print(f"Client {client_id} received: {response}")
        # Send disconnect message
        disconnect_msg = {
            "type": "request",
            "client_id": client_id,
            "action": "disconnect",
            "payload": {"message": f"Goodbye from client {client_id}"}
        }
        await ws.send(json.dumps(disconnect_msg))
        # Connection will be closed after this

async def main():
    await asyncio.gather(*(client_task(str(i)) for i in range(NUM_CLIENTS)))

if __name__ == "__main__":
    asyncio.run(main())
