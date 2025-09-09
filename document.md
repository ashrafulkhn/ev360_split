# EV360 Split Project Documentation

## Project Overview
This project implements a modular, scalable Power Electronics Communication Controller (PECC) server for multi-SECC/multi-gun EV charging, compliant with the PEP-WS protocol. It supports dynamic configuration, robust logging, real-time diagnostics, and full protocol coverage for all message types and kinds.

---

## Architecture & Main Components
- **PECCServer**: Asynchronous WebSocket server handling multiple SECC connections.
- **SECCConnectionHandler**: Manages protocol logic, session state, and message handling for each SECC connection.
- **GunSession**: Per-gun/session state management and protocol compliance.
- **InfoMessageSender**: Periodically sends status/info messages to SECC clients.
- **DispenserDataModel**: Thread-safe, dynamic data model for all gun/session parameters, supporting JSON initialization.
- **Logging & Diagnostics**: Centralized logging with millisecond timestamps, real-time log streaming to `/splitdash` clients.

---

## Protocol Coverage
All PEP-WS protocol message types and kinds are implemented:

### Message Types & Kinds
- **request**
  - configuration
  - cableCheck
  - targetValues
  - contactorsStatus
  - reset
  - getInput
  - setOutput
  - stopCharging
- **response**
  - configuration
  - cableCheck
  - targetValues
  - contactorsStatus
  - reset
  - getInput
  - setOutput
  - stopCharging
- **info**
  - event
  - status
  - evConnectionState
  - chargingSession
- **error**
  - All error categories and details

---

## API Calls & Endpoints
### WebSocket Endpoints
- `/GUNx` (e.g., `/GUN5`): SECC connects for protocol communication; all protocol messages handled per gun/session.
- `/splitdash`: Client connects to receive real-time logs and diagnostics.

### Main API/Method Calls
- `PECCServer.start()`: Starts the WebSocket server.
- `PECCServer.handler(connection, path)`: Handles incoming SECC or splitdash connections.
- `SECCConnectionHandler.run()`: Main protocol loop for each SECC connection.
- `SECCConnectionHandler.start_info_sender()`: Starts periodic info/status sender.
- `SECCConnectionHandler.stop_info_sender()`: Stops periodic info sender.
- `GunSession` methods: State transitions, demand setters/getters.
- `InfoMessageSender.send_status()`: Periodically sends status info.
- `DispenserDataModel.from_json_file(path)`: Loads dynamic data model from JSON.
- `DispenserDataModel.get_<param>()` / `set_<param>(value)`: Dynamic getter/setter for all parameters.
- `log_info(msg)` / `log_error(msg)`: Centralized logging, streamed to `/splitdash` if connected.

---

## Stages & Milestones
1. **Project Setup**: Modular codebase, config management, async server.
2. **Connection Handling**: Multi-SECC support, per-gun session management.
3. **Protocol Implementation**: Full request/response/info/error handling, protocol compliance.
4. **State Machine**: Gun/session state transitions, demand management.
5. **Periodic Info Sender**: Modular, protocol-compliant status/event/chargingSession info messages.
6. **Dynamic Data Model**: Thread-safe, JSON-initialized data model for all gun/session parameters.
7. **Diagnostics & Logging**: Centralized logging, real-time log streaming to `/splitdash`.

---

## Usage Example
- Start the server: `python pecc/server.py`
- SECC connects to `/GUNx` for protocol communication.
- Monitoring client connects to `/splitdash` for real-time logs.
- Data model can be initialized from JSON and used dynamically for all guns.

---

## Next Steps
- Extend diagnostics and monitoring features.
- Add admin/config API for runtime updates.
- Expand automated tests and simulation tools.
- Support vendor-specific protocol extensions if needed.

---

## Contributors
- Project owner: ashrafulkhn
- AI assistant: GitHub Copilot

---

For further details, see code comments and module docstrings.
