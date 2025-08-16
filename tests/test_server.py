"""
Unit test for PECC WebSocket server connection handling.
"""
import asyncio
import pytest
import websockets
from pecc.server import PECCServer

NUM_CLIENTS = 3

@pytest.mark.asyncio
async def test_multiple_clients_connect_and_disconnect():
    server = PECCServer(host='localhost', port=9876) 
    # Start the server
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(0.2)  # Give server time to start

    uris = [f"ws://localhost:9876/client{i}" for i in range(NUM_CLIENTS)]
    clients = []

    # Connect multiple clients
    for uri in uris:
        ws = await websockets.connect(uri)
        clients.append(ws)
        await ws.send(f"hello from {uri}")

    # Each client sends a message and then closes independently
    for i, ws in enumerate(clients):
        await ws.send(f"bye from client{i}")
        await ws.close()

    # Wait a moment for server to process disconnects
    await asyncio.sleep(0.2)

    # Stop the server
    server_task.cancel()
