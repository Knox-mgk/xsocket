# xsocket

`xsocket` is a lightweight and efficient networking module designed to simplify socket communication using **TCP** and **UDP** protocols.

## Features
- Supports both **TCP** and **UDP** protocols.
- Multiplexing with `MULTIPLEX_THREAD` for concurrent connections.
- Simple client-server implementation.
- Customizable socket options.

## Installation

Clone the repository and install the package:

```sh
git clone https://github.com/Knox-mgk/xsocket.git
cd xsocket
pip install .

If setuptools is missing, install it first:

pip install setuptools

How to Run

Running a TCP Server

from xsocket import xsocket, TCP, MULTIPLEX_THREAD

server = xsocket(address="127.0.0.1", port=5000, proto=TCP, io=MULTIPLEX_THREAD)

def handle_client(sock):
    data = sock.recv(1024)
    print(f"Received: {data.decode()}")
    sock.sendall(b"ACK from Server")
    sock.close()

server.tcp_passage = handle_client
server.running = True
server.run()

Running a TCP Client (Using socket)

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect(("127.0.0.1", 5000))
client.sendall(b"Hello, TCP Server!")
response = client.recv(1024)
print(f"Received: {response.decode()}")
client.close()

Running a UDP Server

from xsocket import xsocket, UDP, MULTIPLEX_THREAD

server = xsocket(address="127.0.0.1", port=6000, proto=UDP, io=MULTIPLEX_THREAD)

def handle_message(data, addr):
    print(f"Received from {addr}: {data.decode()}")

server.udp_passage = handle_message
server.running = True
server.run()

Running a UDP Client (Using socket)

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello, UDP Server!", ("127.0.0.1", 6000))

Updating the Repository

If you've updated the code on GitHub, users should run:

git pull origin main
pip install --upgrade .


License

This project is licensed under the MIT License.


---


