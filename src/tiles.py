class Symbol:
    def __init__(
        self,
        name,
        coin_value=0,
        interactions={},
        chance = [],
        other = None,
        self_destruct=False,
        destruction_coin_bonus=0,
        on_destroy_add = [],
        timed = None
    ):
        self.name = name
        self.coin_value = coin_value
        self.multiplier = 1
        self.interactions = interactions.copy()
        if type(self.interactions) != dict:
            print(name)
        self.self_destruct = self_destruct
        self.destruction_coin_bonus = destruction_coin_bonus
        self.on_destroy_add = on_destroy_add
        self.chance = chance
        self.other = other
        self.timed = timed

        self.bonus_coins = 0
        self.bonus_mult  = 1
        self.times_shown = 0

        self.calc_value = 0

def plus(n):
    return (n, 1, False, False)

def minus(n):
    return (-n, 1, False, False)

def mult(n):
    return (0, n, False, False)

def combine(a, b):
    return (a[0] + b[0], a[1] * b[1], a[2] or b[2], a[3])

def add_symbol(symbol):
    return (0, [symbol], False)

def destroy_self():
    return (0, [], True)

def destroy():
    return [destruct, destruct]

def eat_coin(n):
    return [plus(n), destruct]

def eat_mult(n):
    return [mult(n), destruct]

def eat_perm():
    return [(1, 1, False, True), destruct]

def timed_destory(n):
    return (n, (0, True))

def timed_coin(n, coin):
    return (n, (coin, False))

destruct = (0, 1, True, False)

# TODO the code could be refactored to avoid typing each symbol name twice 

IDS = {
    "symbol": {
        # special
        "dud": Symbol("dud", 0),
        "empty": Symbol("empty", 0),
        # common
        "anchor": Symbol("anchor", 1),
        "banana": Symbol("banana", 1, {"thief":  destroy()}, on_destroy_add=["banana_peel"]),
        "banana_peel": Symbol("banana_peel", 1,  {"lockbox":  destroy()}),
        "bee": Symbol("bee", 1, {"flower": mult(2),"beehive": mult(2),"honey": mult(2)}),
        "beer": Symbol("beer", 1),
        "bounty_hunter": Symbol("bounty_hunter", 1, {"thief": [plus(20), destruct]}),
        "bubble": Symbol("bubble", 2),
        "candy": Symbol("candy", 1),
        "cat": Symbol("cat", 1,  {"milk": eat_coin(9)}),
        "cheese": Symbol("cheese", 1),
        "cherry": Symbol("cherry", 1),
        "coal": Symbol("coal", 0, timed = timed_destory(20), on_destroy_add=["diamond"]),
        "coin": Symbol("coin", 1),
        "crab": Symbol("crab", 1),
        "crow": Symbol("crow", 2, timed=timed_coin(4, -3)),
        "cultist": Symbol("cultist", 0, other=1),
        "d3": Symbol("d3", 2),
        "dog": Symbol("dog", 1),
        "dwarf": Symbol("dwarf", 1, {"beer": eat_mult(10), "wine": eat_mult(10)}),
        "egg": Symbol("egg", 1, chance=[(10, destroy_self())], on_destroy_add=["chick"]),
        "flower": Symbol("flower", 1),
        "goldfish": Symbol("goldfish", 1),
        "goose": Symbol("goose", 1, chance=[(1, add_symbol("golden_egg"))]),
        "key": Symbol("key", 1, {"lockbox": destroy(), "safe": destroy(),"treasure_chest": destroy(), "mega_chest": destroy()}),
        "lockbox": Symbol("lockbox", 1, destruction_coin_bonus=15),
        "magpie": Symbol("magpie", -1, timed=timed_coin(4, 9)),
        "milk": Symbol("milk", 1),
        "miner": Symbol("miner", 1, {"ore": eat_coin(10), "big_ore": eat_coin(10)}),
        "monkey": Symbol("monkey", 1, {"coconut":  eat_mult(5), "coconut_half":  eat_mult(5)}),
        "mouse": Symbol("mouse", 1, {"cheese":eat_coin(15)}),
        "ore": Symbol("ore", 1),
        "owl": Symbol("owl", 1),
        "oyster": Symbol("oyster", 0, chance=[(20, add_symbol("pearl"))], on_destroy_add=["pearl"]),
        "pearl": Symbol("pearl", 1),
        "present": Symbol("present", 0, timed=timed_destory(10), destruction_coin_bonus=10),
        "seed": Symbol("seed", 1),
        "shiny_pebble": Symbol("shiny_pebble", 1),
        "snail": Symbol("snail", 0, timed=timed_coin(4, 5)),
        "toddler": Symbol("toddler", 1, {"present": eat_coin(6),"candy": eat_coin(6), "pinata": eat_coin(6), "bubble": eat_coin(6)}),
        "turtle": Symbol("turtle", 0, timed=timed_coin(3, 4)),
        "urn": Symbol("urn", 1, on_destroy_add=["spirit"]),
        # uncommon
        "bar_of_soap": Symbol("bar_of_soap", 1, chance=[(100, add_symbol("bubble"))]),
        "bear": Symbol("bear", 2, {"honey": eat_coin(35)}),
        "big_ore": Symbol("big_ore", 2),
        "big_urn": Symbol("big_urn", 2, on_destroy_add=["spirit", "spirit"]),
        "billionaire": Symbol("billionaire", 0, destruction_coin_bonus=35),
        "bronze_arrow": Symbol("bronze_arrow", 0),
        "buffing_powder": Symbol("buffing_powder", 0, {"any": mult(2)}, self_destruct=True),
        "chemical_seven": Symbol("chemical_seven", 0, self_destruct=True, destruction_coin_bonus=7),
        "chick": Symbol("chick", 1, chance=[(10, destroy_self())], on_destroy_add=["chicken"]),
        "clubs": Symbol("clubs", 1),
        "coconut": Symbol("coconut", 1, on_destroy_add=["coconut_half", "coconut_half"]),
        "coconut_half": Symbol("coconut_half", 2),
        "d5": Symbol("d5", 2.5),
        "diamonds": Symbol("diamonds", 1),
        "essence_capsule": Symbol("essence_capsule", 0, self_destruct=True, destruction_coin_bonus=5), #make them seem takable. Saves runs
        "golem": Symbol("golem", 0, timed=timed_destory(5), on_destroy_add=["ore","ore","ore","ore","ore"]),
        "hearts": Symbol("hearts", 1),
        "hex_of_destruction": Symbol("hex_of_destruction", -99),
        "hex_of_draining": Symbol("hex_of_draining", -99),
        "hex_of_emptiness": Symbol("hex_of_emptiness", -99),
        "hex_of_hoarding": Symbol("hex_of_hoarding", -99), #wrong
        "hex_of_midas": Symbol("hex_of_midas", 3, chance=[(30, add_symbol("coin"))]),
        "hex_of_tedium": Symbol("hex_of_tedium", 3),
        "hex_of_thievery": Symbol("hex_of_thievery", 3, chance=[(30, (-6, None, False))]),
        "hooligan": Symbol("hooligan", 1),
        "hustler": Symbol("hustler", -7),
        "item_capsule": Symbol("item_capsule", 0, self_destruct=True),
        "lucky_capsule": Symbol("lucky_capsule", 0, self_destruct=True, destruction_coin_bonus=10), #Wealthy Caps
        "matryoshka_doll_1": Symbol("matryoshka_doll_1", 0),
        "ninja": Symbol("ninja", 2, other=-1),
        "orange": Symbol("orange", 2),
        "peach": Symbol("peach", 2),
        "pinata": Symbol("pinata", 1, on_destroy_add=["candy","candy","candy","candy","candy"]),
        "plum": Symbol("plum", 2),
        "rabbit": Symbol("rabbit", 1),
        "rabbit_fluff": Symbol("rabbit_fluff", 2),
        "rain": Symbol("rain", 2, {"flower":mult(2)}),
        "rarity_capsule": Symbol("rarity_capsule", 0, self_destruct=True, destruction_coin_bonus=5), #make them seem takable. Saves runs
        "removal_capsule": Symbol("removal_capsule", 0, self_destruct=True),
        "reroll_capsule": Symbol("reroll_capsule", 0, self_destruct=True),
        "safe": Symbol("safe", 1, destruction_coin_bonus=30),
        "sapphire": Symbol("sapphire", 2),
        "sloth": Symbol("sloth", 0, timed=timed_coin(2,3)),
        "spades": Symbol("spades", 1),
        "target": Symbol("target", 2),
        "tedium_capsule": Symbol("tedium_capsule", 0, self_destruct=True, destruction_coin_bonus=5),
        "thief": Symbol("thief", -1, destruction_coin_bonus=10),
        "void_creature": Symbol("void_creature", 0, {"empty":plus(1)}, destruction_coin_bonus=8),
        "void_fruit": Symbol("void_fruit", 0, {"empty":plus(1)}, destruction_coin_bonus=8),
        "void_stone": Symbol("void_stone", 0, {"empty":plus(1)}, destruction_coin_bonus=8),
        "wine": Symbol("wine", 2),
        "wolf": Symbol("wolf", 2),  
        # rare
        "amethyst": Symbol("amethyst", 1),
        "apple": Symbol("apple", 3),
        "archaeologist": Symbol("archaeologist", 2, {"ore":eat_perm(), "big_ore":eat_perm(), "pearl":eat_perm(), "shiny_pebble":eat_perm(), "sapphire":eat_perm()}),
        "bartender": Symbol("bartender", 3),
        "beastmaster": Symbol("beastmaster", 2),
        "beehive": Symbol("beehive", 3, chance=[(10, add_symbol("honey"))]),
        "card_shark": Symbol("card_shark", 2),
        "chef": Symbol("chef", 2),
        "chicken": Symbol("chicken", 2, chance=[(5, add_symbol("egg")), (1, add_symbol("golden_egg"))]),
        "cow": Symbol("cow", 3, chance=[(15, add_symbol("milk"))]),
        "dame": Symbol("dame", 2),
        "diver": Symbol("diver", 2, {"pearl":eat_perm(), "anchor":eat_perm(), "goldfish":eat_perm(), "snail":eat_perm(), "turtle":eat_perm(), "crab":eat_perm(), "oyster":eat_perm()}),
        "emerald": Symbol("emerald", 3),
        "farmer": Symbol("farmer", 2),
        "frozen_fossil": Symbol("frozen_fossil", 0, timed=timed_destory(20), on_destroy_add=["eldritch_beast"]),
        "general_zaroff": Symbol("general_zaroff", 1),
        "golden_egg": Symbol("golden_egg", 3),
        "honey": Symbol("honey", 3),
        "joker": Symbol("joker", 3),
        "king_midas": Symbol("king_midas", 3, {"coin":mult(3)}, chance=[(100, add_symbol("coin"))]),
        "magic_key": Symbol("magic_key", 2, {"lockbox": [destruct, (0, 3, True)], "safe": [destruct, (0, 3, True)],"treasure_chest": [destruct, (0, 3, True)], "mega_chest":  [destruct, (0, 3, True)]}),
        "martini": Symbol("martini", 3),
        "mine": Symbol("mine", 1, timed=timed_destory(4), chance=[(100, add_symbol("ore"))]),
        "moon": Symbol("moon", 3, {"owl":mult(3), "rabbit":mult(3), "wolf":mult(3)}, on_destroy_add=["cheese","cheese","cheese"]),
        "mrs_fruit": Symbol("mrs_fruit", 2, {"cherry":eat_perm(), "banana":eat_perm(), "coconut":eat_perm(), "coconut_half":eat_perm()}),
        "omelette": Symbol("omelette", 3),
        "pear": Symbol("pear", 1),
        "robin_hood": Symbol("robin_hood", -4, {"apple":eat_coin(15), "billionaire":eat_coin(15), "target":eat_coin(15)}, timed=timed_coin(4, 29)),
        "ruby": Symbol("ruby", 3),
        "silver_arrow": Symbol("silver_arrow", 0),
        "spirit": Symbol("spirit", 4, timed=timed_destory(4)),
        "strawberry": Symbol("strawberry", 3),
        "sun": Symbol("sun", 3, {"flower": mult(5)}),
        "tomb": Symbol("tomb", 3, on_destroy_add=["spirit","spirit","spirit","spirit","spirit"]),
        "treasure_chest": Symbol("treasure_chest", 2, destruction_coin_bonus=50),
        "witch": Symbol("witch", 2),
        # very_rare
        "diamond": Symbol("diamond", 5, other=1),
        "eldritch_beast": Symbol("eldritch_beast", 4),
        "golden_arrow": Symbol("golden_arrow", 0),
        "highlander": Symbol("highlander", 6),
        "mega_chest": Symbol("mega_chest", 3, destruction_coin_bonus=100,),
        "midas_bomb": Symbol("midas_bomb", 0, {"any": mult(7)}, self_destruct=True),
        "pirate": Symbol("pirate", 2, {"coin": eat_perm(), "lockbox": eat_perm(), "safe": eat_perm(),"treasure_chest": eat_perm(), "mega_chest":  eat_perm()}),
        "watermelon": Symbol("watermelon", 4),
        "wildcard": Symbol("wildcard", 0),
    },
    "items": {
        "common": {
            "pool_ball",
            "adoption_papers",
            "birdhouse",
            "black_pepper",
            "blue_pepper",
            "brown_pepper",
            "checkered_flag",
            "cyan_pepper",
            "egg_carton",
            "fifth_ace",
            "fish_bowl",
            "frying_pan",
            "grave_robber",
            "gray_pepper",
            "green_pepper",
            "guillotine",
            "happy_hour",
            "jackolantern",
            "kyle_the_kernite",
            "lime_pepper",
            "lockpick",
            "lucky_cat",
            "lucky_seven",
            "lunchbox",
            "maxwell_the_bear",
            "mining_pick",
            "ninja_and_mouse",
            "nori_the_rabbit",
            "oswald_the_monkey",
            "pink_pepper",
            "pizza_the_cat",
            "purple_pepper",
            "quigley_the_wolf",
            "rain_cloud",
            "red_pepper",
            "reroll",
            "ricky_the_banana",
            "shedding_season",
            "swear_jar",
            "symbol_bomb_small",
            "tax_evasion",
            "treasure_map",
            "wanted_poster",
            "watering_can",
            "white_pepper",
            "yellow_pepper",
        },
        "uncommon": {
            "horseshoe",
            "anthropology_degree",
            "barrel_o_dwarves",
            "black_cat",
            "blue_suits",
            "capsule_machine",
            "cardboard_box",
            "cleaning_rag",
            "coin_on_a_string",
            "comfy_pillow",
            "compost_heap",
            "conveyor_belt",
            "cursed_katana",
            "dwarven_anvil",
            "fertilizer",
            "flush",
            "fruit_basket",
            "goldilocks",
            "lefty_the_rabbit",
            "lemon",
            "lint_roller",
            "looting_glove",
            "piggy_bank",
            "red_suits",
            "ritual_candle",
            "rusty_gear",
            "shattered_mirror",
            "shrine",
            "symbol_bomb_big",
            "time_machine",
            "triple_coins",
            "x_ray_machine",
            "zaroffs_contract",
        },
        "rare": {
            "bowling_ball",
            "bag_of_holding",
            "booster_pack",
            "chicken_coop",
            "chili_powder",
            "clear_sky",
            "coffee",
            "devils_deal",
            "dishwasher",
            "holy_water",
            "lucky_carrot",
            "lucky_dice",
            "oil_can",
            "protractor",
            "quiver",
            "recycling",
            "sunglasses",
            "swapping_device",
            "symbol_bomb_very_big",
            "undertaker",
            "void_portal",
        },
        "very_rare": {
            "four_leaf_clover",
            "ancient_lizard_blade",
            "copycat",
            "frozen_pizza",
            "golden_carrot",
            "popsicle",
            "telescope",
        },
    },
}
