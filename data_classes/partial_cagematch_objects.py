from abc import ABC, abstractmethod
from .cagematchobject import CagematchObject
from dataclasses import dataclass
import cagematch

@dataclass
class BasePartialCagematchObject(CagematchObject):
    cagematch_id: int


class PartialCagematchObject(ABC, BasePartialCagematchObject):

    @abstractmethod
    def get_full_object(self):
        pass


class PartialWrestlerCagematchObject(PartialCagematchObject):
    
    def get_full_object(self):
        return cagematch.Cagematch.get_wrestler(self.cagematch_id)