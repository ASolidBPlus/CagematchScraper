from dataclasses import dataclass
from data_classes.cagematchobject import CagematchObject

@dataclass
class Wrestler(CagematchObject):
    main_name: str
    alter_egos: list
    dob: str
    birthplace: str
    gender: str
    height: float
    weight: float
    background_in_sports: list
    social_media_links: list
    roles: list
    wrestling_style: list
    trainers: list
    nicknames: list
    signature_moves: list

    def __str__(self):
        return self.main_name
    