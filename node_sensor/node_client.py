import tcpclient
import util

REMOTE_ADDR = "172.16.69.1"
REMOTE_PORT = 7343

class NodeClient(tcpclient.SecureTCPClient):
    def send_uid(self, uid):
        if type(uid) is not bytearray:
            raise TypeError("{} not bytearray".format(type(uid)))
        super().send_message(uid)
