import threading
import time
import argparse
from socket import socket
import enum
import sys
import random

from chatui.chatui import init_windows, read_command, print_message, end_windows, red, green
from payload import *


class Command(str, enum.Enum):
    QUIT = '/q'


class ChatClient:
    BUFFER_SIZE = 1024

    def __init__(self, host, port, nick) -> None:
        self.port = port
        self.host = host
        self.nickname = nick
        self.socket = socket()
        self.socket.connect((self.host, self.port))
        self.socket.sendall(self.send_hello())

    def send_hello(self):
        message = Data("", PayloadType.HELLO, self.nickname)
        return message.construct_payload()
    
    def receive_packets(self):
        while True:
            data = self.socket.recv(ChatClient.BUFFER_SIZE)
            payload = RecvdPayload(data)
            while not payload.recvd_full_payload():
                payload.add_message(self.socket.recv(ChatClient.BUFFER_SIZE))

            self.parse_server_payload(payload.get_message())
    
    def parse_server_payload(self, payload: bytes):
        payload: dict[str, str] = json.loads(payload)
        match payload["type"]:
            case PayloadType.JOIN:
                print_message(green(f"*** {payload['nick']} has joined the chat"))
            case PayloadType.CHAT:
                print_message(f"[{payload['nick']}]: {payload['message']}")
            case PayloadType.LEAVE:
                print_message(red(f"*** {payload['nick']} has left the chat"))
    
    def exit(self):
        print_message("Quitting...")
        # self.socket.close()
        end_windows()
        sys.exit(0)

    def post_message(self, message: str):
        payload = Data(message, PayloadType.CHAT, self.nickname, True)
        self.socket.sendall(payload.construct_payload())

    def handle_input(self):
        while True:
            input = read_command(f"{self.nickname}> ")
            if input == Command.QUIT:
                self.exit()
            else:
                self.post_message(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WebClient", description="This is a web chat client.")
    
    parser.add_argument("-p", "--port", default=8000, type=int, required=False)
    parser.add_argument("-n", "--nick", required=False, default=f"unknown{random.randrange(1000, 10_000)}")
    parser.add_argument("--host", default="localhost", type=str, required=False)
    args = parser.parse_args()

    port = args.port
    host = args.host
    nick = args.nick

    init_windows()
    client = ChatClient(host, port, nick)
    thread = threading.Thread(target=client.receive_packets, daemon=True)
    
    thread.start()

    client.handle_input()

