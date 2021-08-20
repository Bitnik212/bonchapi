import requests

from app.bonch import Settings


class BonchProfile:

    def __init__(self, miden: str):
        """

        :param miden:
        """
        self.domain = Settings.domain
        self.timeout = Settings.timeout
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('miden', miden, domain=self.domain, path="/")

    def get(self):
        """

        :return:
        """

