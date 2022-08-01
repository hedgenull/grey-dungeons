"""Container file for main game functions/logic."""


import contextlib
import random
from time import sleep

import adventurelib as adv
import pyinputplus as pip
from art import tprint

from character import *
from rooms import *
from settings import *

####################################
# Functions
####################################

# adventurelib function overwrites
adv.prompt = lambda *_: f"{MAIN_COLOR}{my_name.title()} > {YELLOW}"
adv.no_command_matches = lambda *_: error(random.choice(ERROR_MESSAGES))


@adv.when("drop ITEM")
@adv.when("grasp ITEM")
@adv.when("get rid of ITEM")
@adv.when("ditch ITEM")
@adv.when("seize ITEM")
def drop(item: str):
    """Drop an item."""
    if obj := my_inventory.take(item):
        print(f"You drop the {obj}, which falls with a thump to the floor.")

        cur_room.items.add(obj)
    else:
        error(f"You do not have any {item}.")


@adv.when("inventory")
@adv.when("show inventory")
@adv.when("stuff")
def show_inventory():
    """Show your inventory."""
    print("You have:")
    if not my_inventory:
        print("Nothing!")
        return
    for item in my_inventory:
        print(f"* {item}")


def error(msg: str):
    """Print an error in red."""
    print(f"{RED}{msg}{MAIN_COLOR}")


def main():
    """Start the game."""
    print(MAIN_COLOR, end="")
    print(STORY)
    input(f"Press Enter to continue...{MAGENTA}\n")
    font = random.choice(FONTS)
    tprint("GREY DUNGEONS", font=font)
    sleep(0.5)
    global my_name, my_species
    my_name = pip.inputStr(prompt=f"{MAIN_COLOR}What is your name, traveler? {YELLOW}").title()

    my_species = pip.inputMenu(
        SPECIES, prompt=f"{MAIN_COLOR}What race do you belong to?\n{YELLOW}"
    )

    print(f"\nWelcome to the Grey Dungeons, {my_name}! Good luck!")
    print("\nType 'help' for more information.")
    adv.start()


@adv.when("take ITEM")
@adv.when("get ITEM")
@adv.when("grab ITEM")
def take(item: str):
    """Take an item and add it to your inventory."""
    if obj := cur_room.items.take(item):
        if len(my_inventory) < INVENTORY_SIZE:
            if cur_room.visible:
                my_inventory.add(obj)
                print(f"You take the {obj}.")
            else:
                error(
                    f"You grope around in the darkness for the {item}, but you can't seem to find one."
                )

        else:
            error("Your inventory is full! Try dropping/eating something first.")
    elif ent := cur_room.entities.find(item):
        error(f"You can't take {ent.def_name}.")
    elif cur_room.visible:
        error(f"There is no {item}.")
    else:
        error(f"You grope around in the darkness for the {item}, but you can't seem to find one.")


@adv.when("look")
@adv.when("look around")
@adv.when("observe")
@adv.when("describe room")
def look_around():
    """Observe your current surroundings."""
    print("You look around. Here's what you see:")
    print(cur_room)
    if cur_room.visible:
        print("\nExits:")
        for exit in cur_room.exits():
            print(f"* {exit}")
        if cur_room.items:
            print("\nItems:")
            for item in cur_room.items:
                print(f"* {item}")
        if cur_room.entities:
            print("\nCreatures:")
            for entity in cur_room.entities:
                print(f"* {entity}")
    else:
        error("You can't see anything in here.")
    print(MAIN_COLOR, end="")


@adv.when("break down DIRECTION door")
@adv.when("kick down DIRECTION door")
@adv.when("kung fu DIRECTION door")
def break_down(direction: str):
    """Try to break down a door."""
    global cur_room
    if cur_room.exit(direction):
        print(f"You break down the {direction} door.")
        with contextlib.suppress(Exception):
            exec(f"current_room.{direction}.locked = False")


@adv.when("talk to ENTITY")
@adv.when("make conversation with ENTITY")
@adv.when("converse with ENTITY")
def talk_to(entity: str):
    """Talk to an entity."""
    if hopefully_entity := cur_room.entities.find(entity):
        input(f"{MAIN_COLOR}What do you want to say to {hopefully_entity.def_name}?{YELLOW} ")

        print(f'{hopefully_entity.def_name.title()} says "{hopefully_entity.talk()}"')
    elif not_person := cur_room.items.find(entity):
        if not_person:
            error(f"The {hopefully_entity} can't talk, pal.")
    else:
        error(f"There is no {entity}.")


@adv.when("hit TARGET with ITEM")
@adv.when("slap TARGET with ITEM")
@adv.when("use ITEM on TARGET")
@adv.when("attack TARGET with ITEM")
@adv.when("maul TARGET with ITEM")
@adv.when("maim TARGET with ITEM")
@adv.when("beat TARGET with ITEM")
def hit_with(target: str, item: str):
    """Hit something with something else."""
    _target = cur_room.entities.find(target)
    _item = my_inventory.find(item)
    if not _item:
        error(f"You don't have any {item}.")
    elif _target:
        print(f"You hit {_target.def_name} with the {_item}.")
        _target.health -= 1
    elif _target := cur_room.items.find(target):
        print(f"You hit the {_target} with the {_item}.")
    else:
        error(f"There is no {target}.")


@adv.when("hit TARGET")
@adv.when("slap TARGET")
@adv.when("kick TARGET")
@adv.when("attack TARGET")
@adv.when("kung fu TARGET")
@adv.when("maim TARGET")
@adv.when("beat TARGET")
@adv.when("beat TARGET over the head")
@adv.when("punch TARGET")
@adv.when("box TARGET")
@adv.when("whack TARGET")
@adv.when("bonk TARGET")
def hit(target: str):
    """Kung-fu the target."""
    if _target := cur_room.entities.find(target):
        print(f"You flail wildly at {_target.def_name}.")
        _target.health -= 0.5
    elif _target := cur_room.items.find(target):
        print(f"You knock the {_target} around the room.")
    else:
        error(f"There is no {target}.")


@adv.when("use ITEM")
@adv.when("equip ITEM")
def equip(item: str):
    """Equip an item."""
    if obj := my_inventory.find(item):
        global current_item
        current_item = obj
        print(f"You equip the {obj}.")
    else:
        error(f"You don't have any {item}.")


@adv.when("give TARGET brain damage")
@adv.when("give TARGET permanent brain damage")
def brain_damage(target: str):
    """Give a target permanent brain damage."""
    if _target := cur_room.entities.find(target):
        print(
            random.choice(BRAIN_DAMAGE).format(
                name=_target.def_name,
                obj=_target.object_pronoun.title(),
                sbj=_target.subject_pronoun,
            )
        )


@adv.when("soliloquize")
@adv.when("contemplate")
@adv.when("philosophize")
@adv.when("meditate")
def contemplate():
    """Contemplate the universe."""
    saying = random.choice(CONTEMPLATIONS)
    print(f'"{saying}", you think')


@adv.when("burn ITEM")
@adv.when("set fire to ITEM")
@adv.when("set ITEM on fire")
@adv.when("incinerate ITEM")
def burn(item: str):
    """It does what it sounds like."""
    if my_species == "half-dragon":  # Can you breathe fire? If so...
        if obj := cur_room.items.take(item):  # If the item's in the room...
            print(f"You burn the {obj}. Its ashes fall to the floor.")
            cur_room.items.add(Item(f"{obj} ashes", f"{obj} remains", f"{obj} remnants"))
        elif obj := my_inventory.take(item):  # If it's in your inventory...
            print(f"You burn the {obj} and stuff its ashes in your pocket.")
            my_inventory.add(Item(f"{obj} ashes", f"{obj} remains", f"{obj} remnants"))
        elif obj := cur_room.entities.find(item):  # It's not an item after all, it's an entity.
            print(f"You incinerate {obj.def_name}.")
            obj.health -= 1
            if obj.check_dead("{}'s ashes fall to the floor."):
                cur_room.entities.remove(obj)
                cur_room.items.add(
                    Item(
                        f"{obj.name.lower()} ashes",
                        f"{obj.name.lower()} remains",
                        f"{obj.name.lower()} remnants",
                    )
                )
        else:  # There's nothing to burn. How tragic.
            error(f"There is no {item} in the room or in your inventory.")
    else:  # You can't even burn whatever you wanted to. Lame.
        print("What are you, some kind of dragon? (That's a big hint.)")


@adv.when("go north", direction="north")
@adv.when("go south", direction="south")
@adv.when("go east", direction="east")
@adv.when("go west", direction="west")
@adv.when("go n", direction="north")
@adv.when("go s", direction="south")
@adv.when("go e", direction="east")
@adv.when("go w", direction="west")
@adv.when("north", direction="north")
@adv.when("south", direction="south")
@adv.when("east", direction="east")
@adv.when("west", direction="west")
@adv.when("n", direction="north")
@adv.when("s", direction="south")
@adv.when("e", direction="east")
@adv.when("w", direction="west")
def go(direction: str):
    """Go in a direction, if possible."""
    global cur_room
    if room := cur_room.exit(direction):
        if not room.locked:
            prev_room, cur_room = cur_room, room
            print(f"You go through the {direction} door.")
            look_around()
        else:
            error("That door is locked. How could you get in? (Hint: you're a kung-fu master.)")

    else:
        error(f"You can't go {direction}.")


@adv.when("exit")
@adv.when("exit room")
@adv.when("go out")
@adv.when("go back")
def exit_room():
    """Exit the room, if possible."""
    global prev_room, cur_room
    if prev_room == cur_room:
        error("You can't go back the way you came.")
    else:
        print("You exit the room.")
        prev_room, cur_room = cur_room, prev_room
        look_around()


@adv.when("eat ITEM")
@adv.when("ingest ITEM")
@adv.when("swallow ITEM")
def eat(item: str):
    """Eat an item."""
    obj = my_inventory.find(item)

    if ent := cur_room.entities.find(
        item
    ):  # There's an entity to eat, but that's kinda rude, don't you think?
        error(f"You try to eat {ent.def_name}, but {ent.object_pronoun} doesn't seem to like it.")
    elif not obj:  # There is nothing to eat.
        error(f"You do not have any {item}.")
    else:  # Mmm. You'll be the next Gordon Ramsay at this rate.
        taste = random.choice(TASTES)
        print(f"You eat the {obj}. Hmm... rather {taste}.")
        my_inventory.remove(obj)
