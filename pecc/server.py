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
        # GPIO integration
        from contactor_handler.contactor_handlers import GPIOController
        from contactor_handler.gpio_config import GPIO_PIN
        self.gpio_controller = GPIOController(GPIO_PIN.GPIO_PINS)
        # Track evConnectionState per gun
        self.gun_connection_state = {}
        # GPIO integration
        from contactor_handler.contactor_handlers import GPIOController
        from contactor_handler.gpio_config import GPIO_PIN
        self.gpio_controller = GPIOController(GPIO_PIN.GPIO_PINS)
        # For future: 32-bit contactor status
        self.contactor_status_bits = 0  # Each bit represents a contactor

    def update_contactor(self):
        # ON if any gun is 'connected', OFF if all are 'disconnected'
        if any(state in ["connected", "energyTransferAllowed"] for state in self.gun_connection_state.values()):
            self.gpio_controller.set_value("GPIO2_IO01", 0)
        else:
            self.gpio_controller.set_value("GPIO2_IO01", 1)
 
    async def handler(self, *args):   # Use this for Websocket version > 10.1
        # websockets passes a ServerConnection object
        # Find the path and the connection of the Clients
        if len(args) == 2:
            # Old API: (connection, path)
            connection, path = args
        elif len(args) == 1:
            # New API: (connection,)
            connection = args[0]
            path = getattr(connection, "path", None)
        else:
            log_error(f"Unexpected handler args: {args}")
            return

        log_info(f"SECC connected: {path}")
        handler = SECCConnectionHandler(connection, path, server=self)
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
    import threading
    from modules.read_module.read_module_data import perform_action
    from modules.module_handler import manage_modules

    # th1 = threading.Thread(target=update_module)
    th2 = threading.Thread(target=manage_modules)
    th3 = threading.Thread(target=perform_action)
    # th1.start()
    th2.start()
    th3.start()

    async def main():
        await server.start()
        await asyncio.Future()  # Run forever
    asyncio.run(main())
