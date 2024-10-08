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
            # Выполняем команду ping с 1 пакетом
            response = subprocess.run(
                ["ping", "-c", "2", ip],  # Пинг 2 пакета
                stdout=subprocess.PIPE,  # Захватываем вывод команды
                stderr=subprocess.PIPE
            )
            output = response.stdout.decode()

            # Проверяем успешность выполнения по коду возврата
            if response.returncode == 0:
                if stdout:
                    output += "\nConnection established."
                    indented_output = "".join(
                        f"{' ' * 3}{ln}\n" for ln in output.split("\n"))
                    self._outer_logger.info(indented_output)
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
        time_left = 45  # Устанавливаем начальное время ожидания
        self._logger.info("Reboot the router:")

        while time_left >= 0:
            elapsed_time = time.time() - start_time

            # Обновляем сообщение с оставшимся временем
            sys.stdout.write(
                f"\r   Please wait while rebooting... Time left: {time_left} sec.")
            sys.stdout.flush()

            # Рассчитываем время для паузы до следующей секунды
            sleep_time = 1 - (elapsed_time % 1)  # Компенсируем время выполнения
            time.sleep(sleep_time)

            time_left -= 1  # Уменьшаем таймер

        # После завершения вывода добавляем новую строку
        sys.stdout.write("\n\n")
        sys.stdout.flush()
