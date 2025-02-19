from time import sleep
from threading import Thread
from multiprocessing import Process
from xsocket import xsocket, TCP, UDP
from xsocket import STRAIGHT, THREAD, PROCESS, MULTIPLEX, MULTIPLEX_THREAD, MULTIPLEX_PROCESS
from socket import socket, AF_INET, SOCK_DGRAM
# Possible execution modes to test
EXEC_MODES = [STRAIGHT, THREAD, PROCESS, MULTIPLEX, MULTIPLEX_THREAD, MULTIPLEX_PROCESS]

# Test addresses & ports
TCP_ADDR, TCP_PORT = "127.0.0.1", 5000
UDP_ADDR, UDP_PORT = "127.0.0.1", 6000

# TCP Server
def run_tcp_server(io_mode):
    server = xsocket(address=TCP_ADDR, port=TCP_PORT, proto=TCP, io=io_mode)

    def handle_client(sock):
        data = sock.recv(1024)
        print(f"TCP Server [{io_mode}] received: {data.decode()}")
        sock.sendall(b"ACK from TCP Server")
        sock.close()

    server.tcp_passage = handle_client
    server.run()

# TCP Client
def run_tcp_client():
    sleep(1)  # Ensure the server starts first
    client = socket()
    client.connect((TCP_ADDR, TCP_PORT))
    client.sendall(b"Hello, TCP Server!")
    response = client.recv(1024)
    print(f"TCP Client received: {response.decode()}")
    client.close()

# UDP Server
def run_udp_server(io_mode):
    server = xsocket(address=UDP_ADDR, port=UDP_PORT, proto=UDP, io=io_mode)

    def handle_message(data, addr):
        print(f"UDP Server [{io_mode}] received from {addr}: {data.decode()}")

    server.udp_passage = handle_message
    server.running = True
    server.run()

# UDP Client
def run_udp_client():
    sleep(1)
    client = socket(AF_INET, SOCK_DGRAM)
    client.sendto(b"Hello, UDP Server!", (UDP_ADDR, UDP_PORT))

# Run tests for all execution modes
success = 0
for io_mode in EXEC_MODES:
    print(f"\n=== Testing TCP with io_mode={io_mode} ===")
    tcp_server_thread = Thread(target=run_tcp_server, args=(io_mode,), daemon=True)
    tcp_server_thread.start()
    run_tcp_client()
    success += 1
    print(f'SUCCESS: {success}\n')

    print(f"\n=== Testing UDP with io_mode={io_mode} ===")
    udp_server_thread = Thread(target=run_udp_server, args=(io_mode,), daemon=True)
    udp_server_thread.start()
    run_udp_client()
    success += 1
    print(f'SUCCESS: {success}')

    sleep(2)  # Allow servers to process requests before moving to the next mode