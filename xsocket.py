from socket import socket
from socket import AF_INET, AF_INET6
from socket import SOCK_STREAM, SOCK_DGRAM
from socket import IPPROTO_TCP, IPPROTO_UDP
from socket import SOL_SOCKET, SO_REUSEADDR 

from selectors import DefaultSelector as _selector
from threading import Thread as _thread
from multiprocessing import Process as _process


from selectors import EVENT_READ 


INET = AF_INET
INET6 = AF_INET6


TCP = (SOCK_STREAM, IPPROTO_TCP)
UDP = (SOCK_DGRAM, IPPROTO_UDP)

STRAIGHT = 3
PROCESS = 2
THREAD = 1
MULTIPLEX = 0
MULTIPLEX_THREAD = -1
MULTIPLEX_PROCESS = -2


class xsocket:

    def __init__(self, inet=INET, proto=TCP, address='', port=0, io=STRAIGHT):
        self.running = False
        self.inet = inet
        self.proto = proto
        self.address = (address, port)
        self.num_conn = None
        self.buff_size = 1024
        self.io = io

    def run(self):
        self.running = True
        self.server = socket(
            self.inet,
            self.proto[0],
            self.proto[1]
        )
        self.server.setsockopt(
            SOL_SOCKET,
            SO_REUSEADDR, 1
        )
        self.server.bind(self.address)
        self.structure()

    def structure(self):
        struct = self.tcp_engine if self.proto == TCP else self.udp_engine
        self.server.setblocking(False if self.io <= MULTIPLEX else True)
        struct()
        self.close()

    def tcp_engine(self):
        
        if self.num_conn == None:
            self.server.listen()
        else:
            self.server.listen(self.num_conn)

        if self.io in ( THREAD, PROCESS, STRAIGHT ):
            try:
                self.tcp_direct_engine()
            except KeyboardInterrupt:
                self.close()
        else:
            self.selector = _selector()
            self.selector.register(
                self.server,
                EVENT_READ,
                self.tcp_selector_engine
            )

            try:
                while True:
                    event = self.selector.select()

                    for key, mask in event:
                        func = key.data

                        if func == self.tcp_selector_engine:
                            self.tcp_selector_engine()
                        else:
                            func(key.fileobj)
                            
            except KeyboardInterrupt:
                self.close()

    def tcp_direct_engine(self):
        count = 0
        while self.running:
            sock, _ = self.server.accept()

            if self.io == THREAD:
                io = _thread(target=self.tcp_passage, args=(sock,))
                io.start()

            elif self.io == PROCESS:
                ip = _process(target=self.tcp_passage, args=(sock,))
                io.start()

            else:
                self.tcp_passage(sock)

            if self.num_conn is not None:
                count += 1

                if self.num_conn == count:
                    self.running = False
                    break

    def tcp_selector_engine(self):
        
        count = 0
        if self.running:
            sock, addr = self.server.accept()

            sock.setblocking(False)

            if self.io == MULTIPLEX_THREAD:
                io = _thread(target=self.tcp_passage, args=(sock,))
                io.start()

            elif self.io == MULTIPLEX_PROCESS:
                io = _process(target=self.tcp_passage, args=(sock,))
                io.start()

            else:
                self.selector.register(
                    sock,
                    EVENT_READ,
                    self.tcp_passage
                )

            if self.num_conn is not None:
                count += 1

                if self.num_conn == count:
                    self.running = False

    def tcp_passage(self, sock):
        pass

    def udp_engine(self):
        
        if self.io in ( THREAD, PROCESS, STRAIGHT ):
            try:
                self.udp_direct_engine()

            except KeyboardInterrupt:
                self.close()
        else:
            self.selector = _selector()
            self.selector.register(
                self.server,
                EVENT_READ,
                self.udp_selector_engine
            )

            try:
                while True:
                    event = self.selector.select()

                    for key, mask in event:
                        func = key.data

                        if func == self.udp_selector_engine:
                            self.udp_selector_engine()
                            
            except KeyboardInterrupt:
                self.close()

    def udp_direct_engine(self):
        count = 0
        while self.running:
            data, addr = self.server.recvfrom(self.buff_size)

            if self.io == THREAD:
                io = _thread(target=self.udp_passage, args=(data, addr))
                io.start()

            elif self.io == PROCESS:
                io = _process(target=self.udp_passage, args=(data, addr))
                io.start()

            else:
                self.udp_passage(data, addr)

            if self.num_conn is not None:
                count += 1

                if self.num_conn == count:
                    self.running = False
                    break

    def udp_selector_engine(self):
        
        count = 0
        if self.running:
            data, addr = self.server.recvfrom(self.buff_size)

            if self.io == MULTIPLEX_THREAD:
                io = _thread(target=self.udp_passage, args=(data, addr))
                io.start()

            elif self.io == MULTIPLEX_PROCESS:
                io = _process(target=self.udp_passage, args=(data, addr))
                io.start()

            else:
                self.udp_passage(data, addr)

            if self.num_conn is not None:
                count += 1

                if self.num_conn == count:
                    self.running = False

    def udp_passage(self, data, addr):
        print(f'{addr} => {data}')

    def close(self):
        self.running = False

        if self.io <= MULTIPLEX:
            self.selector.close()

        self.server.close()