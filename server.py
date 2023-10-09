import socket
import argparse
import select
import json

from payload import *


class ChatServer:
    BUFFER_SIZE = 1024

    def __init__(self, port: int) -> None:
        self.port = port
        self.sockets: set[socket.socket] = set()
        self.client_buffers: dict[socket.socket, RecvdPayload] = {}
        self.client_nick: dict[socket.socket, str] = {}

        sock = socket.socket()
        sock.bind(('localhost', self.port))
        sock.listen(10)
        print('Waiting for connections')

        self.server_socket = sock
        self.sockets.add(sock)

    def run(self):
        while True:
            ready_socks, _, _ = select.select(self.sockets, set(), set())

            for sock in ready_socks:
                if sock is self.server_socket:
                    new_conn, _ = sock.accept()
                    print(f'{new_conn.getpeername()}: connected')
                    self.sockets.add(new_conn)
                else:
                    self.handle_client(sock)

    def broadcast(self, message: Data):
        for client in self.sockets:
            if client != self.server_socket:
                print(f"Sending {message.data} to {client.getpeername()}")
                client.sendall(message.construct_payload())

    def handle_client(self, socket: socket.socket):
        client_closed = False
        data = None
        try:
            data = socket.recv(ChatServer.BUFFER_SIZE)
        except (ConnectionResetError):
            client_closed = True
        if not data or client_closed:        # client closed connection
            self.parse_client_payload(socket, b'{"type": "leave"}')
            print(f'{socket.getpeername()}: disconnected')
        else:
            payload = RecvdPayload(data)
            while not payload.recvd_full_payload():
                payload.add_message(socket.recv(ChatServer.BUFFER_SIZE))

            self.client_buffers[socket] = payload
            self.parse_client_payload(socket, payload.get_message())

    def parse_client_payload(self, client_sock: socket.socket, payload: bytes):
        payload: dict[str, str] = json.loads(payload)
        if payload["type"] == PayloadType.HELLO:
            self.client_nick[client_sock] = payload["nick"]
            self.broadcast(Data("", PayloadType.JOIN, payload["nick"]))
        elif payload["type"] == PayloadType.CHAT:
                self.broadcast(Data(payload["message"], PayloadType.CHAT, self.client_nick[client_sock]))
        elif payload["type"] == PayloadType.LEAVE:
            nickname = self.client_nick[client_sock]
            del self.client_buffers[client_sock]
            del self.client_nick[client_sock]
            self.sockets.remove(client_sock)
            self.broadcast(Data("", PayloadType.LEAVE, nickname))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WebServer", description="This is a web server that connects to any client.")
    
    parser.add_argument("-p", "--port", default=8000, type=int, required=False)
    args = parser.parse_args()
    port = args.port

    server = ChatServer(port)

    server.run()