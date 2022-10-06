from requests import Session


# ! ADD PROXY SUPPORT
class Requests:
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._session = Session()

        # TODO : Implement parser for later : Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
        self._session.headers = {
            "Host": "www.google.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "*/*",
            "Referer": "https://www.google.com/",
        }

    def get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self._session.post(url, **kwargs)
