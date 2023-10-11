import threading
import argparse
from socket import socket
import sys
import random

from chatui.chatui import init_windows, read_command, print_message, end_windows, grey
from payload import *
from command import *
from message import message_builder


def get_random_name():
    return f"unknown{random.randrange(1000, 100_000)}"


class ChatClient:
    BUFFER_SIZE = 1024

    def __init__(self, host, port, nick) -> None:
        self.port = port
        self.host = host
        self.nickname = nick
        self.socket = socket()
        self.socket.connect((self.host, self.port))
        self.send_hello()
        self.command = UserInput()

    def send_hello(self):
        message = Data("", PayloadType.HELLO, nick=self.nickname)
        return self.socket.sendall(message.construct_payload())

    def receive_packets(self):
        while True:
            data = self.socket.recv(ChatClient.BUFFER_SIZE)
            payload = RecvdPayload(data)
            while not payload.recvd_full_payload():
                payload.add_message(self.socket.recv(ChatClient.BUFFER_SIZE))

            self.parse_server_payload(payload.get_message())

    def parse_server_payload(self, payload: bytes):
        payload: dict[str, str] = json.loads(payload)
        if payload["type"] == PayloadType.ERR_DUP:
            rand_nick = get_random_name()
            print_message(
                grey(
                    f"*** username {self.nickname} taken, assigning you {rand_nick}"
                )
            )
            self.nickname = rand_nick
            self.send_hello()
        else:
            message_cls = message_builder(payload["type"])
            message = message_cls(
                nickname=payload.get("nick", None), msg=payload.get("message", "")
            )
            print_message(message.get_message())

    def exit(self):
        print_message("quitting...")
        # self.socket.close()
        end_windows()
        sys.exit(0)

    def post_message(self, message: bytes):
        self.socket.sendall(message)

    def handle_commands(self, cmd: str):
        payload = self.command.parse_and_handle_cmd(cmd, nickname=self.nickname)
        if payload is None:
            self.exit()
        else:
            return payload

    def handle_input(self):
        while True:
            input_txt = read_command(f"{self.nickname}> ")
            if not input_txt:
                continue
            payload = self.handle_commands(input_txt)
            self.post_message(payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WebClient", description="This is a web chat client."
    )

    parser.add_argument("-p", "--port", default=8000, type=int, required=False)
    parser.add_argument(
        "-n",
        "--nick",
        required=False,
        default=get_random_name(),
    )
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
