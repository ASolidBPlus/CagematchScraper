from dataclasses import dataclass
from data_classes.cagematchobject import CagematchObject

@dataclass
class Trainer(CagematchObject):
    name: str
    cagematch_id: int
