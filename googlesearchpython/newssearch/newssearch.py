from googlesearchpython.newssearch.parser import parse_html_result
from googlesearchpython.requests import Requests
from googlesearchpython.constants import LANGUAGES
from googlesearchpython.googlesearch import GoogleSearch


class NewsSearch(GoogleSearch, Requests):
    def __init__(self, query, limit=10, page=1, lang="fr", region="fr", safe_search=False) -> None:
        super().__init__(query, lang, region, safe_search)

        self._session.headers["Accept-Language"] = f"{LANGUAGES.get(self.lang)},{self.lang};q=0.5"

        self.limit = limit
        self.page = page
        self.results = {
            "page": 1,
            "end": False,
            "results": None
        }

        self.__get_results()

    def next_results(self):
        if not self.results["end"]:
            self.page += 1
            next_results = self.__get_results()

            if len(next_results) == 0:
                print("End of results.")
                self.page -= 1
            else:
                self.results["results"] = next_results
        else:
            print("End of results")

    def __get_results(self):
        html_result = self.__fetch_html_result()

        parsed_results = parse_html_result(html_result)

        if len(parsed_results) == 0:
            self.results["end"] = True

        self.results["results"] = parsed_results

    def __fetch_html_result(self):
        request_body = {
            "q": self.query,
            "num": self.limit,
            "hl": self.lang,
            "tbm": "nws",
            "sclient": "gws-wiz-news"
        }

        if self.page > 1:
            request_body["start"] = (self.page * 10) - 10

        response = self.get(self.url, params=request_body, allow_redirects=True)

        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch HTML results. {response.status_code} {response.reason}")
        return response.text
