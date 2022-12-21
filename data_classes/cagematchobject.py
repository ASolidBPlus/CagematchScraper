from dataclasses import dataclass

@dataclass
class CagematchObject:

    def to_dict(self):
        def recursive_to_dict(obj):
            if isinstance(obj, CagematchObject):
                return obj.to_dict()

            elif isinstance(obj, list):
                return [recursive_to_dict(item) for item in obj]
            
            return obj

        return {attr: recursive_to_dict(value) for attr, value in vars(self).items()}
