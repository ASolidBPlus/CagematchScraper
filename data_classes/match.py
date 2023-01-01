from dataclasses import dataclass
from data_classes import cagematch_object
from data_classes import arrays
from data_classes import partial_cagematch_objects

@dataclass
class BaseParticipant:
    name: str
    notes: str
    manager: list

@dataclass
class WrestlerParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    def get_full_object(self):
        pass

@dataclass
class TeamParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    members: list(WrestlerParticipant)

    def get_full_object(self):
        pass


class MatchParticipantsArray(arrays.ConvertableObjectArray):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._match = None

    def register_match(self, match):
        self._match = match

    def get_participants_str(self):
        if len(self._match.participants) > 1:
            # Logic to return string representing the participants in this array as team members
            return

        elif len(self._match.participants) == 1:
            # Logic to return string representing the participants in this array as opponents
            return

        else:
            raise ValueError("Participants not registered correctly.")

@dataclass
class Match(cagematch_object.CagematchObject):
    match_type: str
    participants: list(MatchParticipantsArray)    
    match_notes: str

    def __post_init__(self):
        for participant in self.participants:
            participant.register_match(self)
