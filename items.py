from dataclasses import dataclass, field
import random

@dataclass
class Item():
    name: str
    probability: int = 50

@dataclass
class Food(Item):
    name:str = 'food'
    amount: int = 1

@dataclass
class Weapon(Item):
    name:str = 'Weapon'
    level:int = 1
    attack: list[int] = field(default_factory=list)

    def __post_init__(self):
        levelremain = self.level
        for i in range(3):
            attackChoice = random.choice(range(levelremain))
            levelremain = max(levelremain - attackChoice, 0)
            self.attack.append(attackChoice)
        self.attack.append(levelremain)

    def damage(self):
        return random.choice(self.attack)

        

