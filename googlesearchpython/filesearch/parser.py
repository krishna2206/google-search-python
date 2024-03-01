import unicodedata
from bs4 import BeautifulSoup

from googlesearchpython.logger import logger


def parse_html_result(html_result: str, filetype: str):
    results_blocks = BeautifulSoup(html_result, features="lxml")

    results = []
    if results_blocks is not None:
        results_blocks = results_blocks.findAll("div", class_="N54PNb BToiNc cvP2Ce")
        if len(results_blocks) != 0:
            for result_block in results_blocks:
                # logger.debug(f"{result_block}\n----------------------------")

                filetype_banner_div = result_block.find("div", class_="eFM0qc BCF2pd iUh30")
                if filetype_banner_div:
                    result = {
                        "title": result_block.find("h3").text,
                        "url": result_block.findAll("a")[0]["href"],
                        "description": None if filetype == "docx" else __get_description(result_block),
                        "page_count": None if filetype != "pdf" else __get_page_count(result_block)
                    }
                    results.append(result)
    return results


def __get_description(result_block):
    class_names = [
        "VwiC3b yXK7lf fS1kJf lVm3ye r025kc hJNv6b Hdw6tb",
        "VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb"
    ]

    for class_name in class_names:
        description_div = result_block.find("div", class_=class_name)
        if description_div:
            return unicodedata.normalize("NFKD", description_div.text)

    raise Exception(f"Error getting description from both classnames.")


def __get_page_count(result_block):
    page_count_div = result_block.find("div", class_="LEwnzc Sqrs4e")
    if page_count_div:
        return int(
            unicodedata.normalize(
                "NFKD", page_count_div.text
            ).split(" ")[0].strip())
    return None
