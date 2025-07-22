"""
Error handling module for PECC system.
Centralized error detection, reporting, and recovery logic.
"""

from pecc.utils import log_error

class PECCError(Exception):
    """Base class for PECC errors."""
    pass

class ProtocolError(PECCError):
    pass

class CANError(PECCError):
    pass

class HardwareError(PECCError):
    pass

# Example error reporting function

def report_error(error: Exception):
    log_error(f"Error reported: {error}")
    # Extend with error category, details, recovery, etc.
