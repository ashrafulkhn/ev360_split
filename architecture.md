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
- Each SECC connection is handled in its own async task

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

## Error Handling
- All errors (protocol, hardware, CAN, etc.) are caught and reported
- Sessions are reset to standby on critical errors
- Error messages include errorCategory and errorDetails
- System logs all errors for diagnostics

---

## Summary
This architecture provides a robust, scalable, and protocol-compliant foundation for a PECC device managing multiple SECCs and multiple guns/vehicles per SECC, with real-time CAN integration, error handling, and flexible configuration.
