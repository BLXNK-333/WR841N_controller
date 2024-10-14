"""
Код в этом говномодуле, не получилось сделать многопоточным, по хуй знает
каким причинам, не пытаться исправить это хуйню.
"""
import sys
import time
import subprocess
from logging import getLogger


class ConnectionChecker:
    def __init__(self):
        self._logger = getLogger()
        self._outer_logger = getLogger("outer")

    def check_connection(self, stdout=True, reboot_waiting=False) -> bool:
        """
        Функция проверяет есть ли соединение, по средствам системной команды ping
        :return: (bool) True - есть, False - нет.
        """
        ip = "8.8.8.8"

        if reboot_waiting:
            self._reboot_waiting()
        if stdout:
            self._logger.debug("Checking the connection...")

        try:
            response = subprocess.run(
                ["ping", "-c", "2", ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output = response.stdout.decode()

            if response.returncode == 0:
                if stdout:
                    indented_output = "".join(
                        f"{' ' * 3}{ln}\n" for ln in output.split("\n")).rstrip()
                    self._outer_logger.info(indented_output)
                    self._outer_logger.debug(f"\n{' ' * 3}Connection established.\n")
                return True
            else:
                if stdout:
                    self._outer_logger.warning(
                        f"{' ' * 3}Ping unsuccessful: no response from IP: {ip}.\n")
                return False

        except subprocess.SubprocessError:
            self._logger.error("Ping command failed.")
            return False

    def _reboot_waiting(self):
        start_time = time.time()
        time_left = 45
        self._logger.info("Reboot the router:")

        while time_left >= 0:
            elapsed_time = time.time() - start_time

            sys.stdout.write(
                f"\r   Please wait while rebooting... Time left: {time_left} sec.")
            sys.stdout.flush()

            sleep_time = 1 - (elapsed_time % 1)
            time.sleep(sleep_time)

            time_left -= 1

        sys.stdout.write("\n\n")
        sys.stdout.flush()
