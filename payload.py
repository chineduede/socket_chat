import enum
import json

class PayloadType(str, enum.Enum):
    HELLO = 'hello'
    CHAT = 'chat'
    JOIN = 'join'
    LEAVE = 'leave'


class Data:

    def __init__(self, data: str, type_: PayloadType, nick: str, remove_nick=False) -> None:
        self.data = data
        self.type_ = type_
        self.nick = nick
        self.remove_nick = remove_nick

    def construct_payload(self) -> bytes:
        message = {
            "type": self.type_.value,
            "nick": self.nick,
        }
        if self.type_ == PayloadType.CHAT:
            message['message'] = self.data

        if self.remove_nick:
            del message["nick"]

        message = json.dumps(message).encode()
        response = len(message).to_bytes(2, 'big')
        response += message
        return response


class RecvdPayload:
    def __init__(self, message: bytes) -> None:
        self.payload_length = 0
        self.message = b""
        self.recvd_payload_length = 0
        self.parse_init_message(message)

    def parse_init_message(self, message: bytes) -> None:
        self.payload_length = int.from_bytes(message[:2], 'big') + 2
        self.message = message[2:]
        self.recvd_payload_length = len(message)

    def add_message(self, message: bytes) -> None:
        self.message += message
        self.recvd_payload_length += len(message)

    def recvd_full_payload(self)-> bool:
        return self.payload_length == self.recvd_payload_length
    
    def get_message(self):
        return self.message
    
if __name__ == "__main__":
    print("hello" == PayloadType.HELLO)