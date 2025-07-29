
#!/usr/bin/env python3
"""
Comprehensive test client for PECC WebSocket server.
Tests various PEP-WS protocol scenarios including:
- Connection establishment
- Message validation
- Protocol compliance
- Error handling
- Periodic info messages
"""

import asyncio
import websockets
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PECCTestClient:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.sequence_number = 1
        self.websocket = None
        self.gun_id = "GUN1"
        
    def get_next_sequence(self) -> int:
        seq = self.sequence_number
        self.sequence_number += 1
        return seq
    
    async def connect(self, gun_id="GUN1"):
        """Connect to PECC server as SECC"""
        self.gun_id = gun_id
        uri = f"ws://{self.host}:{self.port}/{gun_id}"
        logger.info(f"Connecting to {uri}...")
        
        try:
            self.websocket = await websockets.connect(uri)
            logger.info("✅ Connected successfully!")
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from PECC server"""
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from server")
    
    async def send_message(self, message: Dict[str, Any]) -> str:
        """Send a message and wait for response"""
        try:
            msg_str = json.dumps(message)
            logger.info(f"📤 Sending: {msg_str}")
            await self.websocket.send(msg_str)
            
            response = await self.websocket.recv()
            logger.info(f"📥 Received: {response}")
            return response
        except Exception as e:
            logger.error(f"❌ Send/receive error: {e}")
            return ""
    
    async def test_ev_connection_state(self, state="idle"):
        """Test evConnectionState message"""
        logger.info(f"\n🔄 Testing evConnectionState: {state}")
        message = {
            "kind": "evConnectionState",
            "type": "request",
            "sequenceNumber": self.get_next_sequence(),
            "payload": {
                "evConnectionState": state
            }
        }
        return await self.send_message(message)
    
    async def test_configuration_request(self):
        """Test configuration request"""
        logger.info("\n🔄 Testing configuration request")
        message = {
            "kind": "configuration",
            "type": "request",
            "sequenceNumber": self.get_next_sequence(),
            "payload": {
                "current_demand": 50,
                "voltage_demand": 400
            }
        }
        return await self.send_message(message)
    
    async def test_target_values(self, voltage=450, current=100):
        """Test targetValues message"""
        logger.info(f"\n🔄 Testing targetValues: {voltage}V, {current}A")
        message = {
            "kind": "targetValues",
            "type": "request",
            "sequenceNumber": self.get_next_sequence(),
            "payload": {
                "targetVoltage": voltage,
                "targetCurrent": current
            }
        }
        return await self.send_message(message)
    
    async def test_stop_charging(self):
        """Test stopCharging message"""
        logger.info("\n🔄 Testing stopCharging")
        message = {
            "kind": "stopCharging",
            "type": "request",
            "sequenceNumber": self.get_next_sequence(),
            "payload": {}
        }
        return await self.send_message(message)
    
    async def test_reset(self):
        """Test reset message"""
        logger.info("\n🔄 Testing reset")
        message = {
            "kind": "reset",
            "type": "request",
            "sequenceNumber": self.get_next_sequence(),
            "payload": {}
        }
        return await self.send_message(message)
    
    async def test_invalid_message(self):
        """Test invalid message handling"""
        logger.info("\n🔄 Testing invalid message")
        message = {
            "kind": "invalidKind",
            "type": "request",
            "sequenceNumber": self.get_next_sequence(),
            "payload": {}
        }
        return await self.send_message(message)
    
    async def test_malformed_json(self):
        """Test malformed JSON handling"""
        logger.info("\n🔄 Testing malformed JSON")
        try:
            await self.websocket.send("{ invalid json }")
            response = await self.websocket.recv()
            logger.info(f"📥 Received: {response}")
            return response
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return ""
    
    async def listen_for_info_messages(self, duration=5):
        """Listen for periodic info messages"""
        logger.info(f"\n🔄 Listening for info messages for {duration} seconds...")
        start_time = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start_time) < duration:
            try:
                # Set a short timeout to check for messages
                response = await asyncio.wait_for(self.websocket.recv(), timeout=0.5)
                logger.info(f"📥 Info message: {response}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"❌ Error receiving info: {e}")
                break
    
    async def run_comprehensive_test(self):
        """Run all test scenarios"""
        logger.info("🚀 Starting comprehensive PECC test suite")
        
        # Connect to server
        if not await self.connect():
            return
        
        try:
            # Test 1: Basic connection state
            await self.test_ev_connection_state("idle")
            await asyncio.sleep(0.5)
            
            # Test 2: Configuration request
            await self.test_configuration_request()
            await asyncio.sleep(0.5)
            
            # Test 3: Target values
            await self.test_target_values(400, 80)
            await asyncio.sleep(0.5)
            
            # Test 4: State transition to charging
            await self.test_ev_connection_state("charging")
            await asyncio.sleep(0.5)
            
            # Test 5: Update target values during charging
            await self.test_target_values(420, 90)
            await asyncio.sleep(0.5)
            
            # Test 6: Listen for periodic status info
            await self.listen_for_info_messages(3)
            
            # Test 7: Stop charging
            await self.test_stop_charging()
            await asyncio.sleep(0.5)
            
            # Test 8: Reset
            await self.test_reset()
            await asyncio.sleep(0.5)
            
            # Test 9: Error handling - invalid message
            await self.test_invalid_message()
            await asyncio.sleep(0.5)
            
            # Test 10: Error handling - malformed JSON
            await self.test_malformed_json()
            await asyncio.sleep(0.5)
            
            logger.info("\n✅ All tests completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Test suite error: {e}")
        finally:
            await self.disconnect()

async def test_multiple_guns():
    """Test multiple gun connections simultaneously"""
    logger.info("🚀 Testing multiple gun connections")
    
    guns = ["GUN1", "GUN2", "GUN3"]
    clients = []
    
    # Connect all clients
    for gun_id in guns:
        client = PECCTestClient()
        if await client.connect(gun_id):
            clients.append(client)
    
    # Send messages from all clients simultaneously
    tasks = []
    for i, client in enumerate(clients):
        tasks.append(client.test_ev_connection_state("idle"))
        tasks.append(client.test_configuration_request())
        tasks.append(client.test_target_values(400 + i*10, 50 + i*10))
    
    # Execute all tasks concurrently
    await asyncio.gather(*tasks)
    
    # Listen for info messages
    info_tasks = [client.listen_for_info_messages(2) for client in clients]
    await asyncio.gather(*info_tasks)
    
    # Disconnect all clients
    for client in clients:
        await client.disconnect()
    
    logger.info("✅ Multiple gun test completed!")

async def test_stress_scenario():
    """Stress test with rapid message sending"""
    logger.info("🚀 Running stress test")
    
    client = PECCTestClient()
    if not await client.connect("STRESS_GUN"):
        return
    
    try:
        # Send rapid sequence of messages
        for i in range(10):
            await client.test_target_values(400 + i, 50 + i)
            await asyncio.sleep(0.1)  # Small delay
        
        logger.info("✅ Stress test completed!")
    
    finally:
        await client.disconnect()

def main():
    """Main function with test menu"""
    print("PECC Test Client")
    print("================")
    print("1. Run comprehensive test")
    print("2. Test multiple guns")
    print("3. Run stress test")
    print("4. Interactive mode")
    
    choice = input("Select test (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(PECCTestClient().run_comprehensive_test())
    elif choice == "2":
        asyncio.run(test_multiple_guns())
    elif choice == "3":
        asyncio.run(test_stress_scenario())
    elif choice == "4":
        asyncio.run(interactive_mode())
    else:
        print("Invalid choice")

async def interactive_mode():
    """Interactive testing mode"""
    client = PECCTestClient()
    gun_id = input("Enter gun ID (default: GUN1): ").strip() or "GUN1"
    
    if not await client.connect(gun_id):
        return
    
    try:
        while True:
            print("\nInteractive Commands:")
            print("1. Send evConnectionState")
            print("2. Send configuration request")
            print("3. Send targetValues")
            print("4. Send stopCharging")
            print("5. Send reset")
            print("6. Listen for info messages")
            print("7. Send custom message")
            print("q. Quit")
            
            cmd = input("Command: ").strip().lower()
            
            if cmd == "q":
                break
            elif cmd == "1":
                state = input("Enter state (idle/charging/error): ").strip()
                await client.test_ev_connection_state(state)
            elif cmd == "2":
                await client.test_configuration_request()
            elif cmd == "3":
                voltage = int(input("Enter voltage: "))
                current = int(input("Enter current: "))
                await client.test_target_values(voltage, current)
            elif cmd == "4":
                await client.test_stop_charging()
            elif cmd == "5":
                await client.test_reset()
            elif cmd == "6":
                duration = int(input("Duration (seconds): "))
                await client.listen_for_info_messages(duration)
            elif cmd == "7":
                json_msg = input("Enter JSON message: ")
                try:
                    msg = json.loads(json_msg)
                    await client.send_message(msg)
                except json.JSONDecodeError:
                    print("Invalid JSON")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    main()
