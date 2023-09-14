from community import Community
from game import Game, locations
from survivor import Survivor
from narrative import Narrative
from items import Food
from repo import Repo
from task import Task, CurrentTask, Status

def test_community_initial():
    c = Community()
    assert c.defense ==  0
    assert c.food ==  0

def test_defense():
    c = Community()
    c.build_defense(2)
    assert c.defense == 2

def test_game_survivors():
    g = Game(Community(), Narrative())
    assert g.survivors == []
    s = Survivor('john')
    g.add_survivor(s)
    assert g.survivors == [s]
    assert g.is_new_survivor(s.name) == False
    assert g.find_survivor_by_name('john') == s
    assert g.find_survivor_by_name('bob') == None

def test_location_search():
    g = Game(Community(), Narrative())
    s = Survivor('john')
    g.add_survivor(s)
    s.location = locations["hospital"]
    item = s.search()
    assert (type(item) == Food or type(item) == type(None))

def test_repository():
    repo = Repo('winter-test','mongodb://localhost')
    repo.add_task(owner="john", type=Task.BUILD_BARRICADE.value)
    taskFromRepo = repo.get_all_progress_task().pop()
    testTask = CurrentTask(owner="john", type=Task.BUILD_BARRICADE.value)
    assert taskFromRepo.owner == testTask.owner
    assert taskFromRepo.status == testTask.status
    assert taskFromRepo.type.name == testTask.type.name
    assert taskFromRepo.type.location == testTask.type.location
    assert taskFromRepo.type.passive == testTask.type.passive

    repo.add_task(owner="john", type=Task.SEARCH.value)
    taskFromRepo = repo.get_all_progress_task().pop()
    testTask = CurrentTask(owner="john", type=Task.SEARCH.value)
    assert taskFromRepo.owner == testTask.owner
    assert taskFromRepo.status == testTask.status
    assert taskFromRepo.type.name == testTask.type.name
    assert taskFromRepo.type.location == testTask.type.location
    assert taskFromRepo.type.passive == testTask.type.passive

    repo.add_task(owner="john", type=Task.TRAVEL.value)
    taskFromRepo = repo.get_all_progress_task_by_owner("john").pop()
    taskFromRepo.complete()
    repo.update_task(taskFromRepo)
    taskFromRepo = repo.get_all_task().pop()
    testTask = CurrentTask(owner="john", type=Task.TRAVEL.value)
    assert taskFromRepo.owner == testTask.owner
    assert taskFromRepo.status == Status.FINISH.value
    assert taskFromRepo.type.name == testTask.type.name
    assert taskFromRepo.type.location == testTask.type.location

    repo.add_task(owner="john", type=Task.TRAVEL.value)
    repo.delete_all_task_by_owner("john")
    taskFromRepo = repo.get_all_progress_task_by_owner("john")
    assert taskFromRepo == list()


    repo.add_task(owner="john", type=Task.TRAVEL.value)
    repo.add_task(owner="john", type=Task.SEARCH.value)
    repo.delete_all_passive_task_by_owner("john")
    taskFromRepo = repo.get_all_task_by_owner("john")
    assert len(taskFromRepo) == 1

def test_zombies():
    g = Game(Community(), Narrative())
    s = Survivor('john')
    g.add_survivor(s)
    s.location = locations["hospital"]

