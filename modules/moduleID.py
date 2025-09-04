def build_identifier(protocol, monitor_addr, module_addr, prod_date=0, serial_lower=0):
    """
    Build 29-bit identifier into a single integer (CAN ID).
    
    Bit mapping:
      28:25 -> protocol (4 bits)
      24:21 -> monitor address (4 bits)
      20:14 -> module address (7 bits)
      13:9  -> production date (5 bits)
      8:0   -> serial number lower part (9 bits)
    """
    identifier = 0

    identifier |= (protocol & 0xF) << 25        # 4 bits
    identifier |= (monitor_addr & 0xF) << 21    # 4 bits
    identifier |= (module_addr & 0x7F) << 14    # 7 bits
    identifier |= (prod_date & 0x1F) << 9       # 5 bits
    identifier |= (serial_lower & 0x1FF)        # 9 bits

    return identifier

# Example: Protocol=0x1, Monitor=0x1, Module IDs 0x01..0x0F
if __name__ == "__main__":
    protocol = 0x01
    monitor = 0x01

    for module in range(0x01, 0x10):  # 0x01 to 0x0F
        can_id = build_identifier(protocol, monitor, module)
        print(f"Module {module:02X} -> CAN ID: 0x{can_id:08X}")
