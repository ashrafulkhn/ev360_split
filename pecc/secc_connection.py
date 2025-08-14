"""
SECC Connection Handler for PECC system.
Manages communication and sessions for each SECC connection.
Modular and scalable for multiple SECCs.
"""

import asyncio
from pecc.utils import log_info, log_error
from pecc.gun_session import GunSession, GunState
from pecc.data_model.dispenser_data_model import DispenserDataModel

class SECCConnectionHandler:
    def start_info_sender(self):
        from pecc.info_sender import InfoMessageSender
        self.info_sender = InfoMessageSender(self.websocket, self.data_model, self.gun_id)
        self.info_task = asyncio.create_task(self.info_sender.send_status(.25))     # Time interval for sending info message.

    def stop_info_sender(self):
        if hasattr(self, 'info_sender'):
            self.info_sender.stop()
        if hasattr(self, 'info_task'):
            self.info_task.cancel()
    def __init__(self, websocket, path):
        self.websocket = websocket
        # Ensure path is never None; assign a default if missing
        # self.path = path if path else "/UNKNOWN"
        self.path = path
        self.active = True
        # Extract gun id from path, e.g., '/GUN5' -> 'GUN5'
        self.gun_id = path.lstrip('/') if path else None
        log_info(f"Connected to Gun path : {self.gun_id}")
        self.session = GunSession(self.gun_id)
        # Create a unique data model for this gun/session
        from os.path import dirname, abspath, join
        base_dir = dirname(abspath(__file__))
        json_path = join(base_dir, "data_model", "datamodel_dispenser.json")
        self.data_model = DispenserDataModel.from_json_file(json_path)

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
                    # Log info kinds and store latest data in datamodel
                    if kind in ["evConnectionState", "chargingSession", "event"]:
                        log_info(f"Received info message from SECC {self.path}: kind={kind}, payload={payload}")
                        # Store all payload fields in datamodel with kind prefix
                        for k, v in payload.items():
                            self.data_model.set(f"{kind}.{k}", v)
                    elif kind == "status":
                        log_info(f"Received info message from SECC {self.path}: kind=status, payload={payload}")
                        # Optionally store status fields if needed
                    else:
                        log_error(f"Received unknown info kind from SECC {self.path}: kind={kind}, payload={payload}")
                        # Optionally store unknown info kind for diagnostics
                        self.data_model.set(f"unknown_info_kind.{kind}", payload)
                    continue  # Do not reply
                if msg_type == "error":
                    log_info(f"Received error message from SECC {self.path}: kind={kind}, payload={payload}")
                    continue  # Do not reply
                if msg_type != "request":
                    log_info(f"Ignoring message of type {msg_type} from SECC {self.path}")
                    continue
                # --- Full protocol logic for requests ---
                if kind == "configuration":
                    # Update data model with received values
                    for k in ["current_demand", "voltage_demand"]:
                        v = payload.get(k)
                        if v is not None:
                            self.data_model.set(k, v)
                    # Respond with all config from data model
                    response_payload = {key: self.data_model.get(key) for key in self.data_model.get_all().keys() if key.startswith("type.response.kind.configuration.payload.")}
                elif kind == "cableCheck":
                    voltage = payload.get("voltage")
                    self.data_model.set("voltage", voltage)
                    response_payload = {"cableCheckResult": "valid", "voltage": voltage}
                elif kind == "targetValues":
                    for k in ["targetCurrent", "targetVoltage", "batteryStateOfCharge", "chargingState"]:
                        v = payload.get(k)
                        if v is not None:
                            self.data_model.set(k, v)
                    response_payload = {k: self.data_model.get(k) for k in ["targetCurrent", "targetVoltage", "batteryStateOfCharge", "chargingState"]}
                elif kind == "contactorsStatus":
                    status = payload.get("contactorsStatus")
                    self.data_model.set("contactorStatus", status)
                    response_payload = {"contactorStatus": status}
                elif kind == "reset":
                    await self.session.transition_state(GunState.IDLE)
                    self.data_model.set("operationalStatus", "operative")
                    response_payload = {"state": str(await self.session.get_state())}
                elif kind == "getInput":
                    input_ids = payload.get("inputIdentifiers", [])
                    # Simulate input values, update data model
                    input_values = {id_: 0 for id_ in input_ids}
                    self.data_model.set("inputValues", input_values)
                    response_payload = {"inputValues": input_values}
                elif kind == "setOutput":
                    output_values = payload.get("outputValues", {})
                    self.data_model.set("outputValues", output_values)
                    response_payload = {"outputStatus": "ok"}
                elif kind == "stopCharging":
                    await self.session.transition_state(GunState.STOPPED)
                    self.data_model.set("operationalStatus", "inoperative")
                    response_payload = {"state": str(await self.session.get_state())}
                else:
                    log_error(f"Unknown request kind from SECC {self.path}: {kind}")
                    # Store unknown request kind for diagnostics
                    self.data_model.set(f"unknown_request_kind.{kind}", payload)
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
