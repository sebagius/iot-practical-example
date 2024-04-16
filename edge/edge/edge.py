import edge_server

HOST_ADDR = edge_server.HOST_ADDR
HOST_PORT = edge_server.HOST_PORT

def main():
    test = edge_server.EdgeServer(HOST_ADDR, HOST_PORT)
    test.start_server()


# Best way to run program only once
if __name__ == "__main__":
    main()
