import traceback
import unicodedata
from bs4 import BeautifulSoup

from googlesearchpython.logger import logger


def parse_html_result(html_result: str) -> tuple:
    results_block = BeautifulSoup(html_result, features="lxml")

    relevant_result = None
    related_questions = []
    results = []

    if results_block is not None:
        results_items = results_block.findAll("div", class_="N54PNb BToiNc cvP2Ce")

        if len(results_items) != 0:
            relevant_result = results_block.find("div", class_="ifM9O")

            # ? Parsing relevant results
            if relevant_result is not None:
                is_featured_snippet = relevant_result.find("h2", class_="bNg8Rb OhScic zsYMMe BBwThe") is not None # ? "Extrait optimisé sur le Web"
                is_knowledge_panel = relevant_result.find("div", class_="kp-header") is not None

                # ? Featured snippet
                if is_featured_snippet:
                    try:
                        snippet_content = relevant_result.find("span", class_="hgKElc").text
                    # ? Raised when it is not a conventional snippet (eg.: a table)
                    # TODO : need improvements
                    except AttributeError:
                        relevant_result = None
                    else:
                        tooltips = relevant_result.findAll("div", class_="nnFGuf")
                        if tooltips is not None:
                            for tooltip in tooltips:
                                snippet_content = snippet_content.replace(tooltip.text, "")

                        relevant_result = {
                            "type": "featured_snippet",
                            "title": relevant_result.find("h3", class_="LC20lb MBeuO DKV0Md").text,
                            "url": relevant_result.find("a")["href"],
                            # ! Deprecated
                            "date": (
                                None
                                if relevant_result.find("span", class_="kX21rb ZYHQ7e") is None
                                else relevant_result.find("span", class_="kX21rb ZYHQ7e").text),
                            "answer": (
                                None
                                if relevant_result.find("div", class_="IZ6rdc") is None
                                else relevant_result.find("div", class_="IZ6rdc").text),
                            "content": snippet_content
                        }

                # ? Knowledge panel
                # TODO : need more tests
                elif is_knowledge_panel:
                    relevant_result = {
                        "type": "knowledge_panel",
                        "heading": relevant_result.find("div", class_="N6Sb2c i29hTd").text,
                        "header": relevant_result
                            .find("div", class_="kp-header")
                            .find("div", class_="Z0LcW t2b5Cf")
                            .text,
                        "content": (
                            None
                            if relevant_result.find("div", class_="LGOjhe") is None
                            else relevant_result.find("div", class_="LGOjhe").text)
                    }

                else:
                    relevant_result = None

            # ? Parsing "people also ask" part (if it exists)
            related_questions_blocks = results_block.findAll("div", attrs={"jsname": "yEVEwb"})
            if len(related_questions_blocks) > 0:
                for question in related_questions_blocks:
                    try:
                        qst = question.find("span", class_="CSkcDe").text
                    except AttributeError:
                        pass
                    else:
                        related_questions.append(qst)

            # ? Parsing results items
            for item in results_items:
                # if item.find("span", class_="ZGwO7 C0kchf NaCKVc yUTMj VDgVie") is None:
                    try:
                        result_item = {
                            "title": item.find("h3", class_="LC20lb MBeuO DKV0Md").text,
                            "url": item.findAll("a")[0]["href"],
                            "description": unicodedata.normalize(
                                "NFKD", item.find("div", class_="VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb").text)
                        }
                    except AttributeError:
                        logger.error(traceback.format_exc())
                        pass
                    else:
                        results.append(result_item)

    return relevant_result, related_questions, results
