from dataclasses import dataclass
from cagematch.data_classes.partial_cagematch_objects import PartialCagematchObject
import cagematch

@dataclass
class Trainer(PartialCagematchObject):
    name: str
    
    def get_full_object(self):
        return cagematch.get_wrestler(self.cagematch_id)

        