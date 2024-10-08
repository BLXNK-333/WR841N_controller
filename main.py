from src.fixer import FixRouterProblem
from src.config.logging_settings import load_logger_config


def main():
    load_logger_config()
    with FixRouterProblem():
        pass


if __name__ == '__main__':
    main()
