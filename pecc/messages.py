# --- Protocol Message Processor ---
import json

class PEPWSMessageProcessor:
    REQUIRED_FIELDS = ["kind", "type"]

    @staticmethod
    def parse_message(raw):
        try:
            msg = json.loads(raw)
            for field in PEPWSMessageProcessor.REQUIRED_FIELDS:
                if field not in msg:
                    return None, f"Missing required field: {field}"
            return msg, None
        except Exception as e:
            return None, f"Invalid JSON: {e}"

    @staticmethod
    def validate_message(msg):
        # Add protocol-specific validation here
        # Example: check sequenceNumber for requests/responses
        if "sequenceNumber" in msg and not isinstance(msg["sequenceNumber"], int):
            return False, "sequenceNumber must be integer"
        return True, None

    @staticmethod
    def build_response(request_msg, payload=None, error=None):
        resp = {
            "kind": request_msg.get("kind"),
            "type": "response" if not error else "error",
            "sequenceNumber": request_msg.get("sequenceNumber"),
            "payload": payload if payload is not None else {},
        }
        if error:
            resp["errorDetails"] = error
        return json.dumps(resp)

    @staticmethod
    def build_info(kind, payload=None):
        return json.dumps({
            "kind": kind,
            "type": "info",
            "payload": payload if payload is not None else {},
        })
# Message builders and parsers for PEP-WS protocol

def build_configuration_request(seq):
    return {
        "type": "request",
        "kind": "configuration",
        "sequenceNumber": seq,
        "payload": {}
    }

def build_cable_check_request(seq, voltage):
    return {
        "type": "request",
        "kind": "cableCheck",
        "sequenceNumber": seq,
        "payload": {"voltage": voltage}
    }

def build_target_values_request(seq, voltage, current, soc, charging_state):
    return {
        "type": "request",
        "kind": "targetValues",
        "sequenceNumber": seq,
        "payload": {
            "targetVoltage": voltage,
            "targetCurrent": current,
            "batteryStateOfCharge": soc,
            "chargingState": charging_state
        }
    }

def build_contactors_status_request(seq, status):
    return {
        "type": "request",
        "kind": "contactorsStatus",
        "sequenceNumber": seq,
        "payload": {"contactorsStatus": status}
    }

def build_reset_request(seq):
    return {
        "type": "request",
        "kind": "reset",
        "sequenceNumber": seq,
        "payload": {}
    }

def build_get_input_request(seq, input_ids):
    return {
        "type": "request",
        "kind": "getInput",
        "sequenceNumber": seq,
        "payload": {"inputIdentifiers": input_ids}
    }

def build_set_output_request(seq, output_values):
    return {
        "type": "request",
        "kind": "setOutput",
        "sequenceNumber": seq,
        "payload": {"outputValues": output_values}
    }

def build_stop_charging_request(seq):
    return {
        "type": "request",
        "kind": "stopCharging",
        "sequenceNumber": seq,
        "payload": {}
    }