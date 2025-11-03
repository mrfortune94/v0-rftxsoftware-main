"""
Android-adapted BMW Flasher
Modified version of RFTX_FLASHER.py for Android compatibility.
"""

import os
import time
import logging
import struct
from typing import List, Dict, Optional, Callable, Any
from kivy.utils import platform

if platform == 'android':
    from android_usb_serial import create_serial, get_usb_devices
else:
    # Desktop testing fallback
    import serial
    import serial.tools.list_ports

logger = logging.getLogger('RFTX.Flasher')

# Import all constants from original RFTX_FLASHER.py
CAN_ID_REQUEST = 0x6F1
CAN_ID_RESPONSE = 0x6F9

KWP_START_DIAGNOSTIC_SESSION = 0x10
KWP_ECU_RESET = 0x11
KWP_CLEAR_DIAGNOSTIC_INFORMATION = 0x14
KWP_READ_DTC_BY_STATUS = 0x18
KWP_READ_ECU_IDENTIFICATION = 0x1A
KWP_READ_DATA_BY_LOCAL_ID = 0x21
KWP_SECURITY_ACCESS = 0x27
KWP_WRITE_MEMORY_BY_ADDRESS = 0x3D
KWP_TESTER_PRESENT = 0x3E
KWP_READ_MEMORY_BY_ADDRESS = 0x23

UDS_DIAGNOSTIC_SESSION_CONTROL = 0x10
UDS_ECU_RESET = 0x11
UDS_CLEAR_DTC = 0x14
UDS_READ_DTC = 0x19
UDS_READ_DATA_BY_IDENTIFIER = 0x22
UDS_READ_MEMORY_BY_ADDRESS = 0x23
UDS_SECURITY_ACCESS = 0x27
UDS_WRITE_DATA_BY_IDENTIFIER = 0x2E
UDS_ROUTINE_CONTROL = 0x31
UDS_REQUEST_DOWNLOAD = 0x34
UDS_TRANSFER_DATA = 0x36
UDS_REQUEST_TRANSFER_EXIT = 0x37
UDS_WRITE_MEMORY_BY_ADDRESS = 0x3D
UDS_TESTER_PRESENT = 0x3E

POSITIVE_RESPONSE = 0x40
NEGATIVE_RESPONSE = 0x7F

NRC_RESPONSE_PENDING = 0x78

SESSION_DEFAULT = 0x01
SESSION_PROGRAMMING = 0x02
SESSION_EXTENDED = 0x03

SECURITY_LEVEL_PROGRAMMING = 0x01

ROUTINE_ERASE_MEMORY_SECTOR = 0xFF02

# ECU memory maps
ECU_MEMORY_MAPS = {
    "MSD80": {
        "flash_start": 0x800000,
        "flash_size": 0x100000,
        "block_size": 0x1000,
        "sectors": [
            {"name": "Bootloader", "start": 0x800000, "size": 0x10000, "protected": True},
            {"name": "Calibration", "start": 0x810000, "size": 0x40000, "protected": False},
            {"name": "Program", "start": 0x850000, "size": 0xB0000, "protected": True}
        ],
        "protocol": "KWP2000",
        "security_algorithm": "xor",
        "seed_key_length": 2,
        "transfer_size": 0x200,
        "erase_required": True
    },
    "MEVD17.2": {
        "flash_start": 0x800000,
        "flash_size": 0x200000,
        "block_size": 0x1000,
        "sectors": [
            {"name": "Bootloader", "start": 0x800000, "size": 0x10000, "protected": True},
            {"name": "Calibration", "start": 0x810000, "size": 0x80000, "protected": False},
            {"name": "Program", "start": 0x890000, "size": 0x170000, "protected": True}
        ],
        "protocol": "UDS",
        "security_algorithm": "crc",
        "seed_key_length": 4,
        "transfer_size": 0x800,
        "erase_required": True
    }
}

DEFAULT_MEMORY_MAP = {
    "flash_start": 0x800000,
    "flash_size": 0x100000,
    "block_size": 0x1000,
    "sectors": [
        {"name": "Bootloader", "start": 0x800000, "size": 0x10000, "protected": True},
        {"name": "Calibration", "start": 0x810000, "size": 0x40000, "protected": False},
        {"name": "Program", "start": 0x850000, "size": 0xB0000, "protected": True}
    ],
    "protocol": "KWP2000",
    "security_algorithm": "xor",
    "seed_key_length": 2,
    "transfer_size": 0x200,
    "erase_required": True
}


class ISOTPHandler:
    """ISO-TP protocol handler for CAN communication."""
    
    def __init__(self, port, tx_id: int = CAN_ID_REQUEST, rx_id: int = CAN_ID_RESPONSE):
        self.port = port
        self.tx_id = tx_id
        self.rx_id = rx_id
        self.timeout = 5.0
        self.fc_timeout = 1.0
        self.st_min = 0
        self.block_size = 0
        
    def send(self, data: bytes) -> Optional[bytes]:
        """Send data using ISO-TP protocol."""
        if len(data) <= 7:
            return self._send_single_frame(data)
        else:
            return self._send_multi_frame(data)
    
    def _send_single_frame(self, data: bytes) -> Optional[bytes]:
        """Send single frame."""
        frame = bytes([0x00 | len(data)]) + data
        if len(frame) < 8:
            frame += b'\x00' * (8 - len(frame))
        self._send_can_frame(self.tx_id, frame)
        return self._receive_isotp()
    
    def _send_multi_frame(self, data: bytes) -> Optional[bytes]:
        """Send multi-frame message."""
        data_length = len(data)
        first_frame = bytes([0x10 | ((data_length >> 8) & 0x0F), data_length & 0xFF]) + data[:6]
        self._send_can_frame(self.tx_id, first_frame)
        
        fc_frame = self._receive_can_frame(self.rx_id, timeout=self.fc_timeout)
        if not fc_frame or len(fc_frame) < 3 or fc_frame[0] != 0x30:
            logger.error("No valid flow control received")
            return None
            
        self.block_size = fc_frame[1]
        self.st_min = fc_frame[2]
        
        sequence_number = 1
        data_index = 6
        
        while data_index < data_length:
            if self.st_min <= 127:
                time.sleep(self.st_min / 1000.0)
            elif self.st_min >= 0xF1 and self.st_min <= 0xF9:
                time.sleep((self.st_min - 0xF0) * 100 / 1000000.0)
            
            remaining = data[data_index:data_index+7]
            consecutive_frame = bytes([0x20 | (sequence_number & 0x0F)]) + remaining
            
            if len(consecutive_frame) < 8:
                consecutive_frame += b'\x00' * (8 - len(consecutive_frame))
            
            self._send_can_frame(self.tx_id, consecutive_frame)
            
            sequence_number = (sequence_number + 1) & 0x0F
            data_index += 7
            
            if self.block_size != 0 and sequence_number % self.block_size == 0 and data_index < data_length:
                fc_frame = self._receive_can_frame(self.rx_id, timeout=self.fc_timeout)
                if not fc_frame or len(fc_frame) < 3 or fc_frame[0] != 0x30:
                    logger.error("No valid flow control during consecutive frames")
                    return None
                self.block_size = fc_frame[1]
                self.st_min = fc_frame[2]
        
        return self._receive_isotp()
    
    def _receive_isotp(self) -> Optional[bytes]:
        """Receive ISO-TP message."""
        frame = self._receive_can_frame(self.rx_id, timeout=self.timeout)
        if not frame:
            logger.error("No response received")
            return None
            
        frame_type = frame[0] & 0xF0
        
        if frame_type == 0x00:
            length = frame[0] & 0x0F
            return frame[1:1+length]
            
        elif frame_type == 0x10:
            length = ((frame[0] & 0x0F) << 8) | frame[1]
            response_data = bytearray(frame[2:8])
            
            fc_frame = bytes([0x30, 0, 0]) + b'\x00' * 5
            self._send_can_frame(self.tx_id, fc_frame)
            
            expected_sequence = 1
            
            while len(response_data) < length:
                cf_frame = self._receive_can_frame(self.rx_id, timeout=self.timeout)
                if not cf_frame:
                    logger.error("No consecutive frame received")
                    return None
                    
                if (cf_frame[0] & 0xF0) != 0x20:
                    logger.error(f"Invalid consecutive frame: {cf_frame.hex()}")
                    return None
                    
                sequence = cf_frame[0] & 0x0F
                if sequence != expected_sequence:
                    logger.error(f"Wrong sequence: expected {expected_sequence}, got {sequence}")
                    return None
                    
                response_data.extend(cf_frame[1:8])
                expected_sequence = (expected_sequence + 1) & 0x0F
            
            return bytes(response_data[:length])
        
        else:
            logger.error(f"Unexpected frame type: {frame_type:02X}")
            return None
    
    def _send_can_frame(self, can_id: int, data: bytes) -> None:
        """Send CAN frame."""
        can_frame = struct.pack(">I", can_id) + bytes([len(data)]) + data
        self.port.write(can_frame)
        self.port.flush()
        
    def _receive_can_frame(self, expected_id: int = None, timeout: float = None) -> Optional[bytes]:
        """Receive CAN frame."""
        if timeout is None:
            timeout = self.timeout
            
        original_timeout = self.port.timeout
        self.port.timeout = timeout
        
        try:
            header = self.port.read(5)
            if len(header) != 5:
                return None
                
            can_id = struct.unpack(">I", header[:4])[0]
            dlc = header[4]
            
            if expected_id is not None and can_id != expected_id:
                return None
                
            data = self.port.read(dlc)
            if len(data) != dlc:
                return None
                
            return data
            
        finally:
            self.port.timeout = original_timeout


class BMWFlasher:
    """BMW ECU Flasher for Android."""
    
    def __init__(self, port_name=None):
        self.port_name = port_name
        self.port = None
        self.isotp = None
        self.connected = False
        self.protocol = None
        self.security_level = 0
        self.session_type = SESSION_DEFAULT
        self.vin = None
        self.ecu_id = None
        self.sw_version = None
        self.hw_version = None
        self.ecu_type = None
        self.ecu_memory_map = None
        self.in_bootloader = False
        self.last_activity = 0
        
    def find_available_ports(self) -> List[str]:
        """Find available ports/devices."""
        if platform == 'android':
            devices = get_usb_devices()
            return [f"{d['name']}" for d in devices]
        else:
            ports = []
            for port in serial.tools.list_ports.comports():
                if "USB" in port.description:
                    ports.append(port.device)
            return ports
    
    def connect(self, port_name: str = None) -> bool:
        """Connect to ECU."""
        if port_name:
            self.port_name = port_name
            
        try:
            if platform == 'android':
                devices = get_usb_devices()
                if not devices:
                    logger.error("No USB devices found")
                    return False
                # Use first device for now
                device = devices[0]['device']
                self.port = create_serial(device, baudrate=500000, timeout=1.0)
            else:
                # Desktop testing
                import serial
                self.port = serial.Serial(
                    port=self.port_name,
                    baudrate=500000,
                    timeout=1.0
                )
            
            self.isotp = ISOTPHandler(self.port)
            
            if not self._initialize_communication():
                self.port.close()
                self.port = None
                self.isotp = None
                return False
                
            self.connected = True
            logger.info(f"Connected to ECU")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting: {e}")
            if self.port:
                try:
                    self.port.close()
                except:
                    pass
            self.port = None
            self.isotp = None
            return False
    
    def _initialize_communication(self) -> bool:
        """Initialize communication."""
        logger.info("Trying UDS protocol...")
        if self._try_uds_communication():
            self.protocol = "UDS"
            logger.info("UDS protocol detected")
            return True
            
        logger.info("Trying KWP2000 protocol...")
        if self._try_kwp_communication():
            self.protocol = "KWP2000"
            logger.info("KWP2000 protocol detected")
            return True
            
        logger.error("Failed to establish communication")
        return False
    
    def _try_uds_communication(self) -> bool:
        """Try UDS protocol."""
        response = self._send_uds_command(UDS_TESTER_PRESENT, [0x00])
        if response and response[0] == UDS_TESTER_PRESENT + POSITIVE_RESPONSE:
            return True
        response = self._send_uds_command(UDS_DIAGNOSTIC_SESSION_CONTROL, [SESSION_DEFAULT])
        if response and response[0] == UDS_DIAGNOSTIC_SESSION_CONTROL + POSITIVE_RESPONSE:
            return True
        return False
    
    def _try_kwp_communication(self) -> bool:
        """Try KWP2000 protocol."""
        response = self._send_kwp_command(KWP_TESTER_PRESENT, [0x00])
        if response and response[0] == KWP_TESTER_PRESENT + POSITIVE_RESPONSE:
            return True
        response = self._send_kwp_command(KWP_START_DIAGNOSTIC_SESSION, [0x81])
        if response and response[0] == KWP_START_DIAGNOSTIC_SESSION + POSITIVE_RESPONSE:
            return True
        return False
    
    def _send_uds_command(self, service_id: int, data: List[int]) -> Optional[bytes]:
        """Send UDS command."""
        if not self.port or not self.isotp:
            return None
        self.last_activity = time.time()
        message = bytes([service_id]) + bytes(data)
        try:
            response = self.isotp.send(message)
            if response and len(response) >= 3 and response[0] == NEGATIVE_RESPONSE:
                if response[2] == NRC_RESPONSE_PENDING:
                    for _ in range(10):
                        time.sleep(0.1)
                        response = self.isotp._receive_isotp()
                        if not response or response[0] != NEGATIVE_RESPONSE or response[2] != NRC_RESPONSE_PENDING:
                            break
            return response
        except Exception as e:
            logger.error(f"Error sending UDS command: {e}")
            return None
    
    def _send_kwp_command(self, service_id: int, data: List[int]) -> Optional[bytes]:
        """Send KWP2000 command."""
        if not self.port or not self.isotp:
            return None
        self.last_activity = time.time()
        message = bytes([service_id]) + bytes(data)
        try:
            return self.isotp.send(message)
        except Exception as e:
            logger.error(f"Error sending KWP command: {e}")
            return None
    
    def disconnect(self):
        """Disconnect from ECU."""
        if self.port:
            try:
                self.port.close()
            except:
                pass
        self.port = None
        self.isotp = None
        self.connected = False
        logger.info("Disconnected")
    
    def read_ecu_info(self) -> Dict:
        """Read ECU information."""
        if not self.connected and not self.connect():
            raise ConnectionError("Could not connect to ECU")
        
        ecu_info = {}
        
        if self.protocol == "KWP2000":
            response = self._send_kwp_command(KWP_READ_ECU_IDENTIFICATION, [0x90])
            if response and response[0] == KWP_READ_ECU_IDENTIFICATION + POSITIVE_RESPONSE:
                self.vin = response[2:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['vin'] = self.vin
                
            response = self._send_kwp_command(KWP_READ_ECU_IDENTIFICATION, [0x92])
            if response and response[0] == KWP_READ_ECU_IDENTIFICATION + POSITIVE_RESPONSE:
                self.ecu_id = response[2:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['ecu_id'] = self.ecu_id
                
            response = self._send_kwp_command(KWP_READ_ECU_IDENTIFICATION, [0x94])
            if response and response[0] == KWP_READ_ECU_IDENTIFICATION + POSITIVE_RESPONSE:
                self.sw_version = response[2:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['sw_version'] = self.sw_version
                
            response = self._send_kwp_command(KWP_READ_ECU_IDENTIFICATION, [0x93])
            if response and response[0] == KWP_READ_ECU_IDENTIFICATION + POSITIVE_RESPONSE:
                self.hw_version = response[2:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['hw_version'] = self.hw_version
        else:
            response = self._send_uds_command(UDS_READ_DATA_BY_IDENTIFIER, [0xF1, 0x90])
            if response and response[0] == UDS_READ_DATA_BY_IDENTIFIER + POSITIVE_RESPONSE:
                self.vin = response[3:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['vin'] = self.vin
                
            response = self._send_uds_command(UDS_READ_DATA_BY_IDENTIFIER, [0xF1, 0x8A])
            if response and response[0] == UDS_READ_DATA_BY_IDENTIFIER + POSITIVE_RESPONSE:
                self.ecu_id = response[3:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['ecu_id'] = self.ecu_id
                
            response = self._send_uds_command(UDS_READ_DATA_BY_IDENTIFIER, [0xF1, 0x89])
            if response and response[0] == UDS_READ_DATA_BY_IDENTIFIER + POSITIVE_RESPONSE:
                self.sw_version = response[3:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['sw_version'] = self.sw_version
                
            response = self._send_uds_command(UDS_READ_DATA_BY_IDENTIFIER, [0xF1, 0x91])
            if response and response[0] == UDS_READ_DATA_BY_IDENTIFIER + POSITIVE_RESPONSE:
                self.hw_version = response[3:].decode('ascii', errors='ignore').strip('\x00')
                ecu_info['hw_version'] = self.hw_version
        
        if self.ecu_id:
            self.ecu_type = self._determine_ecu_type(self.ecu_id)
            ecu_info['ecu_type'] = self.ecu_type
            self.ecu_memory_map = ECU_MEMORY_MAPS.get(self.ecu_type, DEFAULT_MEMORY_MAP)
            
        self.in_bootloader = False
        ecu_info['in_bootloader'] = self.in_bootloader
        
        logger.info(f"ECU Info: VIN={self.vin}, Type={self.ecu_type}")
        return ecu_info
    
    def _determine_ecu_type(self, ecu_id: str) -> str:
        """Determine ECU type."""
        ecu_id = ecu_id.upper()
        if "MSD80" in ecu_id:
            return "MSD80"
        elif "MEVD17.2" in ecu_id:
            return "MEVD17.2"
        return "MSD80"
    
    # Include simplified versions of flash_ecu, backup_ecu, read_dtcs, clear_dtcs, reset_ecu
    # (Keeping the same logic but adapted for Android)
    
    def flash_ecu(self, flash_file: str, progress_callback: Callable = None) -> bool:
        """Flash ECU (simplified for Android)."""
        logger.info(f"Flash operation: {flash_file}")
        # Implement full flashing logic here (same as original but with Android compatibility)
        raise NotImplementedError("Full flash implementation needed")
    
    def backup_ecu(self, backup_path: str = None, progress_callback: Callable = None) -> str:
        """Backup ECU (simplified for Android)."""
        logger.info("Backup operation")
        raise NotImplementedError("Full backup implementation needed")
    
    def read_dtcs(self) -> List[Dict]:
        """Read DTCs."""
        if not self.connected:
            raise ConnectionError("Not connected")
        
        dtcs = []
        if self.protocol == "KWP2000":
            response = self._send_kwp_command(KWP_READ_DTC_BY_STATUS, [0x00])
            if response and response[0] == KWP_READ_DTC_BY_STATUS + POSITIVE_RESPONSE:
                for i in range(2, len(response), 3):
                    if i + 2 < len(response):
                        status = response[i]
                        dtc_code = (response[i+1] << 8) | response[i+2]
                        dtcs.append({
                            "code": dtc_code,
                            "text": f"P{dtc_code:04X}",
                            "status": status
                        })
        else:
            response = self._send_uds_command(UDS_READ_DTC, [0x02, 0xFF])
            if response and response[0] == UDS_READ_DTC + POSITIVE_RESPONSE:
                for i in range(3, len(response), 4):
                    if i + 3 < len(response):
                        dtc_code = (response[i] << 16) | (response[i+1] << 8) | response[i+2]
                        status = response[i+3]
                        dtc_type = "P" if response[i] & 0xC0 == 0x00 else "C"
                        dtcs.append({
                            "code": dtc_code,
                            "text": f"{dtc_type}{dtc_code:06X}",
                            "status": status
                        })
        
        logger.info(f"Read {len(dtcs)} DTCs")
        return dtcs
    
    def clear_dtcs(self) -> bool:
        """Clear DTCs."""
        if not self.connected:
            raise ConnectionError("Not connected")
        
        if self.protocol == "KWP2000":
            response = self._send_kwp_command(KWP_CLEAR_DIAGNOSTIC_INFORMATION, [0xFF, 0xFF, 0xFF])
            return response and response[0] == KWP_CLEAR_DIAGNOSTIC_INFORMATION + POSITIVE_RESPONSE
        else:
            response = self._send_uds_command(UDS_CLEAR_DTC, [0xFF, 0xFF, 0xFF])
            return response and response[0] == UDS_CLEAR_DTC + POSITIVE_RESPONSE
    
    def reset_ecu(self) -> bool:
        """Reset ECU."""
        if not self.connected:
            raise ConnectionError("Not connected")
        
        if self.protocol == "KWP2000":
            self._send_kwp_command(KWP_ECU_RESET, [0x01])
        else:
            self._send_uds_command(UDS_ECU_RESET, [0x01])
        return True
