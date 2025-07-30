import unittest
from enum import Enum
from community import Community
from game import Game
from survivor import Survivor
from narrative import Narrative

class TestCommunity(unittest.TestCase):

    def test_community_initial(self):
        c = Community()
        self.assertEqual(c.defense, 0)
        # self.assertEqual(c.survivors, [])
        # self.assertEqual(c.zombies, [])
        self.assertEqual(c.food, 0)

    def test_defense(self):
        c = Community()
        c.build_defense(2)
        self.assertEqual(c.defense, 2)

class TestGame(unittest.TestCase):

    def test_game_survivors(self):
        g = Game(Community(), Narrative())
        self.assertEqual(g.survivors, [])
        s = Survivor('john')
        g.add_survivor(s)
        self.assertEqual(g.survivors, [s])
        self.assertFalse(g.is_new_survivor(s.name))
        self.assertEqual(g.find_survivor_by_name('john'),s)
        self.assertIsNone(g.find_survivor_by_name('bob'))

    def test_survivor(self):
        s = Survivor('john')
        self.assertEqual(s.is_ok(),True)





if __name__ == '__main__':
    unittest.main()    