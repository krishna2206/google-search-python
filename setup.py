from setuptools import setup, find_packages

VERSION = '2023.03-beta2'
DESCRIPTION = 'A Python package for searching in Google Search'
LONG_DESCRIPTION = 'A Python package for searching in Google Search, with the ability to search for images, videos, news, and specific file types.'

setup(
    name="google-search-python",
    version=VERSION,
    author="Anhy Krishna Fitiavana",
    author_email="fitiavana.krishna@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'lxml'],
    keywords=['python', 'google', 'scraping'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)