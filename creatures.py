import random


class SimpleEntity:
    def __init__(self):
        self.nutrition = 0
        self.stock_name = 'error'
        self.lifespan = 10

    def interact(self, other):
        return [self, other]


class BoringRock(SimpleEntity):
    def __init__(self):
        super().__init__()
        self.stock_name = 'Rock'


class DeliciousLettuce(SimpleEntity):
    def __init__(self):
        super().__init__()
        self.nutrition = 3
        self.stock_name = 'Lettuce'
        self.lifespan = 30

    def interact(self, other):
        self.lifespan -= 1
        # Death by old age.
        if self.lifespan < 0:
            return [other]

        # Lettuces grow by themselves as if adding energy to the system via photosynthesis.
        self.nutrition += 1

        # Lettuces can get too crowded to grow properly.
        if other.stock_name == 'Lettuce':
            self.nutrition -= 1.3

        # Lettuces will die if too overcrowded or consumed.
        if self.nutrition < 0:
            return [other]

        # Reproduction conditions.
        if self.nutrition > 10:
            self.nutrition = 3
            return [self, DeliciousLettuce(), other]

        return [self, other]


class Caterpillar(SimpleEntity):
    def __init__(self):
        super().__init__()
        self.nutrition = 1
        self.stock_name = 'Caterpillar'
        self.lifespan = 15

    def interact(self, other):
        self.lifespan -= 1
        # Death by old age.
        if self.lifespan < 0:
            return [other]

        # Caterpillars eat lettuces, but not by destroying them.
        if other.stock_name == 'Lettuce':
            self.nutrition += 1
            other.nutrition -= 1
            return [self, other]

        # Reproduction conditions.
        if self.nutrition > 4:
            self.nutrition = 1
            return [self, Caterpillar(), Caterpillar(), other]

        # Ongoing energy expenditure.
        self.nutrition -= 0.1

        # Death by starvation.
        if self.nutrition < 0:
            return [other]

        return [self, other]


class Bluebird(SimpleEntity):
    def __init__(self):
        super().__init__()
        self.nutrition = 1
        self.stock_name = 'Bird'
        self.lifespan = 100

    def interact(self, other):
        self.lifespan -= 1
        # Death by old age.
        if self.lifespan < 0:
            return [other]

        # Birds consume caterpillars if they can spot them.
        if other.stock_name == 'Caterpillar' and random.random() < 0.2:
            self.nutrition += 3
            return [self]

        # Birds will fight one another if overcrowded.
        if other.stock_name == 'Bird':
            other.nutrition -= 0.3

        # Reproduction conditions.
        if self.nutrition > 7:
            self.nutrition = 1
            return [self, Bluebird(), Bluebird(), Bluebird(), other]

        # Ongoing energy expenditure.
        self.nutrition -= 0.05

        # Death by starvation.
        if self.nutrition < 0:
            return [other]

        return [self, other]


class Rabbit(SimpleEntity):
    def __init__(self):
        super().__init__()
        self.stock_name = 'Rabbit'
        self.lifespan = 35
        self.nutrition = 1

    def interact(self, other):
        self.lifespan -= 1
        # Death by old age.
        if self.lifespan < 0:
            return [other]

        if other.stock_name == 'Lettuce':
            self.nutrition += 0.4
            other.nutrition -= 0.4
            return [self, other]

        # Reproduction conditions.
        if self.nutrition > 3:
            self.nutrition = 1
            return [self, Rabbit(), other]

        # Ongoing energy expenditure.
        self.nutrition -= 0.05

        # Death by starvation.
        if self.nutrition < 0:
            return [other]

        return [self, other]


class Raptor(SimpleEntity):
    def __init__(self):
        super().__init__()
        self.nutrition = 2
        self.stock_name = 'Raptor'
        self.lifespan = 80

    def interact(self, other):
        self.nutrition -= 0.05
        self.lifespan -= 1

        # Death by old age.
        if self.lifespan < 0:
            return [other]

        # Raptors will eat caterpillars if they can spot them.
        if other.stock_name == 'Caterpillar' and random.random() < 0.2:
            self.nutrition += 3
            return [self]

        # Raptors love eating rabbits, but the rabbits have a high probability of escaping.
        if other.stock_name == 'Rabbit' and random.random() < 0.07:
            self.nutrition += 5
            return [self]

        # Raptors are very competitive, and will attack each other on sight.
        if other.stock_name == 'Raptor':
            other.nutrition -= 1

        # Reproduction conditions.
        if self.nutrition > 8:
            self.nutrition = 2
            return [self, Raptor(), Raptor(), other]

        # Death by starvation.
        if self.nutrition < 0:
            return [other]

        return [self, other]

