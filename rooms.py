"""All rooms, connections, characters and items in Grey Dungeons 4.0."""

import adventurelib as adv
from adventurelib import Item

from character import *

# By default, all rooms are unlocked, visible, and empty of items and characters.
adv.Room.locked = False
adv.Room.visible = True
adv.Room.items = adv.Bag()
adv.Room.entities = adv.Bag()

# Room variables

entrance = adv.Room(
    "A small room lit by torches. Three wooden doors lead elsewhere, and a rockpile blocks the way out."
)
boring = adv.Room(
    "A dark room that has 2 doors. A small, dusty, three-legged stool sits in the corner. It's quite boring."
)
clinton = adv.Room(
    "A dimly-lit room that has 2 doors forward and a Hillary Clinton 2016 campaign poster. Better get outta here!"
)
chest = adv.Room(
    "A dark room that has 1 door ahead and a locked chest in the corner.")
one_door = adv.Room(
    "A dark room that has one door straight ahead. Maybe you shouldn't go in there..."
)
creepy = adv.Room(
    "A dark room that has 2 doors. On the floor are eerie candles and some voodoo emblem drawn in a red liquid. Pretty sus..."
)
liquid = adv.Room(
    "A dark room that has 1 door, excluding the way you came. It is filled with various puddles of what *looks* like water..."
)
soup_time = adv.Room(
    "A surprisingly bright room that has 2 doors. It's lit up by a mysterious floating orb. Soup time! (- Weird Al Yankovic)"
)
organ = adv.Room(
    "A dark room that has 1 other door. There's a pipe organ, which is eerily playing itself."
)
sword = adv.Room(
    "A dark room that has 1 other door, on which hangs a huge sword.")
secret = adv.Room(
    "A room with 2 doors. It's obvious that this used to be a secret place- there's a big sign saying 'This is a secret place' hanging on the door."
)
peach = adv.Room(
    "A dark room that has 2 doors, and a rotting peach in the corner.")
hat = adv.Room(
    "A dark room that has 2 doors. On the floor lies a random purple hat- ominous."
)
statue = adv.Room(
    "A dark and dusty room. It has a tall statue of a knight in the middle. Wait, did that thing just move?"
)
cake_lie = adv.Room(
    "A dark room that has some cake on a table in the corner. Beside the cake is a scrap of paper saying 'the cake is a lie'. Huh."
)
ham = adv.Room(
    "A dark room that has 2 doors. It smells like rotting ham, but on the floor is a piece of cake. Or is it *really* cake?"
)
death = adv.Room(
    "A dark room that has 3 doors. On the first door, which is locked, there is a message saying 'Certain Death' written in blood. I wonder what's in there?"
)
gold = adv.Room(
    "A semi-dark room that has 4 doors, each of which is made of solid gold.")
dark = adv.Room(
    "A pitch-black room that's perfectly quiet. You can't tell what's lurking in the shadows..."
)
lava = adv.Room(
    "A bright and uncomfortably warm room, lit up by streams of magma crossing the floor. Watch your step!"
)
portal = adv.Room(
    "A dark room. In the center floats a mysterious purple portal. Where does it go?"
)
crypt = adv.Room(
    "A dark passageway that slopes downward. In the walls are carved slots, filled with skeletons and corpses. Yipes!"
)

# Room connections

entrance.west = boring
entrance.north = clinton
entrance.east = chest

boring.north = one_door
boring.west = creepy

clinton.west = liquid
clinton.east = cake_lie

chest.north = dark

one_door.north = liquid

creepy.west = soup_time

soup_time.north = sword
soup_time.south = hat

sword.north = statue

liquid.west = ham

ham.north = gold

gold.east = dark
gold.north = death
gold.west = statue

dark.north = peach
dark.visible = False

death.east = peach
death.north = secret

secret.locked = True

peach.east = organ

organ.south = cake_lie

secret.east = lava

lava.north = portal

portal.north = crypt

# Room items

entrance.items = adv.Bag([Item("torch", "lit torch")])

boring.items = adv.Bag([Item("stool", "small stool")])

clinton.items = adv.Bag(
    [Item("campaign poster", "clinton 2016 poster", "poster")])

one_door.items = adv.Bag([Item("small dagger", "knife", "dagger")])

hat.items = adv.Bag([Item("purple hat", "hat")])

sword.items = adv.Bag([Item("broadsword", "sword")])

ham.items = adv.Bag([Item("suspicious cake", "sus cake")])

gold.items = adv.Bag([Item("small key", "little key")])

cake_lie.items = adv.Bag([Item("piece of cake", "cake slice", "cake")])

peach.items = adv.Bag([Item("rotting peach", "peach")])

dark.items = adv.Bag([Item("large key", "big key")])

secret.items = adv.Bag([Item("bar of gold", "gold bar", "gold ingot", "gold")])

soup_time.items = adv.Bag([
    Item("mysterious floating orb", "orb", "mysterious orb", "floating orb",
         "soup time")
])

crypt.items = adv.Bag([
    Item("skull", "old skull", "ancient skull"),
    Item("femur", "legbone", "femur bone")
])

# Entities in rooms

entrance.entities.add(
    Character("skeleton", "An old, crumbling skeleton of a not-quite-human.",
              ["clank", "creak", "crunch", "crack"]))

liquid.entities.add(
    Character("rat", "A big rat that shambles about the room.",
              ["squeak", "squonk", "screech", "peep"]))

statue.entities.add(
    Character(
        "statue",
        "A statue of an armor-clad warrior. It holds a big spear in its right hand.",
        ["thud", "thunk", "creak", "crack"]))

crypt.entities.add(
    Character("zombie",
              "An undead creature with glowing green eyes and a scimitar.",
              ["bleugh", "blargh", "auch", "throrp", "ugh"]))
