from dataclasses import dataclass
from cagematch import *
from data_classes.cagematchobject import CagematchObject
from data_classes.partialcagematchobject import PartialCagematchObject

@dataclass
class Trainer(PartialCagematchObject):
    name: str
    cagematch_id: int

    def get_full_object(self):
        return Cagematch.get_wrestler(self.cagematch_id)