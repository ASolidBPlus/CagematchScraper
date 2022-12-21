from accessors.cagematch_wrestler_accessor import CagematchWrestlerAccessor
from accessors.cagematch_search_accessor import CagematchSearchAccessor
import multiprocessing

class Cagematch:
    
    @classmethod
    def get_wrestler(cls, cagematch_wrestler_id, search_result=None):
        return CagematchWrestlerAccessor.scrape_wrestler(cagematch_wrestler_id, search_result)

    @classmethod
    def search_wrestler(cls, text=None):
        return CagematchSearchAccessor.search_wrestler(text)

if __name__ == '__main__':
    Cagematch()
