from dataclasses import dataclass
import random

@dataclass
class Narrative():
    

    def travelling(self, location, person):
        events = [
            f"Running low on supplies and in need of help, {person} decide to brave the icy roads and head towards the {location}, praying you'll find what you need to survive.",
            f"With the biting cold gnawing at {location}'s resolve, they set out on a risky mission towards {location}, driven by the need for supplies that could mean life or death.",
            f"Faced with dwindling resources and a sense of urgency, {person} decides to take a leap of faith and set out towards the {location}, their hopes pinned on discovering life-saving supplies.",
            f"Running low on supplies and feeling desperate, {person} chooses to head for the {location}, hoping they can find what they need to stay alive.",
            f"With determination in his heart, {person} makes the brave choice to journey towards the {location}, seeking potential aid."
        ]

        return random.choice(events)
    
    def finished_barricade(self, person):
        events = [
            f"As the snowstorm rages outside, {person}, one of the survivors takes charge, constructing a makeshift barricade at your shelter. The sense of security is palpable.\nCommunity gain +1 defense.",
            f"With determination and teamwork, a survivor successfully completes a sturdy barricade around your camp. The group breathes a sigh of relief, feeling safer than ever.\nCommunity gain +1 defense."
        ]

        return random.choice(events)
    
    def new_arrived(self, person):
        events = [
            f"Amidst the cold and desolation, a stranger appears on the horizon. After cautious introductions, they express a desire to join your community.\n{person} join the community"
        ]

        return random.choice(events)
    
    def found_food(self, person:str, amount:int):
        events = [
            f"{person} stumbles upon a hidden cache of food. Their discovery provides a much-needed boost to the community's supplies.\nCommunity gain +{amount} of food"
        ]

        return random.choice(events)