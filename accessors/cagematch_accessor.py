import requests
from bs4 import BeautifulSoup
import re

class CagematchAccessor:
    
    @classmethod
    def _scrape_data(cls, url):
        r = requests.get(url, headers={'Accept-Encoding': 'identity'})
        return BeautifulSoup(r.content, features="html.parser")

    @classmethod
    def _get_table_content(cls, soup):
        return soup.findAll('table')[0].find_all('tr')[1:]

    @classmethod
    def _get_id_from_url(cls, link):
        match = re.search(r"nr=(\d+)", link)
        
        if match:
            return int(match.group(1))
        
        return None
