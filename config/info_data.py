class InfoData:
    @staticmethod
    def get_gun_info(gun_id):
        gun_map = {
            "GUN1": InfoData.gun1_info_data,
            "GUN2": InfoData.gun2_info_data,
            "GUN3": InfoData.gun3_info_data,
            "GUN4": InfoData.gun4_info_data,
            "GUN5": InfoData.gun5_info_data,
            "GUN6": InfoData.gun6_info_data,
            "GUN7": InfoData.gun7_info_data,
            "GUN8": InfoData.gun8_info_data,
            "GUN9": InfoData.gun9_info_data,
            "GUN10": InfoData.gun10_info_data,
            "GUN11": InfoData.gun11_info_data,
            "GUN12": InfoData.gun12_info_data,
        }
        return gun_map.get(gun_id.upper(), {})
    gun1_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 32.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun2_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 33.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun3_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 34.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun4_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 35.0,
    "contactorsStatus": "closed",
    "isolationStatus": "valid",
    "operationalStatus": "operative"
    }
    gun5_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 36.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun6_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 37.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun7_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 38.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun8_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 39.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun9_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 40.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun10_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 41.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun11_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 42.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }
    gun12_info_data = {"measuredVoltage":  0,
    "measuredCurrent":  0,
    "drivenVoltage":  0,
    "drivenCurrent":  0,
    "temperature": 43.0,
    "contactorsStatus": "open",
    "isolationStatus": "invalid",
    "operationalStatus": "operative"
    }