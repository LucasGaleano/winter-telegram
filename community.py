from dataclasses import dataclass, field

@dataclass
class Community:
    food: int = 0
    defense: int = 0
    emoji: str= '\U0001F3DA'
    #survivors: list = field(default_factory=list)
    #zombies: list = field(default_factory=list)


    def build_defense(self, amount:int):
        self.defense += amount

    def add_food(self, amount:int):
        self.food += amount

    def eat_food(self, amount:int):
        self.food -= amount

    def status(self):
        return {"defense":self.defense,
                "food":self.food}




