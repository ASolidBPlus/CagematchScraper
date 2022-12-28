import requests
from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import urlencode, urlunsplit

class CagematchAccessor:
    
    @classmethod
    def _scrape_data(cls, url):
        r = requests.get(url, headers={'Accept-Encoding': 'identity'})
        return BeautifulSoup(r.content, features="html.parser")

    @classmethod
    def _build_url(cls, id, **kwargs):
        scheme = 'https'
        netloc = 'www.cagematch.net'
        path = '/'
        query = urlencode({**{'id': id}, **kwargs})
        fragment = ''
        return urlunsplit((scheme, netloc, path, query, fragment))

    @classmethod
    def _get_table_content(cls, soup):
        return soup.find_all('tr')[1:]

    @classmethod
    def _separate_row_data(cls, soup) -> list:
        rows = []
        for row in cls._get_table_content(soup):
            rows.append(row.find_all('td'))

        return rows

    @classmethod
    def _get_id_from_url(cls, link):
        match = re.search(r"nr=(\d+)", link)
        
        if match:
            return int(match.group(1))
        
        return None

    @classmethod
    def _safe_extract_table_data(cls, table_data, index, return_text=True):
        try:
            if return_text:
                if table_data[index].text.strip():
                    return table_data[index].text.strip()
                
                return None
            
            return table_data[index]
        
        except (IndexError, AttributeError, TypeError):
            return None

    @classmethod
    def _safe_extract_id_from_table(cls, extract_index, row_data):

        data = cls._safe_extract_table_data(row_data, extract_index, return_text=False)

        if data is not None:
            try:
                link = data.find('a', href=True)
                return cls._get_id_from_url(link['href'])
            
            except (IndexError, TypeError, KeyError):
                return None

        return None