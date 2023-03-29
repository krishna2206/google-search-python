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
                try:
                    result = {
                        "title": result_block.find("h3").text,
                        "fileType": result_block.find("span", class_="ZGwO7 s4H5Cf C0kchf NaCKVc yUTMj VDgVie").text,
                        "url": result_block.findAll("a")[0]["href"],
                        "description": unicodedata.normalize(
                            "NFKD", result_block.find("div", class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf").text)
                    }
                except AttributeError:
                    result = {
                        "title": result_block.find("h3").text,
                        "fileType": None,
                        "url": result_block.findAll("a")[0]["href"],
                        "description": unicodedata.normalize(
                            "NFKD", result_block.find("div", class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf").text)
                    }
                results.append(result)
    return results
