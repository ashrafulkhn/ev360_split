"""
SECC Connection Handler for PECC system.
Manages communication and sessions for each SECC connection.
Modular and scalable for multiple SECCs.
"""

import asyncio
from pecc.utils import log_info, log_error
from pecc.gun_session import GunSession, GunState

class SECCConnectionHandler:
    def start_info_sender(self):
        from pecc.info_sender import InfoMessageSender
        self.info_sender = InfoMessageSender(self.websocket, self.session, self.gun_id)
        self.info_task = asyncio.create_task(self.info_sender.send_status(0.2))

    def stop_info_sender(self):
        if hasattr(self, 'info_sender'):
            self.info_sender.stop()
        if hasattr(self, 'info_task'):
            self.info_task.cancel()
    def __init__(self, websocket, path):
        self.websocket = websocket
        self.path = path
        self.active = True
        # Extract gun id from path, e.g., '/GUN5' -> 'GUN5'
        self.gun_id = path.lstrip('/') if path else None
        self.session = GunSession(self.gun_id)

    async def run(self):
        log_info(f"Handler started for SECC: {self.path}")
        self.start_info_sender()
        try:
            from pecc.messages import PEPWSMessageProcessor
            async for message in self.websocket:
                log_info(f"Received message from SECC {self.path}: {message}")
                msg, err = PEPWSMessageProcessor.parse_message(message)
                if err:
                    log_error(f"Message parse error from SECC {self.path}: {err}")
                    error_resp = PEPWSMessageProcessor.build_response({}, error=err)
                    log_info(f"Sending error response to SECC {self.path}: {error_resp}")
                    await self.websocket.send(error_resp)
                    continue
                valid, err = PEPWSMessageProcessor.validate_message(msg)
                if not valid:
                    log_error(f"Message validation error from SECC {self.path}: {err}")
                    error_resp = PEPWSMessageProcessor.build_response(msg, error=err)
                    log_info(f"Sending error response to SECC {self.path}: {error_resp}")
                    await self.websocket.send(error_resp)
                    continue
                kind = msg.get("kind")
                payload = msg.get("payload", {})
                seq = msg.get("sequenceNumber")
                response_payload = {}
                # --- Full protocol logic ---
                if kind == "evConnectionState":
                    status = payload.get("evConnectionState")
                    await self.session.set_status(status)
                    if status == "error":
                        await self.session.transition_state(GunState.ERROR)
                    elif status == "charging":
                        await self.session.transition_state(GunState.CHARGING)
                    elif status == "idle":
                        await self.session.transition_state(GunState.IDLE)
                    response_payload = {"state": str(await self.session.get_state())}
                    resp = PEPWSMessageProcessor.build_response(msg, payload=response_payload)
                    log_info(f"Sending response to SECC {self.path}: {resp}")
                    await self.websocket.send(resp)
                elif kind == "configuration":
                    current = payload.get("current_demand")
                    voltage = payload.get("voltage_demand")
                    if current is not None:
                        await self.session.set_current_demand(current)
                    if voltage is not None:
                        await self.session.set_voltage_demand(voltage)
                    from config.gun_configs import gun_configs
                    config = gun_configs.get(self.gun_id, gun_configs.get("GUN1"))
                    response_payload = config
                    resp = PEPWSMessageProcessor.build_response(msg, payload=response_payload)
                    log_info(f"Sending response to SECC {self.path}: {resp}")
                    await self.websocket.send(resp)
                elif kind == "targetValues":
                    target_current = payload.get("targetCurrent")
                    target_voltage = payload.get("targetVoltage")
                    if target_current is not None:
                        await self.session.set_current_demand(target_current)
                    if target_voltage is not None:
                        await self.session.set_voltage_demand(target_voltage)
                    response_payload = {
                        "current_demand": await self.session.get_current_demand(),
                        "voltage_demand": await self.session.get_voltage_demand(),
                    }
                    resp = PEPWSMessageProcessor.build_response(msg, payload=response_payload)
                    log_info(f"Sending response to SECC {self.path}: {resp}")
                    await self.websocket.send(resp)
                elif kind == "stopCharging":
                    await self.session.transition_state(GunState.STOPPED)
                    response_payload = {"state": str(await self.session.get_state())}
                    resp = PEPWSMessageProcessor.build_response(msg, payload=response_payload)
                    log_info(f"Sending response to SECC {self.path}: {resp}")
                    await self.websocket.send(resp)
                elif kind == "reset":
                    await self.session.transition_state(GunState.IDLE)
                    response_payload = {"state": str(await self.session.get_state())}
                    resp = PEPWSMessageProcessor.build_response(msg, payload=response_payload)
                    log_info(f"Sending response to SECC {self.path}: {resp}")
                    await self.websocket.send(resp)
                elif kind == "info":
                    # Handle info messages from SECC
                    log_info(f"Received info message from SECC {self.path}: {payload}")
                    # Optionally update session or take action based on info
                else:
                    log_error(f"Unknown message kind from SECC {self.path}: {kind}")
                    error_resp = PEPWSMessageProcessor.build_response(msg, error=f"Unknown kind: {kind}")
                    log_info(f"Sending error response to SECC {self.path}: {error_resp}")
                    await self.websocket.send(error_resp)
        except Exception as e:
            log_error(f"SECC handler error: {e}")
        finally:
            self.active = False
            self.stop_info_sender()
            log_info(f"Handler stopped for SECC: {self.path}")

    async def handle_message(self, message):
        log_info(f"Received message from SECC {self.path}: {message}")
        # Placeholder: parse and dispatch message to session/gun
        # Extend with protocol handling in future milestones
