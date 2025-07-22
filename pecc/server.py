"""
PECC WebSocket server entry point.
Handles multiple SECC connections asynchronously.
Modular, scalable, and maintainable.
"""

import asyncio
import websockets
from pecc.utils import log_info, log_error
from pecc.secc_connection import SECCConnectionHandler
from pecc.config_parser import PECCConfigParser

class PECCServer:
    def __init__(self, host=None, port=None):
        config = PECCConfigParser()
        self.host = host if host is not None else config.get("server_host")
        self.port = port if port is not None else config.get("server_port")
        self.active_connections = {}

    async def handler(self, connection):
        # websockets passes a ServerConnection object
        path = getattr(connection, "path", None)
        log_info(f"SECC connected: {path}")
        handler = SECCConnectionHandler(connection, path)
        self.active_connections[path] = handler
        try:
            await handler.run()
        except Exception as e:
            log_error(f"Connection error: {e}")
        finally:
            del self.active_connections[path]
            log_info(f"SECC disconnected: {path}")

    def start(self):
        log_info(f"Starting PECC WebSocket server on {self.host}:{self.port}")
        return websockets.serve(self.handler, self.host, self.port)

# Entry point for running the server
if __name__ == "__main__":
    server = PECCServer()
    async def main():
        await server.start()
        await asyncio.Future()  # Run forever
    asyncio.run(main())
