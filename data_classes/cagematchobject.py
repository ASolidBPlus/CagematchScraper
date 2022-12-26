import json

class CagematchObject:
    
    def _recursive_to_dict(self, obj):
        if isinstance(obj, CagematchObject):
            return obj.to_dict()

        elif isinstance(obj, list):
            return [self._recursive_to_dict(item) for item in obj]
            
        return obj

    def to_dict(self):
        return {attr: self._recursive_to_dict(value) for attr, value in vars(self).items()}