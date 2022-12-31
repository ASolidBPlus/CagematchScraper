from accessors.cagematch_wrestler_accessor import CagematchWrestlerAccessor
from accessors.cagematch_search_accessor import CagematchSearchAccessor

    
def get_wrestler(cagematch_wrestler_id, search_result=None):
    return CagematchWrestlerAccessor.scrape_wrestler(cagematch_wrestler_id, search_result)

def search_wrestler(maximum_pages=1, **kwargs):
    return CagematchSearchAccessor.scrape_search('wrestler', maximum_pages, **kwargs)

def search_event(maximum_pages=1, **kwargs):
    """
    Search for events using the specified search parameters. These parameters are taken directly from cagematch.net and work just like a cagematch.net event search.

    Parameters:
    - maximum_pages (int): The maximum number of pages to scrape. Default is 1.
    - sEventName (str): The name of the event to search for.
    - sPromotion (int): The ID of the promotion to search for.
    - sDateFromDay (int or str): The day of the start date to search for.
    - sDateFromMonth (int or str): The month of the start date to search for.
    - sDateFromYear (int or str): The year of the start date to search for. - Default is 1800 to ensure Cagematch Search returns all events irrespective of timeframe by default
    - sDateTillDay (int or str): The day of the end date to search for.
    - sDateTillMonth (int or str): The month of the end date to search for.
    - sDateTillYear (int or str): The year of the end date to search for.
    - sRegion (str): The region to search for.
    - sEventType (str): The type of event to search for.
    - sLocation (str): The location to search for.
    - sArena (str): The arena to search for.
    - sAny (str): A keyword to search for in the event name, promotion, location, and arena.

    Returns:
    - A list of event search results.
    """
    if kwargs.get('sDatefromYear') is None:
        return CagematchSearchAccessor.scrape_search('event', maximum_pages, sDateFromYear=1800, **kwargs)

    return CagematchSearchAccessor.scrape_search('event', maximum_pages, **kwargs)
