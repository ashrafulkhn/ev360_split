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
        self.info_task = asyncio.create_task(self.info_sender.send_status(.25))     # Time interval for sending info message.

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
                msg_type = msg.get("type")
                kind = msg.get("kind")
                payload = msg.get("payload", {})
                seq = msg.get("sequenceNumber")
                response_payload = {}
                # Handle all protocol types and kinds
                if msg_type == "info":
                    # Log info kinds
                    if kind in ["event", "status", "evConnectionState", "chargingSession"]:
                        log_info(f"Received info message from SECC {self.path}: kind={kind}, payload={payload}")
                    else:
                        log_info(f"Received unknown info kind from SECC {self.path}: kind={kind}, payload={payload}")
                    continue  # Do not reply
                if msg_type == "error":
                    log_info(f"Received error message from SECC {self.path}: kind={kind}, payload={payload}")
                    continue  # Do not reply
                if msg_type != "request":
                    log_info(f"Ignoring message of type {msg_type} from SECC {self.path}")
                    continue
                # --- Full protocol logic for requests ---
                if kind == "configuration":
                    current = payload.get("current_demand")
                    voltage = payload.get("voltage_demand")
                    if current is not None:
                        await self.session.set_current_demand(current)
                    if voltage is not None:
                        await self.session.set_voltage_demand(voltage)
                    from config.gun_configs import gun_configs
                    config = gun_configs.get(self.gun_id, gun_configs.get("GUN1"))
                    response_payload = config
                elif kind == "cableCheck":
                    voltage = payload.get("voltage")
                    # Implement cable check logic here
                    response_payload = {"cableCheckResult": "valid", "voltage": voltage}
                elif kind == "targetValues":
                    target_current = payload.get("targetCurrent")
                    target_voltage = payload.get("targetVoltage")
                    soc = payload.get("batteryStateOfCharge")
                    charging_state = payload.get("chargingState")
                    if target_current is not None:
                        await self.session.set_current_demand(target_current)
                    if target_voltage is not None:
                        await self.session.set_voltage_demand(target_voltage)
                    response_payload = {
                        "current_demand": await self.session.get_current_demand(),
                        "voltage_demand": await self.session.get_voltage_demand(),
                        "batteryStateOfCharge": soc,
                        "chargingState": charging_state
                    }
                elif kind == "contactorsStatus":
                    status = payload.get("contactorsStatus")
                    # Implement contactors status logic here
                    response_payload = {"contactorsStatus": status}
                elif kind == "reset":
                    await self.session.transition_state(GunState.IDLE)
                    response_payload = {"state": str(await self.session.get_state())}
                elif kind == "getInput":
                    input_ids = payload.get("inputIdentifiers", [])
                    # Implement getInput logic here
                    response_payload = {"inputValues": {id_: 0 for id_ in input_ids}}
                elif kind == "setOutput":
                    output_values = payload.get("outputValues", {})
                    # Implement setOutput logic here
                    response_payload = {"outputStatus": "ok"}
                elif kind == "stopCharging":
                    await self.session.transition_state(GunState.STOPPED)
                    response_payload = {"state": str(await self.session.get_state())}
                else:
                    log_error(f"Unknown request kind from SECC {self.path}: {kind}")
                    error_resp = PEPWSMessageProcessor.build_response(msg, error=f"Unknown kind: {kind}")
                    log_info(f"Sending error response to SECC {self.path}: {error_resp}")
                    await self.websocket.send(error_resp)
                    continue
                # Send response for request
                resp = PEPWSMessageProcessor.build_response(msg, payload=response_payload)
                log_info(f"Sending response to SECC {self.path}: {resp}")
                await self.websocket.send(resp)
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
