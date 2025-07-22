"""
SECC Connection Handler for PECC system.
Manages communication and sessions for each SECC connection.
Modular and scalable for multiple SECCs.
"""

from pecc.utils import log_info, log_error
from pecc.gun_session import GunSession, GunState

class SECCConnectionHandler:
    def __init__(self, websocket, path):
        self.websocket = websocket
        self.path = path
        self.active = True
        # Extract gun id from path, e.g., '/GUN5' -> 'GUN5'
        self.gun_id = path.lstrip('/') if path else None
        self.session = GunSession(self.gun_id)

    async def run(self):
        log_info(f"Handler started for SECC: {self.path}")
        try:
            async for message in self.websocket:
                log_info(f"Received message from SECC {self.path}: {message}")
                # Example: parse message and update session state/data
                # You can expand this logic for real protocol parsing
                # For demonstration, let's assume message is a JSON string
                import json
                try:
                    msg = json.loads(message)
                    kind = msg.get("kind")
                    payload = msg.get("payload", {})
                    if kind == "evConnectionState":
                        status = payload.get("evConnectionState")
                        await self.session.set_status(status)
                        if status == "error":
                            await self.session.transition_state(GunState.ERROR)
                        elif status == "charging":
                            await self.session.transition_state(GunState.CHARGING)
                        elif status == "idle":
                            await self.session.transition_state(GunState.IDLE)
                    elif kind == "configuration":
                        # Example: update current/voltage demand if present
                        current = payload.get("current_demand")
                        voltage = payload.get("voltage_demand")
                        if current is not None:
                            await self.session.set_current_demand(current)
                        if voltage is not None:
                            await self.session.set_voltage_demand(voltage)
                    # Add more message kinds and session updates as needed
                except Exception as e:
                    log_error(f"Failed to parse/update session for SECC {self.path}: {e}")
        except Exception as e:
            log_error(f"SECC handler error: {e}")
        finally:
            self.active = False
            log_info(f"Handler stopped for SECC: {self.path}")

    async def handle_message(self, message):
        log_info(f"Received message from SECC {self.path}: {message}")
        # Placeholder: parse and dispatch message to session/gun
        # Extend with protocol handling in future milestones
