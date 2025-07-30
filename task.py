from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime

TIME_ACTION = 10 #sec


@dataclass
class TaskType():
    name: str
    description: str
    emoji:str = None
    turns_required: float = 1
    location: str = None
    passive: bool = False

    def __eq__(self, other: object) -> bool:
        return self.name == other.name

    def json(self):
        return {
            "name" : self.name,
            "description":self.description,
            "emoji": self.emoji,
            "turns_required": self.turns_required,
            "location": self.location,
            "passive": self.passive
        }


class Task(Enum):
    BUILD_BARRICADE = TaskType(name="build", description="building a barricade", emoji="\U0001f6e0")
    TRAVEL = TaskType(name="travel", description="travelling", emoji="\U0001f697")
    SEARCH = TaskType(name="search", description="seeking supplies", passive=True, emoji="\U0001f50e")
    EXPLORE = TaskType(name="explore", description="exploring for new places", emoji="\U0001f5fa")

class Status(Enum):
    FINISH = 'finish'
    IN_PROGRESS = 'in progress'


@dataclass
class CurrentTask:
    owner: str
    type: TaskType
    time_end: float = 0
    time_start: float = 0
    status: Status = Status.IN_PROGRESS.value

    # def __init__(self, owner:str, type:TaskType):
    #     self.owner = owner
    #     self.type = type
    #     self.time_end = time.time() + TIME_ACTION * type.turns_required
    #     self.time_start = time.time()
         

    def __post_init__(self):
        if not self.time_end:
            self.time_end = time.time() + TIME_ACTION * self.type.turns_required
        if not self.time_start:
            self.time_start = time.time()

    def time_remaind(self):
        # example'0:29:59.99999'
        timeleft = datetime.fromtimestamp(self.time_end) - datetime.now()
        if timeleft.days < 0:
            return "finished" 
        return str(timeleft).split('.')[0]

    def is_finish(self):
        return time.time() > self.time_end
    
    def complete(self):
        self.status = Status.FINISH.value

    def json(self):
        return {
            "owner": self.owner,
            "type":self.type.json(),
            "time_end":self.time_end,
            "time_start": self.time_start,
            "status":self.status
            }