from dataclasses import dataclass
from pymongo import MongoClient
from task import Task, TaskType, Status, CurrentTask




# docker run -d --rm -p 127.0.0.1:27017:27017 --network vuln-network -v mongodb-vuln:/data/db --name mongo mongo:4.4.23
# docker run -d --rm -p 127.0.0.1:27017:27017 --name mongo mongo

@dataclass
class Repo:
    """Class for database management."""
    database: str
    collections: dict[str,str]

    def __init__(self, database, url):
    
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = url
        
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)
        
        # Create the database for our example (we will use the same database throughout the tutorial
        self.database = client[database]

        self.collections = {"task":self.database["task"]}


    def get_all_task(self, filter=None):
        tasks = []
        for data in self.collections['task'].find(filter):
            fetchedType = TaskType(name=data['type']['name'], description=data['type']['description'], turns_required=data['type']['turns_required'], location=data['type']['location'], passive=data['type']['passive'])
            fetchedTask = CurrentTask(owner=data['owner'], type=fetchedType)
            fetchedTask.status = data['status']
            fetchedTask.time_end = data['time_end']
            fetchedTask.time_start = data['time_start']
            tasks.append(fetchedTask)
        return tasks
    
    def get_all_task_by_owner(self, owner:str):
        return self.get_all_task(filter={'owner':owner})

    def get_all_finish_task(self):
        return self.get_all_task(filter={'status':Status.FINISH.value})
    
    def get_all_progress_task(self):
        return self.get_all_task(filter={'status':Status.IN_PROGRESS.value})
    
    def get_all_progress_task_by_owner(self, owner:str):
        return self.get_all_task(filter={'status':Status.IN_PROGRESS.value, 'owner':owner})
    
    def delete_all_task(self, filter=None):
        print(f"deleted all task, filter={filter}")
        self.collections['task'].delete_many(filter)
    
    def delete_all_task_by_owner(self,owner:str):
        self.delete_all_task({"owner":owner})

    def delete_all_passive_task(self):
        self.delete_all_task(filter={"type.passive":True})

    def delete_all_passive_task_by_owner(self,owner:str):
        self.delete_all_task(filter={"type.passive":True,"owner":owner})

    def add_task(self, owner: str, type: TaskType):
        newTask = CurrentTask(owner, type)
        print("Added new task", newTask)
        self.collections['task'].insert_one(newTask.json())

    def update_task(self, task: CurrentTask):
        self.collections['task'].update_one({"owner":task.owner, "time_start":task.time_start}, {"$set":task.json()})

