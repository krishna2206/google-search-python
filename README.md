# Google Search Python

A Python package for searching in Google Search. This package provides the ability to search for images, videos, news, and specific file types.

## Installation

To install the package, you can use pip:

```sh
pip install git+https://github.com/krishna2206/google-search-python
```

## Usage

Here's how you can use the different search modules in this package:

### Page Search

```python
from googlesearchpython import PageSearch

# Create a PageSearch object
page_search = PageSearch("query", page=1)

# Print the results
print(page_search.results)
```

### File Search

```python
from googlesearchpython.filesearch.filesearch import FileSearch

# Create a FileSearch object
file_search = FileSearch("query", "filetype", limit=10, page=1)

# Print the results
print(file_search.results)
```

Note: The "filetype" parameter should be one of the supported file types. Currently, the supported file types are "pdf", "doc", "docx", "xls", "xlsx", "ppt", and "pptx". Please check the `constants.py` file for the most up-to-date list of supported file types.

### News Search

```python
from googlesearchpython import NewsSearch

# Create a NewsSearch object
news_search = NewsSearch("query", page=1)

# Print the results
print(news_search.results)
```

### Image Search

```python
from googlesearchpython import ImageSearch

# Create an ImageSearch object
image_search = ImageSearch("query")

# Getting the next page of results
image_search.next_results()
image_search.next_results()

# Print the results
print(image_search.results)
```

## Dependencies

This package depends on the following Python libraries:

- requests
- beautifulsoup4
- lxml

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.