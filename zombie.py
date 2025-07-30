from dataclasses import dataclass, field
from location import Location
from items import Weapon
from survivor import Person

@dataclass
class Zombie(Person):
    name: str = "Zombie"
    level: int = 1
    #skills: dict = field(default_factory=dict)
    # items: list = field(default_factory=list)
    # weaponExperience: dict = field(default_factory=dict)
    # experienceByWeapon: int = 10
    # status: str = 'Resting...'

    def __post_init__(self):
        self.weapon = Weapon(level=self.level)
        self.health = self.level

    
    def search(self):
        if self.location:
            return self.location.search()
        return None
    
    def show_location(self):
        return f"{self.location.emoji} - {self.name} at the {self.location.name}"