import binascii
import socket
import time

import util

_SECRET = b"thisisasmallstepforsecurity!"

class TCPClient:
    def __init__(self, remote, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._remote = remote
        self._port = port
        self.running = False

    def _is_server_alive(self):
        try:
            self._socket.getpeername()
            return True
        except:
            return False

    def send_message(self, data):
        self._send_message(data)

    def _send_message(self, data):
        msg = data
        self._socket.sendall(msg)
        self._socket.sendall(bytearray([0x00, 0x00, 0x00])) # handle message ending

    def connect(self):
        try:
            self._socket.connect((self._remote, self._port))
        except Exception as e:
            print(e)
            print("Failed to connect, retrying in 10 seconds...")

            time.sleep(10)
            connect()
            return

        self.running = True

class SecureTCPClient(TCPClient):
    def send_message(self, data):
        check = binascii.crc32(data + _SECRET).to_bytes(4, 'big') # sign our message
        print("UID: ", end='')
        util.print_hex(data)
        print("Check: ", end='')
        util.print_hex(check)

        super().send_message(data)
        super().send_message(check)
