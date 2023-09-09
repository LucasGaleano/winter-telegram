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


    # def get_task_by_id(self, id):
    #     data = self.collections['task'].find_one(projection={'_id':id})
    #     if data:
    #         return CurrentTask(task=data['task'], status=data['status'],time_end=data['time_end'])
    #     return None

    def get_all_task(self, filter=None):
        tasks = []
        for data in self.collections['task'].find(filter):
            fetchedType = TaskType(name=data['type']['name'], description=data['type']['description'], turns_required=data['type']['turns_required'], location=data['type']['location'])
            fetchedTask = CurrentTask(owner=data['owner'], type=fetchedType)
            fetchedTask.status = data['status']
            fetchedTask.time_end = data['time_end']
            fetchedTask.time_start = data['time_start']
            tasks.append(fetchedTask)
        return tasks
    
    def get_all_finish_task(self):
        return self.get_all_task(filter={'status':Status.FINISH.value})
    
    def get_all_progress_task(self):
        return self.get_all_task(filter={'status':Status.IN_PROGRESS.value})

    def add_task(self, owner: str, type: TaskType):
        newTask = CurrentTask(owner, type)
        print("Add new task", newTask)
        self.collections['task'].insert_one(newTask.json())

    def update_task(self, task: CurrentTask):
        self.collections['task'].update_one({"owner":task.owner, "time_start":task.time_start}, {"$set":{"status":Status.FINISH.value}})



#     def get_endpoint(self, host, portProtocol):

#         item = self.collections['host'].find_one({"_id" : f"{host.strip()} {portProtocol.strip()}"})
#         if item:
#             endpoint = Endpoint(item['host'], f"{item['port']}/{item['protocol']}", oids=item["oids"], service=item['service'])
#         else:
#             endpoint = None
#         return endpoint

#     #db.testing.update({"_id":"126"},{"$set":{"l":"1334"}},{"upsert":true})

# #   result.acknowledged    result.modified_count  result.upserted_id     
# #   result.matched_count   result.raw_result  
# #   {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
#     def add_endpoint(self, newEndpoint: Endpoint):
#         fetchEndpoint = self.get_endpoint(newEndpoint._id.split()[0], newEndpoint._id.split()[1])
#         if fetchEndpoint:
#             fetchEndpoint.update(newEndpoint)
#             newEndpoint = fetchEndpoint
#         return self.collections['host'].update_one({"_id":newEndpoint._id},{"$set":newEndpoint.json()},upsert=True)

#     def add_vulnerability(self, vulnerability: Vulnerability):
#         return self.collections['vulnerability'].update_one({"_id":vulnerability._id},{"$set":vulnerability.json()},upsert=True)

#     def get_all_oids(self):
#         return [oid['_id'] for  oid in self.collections['vulnerability'].find(projection={'_id':1})]

#     def get_all_host(self):
#         return self.collections['host'].find()
    
#     def find_vuln_by(self, oid):
#         return self.collections['vulnerability'].find_one({"_id":oid})
    
#     def get_summary(self):
#         vulnerabilities = []
#         for host in self.get_all_host():
#             for oid, data in host['oids'].items():
#                 vuln = self.find_vuln_by(oid)
#                 if data['status'] == "Open":
#                     vuln['status'] = data['status']
#                     vuln['notes'] = data['notes']
#                     vuln.update(host)
#                     vuln.pop('oids')
#                     vuln.pop('_id')
#                     vuln['vulnerability ID'] = oid
#                     #{'cvss': '6.4', 'description': '', 'family': 'General', 'name': 'MQTT Broker Does Not Require Authentication', 'solution': '', 'threat': 'Medium', 'value': 'AV:N/AC:L/Au:N/C:P/I:P/A:N', 'status': 'Open', 'notes': '', 'host': '1.2.3.4', 'port': '1456', 'protocol': 'tcp', 'service': '', 'vulnerability ID': '1.3.6.1.4.1.25623.1.0.140167'}
#                     vulnerabilities.append(vuln)
#         return vulnerabilities
