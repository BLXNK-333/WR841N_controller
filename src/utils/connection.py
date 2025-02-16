"""
Код в этом говномодуле, не получилось сделать многопоточным, по хуй знает
каким причинам, не пытаться исправить это хуйню.
"""
from typing import Tuple
import sys
import time
import subprocess
from logging import getLogger

from ..entities import IP


class ConnectionChecker:
    def __init__(self):
        self._logger = getLogger()
        self._outer_logger = getLogger("outer")
        self._reboot_timeout = 45

    def _ping(self, ip: str) -> Tuple[bool, str]:
        try:
            response = subprocess.run(
                ["ping", "-c", "2", ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout = response.stdout.decode()
            if response.returncode == 0:
                return True, stdout
            return False, ""

        except subprocess.SubprocessError:
            self._logger.error("Ping command failed.")
            return False, ""

    def _router_response(self, status: bool):
        if status:
            self._outer_logger.info(
                f"{' ' * 3}The router is available.\n")
            return True
        else:
            self._outer_logger.warning(
                f"{' ' * 3}The router is not available: "
                f"no response from IP: {IP.ROUTER}.\n")
            return False

    def _internet_response(self, status: bool, stdout: str):
        if status:
            indented_output = "".join(
                f"{' ' * 3}{ln}\n" for ln in stdout.split("\n")).rstrip()
            self._outer_logger.info(indented_output)
            self._outer_logger.debug(f"\n{' ' * 3}Connection established.\n")
            return True
        else:
            self._outer_logger.warning(
                f"{' ' * 3}Ping unsuccessful: no response from IP: {IP.INTERNET}.\n")
            return False

    def _reboot_waiting(self):
        start_time = time.time()
        self._logger.info("Reboot the router:")

        while time.time() - start_time < self._reboot_timeout:
            time_left = int(self._reboot_timeout - (time.time() - start_time))
            sys.stdout.write(
                f"\r   Please wait while rebooting... Time left: {time_left} sec."
            )
            sys.stdout.flush()
            time.sleep(1)

        sys.stdout.write("\n\n")
        sys.stdout.flush()

    def check_connection(self, ip: IP, reboot_waiting: bool = False) -> bool:
        """
        Проверяет соединение с помощью команды ping.

        :param ip:
        :param reboot_waiting: Флаг для ожидания перезагрузки роутера.
        :return: True, если соединение установлено, иначе False.
        """
        if reboot_waiting:
            self._reboot_waiting()

        self._logger.debug("Checking the connection...")
        status, stdout = self._ping(ip)

        if ip == IP.ROUTER:
            return self._router_response(status)

        if ip == IP.INTERNET:
            return self._internet_response(status, stdout)
