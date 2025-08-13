"""
PECC WebSocket server entry point.
Handles multiple SECC connections asynchronously.
Modular, scalable, and maintainable.
"""

import asyncio
import websockets
from pecc.utils import log_info, log_error, Versions
from pecc.secc_connection import SECCConnectionHandler
from pecc.config_parser import PECCConfigParser

class PECCServer:
    def __init__(self, host=None, port=None):
        config = PECCConfigParser()
        self.host = host if host is not None else config.get("server_host")
        self.port = port if port is not None else config.get("server_port")
        self.active_connections = {}
 
    async def handler(self, *args):   # Use this for Websocket version > 10.1
        # websockets passes a ServerConnection object
        # Find the path and the connection of the Clients
        if Versions.check_if_websocket_old():
            connection, path = args
        else:
            connection = args[0]
            path = None
            if hasattr(connection, "request") and hasattr(connection.request, "path"):
                path = connection.request.path
        # Ensure path is always a valid string
        if not path or not isinstance(path, str):
            path = "/UNKNOWN"

        log_info(f"SECC connected: {path}")
        handler = SECCConnectionHandler(connection, path)
        self.active_connections[path] = handler
        try:
            await handler.run()
        except Exception as e:
            log_error(f"Connection error: {e}") 
        finally:
            if path in self.active_connections:
                del self.active_connections[path]
            else:
                log_error(f"Tried to remove connection for unknown path: {path}")
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