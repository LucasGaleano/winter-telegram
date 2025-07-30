from dataclasses import dataclass, field
from community import Community
from survivor import Survivor
from zombie import Zombie
from task import CurrentTask, Task
from narrative import Narrative
from location import Location
from items import Food
from time import time
import random


locations = {"hospital": Location(name='Hospital', emoji='\U0001F3E5', items=[Food(amount=1, probability=60), Food(amount=2, probability=30), Food(amount=3, probability=20)]),
             "town": Location(name='Town', emoji='\U0001f3d8', items=[Food(amount=1, probability=60), Food(amount=2, probability=30), Food(amount=3, probability=20)])}


@dataclass
class Game():
    community: Community
    story: Narrative
    survivors: list[Survivor] = field(default_factory=list)
    locationsFound: dict[str:Location] = field(default_factory=dict)
    timeStarted: float = field(default_factory=time)

    def event_happen(self, taskCompleted: CurrentTask):

        match Task(taskCompleted.type):
            case Task.BUILD_BARRICADE:
                return self.task_builded_defense(taskCompleted.owner)

            case Task.TRAVEL:
                return self.task_arrived(taskCompleted.owner, taskCompleted.type.location)

            case Task.SEARCH:
                return self.task_searched(taskCompleted.owner)

            case Task.EXPLORE:
                return self.task_explored(taskCompleted.owner)

            case _:
                return "Command not found!"

    def task_searched(self, survivorName: str):
        survivor = self.find_survivor_by_name(survivorName)
        item = survivor.search()
        match item:
            case Food():
                self.community.add_food(item.amount)
                # TODO Add event depending of the noise acumulate in the place.
                # TODO Add fight between survivor and zombies.
                return self.story.found_food(survivorName, item.amount)
            case None:
                return f"Nothing found at the {survivor.location.name}"
            case _:
                return "Command not found!"

    def task_arrived(self, survivorName: str, location: str):
        survivor = self.find_survivor_by_name(survivorName)
        survivor.location = locations[location]
        return f"{survivorName} arrived to the {location}"

    def task_builded_defense(self, survivorName: str):
        print("Improved comunnity defense")
        self.community.build_defense(1)
        return self.story.finished_barricade(survivorName)
    
    def time_lapsed(self) -> int:
        return int(time() - self.timeStarted)

    def task_explored(self, survivorName: str):        
        newLocation = self.finding_place()
        match newLocation:
            case Location():
                self.locationsFound[newLocation.name] = newLocation
                return f"{survivorName} came across with a {newLocation.name}"
            case None:
                return ""
    
    def finding_place(self):
        newLocation = None
        if self.dice_more_than(5):
            locationsNotFound = locations.keys() - self.locationsFound.keys()
            if locationsNotFound:
                newLocation = locations[random.choice(list(locationsNotFound))]
        return newLocation
    
    def dice_more_than(self, amountSuccess: int, diceFaces: int=20):
        return random.choice(range(diceFaces)) >= amountSuccess

    def add_survivor(self, survivor: Survivor):
        self.survivors.append(survivor)
        print("New survivor", survivor.name, "joined")

    def find_survivor_by_name(self, name: str):
        for survivor in self.survivors:
            if survivor.name == name:
                return survivor
        return None

    def is_new_survivor(self, name: str):
        return not bool(self.find_survivor_by_name(name))

    def get_status_community(self):
        return self.community.status()

    def show_status_community(self):
        return f"Community\n \U0001f6a7: {self.community.defense} \U0001f96b: {self.community.food}"

    def battle(self, survivors: list[Survivor], zombies: list[Zombie])-> str:
        battlelog = ''
        
        while any(survivor.is_ok() for survivor in survivors) and any(zombie.is_ok() for zombie in zombies):
            survivorsAlive = [survivor for survivor in survivors if survivor.is_ok()]
            zombiesAlive = [zombie for zombie in zombies if zombie.is_ok()]
            grupo1, grupo2 = random.sample([survivorsAlive,zombiesAlive],2)
            enemy1 = random.choice(grupo1)
            enemy2 = random.choice(grupo2)
            battlelog += f'{enemy1.attack(enemy2)}\n'
            if enemy2.is_death():
                battlelog += f'{enemy2.name} is incapable to fight anymore\n'

        return battlelog

            
