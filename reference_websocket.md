Status Released
Publisher Vector Informatik GmbH
© 2022 All rights reserved.
Any distribution or copying is subject to prior written approval by Vector.
Note: Hardcopy documents are not subject to change management.

# Power Electronics Protocol over WebSocket

## PEP-WS
Networking and Application Protocol Requirements
Version 1.8 of 2022-10-01

## Change History
| Date       | Name   | Changes                                                                 |
|------------|--------|-------------------------------------------------------------------------|
| 2019-10-08 | vishnt | First Draft: alpha state                                                |
| 2019-11-13 | vishnt | Major changes in chapters Timing and Error Handling. Added chapter IMD  |
| 2020-01-31 | vistrf | Major change of chapters Message Frames, Timings, Error Handling.       |
|            |        | Removed chapters IMD and Charging Illustration. Added JSON schemas.     |
|            |        | Adapted Charging Sequence diagram and PECC state machine proposal       |
| 2020-03-30 | vistio | Keys and values are now case-sensitive and written in camelCase.        |
|            |        | Syntactical errors have been removed from json schemas.                 |
|            |        | Request targetValues now includes the battery’s state of charge         |
|            |        | as field batteryStateOfCharge                                           |
| 2020-04-17 | visjnk | First chapter removed                                                   |
| 2020-08-26 | mkiefer| Added getInput and setOutput request messages                           |
|            |        | Added evConnectionState message                                         |
| 2020-11-27 | mkiefer| Clarified use of PECC operationalStatus==INOPERATIVE                    |
| 2021-02-15 | mkiefer| Added voltage to cableCheck request                                     |
|            |        | Added vehicleId to evConnectionState                                    |
|            |        | Clarified use of websocket PING mechanism                               |
| 2021-03-05 | visert | Clarified difference between driven and measured values                 |
| 2021-04-10 | mkiefer| Added floatValues to configuration response                             |
| 2021-05-25 | mkiefer| Clarified request-configuration update intervals                        |
| 2021-08-15 | mkiefer| Added stopCharging message                                              |
| 2022-01-25 | mkiefer| Added chargingSession message                                           |
| 2022-02-15 | mkiefer| Added PP supervision explanation                                        |
| 2022-04-15 | mkiefer| Removed isolationStatus noImd                                           |
| 2022-05-25 | mkiefer| Extended chargingSession message                                        |
| 2022-10-01 | mkiefer| BPT Extensions (response-configuration, info-chargingSession)           |

---

## Contents
1. Introduction
2. Communication Model
3. Message Frames
4. Timing Recommendations
5. Error Handling
6. Example Scenarios
7. PECC State Machine Proposal
8. Appendix

---

### 1. Introduction
#### 1.1 Scope
This document specifies the communication protocol between the Power Electronics Communication Controller (PECC) and the Supply Equipment Communication Controller (SECC). This Power Electronics Protocol (PEP) is designed to control and monitor the energy transfer of a power electronics used in the context of Electric Vehicle (EV) charging. Its design is based on the requirements of the ISO 15118-2 and DIN EN 61851-23.

#### 1.2 Conventions
The following keywords within the document should be interpreted as written below:
- **SHALL** expresses an obligatory / mandatory requirement.
- **SHALL NOT** expresses an absolute prohibition.
- **SHOULD** expresses a recommendation or an advice. Not following the recommendation should only be done when the consequences are fully understood.
- **SHOULD NOT** expresses a discouragement. Carefully weigh the implications of deviating from the recommended procedure.

#### 1.3 Definitions & Abbreviations
| Abbreviation | Description |
|--------------|-------------|
| EV           | Electric Vehicle |
| PEP          | Power Electronics Protocol |
| SECC         | Supply Equipment Communication Controller |
| PECC         | Power Electronics Communication Controller |
| PE           | Power Electronics (circuitry) |
| IMD          | Isolation Monitoring Device |

#### 1.4 References
- RFC6455 "The WebSocket Protocol". http://tools.ietf.org/html/rfc6455
- RFC3986 "Uniform Resource Identifier (URI): Generic Syntax". http://tools.ietf.org/html/rfc3986
- RFC2616 "Hypertext Transfer Protocol-HTTP/1.1". http://tools.ietf.org/html/rfc2616
- RFC3629 "UTF-8, a transformation format of ISO 10646". http://tools.ietf.org/html/rfc3629
- RFC8259 "The JavaScript Object Notation (JSON) Data Interchange Format". https://tools.ietf.org/html/rfc8259

#### 1.5 PEP Downwards Compatibility
PEP 1.1 is NOT downwards compatible to PEP 1.0. All following versions are downwards compatible to PEP 1.1.

---

### 2. Communication Model
PEP communication is based on WebSocket as described in RFC6455. Two communication entities are defined:
- The Supply Equipment Communication Controller (SECC) acts as WebSocket client. This component governs the charging process, communicates with the EV and PECC, and controls and monitors the energy transfer using PEP. The SECC establishes a WebSocket connection and keeps it open at all times.
- The Power Electronics Communication Controller (PECC) acts as WebSocket server. This component manages and provides an interface to the power electronics (i.e., the physical device) itself. It is primarily responsible for executing and answering requests sent by the SECC. In addition the PECC can also send requests to the SECC, e.g., to control SECC outputs. The PECC waits for the SECC to establish a WebSocket connection.

PEP defines two communication patterns:
- A request-reply pattern implemented by request, response and error messages. This mechanism is intended for reliable control of a remote device such as the power electronics’ contactors.
- A one-way pattern implemented by info messages. This mechanism is intended for letting the other entity know about an internal state.

#### 2.1 The Connection URL
To initiate a WebSocket connection, the SECC needs a URL (RFC3986) to connect to. This PEP endpoint URL is called the connection URL.
A charging session (in the sense of ISO 15118) corresponds to exactly one charge point. A charge point denotes a power outlet that belongs to at most one charging session. Conceptually, a single Power Electronics (PE) managed by its PECC could provide energy for multiple charge points simultaneously.
PEP defines no method of addressing different charge points. This means that a single connection URL corresponds to exactly one charge point. If a single PECC wants to manage multiple charge points, it SHALL offer multiple connection URLs.

Example connection URL: `ws://pep-server.vector.com:1234/chargepoint1`

#### 2.2 Reconnection Attempts
When the WebSocket connection is lost, the SECC SHOULD try to reconnect once every PEP_WS_RECONNECT_INTERVAL (10000 ms). If the reconnection attempt succeeds, the PECC SHALL be ready to answer requests and send the status messages periodically. The SECC SHALL be able to process requests received as soon as it connects to the PECC.

#### 2.3 PEP-specific WebSocket Data
The WebSocket header "Sec-WebSocket-Protocol" header SHALL be set to "pep<PEP version>". PEP described in this document uses the following header: `Sec-WebSocket-Protocol: pep1.5`.

#### 2.4 Synchronicity
There SHALL be at most one request pending for each communication direction. This means that a communication controller (either SECC or PECC) SHALL NOT send request messages unless previous request messages sent by this communication controller have been responded to or have timed out. A request has been responded to if a reply (response or error message) with the same sequenceNumber as sent in the request is received within PEP_REQUEST_TIMEOUT (500 ms). A request has timed out if it has not been responded to within PEP_REQUEST_TIMEOUT (500 ms). Informational messages can be sent at all times, in particular in between processing a request message and sending the response message.

---

### 3. Message Frames
#### 3.1 Message Frame Structure
PEP messages consist of JavaScript Object Notation (JSON) encoded UTF-8 strings. Each information consists of a key-value-pair. String values of both keys and values are case-sensitive and SHALL follow the camelCase notation used in the associated json schemas.

The following two fields exist in every message:
- **type**: This field describes the overall purpose of a message. Four types exist: request, response, error and info. The type is a classification of a message at communication model level. The messageType defines the layout of the overall message. In contrast to all other types, messages with type "info" do not contain a sequence number.
- **kind**: This field refines the respective type and describes the action to be executed or component that is affected by the message. The kind is a classification and description of a message at application level. The kindType defines the layout of the payload field.

A message is a syntactically valid PEP message if and only if the respective JSON schema validates successfully against it. JSON schemas for each message are listed in the appendix Section PEP JSON Schemas.

If a valid request is received, it SHALL be answered with its respective response message. If the request received is
- syntactically (e.g., schema validation failed) or
- semantically (e.g., requested voltage exeeds limits) invalid, an error message SHALL be sent.

In the following subsections, examples given in the message descriptions show the complete message, i.e., with the type, kind and sequenceNumber (where applicable), not just the payload object itself.

---


#### 3.2 Request Messages
Request messages are sent by both the SECC and the PECC. They have the following fields:

| Field Name      | Field Type   | Description                                                        |
|-----------------|--------------|--------------------------------------------------------------------|
| type            | messageType  | Identifies the type of the PEP message. Set to "request".         |
| kind            | kindType     | Identifies the kind of the message and layout of the payload field.|
| sequenceNumber  | integer      | Used to match request and response/error messages.                 |
| payload         | JSON         | Payload corresponding to the message kind. Empty object if not required. |

##### 3.2.1 configuration
This message is used to request the current configuration of the power electronics. It could be sent anytime and multiple times. This implies that it is up to the SECC implementation if these values are requested regularly and when they are sent to the EV (e.g.: on startup of the SECC/ before every charging cycle/regularly during a charging cycle/...).
Answered with response - configuration.

**Example message:**
```json
{
  "type": "request",
  "kind": "configuration",
  "sequenceNumber": 458238,
  "payload": {}
}
```

##### 3.2.2 cableCheck
This message is used to request a high voltage isolation check, usually at the beginning of a charging process. It contains the suggested isolation check voltage, in case of CCS this is the maximum voltage of the EV. For CHAdeMO this is the voltage defined in the specification. The result is reported with info - status.
Answered with response - cableCheck.

**Payload fields:**
| Payload Field Name | Field Type | Physical Unit | Description                  |
|--------------------|------------|--------------|------------------------------|
| voltage            | number     | V/Volts      | Suggested isolation check voltage. |

**Example message:**
```json
{
  "type": "request",
  "kind": "cableCheck",
  "sequenceNumber": 458238,
  "payload": {
    "voltage": 500
  }
}
```

##### 3.2.3 targetValues
This message is used to instruct the power electronics to drive its outputs with the requested values for voltage and current. Furthermore, the current charging process state of the EV and the battery’s state of charge are reported with the chargingState and batteryStateOfCharge field, respectively.
Answered with response - targetValues.

**Payload fields:**
| Payload Field Name      | Field Type         | Physical Unit | Description                                 |
|------------------------|--------------------|--------------|---------------------------------------------|
| targetVoltage          | number             | V/Volts      | Voltage to be driven by the power electronics. |
| targetCurrent          | number             | A/Amperes    | Current to be driven by the power electronics |
| batteryStateOfCharge   | number             | %            | The vehicles’ battery state of charge. Values are in the range from 0 to 100, inclusive. |
| chargingState          | chargingStateType  |              | Current charging state of the EV.            |

**Example message:**
```json
{
  "type": "request",
  "kind": "targetValues",
  "sequenceNumber": 458238,
  "payload": {
    "targetVoltage": 600,
    "targetCurrent": 21,
    "batteryStateOfCharge": 50,
    "chargingState": "charge"
  }
}
```

##### 3.2.4 contactorsStatus
This message is used to instruct the power electronics to open or close its contactors.
Answered with response - contactorsStatus.

**Payload fields:**
| Payload Field Name | Field Type           | Description                  |
|--------------------|---------------------|------------------------------|
| contactorsStatus   | contactorsStatusType| New state of the contactors. |

**Example message:**
```json
{
  "type": "request",
  "kind": "contactorsStatus",
  "sequenceNumber": 458238,
  "payload": {
    "contactorsStatus": "closed"
  }
}
```

##### 3.2.5 reset
This message is used to reset the power electronics’ status to a valid, well-defined standby state. In this state, the contactors are open, the driven voltage and current are set to 0, the PECC sends the periodic info - status messages and is able to receive new requests, i.e., the operationalStatus is "operative". See Error Handling for further details.
This message does not affect the WebSocket communication, i.e., the WebSocket connection is not closed and the PECC is not rebooted.
This message may be received anytime, in particular prior to, during or after a charging process.
Answered with response - reset.

**Example message:**
```json
{
  "type": "request",
  "kind": "reset",
  "sequenceNumber": 458238,
  "payload": {}
}
```

##### 3.2.6 getInput
This message is used by the PECC to read inputs from the SECC. Multiple inputs can be requested with a single message. Available input identifiers depend on the hardware, refer to the SECC hardware manual.
Answered with response - getInput.

**Payload fields:**
| Payload Field Name | Field Type | Description                                 |
|--------------------|------------|---------------------------------------------|
| inputIdentifiers   | array      | Array of input identifiers to be requested. |

**Example message:**
```json
{
  "type": "request",
  "kind": "getInput",
  "sequenceNumber": 458238,
  "payload": {
    "inputIdentifiers" : ["d1","a1","t3"]
  }
}
```

##### 3.2.7 setOutput
This message is used by the PECC to set outputs at the SECC. Multiple outputs can be set with a single message. Available output identifiers depend on the hardware, refer to the SECC hardware manual.
Answered with response – setOutput.

**Payload fields:**
| Payload Field Name | Field Type | Description                                 |
|--------------------|------------|---------------------------------------------|
| outputValues       | JSON       | Key/value pairs of outputs and values to be set. |

**Example message:**
```json
{
  "type": "request",
  "kind": "setOutput",
  "sequenceNumber": 458238,
  "payload": {
    "outputValues" : {
      "d1": 1,
      "d2": 0
    }
  }
}
```

##### 3.2.8 stopCharging
This message is used by the PECC to request a graceful termination of the running charging session.
Answered with response – stopCharging.

**Example message:**
```json
{
  "type": "request",
  "kind": "stopCharging",
  "sequenceNumber": 458238,
  "payload": {}
}
```

---


#### 3.3 Response Messages
Response messages are sent by both the SECC and the PECC. They have the following fields:

| Field Name      | Field Type   | Description                                                        |
|-----------------|--------------|--------------------------------------------------------------------|
| type            | messageType  | Identifies the type of the PEP message. Set to "response".        |
| kind            | kindType     | Set to the kind of the request this message responds to.           |
| sequenceNumber  | integer      | Used to match request and response/error messages.                 |
| payload         | JSON         | Payload of the message kind. Empty object {} if not required.      |

**Example (configuration):**
```json
{
  "type": "response",
  "kind": "configuration",
  "sequenceNumber": 458238,
  "payload": {
    "firmwareVersion": "pe_1.0.2",
    "manufacturer": "pe_manufacturer1",
    "limitVoltageMin": 0,
    "limitVoltageMax": 700,
    "limitCurrentMin": 0,
    "limitCurrentMax": 50,
    "limitPowerMin": 0,
    "limitPowerMax": 30000,
    "limitDischargeCurrentMin": 0,
    "limitDischargeCurrentMax": -30,
    "limitDischargePowerMin": 0,
    "limitDischargePowerMax": -15000,
    "floatValues": true
  }
}
```

**Example (cableCheck):**
```json
{
  "type": "response",
  "kind": "cableCheck",
  "sequenceNumber": 458238,
  "payload": {}
}
```

**Example (targetValues):**
```json
{
  "type": "response",
  "kind": "targetValues",
  "sequenceNumber": 458238,
  "payload": {}
}
```

**Example (getInput):**
```json
{
  "type": "response",
  "kind": "getInput",
  "sequenceNumber": 458238,
  "payload": {
    "inputValues": {
      "d1": 1,
      "a1": 5.2,
      "t3": 40
    }
  }
}
```

---

#### 3.4 Error Messages
Error messages are sent as answers to request messages. They SHALL be sent if a problem with the request itself or the requested action occurs. Possible problems include failed syntax validation or invalid requested values. The most appropriate errorCategory should be chosen and the errorDetails field filled with an additional error description.

| Field Name      | Field Type   | Description                                                        |
|-----------------|--------------|--------------------------------------------------------------------|
| type            | messageType  | Identifies the type of the PEP message. Set to "error".           |
| kind            | kindType     | Set to the respective kind from the request this message answers.   |
| sequenceNumber  | integer      | Used to match request and response/error messages. Set to 0 if sequence number of the request could not be determined. |
| payload         | JSON         | Contains details of the error.                                     |

**Payload fields:**
| Payload Field Name | Field Type         | Description                  |
|--------------------|-------------------|------------------------------|
| errorCategory      | errorCategoryType | Category of the error.       |
| errorDetails       | string            | Detailed description or "".  |

**Example:**
```json
{
  "type": "error",
  "kind": "cableCheck",
  "sequenceNumber": 458238,
  "payload": {
    "errorCategory": "format",
    "errorDetails": "JSON schema validation failed at line 5."
  }
}
```

---

#### 3.5 Informational Messages
Informational messages are sent by both SECC and PECC and have the following fields:

| Field Name      | Field Type   | Description                                                        |
|-----------------|--------------|--------------------------------------------------------------------|
| type            | messageType  | Identifies the type of the PEP message. Set to "info".            |
| kind            | kindType     | Identifies the kind of the message and layout of the payload field.|
| payload         | JSON         | Payload of the message kind. Empty object {} if not required.      |

**Example (event):**
```json
{
  "type": "info",
  "kind": "event",
  "payload": {
    "eventDetails": "vendor specific description of an event"
  }
}
```

**Example (status):**
```json
{
  "type": "info",
  "kind": "status",
  "payload": {
    "measuredVoltage": 599,
    "measuredCurrent": 19,
    "drivenVoltage": 600,
    "drivenCurrent": 20,
    "temperature": 34.72,
    "contactorsStatus": "closed",
    "isolationStatus": "valid",
    "operationalStatus": "operative"
  }
}
```

**Example (evConnectionState):**
```json
{
  "type": "info",
  "kind": "evConnectionState",
  "payload": {
    "evConnectionState": "connected",
    "vehicleId": "AB:CD:12:34:56:78"
  }
}
```

**Example (chargingSession):**
```json
{
  "type": "info",
  "kind": "chargingSession",
  "payload": {
    "chargingProfileMaxPowerLimitWatts": 150000.0
  }
}
```

---

#### 3.6 Sequence Numbers
Sequence numbers are used to match requests to their respective replies, either response or error messages. The sequence number sent in requests SHALL be incremented for each request by 1, its value increases monotonically. If the valid range is exceeded, counting SHALL restart from 1. The sequence number in replies SHALL be set to the same value of the sequenceNumber field in the request it answers. There are two sequence numbers, one for each request direction. They are increased independently.

Regular sequence numbers are valid in the range from 1 to 2147483647 (2^31 - 1) inclusive.

---

#### 3.7 Type Definitions
**messageType:**
- info: Sent by both SECC and PECC. An info message does not get responded to.
- request: Sent by both SECC and PECC. Gets responded to with a response or error.
- response: Sent by both SECC and PECC. Response to a valid request.
- error: Sent by both SECC and PECC. Response to an invalid request.

**kindType:**
- configuration: Identifies messages required for the configuration report mechanism.
- cableCheck: Identifies messages required for an isolation check.
- targetValues: Identifies messages required for supplying of a voltage and current.
- contactorsStatus: Identifies messages required for a contactor state change.
- reset: Identifies messages required for the reset mechanism.
- getInput: Identifies messages required for input readout.
- setOutput: Identifies messages required for setting outputs.
- error: Identifies messages required for error handling.
- event: Identifies messages that report a generic, vendor-specific event.
- status: Identifies messages that report the current status.
- evConnectionState: Identifies messages that report the current EV connection state.
- stopCharging: Identifies messages sent by the PECC to stop charging.
- chargingSession: Identifies messages containing information about the current charging session.

**contactorsStatusType:**
- open: Contactors are open.
- closed: Contactors are closed.

**isolationStatusType:**
- invalid: No isolation test has been carried out yet.
- valid: Isolation test completed without warning or fault.
- warning: Isolation test resulted with a measured isolation resistance below the warning level defined in IEC CDV 61851-23.
- fault: Isolation test resulted with a measured isolation resistance below the fault level defined in IEC CDV 61851-23.

**operationalStatusType:**
- operative: Power electronics is able to supply voltage or power. Normal state of operation.
- inoperative: Power electronics is not able to supply voltage or power.

**chargingStateType:**
- standby: No charging process started yet.
- preCharge: EV is pre-charging.
- charge: EV is charging.
- postCharge: EV completed charging and is in a post-charging state. EV welding detection may be conducted in this state.

**errorCategoryType:**
- format: Message format is incorrect, i.e., the JSON schema validation fails.
- value: Invalid input/output identifier or requested voltage could not be supplied.
- inoperative: The power electronics is not able to execute the request due to its current operationalStatus.
- internal: An error internal to PECC or SECC occurred which prevented the processing of the request.
- generic: Any other error not covered by other categories in this table.

**evConnectionStateType:**
- disconnected: No connection to an EV (not plugged in).
- connected: EV connected (plugged in).
- energyTransferAllowed: Energy transfer to the EV is allowed.
- error: An error has occurred, e.g. short circuit between control pilot and protective conductor, SECC inoperative, ...

---

### 4. Timing Recommendations
SECC and PECC SHOULD comply with the following PEP timings:

| Name                        | Value [ms] | Description                                 |
|-----------------------------|------------|---------------------------------------------|
| PEP_REQUEST_TIMEOUT         | 500        |                                            |
| PEP_WS_RECONNECT_INTERVAL   | 10000      |                                            |
| PEP_STATUS_UPDATE_INTERVAL  | 200        |                                            |
| PEP_SECC_UNRESPONSIVE_TIMEOUT | 5000     |                                            |

---

### 5. Error Handling
The goal of PEP error handling is the prevention of a failure condition or the recovery from an invalid state (possibly distributed across SECC and PECC) to a safe, well-defined and stable state. This well-defined state is called the standby state and characterized by the following properties visible to the SECC:

| Property           | Physical Unit/Type         | Description                                 | Value                |
|--------------------|---------------------------|---------------------------------------------|----------------------|
| measuredVoltage    | V/Volts                   | Voltage measured at the outlet.             | Within local regulations for touch voltage. E.g.: IEC 61851-1: ≤ 60 V |
| measuredCurrent    | A/Amperes                 | Current measured at the outlet.             | 0                    |
| drivenVoltage      | V/Volts                   | Voltage driven at the output.               | 0                    |
| drivenCurrent      | A/Amperes                 | Current driven at the output.               | 0                    |
| temperature        | °C/Degrees Celsius        | Current temperature at the outlet.          | within PE operation limits |
| contactorsStatus   | contactorsStatusType      | Current status of the contactors.           | open                 |
| isolationStatus    | isolationStatusType       | Current isolation status of the cable.      | <neglected>          |
| operationalStatus  | operationalStatusType     | Current operational status of the power electronics as a whole. | operative |

If an invalid state is detected by the PECC, the operationalStatus SHALL be set to "inoperative". If the error condition is remedied, the operationalStatus SHALL be set to “operative”.

---

### 6. Example Scenarios
#### 6.1 Charging Sequence
> The SECC opens a WebSocket connection to the PECC.
> As soon as the WebSocket connection is established, the info – status message is sent periodically.
> The configuration can be requested once or periodically by the SECC at any time.
> The EV triggers the charging process.
> The cable check result "valid" is needed to continue.
> In the pre-charging phase, multiple targetValues requests may be received by the PECC.
> The charging phase begins as soon as a targetValues request is received with chargingState set to "charge".
> The charging process ends with a targetValues request with the chargingState set to "postCharge". The requested voltage and current is set to 0. The EV may then perform an optional welding detection of its internal contactors. After this phase, the reset request is sent and the EV unplugs.
> The evConnectionState message gets sent when the EV signals the corresponding state.

#### 6.2 Input/Output Control
> Accessing inputs and outputs is not part of the charging process.
> getInput and setOutput requests can be sent anytime.

---

### 7. PECC State Machine Proposal
The following state machine is a suggestion and meant as implementation hint. It is NOT required to implement the PECC in exactly this manner. Note that various mechanisms and PEP messages are not included, such as the error messages and the PECC-internal error handling itself.

> A charging procedure begins with the contactorsStatus request with contactorsStatus set to "closed".
> The current charging phase (preCharge, charge, postCharge) is reported by the targetValues request.
> The reset request may be received anytime while charging. The "reset" state shown is meant as a cleanup and reinitialization state. See Error Handling for details. In addition, the reset request is the normal (i.e., non-erroneous) transition from the postCharge state to the standby state.

---

### 8. Appendix
#### 8.1 IEC 61851 Control Pilot (CP) / Proximity Pin (PP) Supervision
The IEC 61851 and SAE J1772 standards impose strict safety requirements on the charging process and power supply monitoring. The charging process is controlled by the EV which sets a specific Control Pilot (CP) state. Six state categories exist: Ax, Bx, Cx, Dx, E and F. Energy transfer is allowed only in state categories Cx and Dx. In some cases (e.g. CCS Type 1) a PP supervision is also required to prevent energy transfer when the PP signal is not valid.

In order to implement this, the SECC provides a logical output called CP/PP supervision. This output controls the power electronics’ ability to energize its outlet. Conceptually, a logical AND conjunction exists in the power electronics between the PECC control input and CP/PP supervision: The PE is able to close its contactors if and only if the CP/PP supervision allows it, i.e., the CP state category is Cx or Dx and PP signal is valid (if applicable).

If a contactorsStatus request could not be processed due to the CP/PP supervision, an error message with the errorCategory set to "internal" should be sent.

---

<!-- End of reformatted protocol document. -->
