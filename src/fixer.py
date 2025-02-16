import signal
from logging import getLogger

from .utils.connection import ConnectionChecker
from .utils.browser import Browser
from .utils.router import Router
from .entities import IP


class FixRouterProblem:
    def __init__(self):
        self._logger = getLogger()
        self._outer_logger = getLogger("outer")

    def __enter__(self):
        try:
            signal.signal(signal.SIGINT, self._exit_callback)

            connection_checker = ConnectionChecker()
            if not connection_checker.check_connection(ip=IP.ROUTER):
                return self

            if connection_checker.check_connection(ip=IP.INTERNET):
                self._outer_logger.warning(
                    "   Internet connection is active. If you want to forcibly continue\n"
                    "   the FIX process, type 'y' and press Enter. To exit, press any\n"
                    "   other key.\n"
                )
                user_input = input("   Your choice (y/n): ").strip().lower()
                print()
                if user_input == 'y':
                    pass
                else:
                    return self

            self._browser = Browser()
            router = Router(
                driver=self._browser.driver
            )

            if not router.authorization():
                return self

            router.reconnect()
            if connection_checker.check_connection(ip=IP.INTERNET):
                router.exit()
                return self

            router.reboot()
            if connection_checker.check_connection(ip=IP.INTERNET, reboot_waiting=True):
                return self

            self._logger.warning(
                "\n   An attempt to reconnect the PPPoE connection and perform a soft\n"
                "   reboot of the router did not resolve the issue. The connection has\n"
                "   not been restored. It is recommended to manually reboot the router\n"
                "   using the physical button or contact your service provider.\n"
            )
            return self
        except KeyboardInterrupt:
            pass
        finally:
            self._free_up_resources()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def _free_up_resources(self):
        if hasattr(self, '_browser') and self._browser:
            self._browser.close_browser()

    def _exit_callback(self, signum, frame):
        """
        Метод для обработки прерывания через горячую клавишу (Ctrl+C).
        """
        self._outer_logger.info("\n\nInterrupt signal received. Exiting...")
        raise KeyboardInterrupt
