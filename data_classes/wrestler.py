from dataclasses import dataclass

@dataclass
class Wrestler:
    main_name: str
    alter_egos: list
    dob: str
    birthplace: str
    gender: str
    height: float
    weight: float
    background_in_sports: list
    social_media_links: list
    roles: list
    wrestling_style: list
    trainers: list
    nicknames: list
    signature_moves: list

    def __str__(self):
        return self.main_name

    def lbs(self):
        return self.weight * 2.20462

    def ft(self):
        return height / 2.54
    