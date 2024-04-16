import binascii
import socket

import util

_SECRET = b"thisisasmallstepforsecurity!"

class TCPServer:
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port
        self.running = False

    def start_server(self):
        self._socket.bind((self._host, self._port))
        self._socket.listen(1) # we only have one iot node so for the purpose of the practical we only accept one connection at a time
        print("Now listening and accepting connections on {}:{}".format(self._host, self._port))

        self.running = True
        while self.running:
            client_socket, client_address = self._socket.accept()
            self._handleConnection(client_socket)

            if self._is_client_alive(client_socket):
                client_socket.close() # safely close if it isn't closed

    def _is_client_alive(self, client):
        try:
            client.getpeername()
            return True
        except:
            return False

    def _handleMessage(self, msg):
        raise NotImplementedError
        pass

    def _handleConnection(self, client):
        buffer = b''
        while True:
            try:
                chunk = client.recv(1024) # 1024 buffer receiving at a time
                if not chunk:
                    continue
                buffer += chunk
            except:
                print("Failed to read data closing connection")
                return
            
            if b'\n' in buffer: #NOTE: May need to potentially process multiple messages in a single buffer but not sure yet
                self._handleMessage(buffer[0:len(buffer)-1])
                
                buffer = b'' # clear buffer ofc
                continue

class SecureTCPServer(TCPServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self._stored_msg = None

    def handleMessage(self, message):
        raise NotImplementedError
        pass

    def _verifyMessage(data, checksum):
        check = binascii.crc32(data + _SECRET)
        return check == checksum

    def _handleMessage(self, msg):
        util.print_hex(msg)

        if not self._stored_msg:
            self._stored_msg = msg
            return
        res = _verifyMessage(self._stored_msg, msg)
        process = self._stored_msg
        self._stored_msg = None
        if not res:
            return # discard message silently (someone is most likely trying to mitm

        self.handleMessage(self.process)
