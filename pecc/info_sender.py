"""
PECC Info Message Builder and Periodic Sender
Handles construction and periodic sending of info messages (status, event, chargingSession, etc.)
"""
import asyncio
from pecc.messages import PEPWSMessageProcessor

class InfoMessageSender:
    def __init__(self, websocket, data_model, gun_id, logger=None):
        self.websocket = websocket
        self.data_model = data_model
        self.gun_id = gun_id
        self.active = True
        self.logger = logger

    def fetch_status_payload(self):
        # Fetch status fields from the data model, use defaults if missing
        keys = [
            "measuredVoltage", "measuredCurrent", "drivenVoltage", "drivenCurrent",
            "temperature", "contactorStatus", "isolationStatus", "operationalStatus"
        ]
        payload = {}
        for k in keys:
            getter = getattr(self.data_model, f"get_{k}", None)
            if getter:
                val = getter()
            else:
                val = None
            # Provide sensible defaults if needed
            if val is None:
                if k == "temperature":
                    val = 35.0
                elif k == "operationalStatus":
                    val = "operative"
                elif k == "isolationStatus":
                    val = "valid"
                elif k == "contactorStatus":
                    val = "closed"
                else:
                    val = 0
            payload[k] = val
        return payload

    async def send_status(self, interval):
        while self.active:
            try:
                payload = self.fetch_status_payload()
                msg = PEPWSMessageProcessor.build_info("status", payload)
                if self.logger:
                    self.logger.info(f"Sending periodic info to SECC /{self.gun_id}: {msg}")
                await self.websocket.send(msg)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error sending status info for /{self.gun_id}: {e}")
            await asyncio.sleep(interval)

    async def send_event(self, event_details, interval=5):
        while self.active:
            try:
                payload = {"eventDetails": event_details}
                msg = PEPWSMessageProcessor.build_info("event", payload)
                if self.logger:
                    self.logger.info(f"Sending periodic info to SECC /{self.gun_id}: {msg}")
                await self.websocket.send(msg)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error sending event info for /{self.gun_id}: {e}")
            await asyncio.sleep(interval)

    async def send_charging_session(self, session_payload, interval=1):
        while self.active:
            try:
                msg = PEPWSMessageProcessor.build_info("chargingSession", session_payload)
                if self.logger:
                    self.logger.info(f"Sending periodic info to SECC /{self.gun_id}: {msg}")
                await self.websocket.send(msg)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error sending chargingSession info for /{self.gun_id}: {e}")
            await asyncio.sleep(interval)

    def stop(self):
        self.active = False
