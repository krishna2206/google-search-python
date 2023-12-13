import traceback
import unicodedata
from bs4 import BeautifulSoup

from googlesearchpython.logger import logger


def parse_html_result(html_result):
    soup = BeautifulSoup(html_result, features="lxml")

    results = []
    results_blocks = soup.find("div", id="rso")
    if results_blocks is not None:
        results_blocks = results_blocks.findAll("div", class_="SoaBEf")
        if len(results_blocks) != 0:
            for result_block in results_blocks:
                try:
                    result = {
                        "title": result_block.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d").text,
                        "url": result_block.find("a", class_="WlydOe")["href"],
                        "published": unicodedata.normalize("NFKD", result_block.find("div", class_="OSrXXb rbYSKb LfVVr").text),
                        "description": unicodedata.normalize(
                            "NFKD", result_block.find("div", class_="GI74Re nDgy9d").text)
                    }
                except AttributeError:
                    logger.error(traceback.format_exc())
                    pass
                else:
                    results.append(result)
    
    return results
