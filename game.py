from dataclasses import dataclass, field
from community import Community
from survivor import Survivor
from task import CurrentTask, Task
from narrative import Narrative
from location import Location
from items import Food

locations = {"hospital":Location(name='hospital', emoji='\U0001F3E5', items=[Food(amount=1,probability=60), Food(amount=1,probability=30), Food(amount=1,probability=20)]),
             "town":Location(name='pueblo', emoji='\U0001f3d8', items=[Food(amount=1,probability=60), Food(amount=1,probability=30), Food(amount=1,probability=20)])}

@dataclass
class Game():
    community: Community
    story: Narrative
    survivors: list[Survivor] = field(default_factory=list)


    def event_happen(self, taskCompleted:CurrentTask):

        match Task(taskCompleted.type):
            case Task.BUILD_BARRICADE:
                return self.task_builded_defense(taskCompleted.owner)
            
            case Task.TRAVEL:
                return self.task_arrived(taskCompleted.owner, taskCompleted.type.location)
            
            case Task.SEARCH:
                return self.task_searched(taskCompleted.owner)

            case _:
                return "Command not found!"

    def task_searched(self, survivorName: str):
        survivor = self.find_survivor_by_name(survivorName)
        item = survivor.search()
        match item:
            case Food():
                self.community.add_food(item.amount)
                return self.story.found_food(survivorName, item.amount)
            case None:
                return f"Nothing found at the {survivor.location.name}"
            case _:
                return "Command not found!"
        

    def task_arrived(self, survivorName: str, location:str):
        survivor = self.find_survivor_by_name(survivorName)
        survivor.location = locations[location]
        return f"Arrived to the {location}"

    def task_builded_defense(self, survivorName: str):
        print("Improved comunnity defense")
        self.community.build_defense(1)
        return self.story.finished_barricade(survivorName)

    def add_survivor(self, survivor:Survivor):
        self.survivors.append(survivor)
        print("New survivor", survivor.name, "joined")

    def find_survivor_by_name(self, name:str):
        for survivor in self.survivors:
            if survivor.name == name:
                return survivor
        return None
    
    def is_new_survivor(self, name:str):
        return  not bool(self.find_survivor_by_name(name))
    
    def get_status_community(self):
        return self.community.status()
    
    def show_status_community(self):
        return  f"Community\n \U0001f6a7: {self.community.defense} \U0001f96b: {self.community.food}"


