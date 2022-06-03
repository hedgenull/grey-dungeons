from adventurelib import Bag
from colorama import init, Fore

# A few important things

my_name = None
my_species = None
my_health = 100
my_inventory = Bag()

INVENTORY_SIZE = 10
current_item = None

FONTS = [
    "calgphy2",
    "amcslash",
    "amcaaa01",
    "alligator",
    "amcrazor",
    "chunky",
    "defleppard",
    "fantasy1",
    "fire_font-s",
    "isometric1",
    "poison",
    "sblood",
]
ERRORS = [
    "What?",
    "I don't know what you mean.",
    "Are you crazy?",
    "Huh?",
    "I don't Kown.",
    "Um, what?",
    "Whatever do you mean?",
    "I don't understand.",
]
SPECIES = ["elf", "human", "dwarf", "half-dragon"]
TASTES = [
    "palpable",
    "disgusting",
    "chewy",
    "sharp",
    "sweet",
    "spicy",
    "moldy",
    "mild",
    "bitter",
    "salty",
    "good",
    "delicious",
    "loathsome",
    "toothsome",
    "tasty",
    "smoky",
    "mouthwatering",
    "greasy",
    "savory",
    "buttery",
    "damp",
    "soggy",
]
CONTEMPLATIONS = [
    "Ergh. Will I ever escape this cursed crypt?",
    "Ah, life is merely a conjuration of the mind seeking its own meaning.",
    "The eggs should be fresh back home today.",
    "Others have perished in these forgotten catacombs before. Soon, unless fortune decrees, I too must meet the same fate.",
    "The universe is nothing. Everything is nothing. Nothing is everything.",
    "Ah, me! Lo, that I would in vain attempt to reach the flower of mine youth!",
    "I think, therefore I am.",
    "The only thing I know is that I know nothing.",
    "Life is the measure of all things.",
]

BRAIN_DAMAGE = [
    "You show {name} the latest CNN article. Its stunning lack of logic gives {obj} a pounding headache just looking at it.",
    "You tell {name} that water is dry. {name}'s head summarily explodes.",
    "You show {name} how Biden clearly won the 2020 election. {obj} faints dead away.",
    "You tell {name} that pay phones are disappearing so that they can't exit the Matrix. {sbj} goes into a coma.",
]

STORY = """
While crossing the Eldon Mountains to travel to the city of Bahreto'kala,
you find yourself hopelessly lost. Stumbling through the whirling snow,
you catch a glimpse of a door in the rock. Eagerly, you rush into the passage-
but barely do you dash in when the door crumbles and a huge boulder covers the
only way out!

You're really in a pickle this time!

What is this dungeon? What lurks inside? Why is it even here?

Will you escape the Grey Dungeons?
"""

# Initialize colorama and set colors

init()

RED = Fore.LIGHTRED_EX
BLUE = Fore.LIGHTCYAN_EX
YELLOW = Fore.LIGHTYELLOW_EX
MAGENTA = Fore.LIGHTMAGENTA_EX

MAIN_COLOR = BLUE
