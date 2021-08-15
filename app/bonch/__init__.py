from enum import Enum


class Settings(Enum):
    """
    Класс настроек
    """

    domain = "lk.sut.ru"
    timeout = 5
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.131 Safari/537.36 "
    }
