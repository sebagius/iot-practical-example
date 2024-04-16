import node_client
import node_hardware
import time

REMOTE_ADDR = node_client.REMOTE_ADDR
REMOTE_PORT = node_client.REMOTE_PORT

def main():
    test = node_client.NodeClient(REMOTE_ADDR, REMOTE_PORT)
    test.connect()
    print("Now connected to {}:{}".format(REMOTE_ADDR, REMOTE_PORT))
    hardware = node_hardware.NodeHardware()
    hardware.setup()
    while True:
        uid = hardware.get_next_uid()
        if not uid:
            time.sleep(0.5) # constant scanning at 0.5 intervals
            continue
        test.send_uid(uid)
        time.sleep(2.5) # card found wait longer for next scan

# Best way to run program only once
if __name__ == "__main__":
    main()
