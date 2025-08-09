import websockets

class Versions:
    WEBSOCKET_OLD = False  # Class variable

    @classmethod
    def detect_websocket_version(cls):
        """Detects installed websocket version and sets WEBSOCKET_OLD automatically"""
        try:
            version_tuple = tuple(map(int, websockets.__version__.split(".")))
            cls.WEBSOCKET_OLD = version_tuple <= (10, 1)
        except Exception:
            cls.WEBSOCKET_OLD = False

    @classmethod
    def check_if_websocket_old(cls):
        return cls.WEBSOCKET_OLD

# Auto-detect on import
Versions.detect_websocket_version()
