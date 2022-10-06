import unicodedata
from bs4 import BeautifulSoup


def parse_html_result(html_result):
    soup = BeautifulSoup(html_result, features="lxml")

    results = []
    results_blocks = soup.find("div", id="rso")
    if results_blocks is not None:
        results_blocks = results_blocks.findAll("div", class_="kvH3mc BToiNc UK95Uc")
        if len(results_blocks) != 0:
            for result_block in results_blocks:
                if result_block.find("span", class_="ZGwO7 C0kchf NaCKVc yUTMj VDgVie") is None:
                    try:
                        result = {
                            "title": result_block.find("h3", class_="LC20lb MBeuO DKV0Md").text,
                            "url": result_block.findAll("a")[0]["href"],
                            "description": unicodedata.normalize(
                                "NFKD", result_block.find("div", class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf").text)
                        }
                    except AttributeError:
                        pass
                    else:
                        results.append(result)

    return results
