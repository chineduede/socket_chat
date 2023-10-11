from enum import Enum
from payload import Data, PayloadType


class UserInput:
    class Command(str, Enum):
        QUIT = "/q"
        EMOTE = "/emote"
        DM = "/message"
        LIST_USERS = "/list-users"

    @staticmethod
    def is_quit(cmd: str):
        return cmd.startswith(UserInput.Command.QUIT)

    @staticmethod
    def handle_emote_cmd(cmd: str, nickname: str):
        _, *emote = cmd.split()
        emote = nickname + " " + " ".join(emote)
        payload = Data(emote, PayloadType.EMOTE)
        return payload.construct_payload()

    @staticmethod
    def handle_direct_message(cmd: str):
        _, recepient, *message = cmd.split()
        payload = Data(" ".join(message), PayloadType.DM, recepient=recepient)
        return payload.construct_payload()

    @staticmethod
    def is_command(cmd: str):
        return cmd.startswith("/")

    @staticmethod
    def parse_and_handle_cmd(cmd: str, **kwargs):
        nickname = kwargs["nickname"]
        if cmd.startswith(UserInput.Command.EMOTE):
            return UserInput.handle_emote_cmd(cmd, nickname)
        elif cmd.startswith(UserInput.Command.DM):
            return UserInput.handle_direct_message(cmd)
        elif UserInput.is_quit(cmd):
            return
        elif cmd.startswith(UserInput.Command.LIST_USERS):
            return Data("", type_=PayloadType.LIST_USERS).construct_payload()
        else:
            return Data(cmd, PayloadType.CHAT, nick=nickname).construct_payload()


if __name__ == "__main__":
    print(UserInput().parse_and_handle_cmd("/me this is me", nickname="chndvz"))
