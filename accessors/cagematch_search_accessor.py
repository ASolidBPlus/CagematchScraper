import re
import logging
from accessors.cagematch_accessor import CagematchAccessor
from data_classes.search_results import *
from data_classes.arrays import SearchResultArray

class CagematchSearchAccessor(CagematchAccessor):

    @classmethod
    def _get_result_placement(cls, data):
        try:
            return int(cls._safe_extract_table_data(data, 0))

        except ValueError:
            return None

    @classmethod
    def _get_search_result_amount(cls, soup):
        table_header = soup.find('div', class_='TableHeaderOff')
        
        if table_header is not None:
            match = re.search(r'(\d+) items', table_header.text)
            
            if match:
                third_number = match.group(1)
                
                return int(third_number)
    
    @classmethod
    def _handle_search(cls, url, maximum_pages=1):
        base_search_soup = cls._scrape_data(url)
        search_amount = cls._get_search_result_amount(base_search_soup)
        
        search_soups = [base_search_soup]
        
        if search_amount > 100 and maximum_pages > 1:
            logging.info("More pages needs to be scraped for the search result")
            
            if search_amount > maximum_pages * 100:
                max_page_range = maximum_pages
                               
            else:
                max_page_range = search_amount // 100
                
            for page in range(1, max_page_range):
                print(page * 100)
                search_soups.append(cls._scrape_data(f"{url}&s={page *100}"))
                

        return search_soups
        
    @classmethod
    def search_wrestler(cls, search_text='', maximum_pages=1):
        search_soups = cls._handle_search(f"https://www.cagematch.net/?id=2&view=workers&search={search_text}", maximum_pages)
                        
        results = []
        for search_soup in search_soups:
            results.extend([cls._construct_wrestler_search_result(row_data) for row_data in cls._separate_row_data(search_soup)])
            
        return SearchResultArray(results)
    
    @classmethod
    def _construct_wrestler_search_result(cls, row_data):
        construct_data = {}
        construct_data['cagematch_id'] = cls._safe_extract_id_from_table(1, row_data)
        construct_data['result_placement'] = cls._get_result_placement(row_data)
        construct_data['gimmick'] = cls._safe_extract_table_data(row_data, 1)
        construct_data['birthday'] = cls._safe_extract_table_data(row_data, 2)
        construct_data['birthplace'] = cls._safe_extract_table_data(row_data, 3)
        construct_data['height'] = cls._safe_extract_table_data(row_data, 4)
        construct_data['weight'] = cls._safe_extract_table_data(row_data, 5)
        construct_data['promotion_id'] = cls._safe_extract_id_from_table(6, row_data)
        construct_data['rating'] = cls._safe_extract_table_data(row_data, 7)
        construct_data['votes'] = cls._safe_extract_table_data(row_data, 8)

        return WrestlerSearchResult(**construct_data)

