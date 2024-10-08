from src.fixer import FixRouterProblem
from src.config.logging_settings import load_logger_config


def main():
    load_logger_config()
    with FixRouterProblem():
        pass


if __name__ == '__main__':
    # TODO:
    #  1. Понять как оптимизировать логику перезагрузки роутера.
    #     Нужно убрать лишнее ожидание, и как-то разобраться с выводом в stdout
    #  2. Написать sh скрипт для запуска с кнопки, должен поднять
    #     консоль, чтобы было видно лог программы.
    main()
