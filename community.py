from dataclasses import dataclass, field

@dataclass
class Community:
    food: int = 0
    defense: int = 0
    #survivors: list = field(default_factory=list)
    #zombies: list = field(default_factory=list)


    def build_defense(self, amount:int):
        self.defense += amount

    def status(self):
        return {"defense":self.defense,
                "food":self.food}



