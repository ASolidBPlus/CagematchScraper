from dataclasses import dataclass
from cagematch.data_classes import cagematch_object, partial_cagematch_objects, arrays
from cagematch.global_utils import pair

@dataclass
class BaseParticipant:
    """A class representing a participant in a cagematch.

    This class is designed to be extended by the SingleParticipant and TeamParticipant classes.
    """
    name: str
    """The name of the participant."""
    manager: list
    """A list of managers for the participant."""
    notes: str
    """Notes about the participant."""
    champion: bool
    """A flag indicating whether the participant is a champion."""

    def __str__(self):
        """Return a string representation of the participant.

        This string will include the name, manager, champion status, and notes of the participant.
        """
        formatted_data = [data for data in [self._format_name(), self._format_manager(), self._format_champion(), self._format_notes()] if data]

        return " ".join(formatted_data)

    def _format_name(self):
        """Return the formatted name of the participant."""
        return self.name

    def _format_champion(self):
        """Return the formatted champion status of the participant."""
        if self.champion:
            return "(c)"
        
        return None

    def _format_manager(self):
        """Return the formatted manager of the participant."""
        if self.manager:
            return f"(w/ {pair(self.manager)})"

        return None

    def _format_notes(self):
        """Return the formatted notes for the participant."""
        if self.notes:
            return f"[{self.notes}]"

        return None


@dataclass
class SingleParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    """A class representing a single participant in a cagematch.

    This class extends the BaseParticipant class and implements the PartialCagematchObject interface.
    """

    def get_full_object(self):
        """Return the full object for this participant.

        This method is required by the PartialCagematchObject interface.
        """
        pass


@dataclass
class TeamParticipant(BaseParticipant, partial_cagematch_objects.PartialCagematchObject):
    """A class representing a team of participants in a cagematch.

    This class extends the BaseParticipant class and implements the PartialCagematchObject interface.
    """
    members: list
    """A list of members in the team."""

    def _format_name(self):
        """Return the formatted name of the team.

        If a name is provided, it will be used and the names of the team members will be appended in parentheses. 
        Otherwise, the names of the team members will be used.
        """
        if self.name:
            return f"{self.name} ({pair(self.members)})"
        
        return pair(self.members)

    def get_full_object(self):
        """Return the full object for this team.

        This method is required by the PartialCagematchObject interface.
        """
        pass


@dataclass
class Match(cagematch_object.CagematchObject):
    """A class representing a match in a cagematch.

    This class extends the CagematchObject class and includes information about the type of match, participants, 
    match notes, winning participants, special match result, and whether there was a title change.
    """
    match_type: str
    """The type of match (e.g. singles, tag team, etc.)."""
    participants: list
    """A list of participants in the match."""
    match_notes: str
    """Notes about the match."""
    winning_participants: list
    """A list of the winning participants in the match."""
    special_match_result: str
    """A special result for the match (e.g. DQ, countout, etc.)."""
    title_change: bool
    """A flag indicating whether there was a title change in the match."""

    def _format_participants(self, join_str, participant_type = None):
        """Return a string of the formatted participants in the match.

        Args:
            join_str (str): The string to join the formatted participants with.
            participant_type (str, optional): The type of participants to include. Can be 'losing', 'winning', or None 
                (default) to include all participants.
        
        Returns:
            str: A string of the formatted participants in the match.
        """
        if participant_type == 'losing':
            working_participants = [participant for participant in self.participants if participant not in self.winning_participants]

        elif participant_type == 'winning':
            working_participants = [participant for participant in self.participants if participant in self.winning_participants]
  
        else:
            working_participants = self.participants
        
        return join_str.join(str(working_participant) for working_participant in working_participants)

    def get_match_fixture(self):
        """Return a string of the match fixture.

        The match fixture is a string representation of the participants in the match, separated by " vs. ".
        
        Returns:
            str: A string of the match fixture.
        """
        return self._format_participants(" vs. ")
    
    def get_result_fixture(self):
        """Return a string of the result fixture.

        The result fixture is a string representation of the result of the match, including the match fixture, special 
        match result (if applicable), and whether there was a title change (if applicable).
        
        Returns:
            str: A string of the result fixture.
        """
        if self.special_match_result in ['No Contest', 'Draw']:
            return f"{self.get_match_fixture()} - {self.special_match_result}"

        formatted_losing_partitipants = self._format_participants(' and ', 'losing')
        formatted_winning_participants = self._format_participants(' and ', 'winning')

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
