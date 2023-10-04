from googlesearchpython.filesearch.parser import parse_html_result
from googlesearchpython.requests import Requests
from googlesearchpython.constants import LANGUAGES
from googlesearchpython.googlesearch import GoogleSearch
from googlesearchpython.utils import extract_html_block


class FileSearch(GoogleSearch, Requests):
	def __init__(self, query, filetype, limit=10, page=1, lang="fr", region="fr", safe_search=False) -> None:
		super().__init__(query, lang, region, safe_search)

		self._session.headers.update({
            "Accept-Language": f"{LANGUAGES.get(self.lang)},{self.lang};q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        })

		self.filetype = filetype
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
		html_result = self.__fetch_raw_result()
		html_result = extract_html_block(html_result)

		parsed_results = parse_html_result(html_result)

		if len(parsed_results) == 0:
			self.results["end"] = True

		self.results["results"] = parsed_results


	def __fetch_raw_result(self):
		request_body = {
			"q": self.query + f" filetype:{self.filetype}",
			"hl": self.lang,
			"safe": "off" if self.safe_search is False else "on",
			"client": "firefox-b-d",
            "sa": "N",
            "asearch": "arc",
            "cs": "1",
            "async": "arc_id:srp_110,ffilt:all,ve_name:MoreResultsContainer,use_ac:false,inf:1,_id:arc-srp_110,_pms:s,_fmt:pc"
		}

		if self.page > 1:
			request_body["start"] = (self.page * 10) - 10

		response = self.get(self.url, params=request_body, allow_redirects=True)

		if response.status_code != 200:
			raise Exception(
				f"Failed to fetch raw results. {response.status_code} {response.reason}")
		return response.text
