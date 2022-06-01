import random
from time import sleep

import adventurelib as adv
import pyinputplus as pip
from art import tprint

from character import *
from constants import *
from rooms import *

# Game variables

current_room = entrance
last_room = entrance

# Functions

# adventurelib function overwrites
adv.prompt = lambda *_: f"{MAIN_COLOR}{my_name.title()} > {YELLOW}"
adv.no_command_matches = lambda *_: error(random.choice(ERRORS))


@adv.when("drop ITEM")
@adv.when("get rid of ITEM")
@adv.when("ditch ITEM")
def drop(item):
    """Drop an item."""
    obj = my_inventory.take(item)
    if not obj:  # There is no spoon. Or rather, there is no item.
        error(f"You do not have any {item}.")
    else:  # Yay, we can drop stuff now.
        print(f"You drop the {obj}, which falls with a thump to the floor.")
        current_room.items.add(obj)


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


def error(msg):
    """Print an error in red."""
    print(f"{RED}{msg}{MAIN_COLOR}")


def main():
    """Start the game."""
    # Print the story in blue...
    print(MAIN_COLOR, end="")
    print(STORY)
    input(f"Press Enter to continue...{MAGENTA}\n")

    # Print the title in a random font + magenta...
    font = random.choice(FONTS)
    tprint(f"GREY DUNGEONS", font=font)
    sleep(0.5)

    # Prepare for variable assignment!
    global my_name, my_species

    my_name = pip.inputStr(
        prompt=f"{MAIN_COLOR}What is your name, traveler? {YELLOW}").title()
    my_species = pip.inputMenu(
        SPECIES, prompt=f"{MAIN_COLOR}What race do you belong to?\n{YELLOW}")

    # Make the player feel as comfortable as possible when they're in a creepy abandoned dungeon.
    print(f"\nWelcome to the Grey Dungeons, {my_name}! Good luck!")
    print("\nType 'help' for more information.")
    adv.start()


@adv.when("take ITEM")
@adv.when("get ITEM")
@adv.when("grab ITEM")
def take(item):
    """Take an item and add it to your inventory."""
    obj = current_room.items.take(item)
    if not obj:  # There's not an item in the room with that name...
        if ent := current_room.entities.find(
                item):  # ...but there is an entity!
            error(f"You can't take {ent.def_name}.")
        else:  # There's no entities either.
            if current_room.visible:
                error(f"There is no {item}.")
            else:
                error(
                    f"You grope around in the darkness for the {item}, but you can't seem to find one."
                )
    else:  # The item exists! Yippee!
        if len(my_inventory
               ) < INVENTORY_SIZE:  # If your pockets aren't full yet...
            if current_room.visible:
                my_inventory.add(obj)
                print(f"You take the {obj}.")
            else:
                error(
                    f"You grope around in the darkness for the {item}, but you can't seem to find one."
                )
        else:  # Dang, you can't carry that.
            error(
                "Your inventory is full! Try dropping/eating something first.")


@adv.when("look")
@adv.when("look around")
@adv.when("observe")
@adv.when("describe room")
def look_around():
    """Observe your current surroundings."""
    print(f"You look around. Here's what you see:")
    print(current_room)  # Print the description
    if current_room.visible:  # Can we even see in this room?
        print("\nExits:")
        for exit in current_room.exits():
            print(f"* {exit}")

        if current_room.items:
            print("\nItems:")
            for item in current_room.items:
                print(f"* {item}")

        if current_room.entities:
            print("\nCreatures:")
            for entity in current_room.entities:
                print(f"* {entity}")
    else:  # Apparently not.
        error("You can't see anything in here.")
    print(MAIN_COLOR, end="")


@adv.when("break down DIRECTION door")
@adv.when("kick down DIRECTION door")
@adv.when("kung fu DIRECTION door")
def break_down(direction):
    """Try to break down a door."""
    global current_room

    if current_room.exit(direction):
        print(f"You break down the {direction} door.")
        try:
            exec(f"current_room.{direction}.locked = False"
                 )  # That door doesn't have a chance after a Dragon Kick.
        except:
            pass


@adv.when("talk to ENTITY")
@adv.when("make conversation with ENTITY")
@adv.when("converse with ENTITY")
def talk_to(entity):
    """Talk to an entity."""
    hopefully_entity = current_room.entities.find(entity)

    if hopefully_entity:  # It's a real entity.
        input(
            f"{MAIN_COLOR}What do you want to say to {hopefully_entity.def_name}?{YELLOW} "
        )
        print(
            f"{hopefully_entity.def_name.title()} says \"{hopefully_entity.talk()}\""
        )
    elif not_person := current_room.items.find(
            entity):  # If it's an item, not an entity...
        if not_person:
            error(f"The {hopefully_entity} can't talk, pal.")
    else:  # Oops, there's nothing to talk to.
        error(f"There is no {entity}.")


@adv.when("hit TARGET")
@adv.when("slap TARGET")
@adv.when("kick TARGET")
@adv.when("attack TARGET")
@adv.when("kung fu TARGET")
@adv.when("punch TARGET")
def hit(target):
    """Kung-fu the target."""
    _target = current_room.entities.find(target)

    if _target:  # There's an entity to attack. Yay, violence!
        print(f"You flail wildly at {_target.def_name}.")
        _target.health -= 0.5
    elif _target := current_room.items.find(
            target):  # There's an item to knock around.
        print(f"You flail wildly at the {_target}.")
    else:
        error(f"There is no {target}.")


@adv.when("hit TARGET with ITEM")
@adv.when("slap TARGET with ITEM")
@adv.when("use ITEM on TARGET")
@adv.when("attack TARGET with ITEM")
@adv.when("maul TARGET with ITEM")
def hit_with(target, item):
    """Hit something with something else."""
    _target = current_room.entities.find(target)
    _item = my_inventory.find(item)

    if not _item:  # You can't hit someone with nothing!
        error(f"You don't have any {item}.")
    else:  # But you can with something.
        if _target:  # There's an entity to hit.
            print(f"You hit {_target.def_name} with the {_item}.")
            _target.health -= 1
        elif _target := current_room.items.find(
                target):  # There's an item to hit.
            print(f"You hit the {_target} with the {_item}.")
        else:  # There is no spoon, or entity, or even an item.
            error(f"There is no {target}.")


@adv.when("use ITEM")
@adv.when("equip ITEM")
def equip(item):
    """Equip an item."""
    if obj := my_inventory.find(item):
        global current_item
        current_item = obj
        print(f"You equip the {obj}.")
    else:
        error(f"You don't have any {item}.")


@adv.when("soliloquize")
@adv.when("contemplate")
@adv.when("philosophize")
@adv.when("meditate")
def contemplate():
    """Contemplate the universe."""
    saying = random.choice(CONTEMPLATIONS)
    print(f"\"{saying}\", you think")


@adv.when("burn ITEM")
@adv.when("set fire to ITEM")
@adv.when("set ITEM on fire")
def burn(item):
    """It does what it sounds like."""
    if my_species == "half-dragon":  # Can you breathe fire? If so...
        if obj := current_room.items.take(
                item):  # If the item's in the room...
            print(f"You burn the {obj}. Its ashes fall to the floor.")
            current_room.items.add(
                Item(f"{obj} ashes", f"{obj} remains", f"{obj} remnants"))
        elif obj := my_inventory.take(item):  # If it's in your inventory...
            print(f"You burn the {obj} and stuff its ashes in your pocket.")
            my_inventory.add(
                Item(f"{obj} ashes", f"{obj} remains", f"{obj} remnants"))
        elif obj := current_room.entities.find(
                item):  # It's not an item after all, it's an entity.
            print(f"You burn {obj.def_name}.")
            obj.health -= 1
            if obj.check_dead("{}'s ashes fall to the floor."):
                current_room.entities.remove(obj)
                current_room.items.add(
                    Item(f"{obj.name.lower()} ashes",
                         f"{obj.name.lower()} remains",
                         f"{obj.name.lower()} remnants"))
        else:  # There's nothing to burn. How tragic.
            error(f"There is no {item} in the room or in your inventory.")
    else:  # You can't even burn whatever you wanted to. Lame.
        print("What are you, some kind of dragon? (That's a big hint.)")


@adv.when("north", direction="north")
@adv.when("south", direction="south")
@adv.when("east", direction="east")
@adv.when("west", direction="west")
@adv.when("n", direction="north")
@adv.when("s", direction="south")
@adv.when("e", direction="east")
@adv.when("w", direction="west")
def go(direction):
    """Go in a direction, if possible."""
    global current_room
    room = current_room.exit(direction)
    if room:  # If there's a door in that direction...
        if not room.locked:  # If it's unlocked...
            current_room = room
            print(f"You go through the {direction} door.")
            look_around()
        else:  # Dang, it's locked.
            error(
                f"That door is locked. How could you get in? (Hint: you're a kung-fu master.)"
            )
    else:  # There's no exit that way, buddy. They altered the Matrix.
        error(f"You can't go {direction}.")


@adv.when("exit")
@adv.when("exit room")
@adv.when("go out")
@adv.when("go back")
def exit_room():
    """Exit the room, if possible."""
    global last_room, current_room
    if last_room == current_room:  # No way are you going out!
        error(f"You can't go back the way you came.")
    else:  # Ok, you go into the previous room.
        print("You exit the room.")
        last_room, current_room = current_room, last_room
        look_around()


@adv.when("eat ITEM")
@adv.when("ingest ITEM")
@adv.when("swallow ITEM")
def eat(item):
    """Eat an item."""
    obj = my_inventory.find(item)

    if ent := current_room.entities.find(
            item
    ):  # There's an entity to eat, but that's kinda rude, don't you think?
        error(
            f"You try to eat {ent.def_name}, but {ent.object_pronoun} doesn't seem to like it."
        )
    elif not obj:  # There is nothing to eat.
        error(f"You do not have any {item}.")
    else:  # Mmm. You'll be the next Gordon Ramsay at this rate.
        taste = random.choice(TASTES)
        print(f"You eat the {obj}. Hmm... rather {taste}.")
        my_inventory.remove(obj)


if __name__ == "__main__":
    main()
