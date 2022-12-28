from dataclasses import dataclass
from data_classes.cagematch_object import CagematchObject
from data_classes.arrays import TrainerArray

@dataclass
class Wrestler(CagematchObject):
    cagematch_wrestler_id: int
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
    beginning_of_in_ring_career: str
    in_ring_experience: str
    wrestling_style: list
    trainers: TrainerArray
    nicknames: list
    signature_moves: list