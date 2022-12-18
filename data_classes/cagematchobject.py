from dataclasses import dataclass

@dataclass
class CagematchObject:
    def read_stats(self):
        stats = []
        for attr, value in vars(self).items():
            attr_name = attr.title()
            stats.append(attr_name + ": " + str(value))
            
        return "\n".join(stats)

    def to_dict(self):
        def recursive_to_dict(obj):
            if isinstance(obj, CagematchObject):
                return obj.to_dict()

            elif isinstance(obj, list):
                return [recursive_to_dict(item) for item in obj]
            
            else:
                return obj

        return {attr: recursive_to_dict(value) for attr, value in vars(self).items()}



            