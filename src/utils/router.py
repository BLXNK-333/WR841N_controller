from logging import getLogger
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..config.app_settings import get_config
from ..entities import TAB, Button, Frame


class Router:
    def __init__(self, driver: webdriver.Firefox):
        self._driver = driver
        self._config = get_config()
        self._logger = getLogger()
        self._outer_logger = getLogger("outer")

        self._user = self._config.authorization.user_name
        self._password = self._config.authorization.password
        self._url = self._config.authorization.url

        self._driver.get(self._url)

    def _wait_page_loading(self) -> None:
        """
        Ждет полной загрузки страницы.
        """
        wait = WebDriverWait(self._driver, 10)
        wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")

    def _is_element_present(self, elem_id: str, timeout: int = 0) -> bool:
        """
        Возвращает True, если объект с elem_id есть на странице, иначе False.
        """
        try:
            self._wait_page_loading()
            WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.ID, elem_id))
            )
            return True
        except TimeoutException:
            return False

    def _click_to(self, obj_id: Union[Button, TAB]):
        """
        Нажимает на кликабельный объект с btn_id.
        """
        button = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.ID, obj_id))
        )
        button.click()

    def _switch_to_frame(self, frame_id: Frame):
        """
        Ожидаем загрузки фрейма frame_id и переключаемся на него.
        """
        self._driver.switch_to.default_content()
        wait = WebDriverWait(self._driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, frame_id)))

    def _accept_alert(self, action: bool = True):
        """
        Для нажатия на кнопку, сообщения alert, которое не из DOM модели.
        :param action: (bool) Если True, то принять, иначе отклонить.
        """
        WebDriverWait(self._driver, 10).until(EC.alert_is_present())
        alert = self._driver.switch_to.alert
        alert.accept() if action else alert.dismiss()

    def _exit(self) -> None:
        """
        Реализует логику де_авторизации.
        """
        self._switch_to_frame(Frame.BOTTOM_LEFT)
        button = self._driver.find_element(By.ID, TAB.EXIT)
        self._driver.execute_script("arguments[0].click();", button)
        button.click()
        self._driver.switch_to.window(self._driver.window_handles[-1])

    def authorization(self) -> bool:
        """
        Реализует логику авторизации.
        :return: (bool) True, если успех.
        """
        wait = WebDriverWait(self._driver, 10)

        user_field = wait.until(EC.presence_of_element_located((By.ID, "userName")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "pcPassword")))

        # Вводим логин и пароль
        user_field.send_keys(self._user)
        password_field.send_keys(self._password)

        # Кликаем на кнопку входа
        self._click_to(Button.LOGIN)

        # Проверяем статус
        auth_status = not self._is_element_present("loginForm")
        if auth_status:
            self._logger.info("Authorization on the router was successful.")
        else:
            self._logger.warning("Failed authorization attempt, bad user or password.")
        return auth_status

    def reconnect(self) -> bool:
        try:
            self._logger.debug("Reconnection attempt...")
            self._switch_to_frame(Frame.MAIN)
            if self._is_element_present(Button.DISCONNECT):
                self._click_to(Button.DISCONNECT)
                self._outer_logger.info("   PPPoE connection disabled.")

            if self._is_element_present(Button.CONNECT):
                self._click_to(Button.CONNECT)
                self._outer_logger.info("   PPPoE connection enabled.\n")

            self._exit()
            return True

        except Exception as e:
            if hasattr(e, "msg"):
                e = e.msg
            self._logger.error(f"Error occurred during reconnect: {e}")
            return False

    def reboot(self) -> bool:
        try:
            self._switch_to_frame(Frame.BOTTOM_LEFT)
            self._click_to(TAB.SYSTEM_TOOLS)
            self._click_to(TAB.REBOOT)
            self._switch_to_frame(Frame.MAIN)
            self._click_to(Button.REBOOT)
            self._accept_alert()
            return True

        except Exception as e:
            if hasattr(e, "msg"):
                e = e.msg
            self._logger.error(f"Error occurred during reboot: {e}")
            return False
