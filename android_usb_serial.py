"""
Android USB Serial Communication Module
Provides USB serial communication for Android devices using pyjnius.
"""

import logging
from kivy.utils import platform

logger = logging.getLogger('RFTX.USB')

if platform == 'android':
    from jnius import autoclass, cast
    from android import mActivity
    
    # Java classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    UsbManager = autoclass('android.hardware.usb.UsbManager')
    UsbDevice = autoclass('android.hardware.usb.UsbDevice')
    UsbDeviceConnection = autoclass('android.hardware.usb.UsbDeviceConnection')
    UsbInterface = autoclass('android.hardware.usb.UsbInterface')
    UsbEndpoint = autoclass('android.hardware.usb.UsbEndpoint')
    UsbConstants = autoclass('android.hardware.usb.UsbConstants')
    Intent = autoclass('android.content.Intent')
    PendingIntent = autoclass('android.app.PendingIntent')
    Context = autoclass('android.content.Context')
    
    # CDC ACM (USB Serial) constants
    USB_CLASS_CDC_DATA = 0x0A
    USB_CLASS_COMM = 0x02
    
    # Common K+DCAN adapter vendor/product IDs
    KDCAN_VENDORS = [
        0x0403,  # FTDI
        0x1A86,  # CH340
        0x067B,  # Prolific
        0x10C4,  # Silicon Labs
    ]


def get_usb_devices():
    """Get list of connected USB devices."""
    if platform != 'android':
        return []
        
    try:
        activity = PythonActivity.mActivity
        usb_manager = activity.getSystemService(Context.USB_SERVICE)
        
        device_list = usb_manager.getDeviceList()
        devices = []
        
        # Convert Java HashMap to Python list
        for device_name in device_list.keySet().toArray():
            device = device_list.get(device_name)
            
            devices.append({
                'name': device.getDeviceName(),
                'vendor_id': device.getVendorId(),
                'product_id': device.getProductId(),
                'device_class': device.getDeviceClass(),
                'device': device
            })
            
        logger.info(f"Found {len(devices)} USB devices")
        return devices
        
    except Exception as e:
        logger.error(f"Error getting USB devices: {e}")
        return []


def request_usb_permission(device):
    """Request permission to access USB device."""
    if platform != 'android':
        return False
        
    try:
        activity = PythonActivity.mActivity
        usb_manager = activity.getSystemService(Context.USB_SERVICE)
        
        if usb_manager.hasPermission(device):
            return True
            
        # Request permission
        permission_intent = PendingIntent.getBroadcast(
            activity,
            0,
            Intent("com.android.example.USB_PERMISSION"),
            0
        )
        
        usb_manager.requestPermission(device, permission_intent)
        
        # Note: This is asynchronous, need to wait for broadcast receiver
        # For simplicity, we'll check permission after a delay
        import time
        time.sleep(2)
        
        return usb_manager.hasPermission(device)
        
    except Exception as e:
        logger.error(f"Error requesting USB permission: {e}")
        return False


class AndroidUSBSerial:
    """Android USB Serial communication class."""
    
    def __init__(self, device=None, baudrate=500000, timeout=1.0):
        """Initialize USB serial connection."""
        self.device = device
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
        self.interface = None
        self.endpoint_in = None
        self.endpoint_out = None
        self.is_open = False
        
        if platform != 'android':
            raise RuntimeError("AndroidUSBSerial only works on Android")
            
    def open(self):
        """Open USB serial connection."""
        if self.is_open:
            return True
            
        try:
            activity = PythonActivity.mActivity
            usb_manager = activity.getSystemService(Context.USB_SERVICE)
            
            # Request permission if needed
            if not usb_manager.hasPermission(self.device):
                if not request_usb_permission(self.device):
                    logger.error("USB permission denied")
                    return False
                    
            # Open connection
            self.connection = usb_manager.openDevice(self.device)
            if not self.connection:
                logger.error("Failed to open USB device")
                return False
                
            # Get interface (usually interface 0 for serial devices)
            if self.device.getInterfaceCount() == 0:
                logger.error("No USB interfaces found")
                return False
                
            self.interface = self.device.getInterface(0)
            
            # Claim interface
            if not self.connection.claimInterface(self.interface, True):
                logger.error("Failed to claim USB interface")
                return False
                
            # Find endpoints
            for i in range(self.interface.getEndpointCount()):
                endpoint = self.interface.getEndpoint(i)
                
                if endpoint.getDirection() == UsbConstants.USB_DIR_IN:
                    self.endpoint_in = endpoint
                elif endpoint.getDirection() == UsbConstants.USB_DIR_OUT:
                    self.endpoint_out = endpoint
                    
            if not self.endpoint_in or not self.endpoint_out:
                logger.error("Failed to find USB endpoints")
                return False
                
            # Configure serial parameters (baudrate, etc.)
            self._configure_serial()
            
            self.is_open = True
            logger.info(f"USB serial opened: {self.device.getDeviceName()}")
            return True
            
        except Exception as e:
            logger.error(f"Error opening USB serial: {e}")
            return False
            
    def _configure_serial(self):
        """Configure serial parameters (baudrate, data bits, etc.)."""
        try:
            # FTDI-specific control requests
            # Set baudrate
            baudrate_value = int(3000000 / self.baudrate)
            
            self.connection.controlTransfer(
                0x40,  # Request type (vendor, out)
                0x03,  # Set baudrate
                baudrate_value & 0xFFFF,  # Value
                baudrate_value >> 16,  # Index
                None,  # Buffer
                0,  # Length
                1000  # Timeout
            )
            
            # Set data bits (8N1)
            self.connection.controlTransfer(
                0x40,  # Request type
                0x04,  # Set data
                0x0008,  # 8 data bits, no parity, 1 stop bit
                0,  # Index
                None,
                0,
                1000
            )
            
            # Set flow control (none)
            self.connection.controlTransfer(
                0x40,
                0x02,  # Set flow control
                0x0000,  # No flow control
                0,
                None,
                0,
                1000
            )
            
            logger.info(f"Serial configured: {self.baudrate} baud, 8N1")
            
        except Exception as e:
            logger.warning(f"Error configuring serial (may not be FTDI): {e}")
            
    def close(self):
        """Close USB serial connection."""
        if not self.is_open:
            return
            
        try:
            if self.connection and self.interface:
                self.connection.releaseInterface(self.interface)
                
            if self.connection:
                self.connection.close()
                
            self.is_open = False
            logger.info("USB serial closed")
            
        except Exception as e:
            logger.error(f"Error closing USB serial: {e}")
            
    def write(self, data):
        """Write data to USB serial."""
        if not self.is_open:
            raise IOError("USB serial not open")
            
        try:
            # Convert to byte array
            if isinstance(data, str):
                data = data.encode()
                
            # Write to endpoint
            bytes_written = self.connection.bulkTransfer(
                self.endpoint_out,
                data,
                len(data),
                int(self.timeout * 1000)
            )
            
            if bytes_written < 0:
                raise IOError("USB write failed")
                
            return bytes_written
            
        except Exception as e:
            logger.error(f"Error writing to USB: {e}")
            raise
            
    def read(self, size=1):
        """Read data from USB serial."""
        if not self.is_open:
            raise IOError("USB serial not open")
            
        try:
            # Create buffer
            buffer = bytearray(size)
            
            # Read from endpoint
            bytes_read = self.connection.bulkTransfer(
                self.endpoint_in,
                buffer,
                size,
                int(self.timeout * 1000)
            )
            
            if bytes_read < 0:
                return b''
                
            return bytes(buffer[:bytes_read])
            
        except Exception as e:
            logger.error(f"Error reading from USB: {e}")
            return b''
            
    def flush(self):
        """Flush output buffer."""
        # USB doesn't require explicit flushing
        pass
        
    @property
    def in_waiting(self):
        """Get number of bytes waiting to be read."""
        # Not easily available on Android USB, return 0
        return 0


class DesktopSerialWrapper:
    """Wrapper for desktop serial (for testing)."""
    
    def __init__(self, port, baudrate=500000, timeout=1.0):
        """Initialize desktop serial."""
        import serial
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )
        self.is_open = self.serial.is_open
        
    def open(self):
        """Open serial port."""
        if not self.serial.is_open:
            self.serial.open()
        self.is_open = self.serial.is_open
        return self.is_open
        
    def close(self):
        """Close serial port."""
        self.serial.close()
        self.is_open = False
        
    def write(self, data):
        """Write data."""
        return self.serial.write(data)
        
    def read(self, size=1):
        """Read data."""
        return self.serial.read(size)
        
    def flush(self):
        """Flush buffer."""
        self.serial.flush()
        
    @property
    def in_waiting(self):
        """Get bytes waiting."""
        return self.serial.in_waiting
        
    @property
    def timeout(self):
        """Get timeout."""
        return self.serial.timeout
        
    @timeout.setter
    def timeout(self, value):
        """Set timeout."""
        self.serial.timeout = value


def create_serial(port, baudrate=500000, timeout=1.0):
    """Create appropriate serial object for platform."""
    if platform == 'android':
        # Port should be a USB device object
        serial_obj = AndroidUSBSerial(port, baudrate, timeout)
        serial_obj.open()
        return serial_obj
    else:
        # Desktop testing
        return DesktopSerialWrapper(port, baudrate, timeout)
