import unicodedata
from bs4 import BeautifulSoup


def parse_html_result(html_result):
    soup = BeautifulSoup(html_result, features="lxml")

    results = []
    results_blocks = soup.find("div", id="rso")
    if results_blocks is not None:
        results_blocks = results_blocks.findAll("div", class_="SoaBEf xuvV6b")
        if len(results_blocks) != 0:
            for result_block in results_blocks:
                try:
                    result = {
                        "title": result_block.find("div", class_="mCBkyc y355M ynAwRc MBeuO jBgGLd OSrXXb").text,
                        "url": result_block.find("a", class_="WlydOe")["href"],
                        "published": unicodedata.normalize("NFKD", result_block.find("div", class_="OSrXXb ZE0LJd YsWzw").text),
                        "description": unicodedata.normalize(
                            "NFKD", result_block.find("div", class_="GI74Re jBgGLd OSrXXb").text)
                    }
                except AttributeError:
                    pass
                else:
                    results.append(result)
    
    return results
