import logging
from base.config import Config


def __start() -> None:
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w")
    Config()


def main() -> None:
    ...


if __name__ == "__main__":
    __start()
    main()
