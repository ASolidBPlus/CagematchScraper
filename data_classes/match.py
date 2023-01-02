from dataclasses import dataclass
from data_classes import cagematch_object
from data_classes import arrays
from data_classes import partial_cagematch_objects

@dataclass
class BaseParticipant:
    name: str
    manager: list
    notes: str


@dataclass
class SingleParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    def get_full_object(self):
        pass


@dataclass
class TeamParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    members: list(SingleParticipant)

    def get_full_object(self):
        pass


class MatchParticipantsArray(arrays.ConvertableObjectArray):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._match = None

    def register_match(self, match):
        self._match = match

    def get_participants_str(self):
        if self._match is not None:
            if len(self) > 1:
                # Multiple participants in this array, representing a team
                # Team formatting logic goes here
                pass
            elif len(self) == 1:
                # Single participant in this array, representing an opponent
                # Opponent formatting logic goes here
                pass
            else:
                raise ValueError("Participants not registered correctly.")
        else:
            raise ValueError("Match not registered with participants.")

@dataclass
class Match(cagematch_object.CagematchObject):
    match_type: str
    participants: list(MatchParticipantsArray)    
    match_notes: str

    def __post_init__(self):
        for participant in self.participants:
            participant.register_match(self)
