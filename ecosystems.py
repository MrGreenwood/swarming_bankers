import random


class PairwiseInteractionEnvironment:
    def __init__(self):
        self.entities = []

    def choose_entity(self):
        return self.entities.pop(random.randrange(len(self.entities)))

    def add_entities(self, entities):
        self.entities.extend(entities)

    def step(self):
        resulting_entities = []
        while len(self.entities) > 3:
            acting_entity = self.choose_entity()
            victim = self.choose_entity()
            resulting_entities.extend(acting_entity.interact(victim))
        resulting_entities.extend(self.entities)
        self.entities = resulting_entities


