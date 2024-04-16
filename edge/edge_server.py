import tcpserver

HOST_ADDR = "172.16.69.1" # We only want to listen on the iot network not the optionally attached ethernet network
HOST_PORT = 7343

class EdgeServer(tcpserver.SecureTCPServer):
    def handleMessage(self, message):
        print(message) # we made it !!!!
        #TODO: check db, and send result over serial to arduino

