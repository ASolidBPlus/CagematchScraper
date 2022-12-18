from dataclasses import dataclass

@dataclass
class CagematchObject:
    def read_stats(self):
        stats = []
        for attr, value in vars(self).items():
            attr_name = attr.title()
            stats.append(attr_name + ": " + str(value))
            
        return "\n".join(stats)