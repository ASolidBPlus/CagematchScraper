from dataclasses import dataclass
from cagematch.data_classes import cagematch_object, partial_cagematch_objects, arrays
from cagematch.global_utils import pair

@dataclass
class BaseParticipant:
    name: str
    manager: list
    notes: str
    champion: bool

    def __str__(self):
        formatted_data = [data for data in [self._format_name(), self._format_manager(), self._format_champion(), self._format_notes()] if data]

        return " ".join(formatted_data)

    def _format_name(self):
        return self.name

    def _format_champion(self):
        if self.champion:
            return "(c)"
        
        return None

    def _format_manager(self):
        if self.manager:
            return f"(w/ {pair(self.manager)})"

        return None

    def _format_notes(self):
        if self.notes:
            return f"[{self.notes}]"

        return None


@dataclass
class SingleParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):

    def get_full_object(self):
        pass


@dataclass
class TeamParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    members: list

    def _format_name(self):
        return f"{self.name} ({pair(self.members)})"

    def get_full_object(self):
        pass


@dataclass
class Match(cagematch_object.CagematchObject):
    match_type: str
    participant_blocks: list
    match_notes: str
    winning_participants: list
    special_match_result: str
    title_change: bool

    def _format_participant_blocks(self, join_str, participant_type = None):
        if participant_type == 'losing':
            working_participants = [participant for participant in self.participant_blocks if participant not in self.winning_participants]

        elif participant_type == 'winning':
            working_participants = [participant for participant in self.participant_blocks if participant in self.winning_participants]

        else:
            working_participants = self.participant_blocks

        formatted_participant_blocks = []
        
        if len(working_participants) > 1:
            for participant_block in working_participants:
                formatted_participant_blocks.append(pair(participant_block))

        elif len(working_participants) == 1 and len(self.participant_blocks) == 1:
            formatted_participant_blocks += working_participants

        elif len(working_participants) == 1 and len(self.participant_blocks) > 1:
            formatted_participant_blocks.append(pair(working_participants))
        
        return join_str.join(str(formatted_participant) for formatted_participant in formatted_participant_blocks)

    def get_match_fixture(self):
        return self._format_participant_blocks(" vs. ")
    
    def get_result_fixture(self):
        if self.special_match_result in ['No Contest', 'Draw']:
            return f"{self.get_match_fixture()} - {self.special_match_result}"

        formatted_losing_partitipants = self._format_participant_blocks(' and ', 'losing')
        formatted_winning_participants = self._format_participant_blocks(' and ', 'winning')

        result = f"{formatted_winning_participants} defeats {formatted_losing_partitipants}"
                
        if self.special_match_result in ['DQ', 'Countout']:
            result = f"{result} By {self.special_match_result}"

        if self.title_change:
            result = f"{result} (Title Change)"
            
        return result

    def to_dict(self, **kwargs):
        dict_data = {}
        dict_data['match_fixture'] = self.get_match_fixture()
        dict_data['result_fixture'] = self.get_result_fixture()
        
        dict_data.update(**kwargs)
        
        return super().to_dict(**dict_data)
