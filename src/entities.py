from enum import StrEnum


class Frame(StrEnum):
    MAIN = "mainFrame"
    BOTTOM_LEFT = "bottomLeftFrame"


class Button(StrEnum):
    LOGIN = "loginBtn"
    REBOOT = "reboot"
    CONNECT = "Connect"
    DISCONNECT = "Disconnect"
    CONNECTING = "t_connecting"


class TAB(StrEnum):
    EXIT = "a54"
    SYSTEM_TOOLS = "a44"
    REBOOT = "a50"


class IP(StrEnum):
    ROUTER = "192.168.0.1"
    INTERNET = "8.8.8.8"
