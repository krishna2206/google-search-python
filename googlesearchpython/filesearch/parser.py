import unicodedata
from bs4 import BeautifulSoup


def parse_html_result(html_result):
    results_blocks = BeautifulSoup(html_result, features="lxml")

    results = []
    if results_blocks is not None:
        results_blocks = results_blocks.findAll("div", class_="N54PNb BToiNc cvP2Ce")
        if len(results_blocks) != 0:
            for result_block in results_blocks:
                try:
                    result = {
                        "title": result_block.find("h3").text,
                        "url": result_block.findAll("a")[0]["href"],
                        "description": unicodedata.normalize(
                            "NFKD", result_block.find("div", class_="VwiC3b yXK7lf fS1kJf lyLwlc yDYNvb W8l4ac lEBKkf").text)
                    }
                except AttributeError:
                    result = {
                        "title": result_block.find("h3").text,
                        "url": result_block.findAll("a")[0]["href"],
                        "description": unicodedata.normalize(
                            "NFKD", result_block.find("div", class_="VwiC3b yXK7lf lyLwlc yDYNvb W8l4ac lEBKkf").text)
                    }
                results.append(result)
    return results
