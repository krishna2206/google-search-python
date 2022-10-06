from .parser import (
    parse_js_data, parse_json_data,
    parse_chips_data, parse_tbs_data, parse_results_data, parse_next_page_data, check_safesearch_block)
from googlesearchpython.requests import Requests
from googlesearchpython.constants import LANGUAGES
from googlesearchpython.googlesearch import GoogleSearch


class ImageSearch(GoogleSearch, Requests):
    def __init__(self, query, lang="fr", region="fr", safe_search=False) -> None:
        super().__init__(query, lang, region, safe_search)

        self.__search_method = "isch"
        self._session.headers["Accept-Language"] = f"{LANGUAGES.get(self.lang)},{self.lang};q=0.5"

        self.status = {"message": None}
        self.chips = {"chips": None}
        self.tbs = {"tbs": None}
        self.results = {"page": 1, "end": False, "results": None}
        self.__next_page_data = None

        self.__get_first_results()

    def next_results(self):
        if not self.results["end"]:
            url = "https://www.google.com/_/VisualFrontendUi/data/batchexecute"

            request_body = {"hl": self.lang}
            data = self.__next_page_data
            response = self.post(url, params=request_body, data=data).text

            try:
                results, next_page_data = parse_json_data(response)
            except TypeError:
                print("End of results.")
                self.results["end"] = True
            else:
                self.results["results"] = parse_results_data(results)
                self.results["page"] += 1
                try:
                    self.__next_page_data = parse_next_page_data(self.query, next_page_data)
                except IndexError:
                    print("End of results.")
                    self.results["end"] = True
        else:
            print("End of results.")

    def next_page_data(self):
        return self.__next_page_data

    def __get_first_results(self):
        html_result = self.__fetch_html_result()

        safesearch_block = None
        if self.safe_search is True:
            safesearch_block = check_safesearch_block(html_result)

        if safesearch_block is not None:
            self.status["message"] = safesearch_block
            self.chips["chips"] = []
            self.tbs["tbs"] = []
            self.results["end"] = True
            self.results["results"] = []
        else:
            chips_data, tbs_data, results_data, next_page_data = parse_js_data(html_result)

            self.status["message"] = "ok"
            self.chips["chips"] = None if chips_data is None else parse_chips_data(chips_data)
            self.tbs["tbs"] = None if tbs_data is None else parse_tbs_data(tbs_data)
            self.results["results"] = parse_results_data(results_data)

            try:
                self.__next_page_data = parse_next_page_data(self.query, next_page_data)
            except (IndexError, TypeError):
                self.results["end"] = True

    def __fetch_html_result(self):
        request_body = {
            "q": self.query,
            "tbm": self.__search_method,
            "oq": self.query,
            "safe": "off" if self.safe_search is False else "on",
            "sclient": "img",
            "bih": 292,
            "biw": 1366,
            "client": "firefox-b-d"
        }

        response = self.get(self.url, params=request_body, allow_redirects=True)

        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch HTML results. {response.status_code} {response.reason}")
        return response.text
