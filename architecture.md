# PECC System Architecture for Multi-SECC, Multi-Gun Charging

## Overview
This architecture enables a Power Electronics Communication Controller (PECC) to manage multiple Supply Equipment Communication Controllers (SECCs), each of which can control multiple charging guns/vehicles. The system is designed to:
- Handle up to 6 SECCs, each with up to 12 guns/vehicles
- Implement the PEP-WS protocol for all message types
- Integrate with power modules via CAN bus
- Provide robust error handling, state management, and real-time data reporting

---

## High-Level Components

### 1. WebSocket Server Layer
- Accepts and manages multiple SECC connections (async, scalable)

### 2. SECC Connection Handler
- For each SECC, manages all communication and sessions for its guns/vehicles
- Maintains a mapping of gun/session IDs to session objects
- Handles message parsing, validation, and dispatch

### 3. Gun/Vehicle Session Manager
- Each gun/vehicle is a session with its own state machine (idle, charging, error, etc.)
- Manages charging process, power limits, and error state per gun
- Handles start/stop charging, cable check, and state transitions

### 4. CAN Interface
- Reads real-time data (voltage, current, temperature, etc.) from power modules
- Maps CAN data to the correct gun/session
- Handles CAN errors and retries

### 5. Message Processor
- Implements all PEP-WS protocol messages (request, response, error, info)
- Handles sequence numbers, message validation, and JSON schema compliance
- Sends periodic info/status messages as required

### 6. Power Limit Manager
- Maintains and enforces power/current/voltage limits per gun/session
- Provides configuration and update interface for limits
- Responds to SECC requests for power limits

### 7. Error Handling & Recovery
- Detects protocol, hardware, and communication errors
- Sends error messages with appropriate errorCategory and errorDetails
- Recovers sessions to standby state as per protocol
- Logs and reports errors for diagnostics

### 8. Configuration & Utilities
- Loads and manages system configuration (limits, intervals, etc.)
- Provides logging, monitoring, and diagnostics

---

## Directory Structure Example

```
pecc/
  ├── server.py                # WebSocket server entry point
  ├── secc_connection.py       # Handles each SECC connection
  ├── gun_session.py           # Manages each gun/vehicle session and state machine
  ├── messages.py              # PEP-WS message builders/parsers
  ├── can_interface.py         # CAN bus integration for power module data
  ├── power_limits.py          # Power limit management
  ├── error_handling.py        # Error detection and reporting
  ├── utils.py                 # Common utilities
  └── config.py                # Configuration (limits, intervals, etc.)
```

---

## Data Flow Example
1. **SECC connects** to PECC server (WebSocket)
2. **SECC sends request** (e.g., configuration, cableCheck, targetValues)
3. **Connection handler** parses and validates message, dispatches to correct gun/session
4. **Session manager** updates state, triggers CAN read if needed
5. **CAN interface** reads power module data, updates session
6. **Session manager** sends info/status messages to SECC, responds to requests
7. **Power limit manager** enforces and reports limits
8. **Error handler** manages and reports any errors

---

## Key Implementation Points
- Use asyncio for concurrency (multiple SECCs, multiple guns per SECC)
- Each gun/session is independent and can be started/stopped/errored separately
- CAN reads are non-blocking and mapped to correct session
- All protocol messages are validated and sequence numbers tracked
- Errors are handled and reported as per protocol
- Power limits are enforced and can be updated/configured
- Status/info messages are sent periodically as required

---

## Extensibility
- Add support for more SECCs/guns by scaling session management
- Extend CAN interface for new hardware
- Update message processor for protocol changes
- Add monitoring, logging, and diagnostics as needed

---

## Example Sequence: Start Charging a Vehicle
1. SECC connects and requests configuration
2. SECC requests cableCheck for a gun
3. SECC sends contactorsStatus (closed) for a gun
4. SECC sends targetValues (preCharge, then charge) for a gun
5. PECC reads power data from CAN, sends status/info to SECC
6. SECC sends stopCharging or reset to end session
7. Errors at any step are reported and handled per protocol

---

## Comprehensive Flow Chart: Multi-SECC, Multi-Gun Charging System

```plaintext
Start
  |
  v
[PECC WebSocket Server Starts]
  |
  v
[Wait for SECC Connections]
  |
  v
[SECC Connects] <--- Multiple SECCs (up to 6)
  |
  v
[Create SECC Connection Handler]
  |
  v
[For Each Gun/Vehicle (up to 12 per SECC)]
  |
  v
[Create Gun Session State Machine]
  |
  v
[Main Loop: Handle Requests]
  |
  +--> [Receive Message from SECC]
  |      |
  |      v
  |  [Parse & Validate Message]
  |      |
  |      v
  |  [Dispatch to Gun Session]
  |      |
  |      v
  |  [Process Message]
  |      |
  |      +--> [If configuration/cableCheck]
  |      |      |
  |      |      v
  |      |  [Respond with config/cableCheck result]
  |      |
  |      +--> [If contactorsStatus]
  |      |      |
  |      |      v
  |      |  [Open/Close Contactors]
  |      |
  |      +--> [If targetValues]
  |      |      |
  |      |      v
  |      |  [Update Charging State]
  |      |      |
  |      |      v
  |      |  [Trigger CAN Read]
  |      |      |
  |      |      v
  |      |  [Send Info/Status to SECC]
  |      |
  |      +--> [If getInput/setOutput]
  |      |      |
  |      |      v
  |      |  [Read/Set Hardware I/O]
  |      |
  |      +--> [If stopCharging/reset]
  |      |      |
  |      |      v
  |      |  [Reset Session State]
  |      |
  |      +--> [If Error]
  |             |
  |             v
  |         [Send Error Message]
  |             |
  |             v
  |         [Reset Session to Standby]
  |
  v
[Periodic Tasks]
  |
  +--> [Read CAN Data]
  |      |
  |      v
  |  [Update Gun Sessions]
  |
  +--> [Send Status/Info to SECC]
  |
  +--> [Monitor Power Limits]
  |
  +--> [Log & Monitor Errors]
  |
  v
[End]
```

```plaintext
+-------------------+         +-------------------+         +-------------------+
|                   |         |                   |         |                   |
|   SECC #1         |  ...    |   SECC #N         |         |   SECC #6         |
| (WebSocket Client)|         | (WebSocket Client)|         | (WebSocket Client)|
+--------+----------+         +--------+----------+         +--------+----------+
         |                             |                             |
         |                             |                             |
         +-----------------------------+-----------------------------+
                                       |
                                       v
                          +-------------------------------+
                          |        PECC WebSocket         |
                          |         Server Layer          |
                          +-------------------------------+
                                       |
                                       v
                +---------------------------------------------------+
                |                 SECC Connection Handler           |
                |  (One per SECC, manages all guns/sessions)        |
                +---------------------------------------------------+
                  |         |         |         |         |         |
                  v         v         v         v         v         v
           +---------+ +---------+ ... +---------+ ... +---------+ +---------+
           | Gun #1  | | Gun #2  |     | Gun #n  |     | Gun #12 | | Gun #n  |
           | Session | | Session |     | Session |     | Session | | Session |
           +---------+ +---------+     +---------+     +---------+ +---------+
                  |         |         ...       |         |         |
                  +---------+---------+---------+---------+---------+
                                       |
                                       v
                          +-------------------------------+
                          |         CAN Interface         |
                          | (Reads power module data)     |
                          +-------------------------------+
                                       |
                                       v
                          +-------------------------------+
                          |      Power Modules (HW)       |
                          +-------------------------------+

Other cross-cutting modules (not shown for clarity):
- Power Limit Manager
- Error Handling & Recovery
- Configuration & Utilities
```

---

## Development Plan

1. **Project Setup**
   - Create the directory structure as described above.
   - Set up a Python environment and install required packages (e.g., websockets, can).

2. **WebSocket Server Implementation**
   - Implement the server to accept multiple SECC connections asynchronously.
   - For each connection, spawn a handler.

3. **Session Management**
   - Design and implement the gun/vehicle session state machine.
   - Map SECC requests to the correct session.

4. **PEP-WS Protocol Handling**
   - Implement message parsing, validation, and response logic for all protocol messages.
   - Track sequence numbers and ensure compliance.

5. **CAN Integration**
   - Implement CAN interface to read power module data.
   - Map CAN data to gun sessions and handle errors.

6. **Power Limit Management**
   - Implement logic to enforce and update power limits per gun/session.
   - Provide configuration interface for limits.

7. **Error Handling & Logging**
   - Implement error detection, reporting, and recovery.
   - Add logging and monitoring for diagnostics.

8. **Periodic Tasks**
   - Implement periodic status/info reporting to SECC.
   - Monitor and enforce power limits.

9. **Testing & Validation**
   - Write unit and integration tests for all modules.
   - Validate protocol compliance and error handling.

10. **Documentation & Extensibility**
    - Document all modules and flows.
    - Plan for future hardware/protocol updates.

---

## Summary
This architecture provides a robust, scalable, and protocol-compliant foundation for a PECC device managing multiple SECCs and multiple guns/vehicles per SECC, with real-time CAN integration, error handling, and flexible configuration.


## Error Handling
- All errors (protocol, hardware, CAN, etc.) are caught and reported
