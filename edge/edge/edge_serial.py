import binascii
import serial

DEVICE = '/dev/ttyACM0'

_SECRET = b"thisisasmallstepforsecurity!"

class EdgeSerial:
    def __init__(self, device):
        self._device = device
        self.serial = serial.Serial(device, 9600)

    def send_uid(self, uid):
        checksum = binascii.crc32(uid + _SECRET).to_bytes(4, 'big')
        self.serial.write(uid)
        self.serial.write(b'\n')
        self.serial.write(checksum)
        self.serial.write(b'\n')

        print(self.serial.readline())
