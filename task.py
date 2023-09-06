from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime

TIME_ACTION = 10 #sec


@dataclass
class TaskType():
    name: str
    description: str
    turns_required: int = 1

    def json(self):
        return {
            "name" : self.name,
            "description":self.description,
            "turns_required": self.turns_required
        }


class Task(Enum):
    BUILD_BARRICADE = TaskType(name="build", description="building a barricade")
    TRAVEL = TaskType(name="travel", description="travelling to")

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
        timeRemaind = str(datetime.fromtimestamp(self.time_end) - datetime.now())
        return timeRemaind.split('.')[0]

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