from dataclasses import dataclass
from typing import Callable

from environs import Env


@dataclass
class Authorization:
    user_name: str
    password: str
    url: str


@dataclass
class Config:
    authorization: Authorization


def config_singleton(func: Callable):
    _instance = None

    def wrapper(*args, **kwargs):
        nonlocal _instance
        if _instance is None:
            _instance = func(*args, **kwargs)

        assert isinstance(_instance, Config)
        return _instance

    return wrapper


@config_singleton
def get_config(env_path: str = ".env") -> Config:
    """Возвращает файл конфигурации. Singleton."""
    env = Env()
    env.read_env(env_path)

    return Config(
        Authorization(
            user_name=env.str("USER_NAME", "admin"),
            password=env.str("PASSWORD", "password"),
            url=env.str("URL", "http://127.0.0.1/"),
        )
    )
