from accessors.cagematch_accessor import CagematchAccessor
from data_classes.search_results import *
from data_classes.arrays import SearchResultArray

class CagematchSearchAccessor(CagematchAccessor):

    @classmethod
    def _safe_extract_data(cls, data, index, return_text=True):
        try:
            if return_text:
                if data[index].text.strip():
                    return data[index].text.strip()
                
                return None
            
            return data[index]
        
        except (IndexError, AttributeError, TypeError):
            return None

    @classmethod
    def _get_result_placement(cls, data):
        try:
            return int(cls._safe_extract_data(data, 0))

        except ValueError:
            return None
    
    @classmethod
    def _safe_extract_id(cls, extract_index, row_data):
        data = cls._safe_extract_data(row_data, extract_index, return_text=False)

        if data is not None:
            try:
                link = data.find('a', href=True)
                return cls._get_id_from_url(link['href'])
            
            except (IndexError, TypeError):
                return None

        return None
    
    @classmethod
    def search_wrestler(cls, search_text='', maximum_results=100):
        search_soup = cls._scrape_data(f"https://www.cagematch.net/?id=2&view=workers&search={search_text}")
        search_results_array_data = []
        
        for row in search_soup.find_all("tr")[1:]:
            row_data = row.find_all('td')
            search_results_array_data.append(cls._construct_wrestler_search_result(row_data))
            
        return SearchResultArray(search_results_array_data)
    
    @classmethod
    def _construct_wrestler_search_result(cls, row_data):
        construct_data = {}
        construct_data['result_id'] = cls._safe_extract_id(1, row_data)
        construct_data['result_placement'] = cls._get_result_placement(row_data)
        construct_data['gimmick'] = cls._safe_extract_data(row_data, 1)
        construct_data['birthday'] = cls._safe_extract_data(row_data, 2)
        construct_data['birthplace'] = cls._safe_extract_data(row_data, 3)
        construct_data['height'] = cls._safe_extract_data(row_data, 4)
        construct_data['weight'] = cls._safe_extract_data(row_data, 5)
        construct_data['promotion_id'] = cls._safe_extract_id(6, row_data)
        construct_data['rating'] = cls._safe_extract_data(row_data, 7)
        construct_data['votes'] = cls._safe_extract_data(row_data, 8)

        return WrestlerSearchResult(**construct_data)

