class GoogleSearch:
    def __init__(self, query, lang, region, safe_search) -> None:
        super().__init__()

        self.url = "https://www.google.com/search"
        self.query = query
        self.lang = lang
        self.region = region
        self.safe_search = safe_search
