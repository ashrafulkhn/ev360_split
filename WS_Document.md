Status Released
Publisher Vector Informatik GmbH
© 2022 All rights reserved.
Any distribution or copying is subject to prior written approval by Vector.
Note: Hardcopy documents are not subject to change management.
Power Electronics Protocol overWebSocket
PEP-WS
Networking and Application Protocol Requirements
Version 1.8 of 2022-10-01
Change History
Date Name Changes
2019-10-08 vishnt First Draft: alpha state
2019-11-13 vishnt Major changes in chapters Timing and Error Handling. Added chapter IMD
Self Test Status
2020-01-31 vistrf Major change of chapters Message Frames, Timings, Error Handling.
Removed chapters IMD and Charging Illustration. Added JSON schemas.
Adapted Charging Sequence diagram and PECC state machine proposal
2020-03-30 vistio Keys and values are now case-sensitive and written in camelCase. Syntactical
errors have been removed from json schemas. Request targetValues
now includes the battery’s state of charge as field batteryStateOfCharge
2020-04-17 visjnk First chapter removed
2020-08-26 mkiefer Added getInput and setOutput request messages
Added evConnectionState message
2020-11-27 mkiefer Clarified use of PECC operationalStatus==INOPERATIVE
2021-02-15 mkiefer Added voltage to cableCheck request
Added vehicleId to evConnectionState
Clarified use of websocket PING mechanism
2021-03-05 visert Clarified difference between driven and measured values
2021-04-10 mkiefer Added floatValues to configuration response
2021-05-25 mkiefer Clarified request-configuration update intervals
2021-08-15 mkiefer Added stopCharging message
2022-01-25 mkiefer Added chargingSession message
2022-02-15 mkiefer Added PP supervision explanation
2022-04-15 mkiefer Removed isolationStatus noImd
2022-05-25 mkiefer Extended chargingSession message
2022-10-01 mkiefer BPT Extensions (response-configuration, info-chargingSession)
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
1 / 54
Contents
1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.1 Scope 4
1.2 Conventions 4
1.3 Definitions & Abbreviations 4
1.4 References 4
1.5 PEP Downwards Compatibility 4
2 Communication Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
2.1 The Connection URL 5
2.2 Reconnection Attempts 6
2.3 PEP-specific WebSocket Data 6
2.4 Synchronicity 6
3 Message Frames . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
3.1 Message Frame Structure 7
3.2 Request Messages 7
3.2.1 configuration 7
3.2.2 cableCheck 8
3.2.3 targetValues 8
3.2.4 contactorsStatus 9
3.2.5 reset 10
3.2.6 getInput 11
3.2.7 setOutput 11
3.2.8 stopCharging 12
3.3 Response Messages 13
3.3.1 configuration 13
3.3.2 cableCheck 15
3.3.3 targetValues 15
3.3.4 contactorsStatus 16
3.3.5 reset 16
3.3.6 getInput 17
3.3.7 setOutput 17
3.3.8 stopCharging 18
3.4 Error Messages 18
3.4.1 error 18
3.5 Informational Messages 19
3.5.1 event 19
3.5.2 status 20
3.5.3 evConnectionState 21
3.5.4 chargingSession 22
3.6 Sequence Numbers 24
3.7 Type Definitions 25
3.7.1 messageType 25
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
2 / 54
3.7.2 kindType 25
3.7.3 contactorsStatusType 25
3.7.4 isolationStatusType 25
3.7.5 operationalStatusType 26
3.7.6 chargingStateType 26
3.7.7 errorCategoryType 26
3.7.8 evConnectionStateType 26
4 Timing Recommendations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
5 Error Handling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
6 Example Scenarios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
6.1 Charging Sequence 30
6.2 Input/Output Control 31
7 PECC State Machine Proposal . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
8 Appendix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
8.1 IEC 61851 Control Pilot (CP) / Proximity Pin (PP) Supervision 33
8.2 PEP JSON Schemas 34
8.2.1 request – configuration 34
8.2.2 request - cableCheck 34
8.2.3 request - targetValues 35
8.2.4 request - contactorsStatus 37
8.2.5 request - getInput 38
8.2.6 request - setOutput 39
8.2.7 request - reset 39
8.2.8 request - stopCharging 40
8.2.9 response - configuration 41
8.2.10 response - cableCheck 43
8.2.11 response - targetValues 44
8.2.12 response - contactorsStatus 44
8.2.13 response - getInput 45
8.2.14 response - setOuput 46
8.2.15 response - reset 46
8.2.16 response - stopCharging 47
8.2.17 error - error 48
8.2.18 info - event 49
8.2.19 info - status 50
8.2.20 info - evConnectionState 51
8.2.21 info - chargingSession 52
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
3 / 54
1 Introduction
1.1 Scope
This document specifies the communication protocol between the Power Electronics Communication
Controller (PECC) and the Supply Equipment Communication Controller (SECC). This Power Electronics
Protocol (PEP) is designed to control and monitor the energy transfer of a power electronics
used in the context of Electric Vehicle (EV) charging. Its design is based on the requirements of the
ISO 15118-2 and DIN EN 61851-23.
1.2 Conventions
The following keywords within the document should be interpreted as written below:
SHALL expresses an obligatory / mandatory requirement.
SHALL NOT expresses an absolute prohibition.
SHOULD expresses a recommendation or an advice. Not following the recommendation should only
be done when the consequences are fully understood.
SHOULD NOT expresses a discouragement. Carefully weigh the implications of deviating from the
recommended procedure.
1.3 Definitions & Abbreviations
Abbreviation Description
EV Electric Vehicle
PEP Power Electronics Protocol
SECC Supply Equipment Communication Controller
PECC Power Electronics Communication Controller
PE Power Electronics (circuitry)
IMD Isolation Monitoring Device
1.4 References
Reference Description
RFC6455 "The WebSocket Protocol". http://tools.ietf.org/html/rfc6455
RFC3986 "Uniform Resource Identifier (URI): Generic Syntax". http://tools.ietf.org/html/
rfc3986
RFC2616 "Hypertext Transfer Protocol-HTTP/1.1". http://tools.ietf.org/html/rfc2616
RFC3629 "UTF-8, a transformation format of ISO 10646". http://tools.ietf.org/html/
rfc3629
RFC8259 "The JavaScript Object Notation (JSON) Data Interchange Format". https://tools.
ietf.org/html/rfc8259
1.5 PEP Downwards Compatibility
PEP 1.1 is NOT downwards compatible to PEP 1.0.
All following versions are downwards compatible to PEP 1.1.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
4 / 54
2 Communication Model
PEP communication is based on WebSocket as described in RFC6455. Two communication entities
are defined:
> The Supply Equipment Communication Controller (SECC) acts as WebSocket client. This component
governs the charging process, communicates with the EV and PECC, and controls and
monitors the energy transfer using PEP. The SECC establishes a WebSocket connection and
keeps it open at all times.
> The Power Electronics Communication Controller (PECC) acts as WebSocket server. This component
manages and provides an interface to the power electronics (i.e., the physical device) itself. It
is primarily responsible for executing and answering requests sent by the SECC. In addition the
PECC can also send requests to the SECC, e.g., to control SECC outputs. The PECC waits for the
SECC to establish a WebSocket connection.
PEP defines two communication patterns:
> A request-reply pattern implemented by request, response and error messages. This mechanism
is intended for reliable control of a remote device such as the power electronics’ contactors.
> A one-way pattern implemented by info messages. This mechanism is intended for letting the other
entity know about an internal state.
2.1 The Connection URL
To initiate a WebSocket connection, the SECC needs a URL (RFC3986) to connect to. This PEP
endpoint URL is called the connection URL.
A charging session (in the sense of ISO 15118) corresponds to exactly one charge point. A charge
point denotes a power outlet that belongs to at most one charging session. Conceptually, a single
Power Electronics (PE) managed by its PECC could provide energy for multiple charge points
simultaneously.
PEP defines no method of addressing different charge points. This means that a single connection
URL corresponds to exactly one charge point. If a single PECC wants to manage multiple charge
points, it SHALL offer multiple connection URLs.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
5 / 54
An example connection URL is “ws://pep-server.vector.com:1234/chargepoint1”.
SECC
PECC
Power supply
Plug, e.g., CCS
EV-SECC communication
e.g. ISO15118-2
e.g. DIN SPEC 70121
URL: ws://pep.vector.com:1234/chargepoint2
URL: ws://pep.vector.com:1234/chargepoint1
outlet 1
outlet 2
PE
PEP
2.2 Reconnection Attempts
When the WebSocket connection is lost, the SECC SHOULD try to reconnect once every
PEP_WS_RECONNECT_INTERVAL (10000 ms).
If the reconnection attempt succeeds, the PECC SHALL be ready to answer requests and send the
status messages periodically. The SECC SHALL be able to process requests received as soon as it
connects to the PECC.
2.3 PEP-specific WebSocket Data
The WebSocket header "Sec-WebSocket-Protocol" header SHALL be set to "pep<PEP version>".
PEP described in this document uses the following header: "Sec-WebSocket-Protocol: pep1.5".
2.4 Synchronicity
There SHALL be at most one request pending for each communication direction. This means that
a communication controller (either SECC or PECC) SHALL NOT send request messages unless
previous request messages sent by this communication controller have been responded to or have
timed out.
A request has been responded to if a reply (response or error message) with the same sequenceNumber
as sent in the request is received within PEP_REQUEST_TIMEOUT (500 ms).
A request has timed out if it has not been responded to within PEP_REQUEST_TIMEOUT (500 ms).
Informational messages can be sent at all times, in particular in between processing a request
message and sending the response message.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
6 / 54
3 Message Frames
3.1 Message Frame Structure
PEP messages consist of JavaScript Object Notation (JSON) encoded UTF-8 strings. Each information
consists of a key-value-pair. String values of both keys and values are case-sensitive and SHALL
follow the camelCase notation used in the associated json schemas.
The following two fields exist in every message:
type: This field describes the overall purpose of a message. Four types exist: request, response,
error and info. The type is a classification of a message at communication model level. The
messageType defines the layout of the overall message. In contrast to all other types, messages
with type "info" do not contain a sequence number.
kind: This field refines the respective type and describes the action to be executed or component
that is affected by the message. The kind is a classification and description of a message at
application level. The kindType defines the layout of the payload field.
A message is a syntactically valid PEP message if and only if the respective JSON schema validates
successfully against it. JSON schemas for each message are listed in the appendix Section PEP
JSON Schemas.
If a valid request is received, it SHALL be answered with its respective response message. If the
request received is
> syntactically (e.g., schema validation failed) or
> semantically (e.g., requested voltage exeeds limits) invalid, an error message SHALL be sent.
In the following subsections, examples given in the message descriptions show the complete message,
i.e., with the type, kind and sequenceNumber (where applicable), not just the payload object itself.
3.2 Request Messages
Request messages are sent by both the SECC and the PECC. They have the following fields:
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the message and layout of the payload
field.
sequenceNumber integer Used to match request and response/error messages.
payload JSON Payload corresponding to the message kind. Empty object if
not required.
3.2.1 configuration
This message is used to request the current configuration of the power electronics. It could be sent
anytime and multiple times. This implies that it is up to the SECC implementation if these values are
requested regularly and when they are sent to the EV (e.g.: on startup of the SECC/ before every
charging cycle/regularly during a charging cycle/. . . )
Answered with response - configuration.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
7 / 54
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "configuration".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
Example message:
1 {
2 "type": "request",
3 "kind": "configuration",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.2.2 cableCheck
This message is used to request a high voltage isolation check, usually at the beginning of a charging
process. It contains the suggested isolation check voltage, in case of CCS this is the maximum voltage
of the EV. For CHAdeMO this is the voltage defined in the specification. The result is reported with
info - status.
Answered with response - cableCheck.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "cableCheck".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Payload containing the suggested isolation check voltage.
Payload fields:
Payload Field Name Field Type Physical Unit Description
voltage number V/Volts Suggested isolation check voltage.
Example message:
1 {
2 "type": "request",
3 "kind": "cableCheck",
4 "sequenceNumber": 458238,
5 "payload": {
6 "voltage": 500
7 }
8 }
3.2.3 targetValues
This message is used to instruct the power electronics to drive its outputs with the requested values
for voltage and current. Furthermore, the current charging process state of the EV and the battery’s
state of charge are reported with the chargingState and batteryStateOfCharge field, respectively.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
8 / 54
Answered with response - targetValues.
If the requested voltage exceeds the power electronics’ internal voltage limit, this message SHALL
be answered with an error message with the errorCategory set to valueError. In this case, the
communication SHALL NOT stop, i.e., the Websocket connection is kept open and other actions (e.g.,
contactor state changes) SHALL NOT be executed as a direct consequence of this message.
If the requested voltage is within the power electronics’ internal voltage limit but the requested current
could not be supplied, this message SHALL be answered with response - targetValues. In this case,
the output should be driven with the requested voltage and the maximum current the power electronics
is able to supply with respect to both power and electrical current limits (degraded performance).
If this message is received at an inappropriate instant (e.g., if contactors are open), it SHALL be
ignored.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "targetValues".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Payload containing the requested values for voltage and current.
Payload fields:
Payload Field Name Field Type Physical Unit Description
targetVoltage number V/Volts Voltage to be driven by the power
electronics.
targetCurrent number A/Amperes Current to be driven by the power
electronics
batteryStateOfCharge number % The vehicles’ battery state of
charge. Values are in the range
from 0 to 100, inclusive.
chargingState chargingStateType Current charging state of the EV.
See chargingStateType for details.
Example message:
1 {
2 "type": "request",
3 "kind": "targetValues",
4 "sequenceNumber": 458238,
5 "payload": {
6 "targetVoltage": 600,
7 "targetCurrent": 21,
8 "batteryStateOfCharge": 50,
9 "chargingState": "charge"
10 }
11 }
3.2.4 contactorsStatus
This message is used to instruct the power electronics to open or close its contactors.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
9 / 54
Answered with response - contactorsStatus.
If the actual state equals the one requested, this message SHALL be ignored.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "contactorsStatus".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Payload containing the requested new state of the contactors.
Payload fields:
Payload Field Name Field Type Description
contactorsStatus contactorsStatusType New state of the contactors.
Example message:
1 {
2 "type": "request",
3 "kind": "contactorsStatus",
4 "sequenceNumber": 458238,
5 "payload": {
6 "contactorsStatus": "closed"
7 }
8 }
3.2.5 reset
This message is used to reset the power electronics’ status to a valid, well-defined standby state. In
this state, the contactors are open, the driven voltage and current are set to 0, the PECC sends the
periodic info - status messages and is able to receive new requests, i.e., the operationalStatus is
"operative". See Error Handling for further details.
This message does not affect the WebSocket communication, i.e., the WebSocket connection is not
closed and the PECC is not rebooted.
This message may be received anytime, in particular prior to, during or after a charging process.
Answered with response - reset.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "reset".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
10 / 54
Example message:
1 {
2 "type": "request",
3 "kind": "reset",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.2.6 getInput
This message is used by the PECC to read inputs from the SECC. Multiple inputs can be requested
with a single message. Available input identifiers depend on the hardware, refer to the SECC hardware
manual.
Answered with response - getInput.
If one of the requested input identifiers is invalid, this message SHALL be answered with an error
message with the errorCategory set to valueError.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "getInput".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Contains the requested inputs.
Payload fields:
Payload Field Name Field Type Description
inputIdentifiers array Array of input identifiers to be requested.
Example message:
1 {
2 "type": "request",
3 "kind": "getInput",
4 "sequenceNumber": 458238,
5 "payload": {
6 "inputIdentifiers" : ["d1","a1","t3"]
7 }
8 }
3.2.7 setOutput
This message is used by the PECC to set outputs at the SECC. Multiple outputs can be set with a
single message. Available output identifiers depend on the hardware, refer to the SECC hardware
manual.
Answered with response – setOutput.
If one of the requested output identifiers or values is invalid, this message SHALL be answered with
an error message with the errorCategory set to valueError.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
11 / 54
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "setOutput".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Contains the outputs to be set.
Payload fields:
Payload Field Name Field Type Description
outputValues JSON Key/value pairs of outputs and values to be set. Keys are of
type string and refer to the identifier of the output. Type of
a value depends on the corresponding output. Refer to the
SECC hardware manual.
Example message:
1 {
2 "type": "request",
3 "kind": "setOutput",
4 "sequenceNumber": 458238,
5 "payload": {
6 "outputValues" : {
7 "d1": 1,
8 "d2": 0
9 }
10 }
11 }
3.2.8 stopCharging
This message is used by the PECC to request a graceful termination of the running charging session.
Answered with response – stopCharging.
If no charging session is running, or it cannot be terminated in the current state, this message SHALL
be ignored.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "request".
kind kindType Identifies the kind of the request. Set to "stopCharging".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
12 / 54
Example message:
1 {
2 "type": "request",
3 "kind": "stopCharging",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.3 Response Messages
Response messages are sent by both the SECC and the PECC. They have the following fields:
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Set to the kind of the request this message responds to.
sequenceNumber integer Used to match request and response/error messages.
payload JSON Payload of the message kind. Empty object {} if not required.
3.3.1 configuration
This message is used to answer request - configuration messages. It provides the current configuration
of the power electronics.
The fields limitPowerMin, limitDischargeCurrentMin, limitDischargeCurrentMax, limitDischargePower-
Min and limitDischargePowerMax are only required for ISO 15118–20 BPT.
Note: Discharge values are always negative.
It is recommended to set floatValues to true. Setting it to false or omitting the floatValues key leads to
a replacement of all values of type number (floating point) with values of type integer in every JSON
message schema. This entails a loss of precision and is only supported for compatibility reasons.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to “response”.
kind kindType Identifies the kind of the request. Set to “configuration”.
sequenceNumber integer Used to match request and response/error messages.
payload JSON Contains the requested configuration values.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
13 / 54
Payload fields:
Payload Field Name Field Type Physical Unit Description
firmwareVersion string Firmware version of the power electronics
software
manufacturer string Power electronics manufacturer
limitVoltageMin number V/Volts Minimum voltage supported by the
power electronics
limitVoltageMax number V/Volts Maximum voltage supported by the
power electronics
limitCurrentMin number A/Amperes Minimum current supported by the
power electronics
limitCurrentMax number A/Amperes Maximum current supported by the
power electronics
limitPowerMin number W/Watts Minimum power output supported by
the power electronics
limitPowerMax number W/Watts Maximum power output supported by
the power electronics
limitDischargeCurrentMin number W/Watts Minimum discharge current supported
by the power electronics (negative
value)
limitDischargeCurrentMax number W/Watts Maximum discharge current supported
by the power electronics (negative
value)
limitDischargePowerMin number W/Watts Minimum discharge power supported
by the power electronics (negative
value)
limitDischargePowerMax number W/Watts Maximum discharge power supported
by the power electronics (negative
value)
floatValues boolean Use floating point numbers for voltages
and currents
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
14 / 54
Example message:
1 {
2 "type": "response",
3 "kind": "configuration",
4 "sequenceNumber": 458238,
5 "payload": {
6 "firmwareVersion": "pe_1.0.2",
7 "manufacturer": "pe_manufacturer1",
8 "limitVoltageMin": 0,
9 "limitVoltageMax": 700,
10 "limitCurrentMin": 0,
11 "limitCurrentMax": 50,
12 "limitPowerMin": 0,
13 "limitPowerMax": 30000,
14 "limitDischargeCurrentMin": 0,
15 "limitDischargeCurrentMax": -30,
16 "limitDischargePowerMin": 0,
17 "limitDischargePowerMax": -15000,
18 "floatValues": true
19 }
20 }
3.3.2 cableCheck
This message is used to answer request - cableCheck messages. It acknowledges the reception and
processing.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "configuration".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Contains the requested configuration values.
Example message:
1 {
2 "type": "response",
3 "kind": "cableCheck",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.3.3 targetValues
This message is used to answer request - targetValues messages. It acknowledges the reception and
processing.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
15 / 54
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "targetValues".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
Example message:
1 {
2 "type": "response",
3 "kind": "targetValues",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.3.4 contactorsStatus
This message is used to answer request - contactorsStatus messages. It acknowledges the reception
and processing.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "contactorsStatus".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
Example message:
1 {
2 "type": "response",
3 "kind": "contactorsStatus",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.3.5 reset
This message is used to answer request - reset messages. It acknowledges the reception and
processing.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "reset".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
16 / 54
Example message:
1 {
2 "type": "response",
3 "kind": "reset",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.3.6 getInput
This message is used to answer request – getInput messages. It returns the values corresponding to
the requested input identifiers.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "getInput".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Values of the requested input identifiers.
Payload fields:
Payload Field Name Field Type Description
inputValues JSON Key/value pairs of input identifiers and values
Example message:
1 {
2 "type": "response",
3 "kind": "getInput",
4 "sequenceNumber": 458238,
5 "payload": {
6 "inputValues": {
7 "d1": 1,
8 "a1": 5.2,
9 "t3": 40
10 }
11 }
12 }
3.3.7 setOutput
This message is used to answer request - setOutput messages. It acknowledges the reception and
processing.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
17 / 54
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "setOutput".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
Example message:
1 {
2 "type": "response",
3 "kind": "setOutput",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.3.8 stopCharging
This message is used to answer request - stopCharging messages. It acknowledges the reception
and processing.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "response".
kind kindType Identifies the kind of the request. Set to "stopCharging".
sequenceNumber integer Used to match request and response/error messages.
payload JSON Empty object {}.
Example message:
1 {
2 "type": "response",
3 "kind": "stopCharging",
4 "sequenceNumber": 458238,
5 "payload": {}
6 }
3.4 Error Messages
3.4.1 error
Error messages are sent as answers to request messages. They SHALL be sent if a problem with the
request itself or the requested action occurs. Possible problems include failed syntax validation or
invalid requested values. The most appropriate errorCategory should be chosen and the errorDetails
field filled with an additional error description.
If the sequence number of a request could not be determined (e.g., if the JSON could not be parsed),
it SHALL be set to the special value 0. See Sequence Numbers for details.
All error messages have the following fields:
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
18 / 54
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "error".
kind kindType Identifies the kind of the request. Set to the respective kind
from the request this message answers.
sequenceNumber integer Used to match request and response/error messages. Set to
0 if sequence number of the request could not be determined.
payload JSON Contains details of the error.
Payload fields:
Payload Field Name Field Type Description
errorCategory errorCategoryType Category of the error described further in the errorDetails
field.
errorDetails string Detailed description or "" (empty string).
Example message:
1 {
2 "type": "error",
3 "kind": "cableCheck",
4 "sequenceNumber": 458238,
5 "payload": {
6 "errorCategory": "format",
7 "errorDetails": "JSON schema validation failed at line 5."
8 }
9 }
3.5 Informational Messages
Informational messages are sent by both SECC and PECC and have the following fields:
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "info".
kind kindType Identifies the kind of the message and layout of the payload field.
payload JSON Payload of the message kind. Empty object {} if not required.
3.5.1 event
This message is used to inform the SECC about an event that happened at the power electronics. It
is intended to send vendor-specific messages. The detailed event description is given in the payload
field "eventDetails".
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "info".
kind kindType Identifies the kind of the information. Set to “event”.
payload JSON Contains details of the event.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
19 / 54
Payload fields:
Payload Field Name Field Type Description
eventDetails string Event description.
Example message:
1 {
2 "type": "info",
3 "kind": "event",
4 "payload": {
5 "eventDetails": "vendor specific description of an event"
6 }
7 }
3.5.2 status
This message is used to report the current status of the power electronics, including currently
measured values and other status information, e.g., the contactorsStatus. The field isolationStatus
has to be set according to ISO 15118-2.
Whenever the PECC encounters a problem and cannot operate normally, it SHALL set operational-
Status to INOPERATIVE, which SHALL cause the SECC to abort the charging process and prevent
further charging sessions until the PECC returns to an OPERATIVE state.
In this message, the PECC is able to differentiate driven values from actual measured ones with
the fields drivenVoltage/-Current and measuredVoltage/-Current. This becomes handy when no
power is driven but the currently measured values are of interest for the charging phase. This is for
example the case during WeldingDetection in DIN/ISO charging. The driven values currently are
only for informational purpose and may be set equal to the measured values. The measured values
however are the values reported to the EV and SHALL always present the actual values from PECC’s
perspective.
The status message SHALL be sent periodically every PEP_STATUS_UPDATE_INTERVAL (200 ms).
It may be used by the SECC to detect that the PECC is unresponsive.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "info".
kind kindType Identifies the kind of the information. Set to “status”.
payload JSON Contains the current status of the power electronics.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
20 / 54
Payload fields:
Payload Field Name Field Type Physical Unit Description
measuredVoltage number V/Volts Voltage measured at the
outlet.
measuredCurrent number A/Amperes Current measured at the
outlet.
drivenVoltage number V/Volts Voltage driven at the output.
drivenCurrent number A/Amperes Current driven at the output.
temperature number °C/Degrees Celsius Current temperature of the
power electronics.1
contactorsStatus contactorsStatusType Current status of the contactors.
isolationStatus isolationStatusType Current isolation status of
the cable.
operationalStatus operationalStatusType Current operational status
of the power electronics as
a whole.
Example message:
1 {
2 "type": "info",
3 "kind": "status",
4 "payload": {
5 "measuredVoltage": 599,
6 "measuredCurrent": 19,
7 "drivenVoltage": 600,
8 "drivenCurrent": 20,
9 "temperature": 34.72,
10 "contactorsStatus": "closed",
11 "isolationStatus": "valid",
12 "operationalStatus": "operative"
13 }
14 }
3.5.3 evConnectionState
This message is used to report the connection state of the EV. If available, the vehicle identifier is
transmitted when the connection state changes to connected. The vehicleId field is not present for all
other values of evConnectionState.
The evConnectionState message SHALL be sent by the SECC whenever the EV connection state
changes. Safety critical decisions SHALL NOT be made based on this purely informational message
(see CP/PP supervision). Also, the charging cycle is controlled by the contactorsStatus and
targetValues messages.
1This value is used for diagnostic/monitoring purposes only. The SECC does not act on this value.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
21 / 54
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "info".
kind kindType Identifies the kind of the information. Set to “evConnectionState”.
payload JSON Contains the current EV connection state.
Payload fields:
Payload Field Name Field Type Description
evConnectionState evConnectionStateType Current EV connection state.
vehicleId string Identifier of the connected vehicle. Only present
if evConnectionState==CONNECTED.
Example message:
1 {
2 "type": "info",
3 "kind": "evConnectionState",
4 "payload": {
5 "evConnectionState": "connected",
6 "vehicleId": "AB:CD:12:34:56:78"
7 }
8 }
3.5.4 chargingSession
This message is used to provide information about the current charging session.
The chargingSession message SHALL be sent by the SECC whenever the information contained
in the message changes. It is not required to send all the fields in the payload, so only fields with
updated information need to be transmitted.
Note: Discharge values are always negative.
Field Name Field Type Description
type messageType Identifies the type of the PEP message. Set to "info".
kind kindType Identifies the kind of the information. Set to “chargingSession”.
payload JSON Contains information about the current charging session.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
22 / 54
Payload fields:
Payload Field Name Field Type Description
chargingProfileMaxPowerLimitWatts number Maximum power in Watts contained in the current
charging profile.
timeToFullSocSeconds number Remaining time in seconds to full SOC.
evMinVoltageVolts number Minimum voltage the EV can handle in Volts.
evMaxVoltageVolts number Maximum voltage the EV can handle in Volts.
evMinCurrentAmperes number Minimum current the EV can handle in Amperes.
evMaxCurrentAmperes number Maximum current the EV can handle in Amperes.
evMinPowerWatts number Minimum power the EV can handle in Watts.
evMaxPowerWatts number Maximum power the EV can handle in Watts.
evMinDischargeCurrentAmperes number Minimum discharge current (negative value)
the EV can handle in Amperes.
evMaxDischargeCurrentAmperes number Maximum discharge current (negative value)
the EV can handle in Amperes.
evMinDischargePowerWatts number Minimum discharge power (negative value)
the EV can handle in Watts.
evMaxDischargePowerWatts number Maximum discharge power (negative value)
the EV can handle in Watts.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
23 / 54
Example messages:
1 {
2 "type": "info",
3 "kind": "chargingSession",
4 "payload": {
5 "chargingProfileMaxPowerLimitWatts": 150000.0
6 }
7 }
1 {
2 "type": "info",
3 "kind": "chargingSession",
4 "payload": {
5 "evMinVoltageVolts": 0,
6 "evMaxVoltageVolts": 400,
7 "evMinCurrentAmperes": 0,
8 "evMaxCurrentAmperes": 350,
9 "evMinPowerWatts": 0,
10 "evMaxPowerWatts": 125000,
11 "evMinDischargeCurrentAmperes": 0,
12 "evMaxDischargeCurrentAmperes": -100,
13 "evMinDischargePowerWatts": 0,
14 "evMaxDischargePowerWatts": -20000,
15 "chargeMode": "dynamicBpt"
16 }
17 }
3.6 Sequence Numbers
Sequence numbers are used to match requests to their respective replies, either response or error
messages. The sequence number sent in requests SHALL be incremented for each request by 1,
its value increases monotonically. If the valid range is exceeded, counting SHALL restart from 1.
The sequence number in replies SHALL be set to the same value of the sequenceNumber field in
the request it answers. There are two sequence numbers, one for each request direction. They are
increased independently.
If the sequence number from a request message could not be determined (e.g., if the JSON parsing
fails), it SHALL be set to the special value 0.
Regular sequence numbers are valid in the range from 1 to 2147483647 (231 - 1) inclusive.
Field Name Field Type Description
sequenceNumber integer Valid in the range between 1 and 231 - 1.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
24 / 54
3.7 Type Definitions
3.7.1 messageType
type Description
info Sent by both SECC and PECC. An info message does not get responded to.
request Sent by both SECC and PECC. Gets responded to with a response or error.
response Sent by both SECC and PECC. Response to a valid request.
error Sent by both SECC and PECC. Response to an invalid request.
3.7.2 kindType
type Description
configuration Identifies messages required for the configuration report mechanism.
cableCheck Identifies messages required for an isolation check.
targetValues Identifies messages required for supplying of a voltage and current.
contactorsStatus Identifies messages required for a contactor state change.
reset Identifies messages required for the reset mechanism.
getInput Identifies messages required for input readout.
setOutput Identifies messages required for setting outputs.
error Identifies messages required for error handling.
event Identifies messages that report a generic, vendor-specific event.
status Identifies messages that report the current status.
evConnectionState Identifies messages that report the current EV connection state.
stopCharging Identifies messages sent by the PECC to stop charging.
chargingSession Identifies messages containing information about the current charging session.
3.7.3 contactorsStatusType
type Description
open Contactors are open.
closed Contactors are closed.
3.7.4 isolationStatusType
See ISO 15118-2 for details.
type Description
invalid No isolation test has been carried out yet.
valid Isolation test completed without warning or fault.
warning Isolation test resulted with a measured isolation resistance below the warning level
defined in IEC CDV 61851-23.
fault Isolation test resulted with a measured isolation resistance below the fault level defined
in IEC CDV 61851-23.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
25 / 54
3.7.5 operationalStatusType
type Description
operative Power electronics is able to supply voltage or power. Normal state of operation.
inoperative Power electronics is not able to supply voltage or power.
3.7.6 chargingStateType
type Description
standby No charging process started yet.
preCharge EV is pre-charging.
charge EV is charging.
postCharge EV completed charging and is in a post-charging state. EV welding detection may
be conducted in this state.
3.7.7 errorCategoryType
type Description
format Message format is incorrect, i.e., the JSON schema validation fails.
value Invalid input/output identifier.
or
Requested voltage could not be supplied.
Note: It is not a valueError if the requested voltage could be supplied but the requested
current could not be supplied. In this case, the output should be driven with the
requested voltage and the electrical current limit (degraded performance).
inoperative The power electronics is not able to execute the request due to its current operational-
Status.
internal An error internal to PECC or SECC occurred which prevented the processing of the
request.
generic Any other error not covered by other categories in this table.
3.7.8 evConnectionStateType
type Description
disconnected No connection to an EV (not plugged in).
connected EV connected (plugged in).
energyTransferAllowed Energy transfer to the EV is allowed.
error An error has occured, e.g. short circuit between control pilot and protective
conductor, SECC inoperative, ...
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
26 / 54
4 Timing Recommendations
The communication between an EV and SECC SHALL satisfy strict timing requirements. These
requirements are detailed in the respective standard, e.g., ISO 15118.
PEP itself does not require neither SECC nor PECC to adhere to these timing requirements. However,
it does recommend compliance with the following timings. If these timing recommendations are met,
a charging session is not aborted due to a timing violation caused by the communication between
SECC and PECC. This applies to charging sessions using ISO 15118-2 or DIN SPEC 70121 for
EV-SECC communication.
SECC and PECC SHOULD comply with the following PEP timings:
Name Value [ms]
PEP_REQUEST_TIMEOUT 500
PEP_WS_RECONNECT_INTERVAL 10000
PEP_STATUS_UPDATE_INTERVAL 200
PEP_SECC_UNRESPONSIVE_TIMEOUT 5000
In addition, the power electronics SHOULD satisfy the following non-PEP timings :
Name Value [ms] Description Derived
from
PE_CABLE_CHECK_TIME 37000 Time needed to perform a cable check.
Measurement start: cableCheck request
is received by PECC.
Measurement end: Result is available
at PECC.
The time needed for reporting and processing
a status update is taken into
account.
V2G_SECC_
CableCheck_
Performance_
Time
PE_PRE_CHARGE_TIME 4000 Time needed to pre-charge.
Measurement start: targetValues request
with the "chargingState" field
set to "preCharge" is received by the
PECC.
Measurement end: The measured output
voltage equals the requested voltage
with a maximum deviation according
to IEC CDV 61851-23.
Note that multiple pre-charging requests
may be received. The timer is
reset for each pre-charge request.
The time needed for reporting and processing
a status update is taken into
account.
V2G_SECC_
PreCharge_
Performance_
Time
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
27 / 54
5 Error Handling
The goal of PEP error handling is the prevention of a failure condition or the recovery from an invalid
state (possibly distributed across SECC and PECC) to a safe, well-defined and stable state.
This well-defined state is called the standby state and characterized by the following properties visible
to the SECC:
Property Physical Unit/Type Description Value
measuredVoltage V/Volts Voltage measured at
the outlet.
Within local regulations for
touch voltage.
E.g.: IEC 61851-1:  60 V
measuredCurrent A/Amperes Current measured at
the outlet.
02
drivenVoltage V/Volts Voltage driven at the
output.
0
drivenCurrent A/Amperes Current driven at the
output.
0
temperature °C/Degrees Celcius Current temperature at
the outlet.
within PE operation limits
contactorsStatus contactorsStatusType Current status of the
contactors.
open
isolationStatus isolationStatusType Current isolation status
of the cable.
<neglected>
operationalStatus operationalStatusType Current operational status
of the power electronics
as a whole.
operative
If an invalid state is detected by the PECC, the operationalStatus SHALL be set to "inoperative". If the
error condition is remedied, the operationalStatus SHALL be set to “operative”.
The following conditions SHALL lead to a transition of the PECC and power electronics to the standby
state:
> It is detected that the SECC is unresponsive. This may be due to a networking failure or SECCinternal
error. The SECC is considered unresponsive if it does not respond to messages within
PEP_SECC_UNRESPONSIVE_TIMEOUT (5000 ms). This may be implemented using WebSocket
Ping and Pong messages RFC6455. THE SECC SHALL NOT use this mechanism to detect an
unresponsive PECC, for this purpose the periodic info - status message may be used.
> PECC receives a reset request. This is used by the SECC to handle errors from the EV-SECC
communication such as message timeouts.
> PECC receives a contactorsStatus request with contactorsStatus set to "open" while the current
(i.e., actual) contactorsStatus is "closed".
Note that it is possible to implement a transition phase, i.e., a period between the invalid and standby
state. This allows for example the discharging of capacities. While in this transition phase, the
operationalStatus SHALL be set to "inoperative" and requests received SHALL be answered with an
error message with the errorCategory set to "inoperative". The periodic status update is unaffected
and sent continuously.
If requests could not be processed by the PECC due to the CP/PP supervision, an error message
2may not actually be zero, but the value is transmitted to the EV and SHALL meet applicable requirements.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
28 / 54
SHALL be sent with the errorCategory set to "internal".
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
29 / 54
6 Example Scenarios
6.1 Charging Sequence
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
30 / 54
> The SECC opens a WebSocket connection to the PECC.
> As soon as the WebSocket connection is established, the info – status message is sent periodically.
> The configuration can be requested once or periodically by the SECC at any time.
> The EV triggers the charging process.
> The cable check result "valid" is needed to continue.
> In the pre-charging phase, multiple targetValues requests may be received by the PECC.
> The charging phase begins as soon as a targetValues request is received with chargingState set
to "charge".
> The charging process ends with a targetValues request with the chargingState set to "postCharge".
The requested voltage and current is set to 0. The EV may then perform an optional welding
detection of its internal contactors. After this phase, the reset request is sent and the EV unplugs.
> The evConnectionState message gets sent when the EV signals the corresponding state.
6.2 Input/Output Control
> Accessing inputs and outputs is not part of the charging process.
> getInput and setOutput requests can be sent anytime.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
31 / 54
7 PECC State Machine Proposal
The following state machine is a suggestion and meant as implementation hint. It is NOT required to
implement the PECC in exactly this manner. Note that various mechanisms and PEP messages are
not included, such as the error messages and the PECC-internal error handling itself.
Note the following crucial properties:
> A charging procedure begins with the contactorsStatus request with contactorsStatus set to
"closed".
> The current charging phase (preCharge, charge, postCharge) is reported by the targetValues
request.
> The reset request may be received anytime while charging. The "reset" state shown is meant as a
cleanup and reinitialization state. See Error Handling for details. In addition, the reset request is
the normal (i.e., non-erroneous) transition from the postCharge state to the standby state.
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
32 / 54
8 Appendix
8.1 IEC 61851 Control Pilot (CP) / Proximity Pin (PP) Supervision
The IEC 61851 and SAE J1772 standards impose strict safety requirements on the charging process
and power supply monitoring. The charging process is controlled by the EV which sets a specific
Control Pilot (CP) state. Six state categories exist: Ax, Bx, Cx, Dx, E and F. Energy transfer is allowed
only in state categories Cx and Dx. In some cases (e.g. CCS Type 1) a PP supervision is also required
to prevent energy transfer when the PP signal is not valid.
In order to implement this, the SECC provides a logical output called CP/PP supervision. This output
controls the power electronics’ ability to energize its outlet. Conceptually, a logical AND conjunction
exists in the power electronics between the PECC control input and CP/PP supervision: The PE is
able to close its contactors if and only if the CP/PP supervision allows it, i.e., the CP state category is
Cx or Dx and PP signal is valid (if applicable).
If a contactorsStatus request could not be processed due to the CP/PP supervision, an error message
with the errorCategory set to "internal" should be sent.
SECC PECC
outlet
PE
PEP
PECC
contactors control
& HVDC
CP/PP supervision
CP/PP signal
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
33 / 54
8.2 PEP JSON Schemas
8.2.1 request – configuration
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "configuration"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.2 request - cableCheck
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "cableCheck"
16 ]
17 },
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
34 / 54
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 "$ref": "#/definitions/cableCheckRequestPayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "cableCheckRequestPayload": {
38 "type": "object",
39 "properties": {
40 "voltage": {
41 "$ref": "#/definitions/voltage"
42 }
43 },
44 "required": [
45 "voltage"
46 ]
47 },
48 "voltage": {
49 "type": "number",
50 "minimum": 0,
51 "maximum": 2147483647
52 }
53 }
54 }
8.2.3 request - targetValues
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "targetValues"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
35 / 54
22 "$ref": "#/definitions/targetValuesRequestPayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "targetValuesRequestPayload": {
38 "type": "object",
39 "properties": {
40 "targetVoltage": {
41 "$ref": "#/definitions/targetVoltage"
42 },
43 "targetCurrent": {
44 "$ref": "#/definitions/targetCurrent"
45 },
46 "batteryStateOfCharge": {
47 "$ref": "#/definitions/batteryStateOfCharge"
48 },
49 "chargingState": {
50 "$ref": "#/definitions/chargingState"
51 }
52 },
53 "required": [
54 "targetVoltage",
55 "targetCurrent",
56 "batteryStateOfCharge",
57 "chargingState"
58 ]
59 },
60 "targetVoltage": {
61 "type": "number",
62 "minimum": 0,
63 "maximum": 2147483647
64 },
65 "targetCurrent": {
66 "type": "number",
67 "minimum": 0,
68 "maximum": 2147483647
69 },
70 "batteryStateOfCharge": {
71 "type": "number",
72 "minimum": 0,
73 "maximum": 100
74 },
75 "chargingState": {
76 "$ref": "#/definitions/chargingStateType"
77 },
78 "chargingStateType": {
79 "type": "string",
80 "enum": [
81 "standby",
82 "preCharge",
83 "charge",
84 "postCharge"
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
36 / 54
85 ]
86 }
87 }
88 }
8.2.4 request - contactorsStatus
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "contactorsStatus"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 "$ref": "#/definitions/contactorsStatusRequestPayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "contactorsStatusRequestPayload": {
38 "type": "object",
39 "properties": {
40 "contactorsStatus": {
41 "$ref": "#/definitions/contactorStatusType"
42 }
43 },
44 "required": [
45 "contactorsStatus"
46 ]
47 },
48 "contactorStatusType": {
49 "type": "string",
50 "enum": [
51 "open",
52 "closed"
53 ]
54 }
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
37 / 54
55 }
56 }
8.2.5 request - getInput
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "getInput"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 "$ref": "#/definitions/getInputRequestPayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "getInputRequestPayload": {
38 "type" : "object",
39 "properties": {
40 "inputIdentifiers": {
41 "$ref": "#/definitions/inputIdentifiers"
42 }
43 },
44 "required": [
45 "inputIdentifiers"
46 ]
47 },
48 "inputIdentifiers": {
49 "type": "array",
50 "items": {
51 "type" : "string"
52 }
53 }
54 }
55 }
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
38 / 54
8.2.6 request - setOutput
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "setOutput"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 "$ref": "#/definitions/setOutputRequestPayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "setOutputRequestPayload": {
38 "type" : "object",
39 "properties": {
40 "outputValues": {
41 "type": "object"
42 }
43 },
44 "required": [
45 "outputValues"
46 ]
47 }
48 }
49 }
8.2.7 request - reset
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
39 / 54
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "reset"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.8 request - stopCharging
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "request"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "stopCharging"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
40 / 54
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.9 response - configuration
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "configuration"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 "$ref": "#/definitions/configurationResponsePayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "configurationResponsePayload": {
38 "type": "object",
39 "properties": {
40 "firmwareVersion": {
41 "type": "string"
42 },
43 "manufacturer": {
44 "type": "string"
45 },
46 "limitVoltageMin": {
47 "$ref": "#/definitions/limitVoltageMin"
48 },
49 "limitVoltageMax": {
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
41 / 54
50 "$ref": "#/definitions/limitVoltageMax"
51 },
52 "limitCurrentMin": {
53 "$ref": "#/definitions/limitCurrentMin"
54 },
55 "limitCurrentMax": {
56 "$ref": "#/definitions/limitCurrentMax"
57 },
58 "limitPowerMin": {
59 "$ref": "#/definitions/limitPowerMin"
60 },
61 "limitPowerMax": {
62 "$ref": "#/definitions/limitPowerMax"
63 },
64 "limitDischargeCurrentMin": {
65 "$ref": "#/definitions/limitDischargeCurrentMin"
66 },
67 "limitDischargeCurrentMax": {
68 "$ref": "#/definitions/limitDischargeCurrentMax"
69 },
70 "limitDischargePowerMin": {
71 "$ref": "#/definitions/limitDischargePowerMin"
72 },
73 "limitDischargePowerMax": {
74 "$ref": "#/definitions/limitDischargePowerMax"
75 },
76 "floatValues": {
77 "type": "boolean"
78 }
79 },
80 "required": [
81 "firmwareVersion",
82 "manufacturer",
83 "limitVoltageMin",
84 "limitVoltageMax",
85 "limitCurrentMin",
86 "limitCurrentMax",
87 "limitPowerMax"
88 ]
89 },
90 "limitVoltageMin": {
91 "type": "number",
92 "minimum": 0,
93 "maximum": 2147483647
94 },
95 "limitVoltageMax": {
96 "type": "number",
97 "minimum": 0,
98 "maximum": 2147483647
99 },
100 "limitCurrentMin": {
101 "type": "number",
102 "minimum": 0,
103 "maximum": 2147483647
104 },
105 "limitCurrentMax": {
106 "type": "number",
107 "minimum": 0,
108 "maximum": 2147483647
109 },
110 "limitPowerMin": {
111 "type": "number",
112 "minimum": 0,
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
42 / 54
113 "maximum": 2147483647
114 },
115 "limitPowerMax": {
116 "type": "number",
117 "minimum": 0,
118 "maximum": 2147483647
119 },
120 "limitDischargeCurrentMin": {
121 "type": "number",
122 "minimum": -2147483647,
123 "maximum": 0
124 },
125 "limitDischargeCurrentMax": {
126 "type": "number",
127 "minimum": -2147483647,
128 "maximum": 0
129 },
130 "limitDischargePowerMin": {
131 "type": "number",
132 "minimum": -2147483647,
133 "maximum": 0
134 },
135 "limitDischargePowerMax": {
136 "type": "number",
137 "minimum": -2147483647,
138 "maximum": 0
139 }
140 }
141 }
8.2.10 response - cableCheck
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "cableCheck"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
29 ],
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
43 / 54
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.11 response - targetValues
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "targetValues"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.12 response - contactorsStatus
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
44 / 54
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "contactorsStatus"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.13 response - getInput
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "getInput"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 "$ref": "#/definitions/getInputResponsePayload"
23 }
24 },
25 "required": [
26 "type",
27 "kind",
28 "sequenceNumber",
29 "payload"
30 ],
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
45 / 54
31 "definitions": {
32 "sequenceNumber": {
33 "type": "integer",
34 "minimum": 0,
35 "maximum": 2147483647
36 },
37 "getInputResponsePayload":
38 {
39 "type": "object"
40 }
41 }
42 }
8.2.14 response - setOuput
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "setOutput"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {}
22 },
23 "required": [
24 "type",
25 "kind",
26 "sequenceNumber",
27 "payload"
28 ],
29 "definitions": {
30 "sequenceNumber": {
31 "type": "integer",
32 "minimum": 0,
33 "maximum": 2147483647
34 }
35 }
36 }
8.2.15 response - reset
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
46 / 54
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "reset"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
28 "payload"
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.16 response - stopCharging
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "response"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "stopCharging"
16 ]
17 },
18 "sequenceNumber": {
19 "$ref": "#/definitions/sequenceNumber"
20 },
21 "payload": {
22 }
23 },
24 "required": [
25 "type",
26 "kind",
27 "sequenceNumber",
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
47 / 54
28 "payload"
29 ],
30 "definitions": {
31 "sequenceNumber": {
32 "type": "integer",
33 "minimum": 0,
34 "maximum": 2147483647
35 }
36 }
37 }
8.2.17 error - error
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "error"
10 ]
11 },
12 "kind": {
13 "$ref": "#/definitions/kindType"
14 },
15 "sequenceNumber": {
16 "$ref": "#/definitions/sequenceNumber"
17 },
18 "payload": {
19 "$ref": "#/definitions/errorMessagePayload"
20 }
21 },
22 "required": [
23 "type",
24 "kind",
25 "sequenceNumber",
26 "payload"
27 ],
28 "definitions": {
29 "kindType": {
30 "type": "string",
31 "enum": [
32 "configuration",
33 "cableCheck",
34 "targetValues",
35 "contactorsStatus",
36 "error",
37 "event",
38 "status"
39 ]
40 },
41 "sequenceNumber": {
42 "type": "integer",
43 "minimum": 0,
44 "maximum": 2147483647
45 },
46 "errorMessagePayload": {
47 "type": "object",
48 "properties": {
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
48 / 54
49 "errorCategory": {
50 "$ref": "#/definitions/errorCategory"
51 },
52 "errorDetails": {
53 "type": "string"
54 }
55 },
56 "required": [
57 "errorCategory",
58 "errorDetails"
59 ]
60 },
61 "errorCategory": {
62 "type": "string",
63 "enum": [
64 "format",
65 "value",
66 "inoperative",
67 "internal",
68 "generic"
69 ]
70 }
71 }
72 }
8.2.18 info - event
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "info"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "event"
16 ]
17 },
18 "payload": {
19 "$ref": "#/definitions/eventInfoPayload"
20 }
21 },
22 "required": [
23 "type",
24 "kind",
25 "payload"
26 ],
27 "definitions": {
28 "eventInfoPayload": {
29 "type": "object",
30 "properties": {
31 "eventDetails": {
32 "type": "string"
33 }
34 },
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
49 / 54
35 "required": [
36 "eventDetails"
37 ]
38 }
39 }
40 }
8.2.19 info - status
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "info"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "status"
16 ]
17 },
18 "payload": {
19 "$ref": "#/definitions/statusInfoPayload"
20 }
21 },
22 "required": [
23 "type",
24 "kind",
25 "payload"
26 ],
27 "definitions": {
28 "statusInfoPayload": {
29 "type": "object",
30 "properties": {
31 "measuredVoltage": {
32 "$ref": "#/definitions/voltageType"
33 },
34 "measuredCurrent": {
35 "$ref": "#/definitions/currentType"
36 },
37 "drivenVoltage": {
38 "$ref": "#/definitions/voltageType"
39 },
40 "drivenCurrent": {
41 "$ref": "#/definitions/currentType"
42 },
43 "temperature": {
44 "type": "number"
45 },
46 "contactorsStatus": {
47 "$ref": "#/definitions/contactorsStatusType"
48 },
49 "isolationStatus": {
50 "$ref": "#/definitions/isolationStatusType"
51 },
52 "operationalStatus": {
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
50 / 54
53 "$ref": "#/definitions/operationalStatusType"
54 }
55 },
56 "required": [
57 "measuredVoltage",
58 "measuredCurrent",
59 "drivenVoltage",
60 "drivenCurrent",
61 "temperature",
62 "contactorsStatus",
63 "isolationStatus",
64 "operationalStatus"
65 ]
66 },
67 "voltageType": {
68 "type": "number",
69 "minimum": 0,
70 "maximum": 2147483647
71 },
72 "currentType": {
73 "type": "number",
74 "minimum": 0,
75 "maximum": 2147483647
76 },
77 "contactorsStatusType": {
78 "type": "string",
79 "enum": [
80 "open",
81 "closed"
82 ]
83 },
84 "isolationStatusType": {
85 "type": "string",
86 "enum": [
87 "valid",
88 "invalid",
89 "warning",
90 "fault"
91 ]
92 },
93 "operationalStatusType": {
94 "type": "string",
95 "enum": [
96 "operative",
97 "inoperative"
98 ]
99 }
100 }
101 }
8.2.20 info - evConnectionState
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "info"
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
51 / 54
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "evConnectionState"
16 ]
17 },
18 "payload": {
19 "$ref": "#/definitions/evConnectionStatePayload"
20 }
21 },
22 "required": [
23 "type",
24 "kind",
25 "payload"
26 ],
27 "definitions": {
28 "evConnectionStatePayload": {
29 "type": "object",
30 "properties": {
31 "evConnectionState": {
32 "type": "string",
33 "enum": [
34 "disconnected",
35 "connected",
36 "energyTransferAllowed",
37 "error"
38 ]
39 },
40 "vehicleId": {
41 "type": "string"
42 }
43 },
44 "required": [
45 "evConnectionState"
46 ]
47 }
48 }
49 }
8.2.21 info - chargingSession
1 {
2 "$schema": "http://json-schema.org/draft-06/schema#",
3 "comment": "pep1.8",
4 "type": "object",
5 "properties": {
6 "type": {
7 "type": "string",
8 "enum": [
9 "info"
10 ]
11 },
12 "kind": {
13 "type": "string",
14 "enum": [
15 "chargingSession"
16 ]
17 },
18 "payload": {
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
52 / 54
19 "$ref": "#/definitions/chargingSessionInfoPayload"
20 }
21 },
22 "required": [
23 "type",
24 "kind",
25 "payload"
26 ],
27 "definitions": {
28 "chargingSessionInfoPayload": {
29 "type": "object",
30 "properties": {
31 "chargingProfileMaxPowerLimitWatts": {
32 "$ref": "#/definitions/chargingProfileMaxPowerLimitWatts"
33 },
34 "timeToFullSocSeconds": {
35 "$ref": "#/definitions/timeToFullSocSeconds"
36 },
37 "evMinVoltageVolts": {
38 "$ref": "#/definitions/evMinVoltageVolts"
39 },
40 "evMaxVoltageVolts": {
41 "$ref": "#/definitions/evMaxVoltageVolts"
42 },
43 "evMinCurrentAmperes": {
44 "$ref": "#/definitions/evMinCurrentAmperes"
45 },
46 "evMaxCurrentAmperes": {
47 "$ref": "#/definitions/evMaxCurrentAmperes"
48 },
49 "evMinPowerWatts": {
50 "$ref": "#/definitions/evMinPowerWatts"
51 },
52 "evMaxPowerWatts": {
53 "$ref": "#/definitions/evMaxPowerWatts"
54 },
55 "evMinDischargeCurrentAmperes": {
56 "$ref": "#/definitions/evMinDischargeCurrentAmperes"
57 },
58 "evMaxDischargeCurrentAmperes": {
59 "$ref": "#/definitions/evMaxDischargeCurrentAmperes"
60 },
61 "evMinDischargePowerWatts": {
62 "$ref": "#/definitions/evMinDischargePowerWatts"
63 },
64 "evMaxDischargePowerWatts": {
65 "$ref": "#/definitions/evMaxDischargePowerWatts"
66 },
67 "chargeMode": {
68 "$ref": "#/definitions/chargeMode"
69 }
70 }
71 },
72 "chargingProfileMaxPowerLimitWatts": {
73 "type": "number",
74 "minimum": 0,
75 "maximum": 2147483647
76 },
77 "timeToFullSocSeconds": {
78 "type": "number",
79 "minimum": 0,
80 "maximum": 2147483647
81 },
1.8 of 2022-10-01 Power Electronics Protocol over WebSocket
PEP-WS
Networking and Application Protocol Requirements
53 / 54
82 "evMinVoltageVolts": {
83 "type": "number",
84 "minimum": 0,
85 "maximum": 2147483647
86 },
87 "evMaxVoltageVolts": {
88 "type": "number",
89 "minimum": 0,
90 "maximum": 2147483647
91 },
92 "evMinCurrentAmperes": {
93 "type": "number",
94 "minimum": 0,
95 "maximum": 2147483647
96 },
97 "evMaxCurrentAmperes": {
98 "type": "number",
99 "minimum": 0,
100 "maximum": 2147483647
101 },
102 "evMinPowerWatts": {
103 "type": "number",
104 "minimum": 0,
105 "maximum": 2147483647
106 },
107 "evMaxPowerWatts": {
108 "type": "number",
109 "minimum": 0,
110 "maximum": 2147483647
111 },
112 "evMinDischargeCurrentAmperes": {
113 "type": "number",
114 "minimum": -2147483647,
115 "maximum": 0
116 },
117 "evMaxDischargeCurrentAmperes": {
118 "type": "number",
119 "minimum": -2147483647,
120 "maximum": 0
121 },
122 "evMinDischargePowerWatts": {
123 "type": "number",
124 "minimum": -2147483647,
125 "maximum": 0
126 },
127 "evMaxDischargePowerWatts": {
128 "type": "number",
129 "minimum": -2147483647,
130 "maximum": 0
131 },
132 "chargeMode": {
133 "type": "string",
134 "enum": [
135 "scheduled",
136 "dynamic",
137 "dynamicBpt"
138 ]
139 }
140 }
141 }