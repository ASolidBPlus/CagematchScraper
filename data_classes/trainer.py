import cagematch
from dataclasses import dataclass
from data_classes.cagematch_object import CagematchObject
from data_classes.partial_cagematch_objects import PartialCagematchObject

@dataclass
class Trainer(PartialCagematchObject):
    name: str
    
    def get_full_object(self):
        return cagematch.get_wrestler(self.cagematch_id)