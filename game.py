from dataclasses import dataclass, field
from community import Community
from survivor import Survivor
from task import CurrentTask, Task
from narrative import Narrative

@dataclass
class Game():
    community: Community
    story: Narrative
    survivors: list[Survivor] = field(default_factory=list)


    def event_happen(self, taskComplete:CurrentTask):

        match Task(taskComplete.type):
            case Task.BUILD_BARRICADE:
                print("Improved comunnity defense")
                self.community.build_defense(1)
                return self.story.finish_barricade(taskComplete.owner)

            case _:
                print("No command")

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


