from dataclasses import dataclass, field
from community import Community
from survivor import Survivor
from task import CurrentTask, Task
from narrative import Narrative
from location import Location
from items import Food

locations = {"hospital":Location('hospital', [Food(amount=1,probability=60), Food(amount=1,probability=30), Food(amount=1,probability=20)])}

@dataclass
class Game():
    community: Community
    story: Narrative
    survivors: list[Survivor] = field(default_factory=list)


    def event_happen(self, taskCompleted:CurrentTask):

        match Task(taskCompleted.type):
            case Task.BUILD_BARRICADE:
                return self.task_build_defense(taskCompleted.owner)
            
            case Task.TRAVELHOSPITAL:
                return self.task_travel(taskCompleted.owner)
            
            case Task.SEARCH:
                return self.task_search(taskCompleted.owner)

            case _:
                return "Command not found!"

    def task_search(self, survivorName: str):
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
        

    def task_travel(self, survivorName: str):
        survivor = self.find_survivor_by_name(survivorName)
        survivor.location = locations["hospital"]
        return "travel"

    def task_build_defense(self, survivorName: str):
        print("Improved comunnity defense")
        self.community.build_defense(1)
        return self.story.finished_barricade(survivorName)

    def add_survivor(self, survivor:Survivor):
        self.survivors.append(survivor)
        print("New survivor", survivor.name)

    def find_survivor_by_name(self, name:str):
        for survivor in self.survivors:
            if survivor.name == name:
                return survivor
        return None
    
    def is_new_survivor(self, name:str):
        return  not bool(self.find_survivor_by_name(name))
    
    def get_status_community(self):
        return self.community.status()


