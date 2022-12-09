import json

from bs4 import BeautifulSoup


def parse_js_data(html_content: str):
    """
    > It parses the HTML content of the Google Images page to extract the JSON data that is used to
    display the images
    
    :param html_content: the HTML content of the page to be parsed
    :type html_content: str
    :return: chips, tbs, results, next_page_data
    """
    soup = BeautifulSoup(html_content, features="lxml")

    nonce_value = soup.find("script", attrs={"data-id": "_gd"})["nonce"]
    nonce_scripts = soup.findAll("script", attrs={"nonce": nonce_value})

    raw_data_script = None
    for i, nonce_script in enumerate(nonce_scripts):
        if "AF_initDataCallback(" in nonce_script.text:
            raw_data_script = nonce_scripts[i].text

    raw_data_script = raw_data_script.replace(
        "AF_initDataCallback(", "").replace(");", "")
    raw_data_script = raw_data_script.replace(
        "key: 'ds:1', hash: '2', data:",
        "\"key\": \"ds:1\", \"hash\": \"2\", \"data\":").replace("sideChannel:", "\"sideChannel\":")

    json_data = json.loads(raw_data_script)

    # Locate each part of the json data to be cleaned
    #? Google images regularly updates its HTML, 
    #? it may be that the following localizations can break,
    #? it will then be necessary to update the scraper
    try:
        chips = json_data["data"][1][0][0][1]
        tbs = json_data["data"][7][0]
    except IndexError:
        chips = None
        tbs = None

    results = json_data["data"][56][1][0][0][1][0]
    next_page_data = (
        json_data["data"][56][1][0][0][0][0]["444383007"][12][11],
        json_data["data"][56][1][0][0][0][0]["444383007"][12][16])

    return chips, tbs, results, next_page_data


def parse_json_data(json_data: str):
    """
    > It parses the json data (that is returned after requesting next page) 
    and returns the next results and the next page data
    
    :param json_data: the json data to parse
    :type json_data: str
    :return: The results and next_page_data are being returned.
    """
    json_to_parse = None
    for line in json_data.split("\n"):
        if '[["wrb.fr","HoAMBc",' in line:
            json_to_parse = json.loads(line)
            break
    if json_to_parse is not None:
        json_to_parse = json_to_parse[0][2]
        json_to_parse = json.loads(json_to_parse)

        # Locate each part of the json data to be cleaned
        #? Google images regularly updates its HTML, 
        #? it may be that the following localizations can break,
        #? it will then be necessary to update the scraper
        #? The location is the same as in the parse_js_data function, minus the "data" index
        results = json_to_parse[56][1][0][0][1][0]
        next_page_data = (
            json_to_parse[56][1][0][0][0][0]["444383007"][12][11],
            json_to_parse[56][1][0][0][0][0]["444383007"][12][16])

        return results, next_page_data
    return None, None


def parse_chips_data(chips_data: list):
    """
    It parse the chips (search suggestions) in the Google Images results page.
    
    :param chips_data: list
    :type chips_data: list
    :return: A list of dictionaries.
    """
    cleaned_chips = chips_data
    for i in range(len(chips_data)):
        try:
            cleaned_chips[i] = {
                "name": cleaned_chips[i][0],
                "thumbnail": cleaned_chips[i][1][0],
                "link": cleaned_chips[i][2]
            }
        except TypeError:
            cleaned_chips[i] = {
                "name": cleaned_chips[i][0],
                "thumbnail": None,
                "link": cleaned_chips[i][2]
            }
    return cleaned_chips


def parse_tbs_data(tbs_data: list):
    """
    > This will parse the TBS (Unofficialy called 'Term By Search') of the Google Images results page.
    
    :param tbs_data: list
    :type tbs_data: list
    :return: A list of dictionaries.
    """
    cleaned_tbs = []
    for i, category in enumerate(tbs_data):
        cleaned_tbs.append({
            "name": category[1],
            "specificValues": []
        })
        for j in range(len(tbs_data[i][7])):
            if j != 0:  # Skip first element
                cleaned_tbs[i]["specificValues"].append(
                    {
                        "name": tbs_data[i][7][j][1],
                        "link": tbs_data[i][7][j][0]
                    }
                )
    return cleaned_tbs


def parse_results_data(results_data: list):
    """
    It takes the raw data from the Google Images AJAX API and parses it into a more readable format
    
    :param results_data: list
    :type results_data: list
    :return: A list of dictionaries containing the image's title, original image's url, width, and
    height, thumbnail's url, width, and height, source website, and page url.
    """
    cleaned_results = []
    for i in range(len(results_data)):
        results_data[i] = results_data[i][0][0]["444383007"]

        if results_data[i] is not None:
            try:
                cleaned_results.append({
                    "title": results_data[i][1][22].get(list(results_data[i][1][22].keys())[-1])[-1],
                    "original": {
                        "url": results_data[i][1][3][0],
                        "width": results_data[i][1][3][2],
                        "height": results_data[i][1][3][1]
                    },
                    "thumbnail": {
                        "url": results_data[i][1][2][0],
                        "width": results_data[i][1][2][2],
                        "height": results_data[i][1][2][1]
                    },
                })
            #? Raised when parsing "Similar searches"
            except TypeError:
                pass
            else:
                try:
                    cleaned_results[-1]["sourceWebsite"] = results_data[i][1][22].get(list(results_data[i][1][22].keys())[-2])[17]
                    cleaned_results[-1]["pageURL"] = results_data[i][1][22].get(list(results_data[i][1][22].keys())[-2])[2]
                except (IndexError, KeyError):
                    cleaned_results[-1]["sourceWebsite"] = None
                    cleaned_results[-1]["pageURL"] = None

    for index, data in enumerate(cleaned_results):
        if data is None:
            cleaned_results.pop(index)
    return cleaned_results


def parse_next_page_data(query: str, data: tuple):
    """
    It parse the json data and extract that is necessary for requesting next page
    Google Images doesn't update this data so it will work for an undetermined time.
    
    :param query: The query search
    :type query: str
    :param data: The data that we got from the first request
    :type data: tuple
    :return: A list of dictionaries.
    """
    #* Get data from data[0]
    first_data = []
    for d in data[0]:
        if isinstance(d, list):
            break
        first_data.append(d)

    second_data = []
    for d in data[0]:
        if isinstance(d, list):
            second_data = d
            break

    #* Get data from data[1]
    third_data = data[1][-1]
    fourth_data = data[1][-2]

    next_page_data = [None, None, [], None, None, None, None, None, None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None, None, None, None, None, [query], None, None, None,
                      None, None, None, None, None, [None, fourth_data, third_data], None, False]

    #* Add data from first data and second data in next_page_data[2]
    for d in first_data:
        next_page_data[2].append(d)
    next_page_data[2].append(second_data)
    next_page_data[2] = next_page_data[2] + [[], [], None, None, None, 0]

    next_page_data = json.dumps(next_page_data)

    next_page_data = [[["HoAMBc", f"{next_page_data}", None, "generic"]]]
    next_page_data = {
        "f.req": json.dumps(next_page_data)
    }

    return next_page_data


def check_safesearch_block(html_content):
    soup = BeautifulSoup(html_content, features="lxml")
    safesearch_block = soup.find("div", class_="pctrN")
    if safesearch_block is not None:
        return safesearch_block.find("div", class_="Zd9MXe").text
