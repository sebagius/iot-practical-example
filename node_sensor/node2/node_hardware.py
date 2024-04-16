from pn532pi import Pn532, pn532
from pn532pi import Pn532Spi
from pn532pi import EmulateTag


class NodeHardware:
    def __init__(self):
        PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
        self.nfc = Pn532(PN532_SPI)

    def setup(self):
        self.nfc.begin()
        v = self.nfc.getFirmwareVersion()
        if not v:
            print("Not connected to PN532")
            exit()

        self.nfc.SAMConfig()

    def get_next_uid(self):
        s, u = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
        if len(u) == 0:
            return None
        return u
