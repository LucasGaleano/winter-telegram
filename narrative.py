from dataclasses import dataclass
import random

@dataclass
class Narrative():
    
    lang: str = 'en'

    def travelling(self, location, person):
        if self.lang == 'en':
            events = [
                f"Running low on supplies and in need of help, {person} decide to brave the icy roads and head towards the {location}, praying you'll find what you need to survive.",
                f"With the biting cold gnawing at {location}'s resolve, they set out on a risky mission towards {location}, driven by the need for supplies that could mean life or death.",
                f"Faced with dwindling resources and a sense of urgency, {person} decides to take a leap of faith and set out towards the {location}, their hopes pinned on discovering life-saving supplies.",
                f"Running low on supplies and feeling desperate, {person} chooses to head for the {location}, hoping they can find what they need to stay alive.",
                f"With determination in his heart, {person} makes the brave choice to journey towards the {location}, seeking potential aid."
            ]
        if self.lang == 'es':
            events = [f'{person} se encamina hacia el {location} en busca de recursos, esperando encontrar lo necesario para mantenerse con vida en este mundo invernal lleno de peligros.',
                    f'Con determinación, {person} se aventura en el {location} en busca de recursos para el grupo. El frío mordiente y el temor a los zombies son su compañía mientras se adentra en lo desconocido, con la esperanza de encontrar lo que tanto necesitan.',
                    f"{person} se dirige a su destino, decidido a encontrar recursos vitales para la supervivencia del grupo en el {location}.",
                    f"Mientras el invierno se hace más implacable, {person} toma la valiente decisión de explorar el {location} en busca de recursos que mantendrán a todos con vida.",
                    f"{person} se aventura en territorio desconocido, enfrentando los desafíos del invierno en su búsqueda por recursos vitales en el {location}.",
                    f"La esperanza lleva a {person} a explorar el {location}, esperando encontrar los recursos necesarios para mantener a raya a los zombies y sobrevivir al invierno."]

        return random.choice(events)
    
    def finished_barricade(self, person):
        if self.lang == 'en':
            events = [
                f"As the snowstorm rages outside, {person}, one of the survivors takes charge, constructing a makeshift barricade at your shelter. The sense of security is palpable.\n*Community gain +1 defense.*",
                f"With determination and teamwork, a survivor successfully completes a sturdy barricade around your camp. The group breathes a sigh of relief, feeling safer than ever.\n*Community gain +1 defense.*"
            ]
        if self.lang == 'es':
            events = [
                f"Mientras la tormenta golpea afuera, {person}, uno de los sobrevivientes se hace cargo, construyendo una barricada. La sensacion de seguridad es palpable.\n*Comunidad gana +1 de defensa.*",
                f"Con determinacion y valentia, un sobreviviente completa la barricada. El grupo respira de tranquilidad, sintiendose mas seguro que nunca.\n*Comunidad gana +1 de defensa.*"
            ]
        return random.choice(events)
    
    def new_arrived(self, person):
        if self.lang == 'en':
            events = [
                f"Amidst the cold and desolation, a stranger appears on the horizon. After cautious introductions, they express a desire to join your community.\n*{person} joined the community*"
            ]

        if self.lang == 'es':
            events = [f"En medio del frío y la desolación, un extraño aparece en el horizonte. Tras unas cautelosas presentaciones, expresa su deseo de unirse a su comunidad.\n*{person} se une a la comunidad.*"]

        return random.choice(events)
    
    def found_food(self, person:str, amount:int):
        if self.lang == 'en':
            events = [
                f"{person} stumbles upon a hidden cache of food. Their discovery provides a much-needed boost to the community's supplies.\n*Community gain +{amount} of food*"
            ]
        if self.lang == 'es':
            events = [
                f"{person} tropieza con un alijo oculto de alimentos. Su descubrimiento proporciona un impulso muy necesario a los suministros de la comunidad.\n*Comunidad gana +{amount} de alimento.*"
            ]
        return random.choice(events)