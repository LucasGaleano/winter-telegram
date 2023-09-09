
from dataclasses import dataclass, field
from location import Location
from items import Food
# from weapon import Weapon, hands

@dataclass
class Survivor:
    name: str
    location: Location = None
    # order: list = field(default_factory=lambda: ['rest'])
    #health: int = 100
    # weapon: Weapon = hands
    #level: int =  1
    #experience: int = 0
    #skills: dict = field(default_factory=dict)
    # items: list = field(default_factory=list)
    # weaponExperience: dict = field(default_factory=dict)
    # experienceByWeapon: int = 10
    # status: str = 'Resting...'

    
    def search(self):
        if self.location:
            return self.location.search()
        return None

#     def attack(self, person):
#         print(f"{self.name} attacked {person.name}")
#         damage = self.weapon.damage
#         person.attacked(damage)
#         # self.weaponExperience[self.weapon.type] = self.weaponExperience.setdefault(self.weapon.type,0) + self.experienceByWeapon

#     def attacked(self, damage):
#         self.loss_health(damage)

#     def loss_health(self, damage):
#         self.health = max(0, self.health - damage)
#         print(f"{self.name} losses {damage} of health")

#     def search(self, location):
#         item = location.search()
#         console.print(f"{self.name} has found a {item.name} on the {location.name}")
#         self.items.append(item)

#     def rest(self):
#         console.print(f"{self.name} is resting.")

#     def do_action(self):
#         action, *parameters = self.order
#         if action == 'search':
#             location = find_location_by_name(parameters[0])
#             self.search(location)
#         elif action == 'rest':
#             self.rest()
            

# survivors = [Survivor('Clara'), Survivor('John')]