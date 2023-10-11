from abc import ABC, abstractmethod
from chatui.chatui import red, green, blue, yellow, grey
from payload import PayloadType


class BaseMessage:
    def __init__(self, *, msg: str, nickname: str) -> None:
        self.message = msg
        self.nickname = nickname

    def get_message(self) -> str:
        return f"[{self.nickname}]: {self.message}"


class ChatMessage(BaseMessage):
    pass


class LeaveMessage(BaseMessage):
    def get_message(self) -> str:
        return red(f"*** {self.nickname} has left the chat.")


class JoinMessage(BaseMessage):
    def get_message(self) -> str:
        return green(f"*** {self.nickname} has joined the chat.")


class EmoteMessage(BaseMessage):
    def get_message(self) -> str:
        return blue(f"[{self.message}]")


class DirectMessage(BaseMessage):
    def get_message(self) -> str:
        return yellow(f"{self.message}")


class ListUsersMessage(BaseMessage):
    def get_message(self) -> str:
        string = "*** List of online Users***\n\n"

        for idx, user in enumerate(self.message, 1):
            string += f"{idx}.\t{user}\n"
        return grey(string)


class ErrorMessage(BaseMessage):
    def get_message(self) -> str:
        return red(f"!!!! {self.message}")


def message_builder(type_: PayloadType):
    message = None
    match type_:
        case PayloadType.CHAT:
            message = ChatMessage
        case PayloadType.LEAVE:
            message = LeaveMessage
        case PayloadType.JOIN:
            message = JoinMessage
        case PayloadType.EMOTE:
            message = EmoteMessage
        case PayloadType.DM:
            message = DirectMessage
        case PayloadType.LIST_USERS:
            message = ListUsersMessage
        case PayloadType.ERROR:
            message = ErrorMessage
        case _:
            message = BaseMessage

    def inner(**kwargs):
        return message(**kwargs)

    return inner
