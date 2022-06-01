import random

from adventurelib import Item


class Character(Item):
    """A generic character class that can speak, die, and more."""

    def __init__(
        self,
        name: str,
        description: str,
        speech: list = [],
        def_name: str = None,
        gender: str = None,
        health: int = 10,
    ):
        """Construct a Character object."""
        super().__init__(name.title())
        self.name = name.title()
        self.def_name = def_name.lower(
        ) if def_name else f"the {self.name.lower()}"
        self.gender = gender
        self.description = description
        self.health = health
        self.speech = speech
        self.subject_pronoun = "they"
        self.object_pronoun = "it"

    def talk(self):
        if self.speech:
            return random.choice(self.speech)

    def die(self, msg: str = "{} died."):
        print(msg.format(self.def_name))

    def check_dead(self, msg: str = None):
        if self.health <= 0:
            self.die(msg) if msg else self.die()
            return True


class MaleCharacter(Character):
    """A male character."""

    def __init__(
        self,
        name: str,
        description: str,
        speech: list = [],
        def_name: str = None,
        health: int = 100,
    ):
        super().__init__(name, def_name, description, speech, "m", health)
        self.subject_pronoun = "he"
        self.object_pronoun = "him"


class FemaleCharacter(Character):
    """A female character."""

    def __init__(
        self,
        name: str,
        description: str,
        speech: list = [],
        def_name: str = None,
        health: int = 100,
    ):
        super().__init__(name, def_name, description, speech, "f", health)
        self.subject_pronoun = "she"
        self.object_pronoun = "her"
