from abc import ABC, abstractmethod
from .cagematchobject import CagematchObject
from dataclasses import dataclass

@dataclass
class PartialCagematchObject(ABC, CagematchObject):

    @abstractmethod
    def get_full_object(self):
        pass
