import requests
from bs4 import BeautifulSoup
from typing import Optional, Callable, Any, Union
import re
import logging
from urllib.parse import urlencode, urlunsplit

class CagematchAccessor:
    
    @classmethod
    def _scrape_data(cls, url):
        r = requests.get(url, headers={'Accept-Encoding': 'identity'})
        return BeautifulSoup(r.content, features="html.parser")

    @classmethod
    def _build_url(cls, **kwargs):
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
    def _safe_extract_table_data(cls, table_data: list[BeautifulSoup], index: int, return_type: Union[Callable[[str], Any], None] = None, return_text: bool = True) -> Optional[Any]:
        try:
            if return_text:
                value = table_data[index].text.strip()
                if value:
                    if callable(return_type):
                        return return_type(value)
                    else:
                        return value
                else:
                    return None
            else:
                return table_data[index]
        except (IndexError, AttributeError, TypeError):
            return None

    @classmethod
    def _safe_extract_ids_from_table(cls, extract_index, row_data, return_single=True):
        data = cls._safe_extract_table_data(row_data, extract_index, return_text=False)

        if data is not None:
            try:
                links = data.find_all('a', href=True)
                ids = [cls._get_id_from_url(link['href']) for link in links]
                if return_single:
                    return ids[0]
                else:
                    return ids
            except (IndexError, TypeError, KeyError):
                return None

        return None

    @classmethod
    def _get_element_by_text_in_information_box(cls, soup, text_search, return_text=True):
        selected_element = soup.select(f"div.InformationBoxTitle:-soup-contains('{text_search}') + div.InformationBoxContents")
        
        if selected_element:
            try:
                if return_text:
                    return selected_element[0].text.strip()

                return selected_element[0]
            except:
                logging.warning(f"An exception was raised when attempting to get the content of the elected element in _get_selected_element when searching for {text_search}")

        logging.info(f"No data was found when searching for {text_search}")
        return None

