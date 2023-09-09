from community import Community
from game import Game, locations
from survivor import Survivor
from narrative import Narrative
from items import Food
from repo import Repo
from task import Task, CurrentTask

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
    assert type(s.search()) == Food

def test_repository():
    repo = Repo('winter-test','mongodb://localhost')
    repo.add_task(owner="john", type=Task.BUILD_BARRICADE.value)
    taskFromRepo = repo.get_all_progress_task().pop()
    testTask = CurrentTask(owner="john", type=Task.BUILD_BARRICADE.value)
    assert taskFromRepo.owner == testTask.owner
    assert taskFromRepo.status == testTask.status
    assert taskFromRepo.type.name == testTask.type.name
    assert taskFromRepo.type.location == testTask.type.location

    repo.add_task(owner="john", type=Task.TRAVELHOSPITAL.value)
    taskFromRepo = repo.get_all_progress_task().pop()
    testTask = CurrentTask(owner="john", type=Task.TRAVELHOSPITAL.value)
    assert taskFromRepo.owner == testTask.owner
    assert taskFromRepo.status == testTask.status
    assert taskFromRepo.type.name == testTask.type.name
    assert taskFromRepo.type.location == testTask.type.location
