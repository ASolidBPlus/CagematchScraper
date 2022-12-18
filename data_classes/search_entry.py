from dataclasses import dataclass
from data_classes.cagematchobject import CagematchObject

# Building Block Classes
# Shared attributes that all the "main" classes use
@dataclass
class SearchEntry(CagematchObject):
    entry_type: str
    search_id: int
    result_placement: int

@dataclass
class RatingsEntry(SearchEntry):
    rating: float
    votes: int

@dataclass
class DateEntry(SearchEntry):
    date: str

@dataclass
class LocationEntry(SearchEntry):
    location: str

@dataclass
class MembersEntry(SearchEntry):
    members: list

@dataclass
class PromotionIdEntry(SearchEntry):
    id: int

@dataclass
class MatchTypeEntry(SearchEntry):
    match_type: str

@dataclass
class EventNameEntry(SearchEntry):
    event_name: str

# Main Search Classes
@dataclass
class WrestlerSearchEntry(RatingsEntry, PromotionIdEntry):
    gimmick: str
    birthday: str
    birthplace: str
    height: int
    weight: int

@dataclass
class EventSearchEntry(DateEntry, RatingsEntry, EventNameEntry):
    pass

@dataclass
class MatchguideSearchEntry(DateEntry, PromotionIdEntry, RatingsEntry, MatchTypeEntry):
    match_fixture: str
    won: str

@dataclass
class AdvancedMatchSearchEntry(DateEntry, PromotionIdEntry, LocationEntry, EventNameEntry):
    match: str

@dataclass
class PromotionSearchEntry(PromotionIdEntry, LocationEntry, RatingsEntry):
    name: str
    years: str

@dataclass
class TitleSearchEntry(PromotionIdEntry, RatingsEntry):
    title: str
    status: str

@dataclass
class TagTeamSearchEntry(MembersEntry, RatingsEntry):
    most_popular_name: str

@dataclass
class StableSearchEntry(MembersEntry, RatingsEntry):
    name: str
    active_time: str

@dataclass
class TournamentSearchEntry(PromotionIdEntry, RatingsEntry):
    title: str
    timeframe: str
    winners: list