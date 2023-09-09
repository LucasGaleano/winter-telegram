from dataclasses import dataclass, field


@dataclass
class Item():
    name: str
    probability: int = 50

@dataclass
class Food(Item):
    name:str = 'food'
    amount: int = 1