import re
import logging
from accessors.cagematch_accessor import CagematchAccessor
from data_classes.search_results import *
from data_classes.arrays import SearchResultArray

class CagematchSearchAccessor(CagematchAccessor):

    @classmethod
    def _get_result_placement(cls, data):
        return cls._safe_extract_table_data(data, 0, int)
        
    @classmethod
    def _get_rating_from_table(cls, data, index):
        try:
            return float(cls._safe_extract_table_data(data, index))

        except (ValueError, TypeError):
            return None

    @classmethod
    def _get_votes_from_table(cls, data, index):
        try:
            return int(cls._safe_extract_table_data(data, index))
        
        except (ValueError, TypeError):
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
    def _get_event_promotions_involved(cls, soup):
        row_url_ids = cls._safe_extract_ids_from_table(2, soup, False)

        if len(row_url_ids) > 1:
            return row_url_ids[:-1]

        return None

    @classmethod
    def _get_event_cagematch_id(cls, soup):
        row_url_ids = cls._safe_extract_ids_from_table(2, soup, False)

        if row_url_ids is not None:
            return row_url_ids[-1]

    
    @classmethod
    def _handle_search(cls, search_url, maximum_pages=1):
        logging.info(f"Searching using base URL: {search_url}")
        base_search_soup = cls._scrape_data(search_url)
        search_amount = cls._get_search_result_amount(base_search_soup)
        
        search_soups = [base_search_soup]

        if search_amount is not None:
            if search_amount > 100 and maximum_pages > 1:
                logging.info("More pages needs to be scraped for the search result")
                
                if search_amount > maximum_pages * 100:
                    max_page_range = maximum_pages
                                
                else:
                    max_page_range = search_amount // 100
                    
                for page in range(1, max_page_range):
                    search_soups.append(cls._scrape_data(f"{search_url}&s={page *100}"))

        return search_soups

    @classmethod
    def _construct_wrestler_search_result(cls, row_data):
        construct_data = {}
        construct_data['cagematch_id'] = cls._safe_extract_ids_from_table(1, row_data)
        construct_data['result_placement'] = cls._get_result_placement(row_data)
        construct_data['gimmick'] = cls._safe_extract_table_data(row_data, 1)
        construct_data['birthday'] = cls._safe_extract_table_data(row_data, 2)
        construct_data['birthplace'] = cls._safe_extract_table_data(row_data, 3)
        construct_data['height'] = cls._safe_extract_table_data(row_data, 4)
        construct_data['weight'] = cls._safe_extract_table_data(row_data, 5)
        construct_data['promotion_id'] = cls._safe_extract_ids_from_table(6, row_data)
        construct_data['rating'] = cls._get_rating_from_table(row_data, 7)
        construct_data['votes'] = cls._get_votes_from_table(row_data, 8)

        return WrestlerSearchResult(**construct_data)

    @classmethod
    def _construct_event_search_result(cls, row_data):
        construct_data = {}
        construct_data['cagematch_id'] = cls._get_event_cagematch_id(row_data)
        construct_data['result_placement'] = cls._get_result_placement(row_data)
        construct_data['date'] = cls._safe_extract_table_data(row_data, 1)
        construct_data['promotions_involved'] = cls._get_event_promotions_involved(row_data)
        construct_data['event_name'] = cls._safe_extract_table_data(row_data, 2)
        construct_data['location'] = cls._safe_extract_table_data(row_data, 3)
        construct_data['rating'] = cls._safe_extract_table_data(row_data, 6, float)
        construct_data['votes'] = cls._safe_extract_table_data(row_data, 7, int)

        return EventSearchResult(**construct_data)

    @classmethod
    def scrape_search(cls, search_type, maximum_pages=1, **kwargs):
        search_type_mapping = {
            'wrestler': {'id': 2, 'view': 'workers'},
            'event': {'id': 1, 'view': 'search'}
        }

        construct_result_mapping = {
        'wrestler': cls._construct_wrestler_search_result,
        'event': cls._construct_event_search_result
        }

        search_params = search_type_mapping.get(search_type)
        construct_result_method = construct_result_mapping.get(search_type)

        if search_params is None or construct_result_method is None:
            raise ValueError(f"Invalid search type: {search_type}. This could mean the provided search type has no search parameters, construct method, or both.")

        search_soups = cls._handle_search(cls._build_url(**search_params, **kwargs), maximum_pages)
                        
        results = []

        for search_soup in search_soups:
            results.extend([construct_result_method(row_data) for row_data in cls._separate_row_data(search_soup)])
            
        return SearchResultArray(results, **kwargs)
