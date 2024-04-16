import tcpserver
import edge_serial

HOST_ADDR = "172.16.69.1" # We only want to listen on the iot network not the optionally attached ethernet network
HOST_PORT = 7343
DEVICE = edge_serial.DEVICE

class EdgeServer(tcpserver.SecureTCPServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.edgeserial = edge_serial.EdgeSerial(DEVICE)

    def handleMessage(self, message):
        print(message) # we made it !!!!

        self.edgeserial.send_uid(message)
        #TODO: check db, and send result over serial to arduino

