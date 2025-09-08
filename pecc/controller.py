# import asyncio
# from pecc.websocket_client import WebSocketClient
# import pecc.messages as messages

# class PECCController:
#     def __init__(self, ws_uri):
#         self.client = WebSocketClient(ws_uri)

#     async def start(self):
#         await self.client.connect()
#         # Example: Request configuration
#         seq = self.client.next_sequence()
#         config_msg = messages.build_configuration_request(seq)
#         await self.client.send(config_msg)
#         response = await self.client.receive()
#         print("Received configuration response:", response)
#         # Add more process logic here

#     async def stop(self):
#         await self.client.close()

# # Example usage
# if __name__ == "__main__":
#     async def main():
#         controller = PECCController("ws://localhost:8765")
#         await controller.start()
#         await controller.stop()
#     asyncio.run(main())
