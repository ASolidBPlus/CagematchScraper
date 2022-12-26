from dataclasses import dataclass
from data_classes.cagematchobject import CagematchObject
from data_classes.partial_cagematch_objects import PartialWrestlerCagematchObject

@dataclass
class Trainer(PartialWrestlerCagematchObject):
    name: str