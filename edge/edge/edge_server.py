import tcpserver
import edge_serial
import edge_db

HOST_ADDR = "172.16.69.1" # We only want to listen on the iot network not the optionally attached ethernet network
HOST_PORT = 7343
DB_HOST = edge_db.DB_HOST_ADDR
DB_PORT = edge_db.DB_HOST_PORT

DEVICE = edge_serial.DEVICE

class EdgeServer(tcpserver.SecureTCPServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.edgeserial = edge_serial.EdgeSerial(DEVICE)
        self.edgedb = edge_db.EdgeDatabase(DB_HOST, DB_PORT)

    def handleMessage(self, message):
        self.edgedb.log(message)
        auth = self.edgedb.checkAuth(message)
        self.edgeserial.send_status(message, auth) # id and auth = true
        #TODO: check db, and send result over serial to arduino

