from accessors.cagematch_wrestler_accessor import CagematchWrestlerAccessor
from accessors.cagematch_search_accessor import CagematchSearchAccessor

class Cagematch:
    
    @classmethod
    def get_wrestler(cls, cagematch_wrestler_id, search_result=None):
        return CagematchWrestlerAccessor.scrape_wrestler(cagematch_wrestler_id, search_result)

    @classmethod
    def search_wrestler(cls, maximum_pages=1, **kwargs):
        return CagematchSearchAccessor.scrape_search('wrestler', maximum_pages, **kwargs)
