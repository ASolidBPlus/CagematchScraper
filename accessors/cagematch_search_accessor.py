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
        pass
    
    @classmethod
    def search_wrestler(cls, search_text='', maximum_pages=1):
        search_soup = cls._scrape_data(f"https://www.cagematch.net/?id=2&view=workers&search={search_text}")
        # print(cls._get_selected_element("TableHeaderOff", search_soup, "Displaying"))
            
        return SearchResultArray([cls._construct_wrestler_search_result(row_data) for row_data in cls._separate_row_data(search_soup)])
    
    @classmethod
    def _construct_wrestler_search_result(cls, row_data):
        construct_data = {}
        construct_data['result_id'] = cls._safe_extract_id_from_table(1, row_data)
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

