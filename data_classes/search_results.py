from dataclasses import dataclass
from data_classes.partial_cagematch_objects import PartialCagematchObject
from data_classes.cagematch_object import CagematchObject
import cagematch

# Building Block Classes
# Shared attributes that all the "main" classes use
@dataclass
class BaseSearchEntry(CagematchObject):
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
class WrestlerSearchResult(PartialCagematchObject, RatingsEntry, PromotionIdEntry):
    gimmick: str
    birthday: str
    birthplace: str
    height: int
    weight: int
    
    def get_full_object(self):
        return cagematch.Cagematch.get_wrestler(self.cagematch_id, self)


@dataclass
class EventSearchResult(PartialCagematchObject, DateEntry, LocationEntry, RatingsEntry, EventNameEntry):
    
    promotions_involved: list

    def get_full_object(self):
        return None # Not implemented


@dataclass
class MatchguideSearchResult(PartialCagematchObject, DateEntry, PromotionIdEntry, RatingsEntry, MatchTypeEntry):
    match_fixture: str
    won: str

    def get_full_object(self):
        return None # Not implemented


@dataclass
class AdvancedMatchSearchResult(PartialCagematchObject, DateEntry, PromotionIdEntry, LocationEntry, EventNameEntry):
    match: str

    def get_full_object(self):
        return None # Not implemented


@dataclass
class PromotionSearchResult(PartialCagematchObject, PromotionIdEntry, LocationEntry, RatingsEntry):
    promotion_name: str
    years: str

    def get_full_object(self):
        return None # Not implemented


@dataclass
class TitleSearchResult(PartialCagematchObject, PromotionIdEntry, RatingsEntry):
    title: str
    status: str

    def get_full_object(self):
        return None # Not implemented


@dataclass
class TagTeamSearchResult(PartialCagematchObject, MembersEntry, RatingsEntry):
    most_popular_name: str

    def get_full_object(self):
        return None # Not implemented


@dataclass
class StableSearchResult(PartialCagematchObject, MembersEntry, RatingsEntry):
    stable_name: str
    active_time: str

    def get_full_object(self):
        return None # Not implemented


@dataclass
class TournamentSearchResult(PartialCagematchObject, PromotionIdEntry, RatingsEntry):
    title: str
    timeframe: str
    winners: list

    def get_full_object(self):
        return None # Not implemented
