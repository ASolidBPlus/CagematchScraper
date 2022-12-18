import requests
from bs4 import BeautifulSoup

class CagematchAccessor:
    def __init__(self) -> None:
        pass

    def _scrape_data(self, url):
        r = requests.get(url, headers={'Accept-Encoding': 'identity'})
        return BeautifulSoup(r.content, features="html.parser")

    @classmethod
    def _get_table_content(cls, soup):
        return soup.findAll('table')[0].find_all('tr')[1:]
