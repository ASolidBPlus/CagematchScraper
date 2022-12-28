from abc import ABC, abstractmethod
from .cagematch_object import CagematchObject
from dataclasses import dataclass

@dataclass
class BasePartialCagematchObject(CagematchObject):
    cagematch_id: int


class PartialCagematchObject(ABC, BasePartialCagematchObject):

    @abstractmethod
    def get_full_object(self):
        pass
