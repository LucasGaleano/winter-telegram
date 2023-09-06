from dataclasses import dataclass
from weapon import Weapon, weapons
import random


@dataclass
class Location:
    name: str
    items: list[Weapon]
     
    def search(self):
        random.shuffle(self.items)
        return self.items.pop()



itemsHospital = random.choices(weapons,k=2)

locations = [Location('hospital', itemsHospital)]

def find_location_by_name(location_name):
    return [location for location in locations if location.name.lower() == location_name.lower()][0]


@dataclass
class Community:
    survivors: list
    zombies: list
    food: list

    def pass_night(self):
        for survivor in self.survivors:
            survivor.eat(self.food)
