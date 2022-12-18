from accessors.cagematch_wrestler_accessor import CagematchWrestlerAccessor
from accessors.cagematch_search_accessor import CagematchSearchAccessor


class Cagematch:
    def __init__(self) -> None:
        self.__wrestler_access = CagematchWrestlerAccessor()
        self.__search_access = CagematchSearchAccessor()
        self.__event_access = None
        self.__match_access = None

    def get_wrestler(self, cagematch_wrestler_id):
        return self.__wrestler_access.scrape_wrestler(cagematch_wrestler_id)

