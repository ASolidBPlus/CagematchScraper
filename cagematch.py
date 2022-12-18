from cagematch_access import CagematchWrestlerAccess

class Cagematch:
    def __init__(self) -> None:
        __wrestler_access = CagematchWrestlerAccess()
        __event_access = None
        __match_access = None
        __error_handler = None

    def get_wrestler(self, cagematch_wrestler_id):
        return self.__wrestler_access.scrape_wrestler(cagematch_wrestler_id)