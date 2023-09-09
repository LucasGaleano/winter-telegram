from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime

TIME_ACTION = 30 #sec


@dataclass
class TaskType():
    name: str
    description: str
    turns_required: int = 1
    location: str = None

    def json(self):
        return {
            "name" : self.name,
            "description":self.description,
            "turns_required": self.turns_required,
            "location": self.location
        }


class Task(Enum):
    BUILD_BARRICADE = TaskType(name="build", description="building a barricade")
    TRAVELHOSPITAL = TaskType(name="travel", description="travelling to the hospital", location="hospital")
    SEARCH = TaskType(name="search", description="searching")

class Status(Enum):
    FINISH = 'finish'
    IN_PROGRESS = 'in progress'


@dataclass
class CurrentTask:
    owner: str
    time_end: int
    time_start: int
    type: TaskType
    status: Status = Status.IN_PROGRESS.value

    def __init__(self, owner:str, type:TaskType):
        self.owner = owner
        self.type = type
        self.time_end = time.time() + TIME_ACTION + type.turns_required
        self.time_start = time.time()

    def time_remaind(self):
        # example'0:29:59.99999'
        timeRemaind = datetime.fromtimestamp(self.time_end) - datetime.now()
        if timeRemaind.days < 0:
            return "finished" 
        return str(timeRemaind).split('.')[0]

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