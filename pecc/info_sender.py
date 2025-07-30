"""
PECC Info Message Builder and Periodic Sender
Handles construction and periodic sending of info messages (status, event, chargingSession, etc.)
"""
import asyncio
from pecc.messages import PEPWSMessageProcessor

class InfoMessageSender:
    def __init__(self, websocket, session, gun_id, logger=None):
        self.websocket = websocket
        self.session = session
        self.gun_id = gun_id
        self.active = True
        self.logger = logger

    async def send_status(self, interval):
        while self.active:
            try:
                payload = {
                    "measuredVoltage": await self.session.get_voltage_demand() or 0,
                    "measuredCurrent": await self.session.get_current_demand() or 0,
                    "drivenVoltage": await self.session.get_voltage_demand() or 0,
                    "drivenCurrent": await self.session.get_current_demand() or 0,
                    "temperature": 35.0,
                    "contactorsStatus": "open",
                    "isolationStatus": "valid",
                    "operationalStatus": "operative"
                }
                 
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
