from enum import StrEnum


class Frame(StrEnum):
    MAIN = "mainFrame"
    BOTTOM_LEFT = "bottomLeftFrame"


class Button(StrEnum):
    LOGIN = "loginBtn"
    REBOOT = "reboot"
    CONNECT = "Connect"
    DISCONNECT = "Disconnect"


class TAB(StrEnum):
    EXIT = "a54"
    SYSTEM_TOOLS = "a44"
    REBOOT = "a50"

