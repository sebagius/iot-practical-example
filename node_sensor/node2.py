import time
import binascii
import socket

from pn532pi import Pn532, pn532
from pn532pi import Pn532Spi
from pn532pi import EmulateTag

PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
nfc = Pn532(PN532_SPI)

SERVER_ADDR = "172.16.69.1" # edge will always be the gateway
SERVER_PORT = 7343

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ourSecret = "thisisasmallstepforsecurity!"

attempted_con = False

def check_connection():
    global attempted_con
    try:
        client_socket.getpeername()
        attempted_con = False
        return
    except OSError:
        if attempted_con:
            time.sleep(1) # wait before retrying
        attempted_con = True
    try:
        client_socket.connect((SERVER_ADDR, SERVER_PORT))
    except ConnectionRefusedError:
        print("Connection refused, retrying in 10 seconds")
        time.sleep(10)
    check_connection() # keep checking until connection is made

def setup():
    check_connection()
    print("Successful connection to {}:{}".format(SERVER_ADDR, SERVER_PORT))
    nfc.begin()
    v = nfc.getFirmwareVersion()
    if not v:
        print("Not connected to PN532")
        exit()

    nfc.SAMConfig()

    print("Setup complete")

def loop():
    s, u = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
    if len(u) == 0:
        return
    print(''.join('{:02x}'.format(x) for x in u))
    check_connection()
    client_socket.sendall(u)
    client_socket.sendall('\n'.encode('utf8'))

setup()

while True:
    loop()
    time.sleep(1)
