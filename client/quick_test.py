
#!/usr/bin/env python3
"""
Quick test client for basic PECC server verification.
"""

import asyncio
import websockets
import json

async def quick_test():
    """Quick test to verify PECC server is working"""
    uri = "ws://localhost:8765/GUN1"
    print(f"🔗 Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected!")
            
            # Test 1: Send evConnectionState
            message = {
                "kind": "evConnectionState",
                "type": "request", 
                "sequenceNumber": 1,
                "payload": {"evConnectionState": "idle"}
            }
            
            print("📤 Sending evConnectionState message...")
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print(f"📥 Response: {response}")
            
            # Test 2: Send configuration request
            config_msg = {
                "kind": "configuration",
                "type": "request",
                "sequenceNumber": 2,
                "payload": {"current_demand": 50, "voltage_demand": 400}
            }
            
            print("📤 Sending configuration request...")
            await websocket.send(json.dumps(config_msg))
            response = await websocket.recv()
            print(f"📥 Response: {response}")
            
            # Test 3: Listen for status info
            print("📡 Listening for status info (3 seconds)...")
            for i in range(6):
                try:
                    info = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    print(f"📥 Info: {info}")
                except asyncio.TimeoutError:
                    continue
            
            print("✅ Quick test completed!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())
