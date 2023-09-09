from dataclasses import dataclass, field
#from weapon import Weapon, weapons
import random
from items import Food


@dataclass
class Location:
    name: str
    items: list[Food] = field(default_factory=list)
       
    def search(self):
        chance = random.randint(1,10)
        if chance > 8:
            return random.choices(self.items, weights=[item.probability for item in self.items])[0]
        return None
