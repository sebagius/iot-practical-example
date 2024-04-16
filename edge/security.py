import binascii

ourSecret = "thisisasmallstepforsecurity!"

def calculateChecksum(data):
    return binascii.crc32((data + ourSecret).encode('utf8')) # this is a lot easier in python than c lol

def verifyData(data, checksum):
    check = calculateChecksum(data)
    return check == checksum # so much easier *crying*
