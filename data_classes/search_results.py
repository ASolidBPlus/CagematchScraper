from dataclasses import dataclass
from data_classes.cagematchobject import *
from abc import ABC, abstractmethod
import cagematch
# Building Block Classes
# Shared attributes that all the "main" classes use
@dataclass
class BaseSearchEntry(CagematchObject):
    result_id: int
    result_placement: int


@dataclass
class RatingsEntry(BaseSearchEntry):
    rating: float
    votes: int


@dataclass
class DateEntry(BaseSearchEntry):
    date: str


@dataclass
class LocationEntry(BaseSearchEntry):
    location: str


@dataclass
class MembersEntry(BaseSearchEntry):
    members: list


@dataclass
class PromotionIdEntry(BaseSearchEntry):
    promotion_id: int


@dataclass
class MatchTypeEntry(BaseSearchEntry):
    match_type: str


@dataclass
class EventNameEntry(BaseSearchEntry):
    event_name: str

# Main Search Classes
# Classes that search methods will be built around

@dataclass
class SearchResult(ABC):
    @abstractmethod
    def get_full_object(self):
        pass


@dataclass
class WrestlerSearchResult(SearchResult, RatingsEntry, PromotionIdEntry):
    gimmick: str
    birthday: str
    birthplace: str
    height: int
    weight: int

    def get_full_object(self):
        return cagematch.Cagematch.get_wrestler(self.result_id, self)



@dataclass
class EventSearchResult(SearchResult, DateEntry, RatingsEntry, EventNameEntry):
    pass


@dataclass
class MatchguideSearchResult(SearchResult, DateEntry, PromotionIdEntry, RatingsEntry, MatchTypeEntry):
    match_fixture: str
    won: str


@dataclass
class AdvancedMatchSearchResult(SearchResult, DateEntry, PromotionIdEntry, LocationEntry, EventNameEntry):
    match: str


@dataclass
class PromotionSearchResult(SearchResult, PromotionIdEntry, LocationEntry, RatingsEntry):
    name: str
    years: str


@dataclass
class TitleSearchResult(SearchResult, PromotionIdEntry, RatingsEntry):
    title: str
    status: str


@dataclass
class TagTeamSearchResult(SearchResult, MembersEntry, RatingsEntry):
    most_popular_name: str


@dataclass
class StableSearchResult(SearchResult, MembersEntry, RatingsEntry):
    name: str
    active_time: str


@dataclass
class TournamentSearchResult(SearchResult, PromotionIdEntry, RatingsEntry):
    title: str
    timeframe: str
    winners: list