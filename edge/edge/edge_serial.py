import binascii
import serial

DEVICE = '/dev/ttyACM0'

_SECRET = b"thisisasmallstepforsecurity!"

class EdgeSerial:
    def __init__(self, device):
        self._device = device
        self.serial = serial.Serial(device, 9600)

    def send_status(self, uid, status):
        msg = uid + b'\x00\x00\x00' + (b'\xda' if status else b'\x00')
        print(msg)
        checksum = binascii.crc32(msg + _SECRET).to_bytes(4, 'big')
        self.serial.write(msg)
        self.serial.write(b'\n')
        self.serial.write(checksum)
        self.serial.write(b'\n')

        print(self.serial.readline())
