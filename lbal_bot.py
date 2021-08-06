import os
import time
from pydirectinput import click, press
import json
import numpy as np
import random
from copy import copy, deepcopy

from tiles import IDS

save_path = os.getenv('APPDATA') +"\\Godot\\app_userdata\\Luck be a Landlord\\LBAL.save"

nodes = 1000

def startup():
    os.startfile("steam://rungameid/1404850")
    time.sleep(2)


def new_game():
    click(961, 540)
    click(380, 730)
    click(950, 850)
    time.sleep(0.5)
    accept()


def add(index):
    press(str(index))


def accept():
    press("enter")


def spin():
    press("space")


def deny():
    press("backspace")


def skip():
    press("s")

def predict_board(symbols, nodes, layers):
    returned = []
    for _ in range(nodes):
        out = predict_thread(symbols, layers)
        returned.append(sum(out) / len(out))

    return sum(returned) / len(returned)

def predict_thread(symbols, layers, layer=1):
    coin = 0

    symbols = deepcopy(symbols)
    tiles = copy(symbols)

    tiles.extend([IDS["symbol"]["empty"]] * max(0, 20 - len(tiles)))
    tiles = np.reshape(random.sample(tiles, 20), (4, 5))

    removal = set()
    add = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile.bonus_coins != 0:
                print(tile.bonus_coins)
            neighbours = [tiles[yn][xn] 
                            for xoff in range(-1, 2)
                            for yoff in range(-1, 2)
                            if (not (xoff == 0 and yoff == 0)
                                and 0 <= (xn := x+xoff) < 5
                                and 0 <= (yn := y+yoff) < 4)]

            for z in neighbours:
                if z.name in tile.interactions or "any" in tile.interactions:
                    interaction = tile.interactions[z.name if z.name in tile.interactions else "any"]
                    if type(interaction) == list:
                        tile.coin_value += interaction[0][0]
                        tile.coin_value += interaction[0][1] * z.coin_value if interaction[0][1] != 0 else 0
                        if interaction[0][2]: removal.add(tile)
                        interaction = interaction[1]

                    z.coin_value += interaction[0]
                    z.multiplier *= interaction[1]
                    if interaction[2]: removal.add(z)
            
            for x in tile.chance:
                if x[0] >= random.random():
                    tile.coin_value += x[1][0]
                    if x[1][1] != None: add.extend(x[1][1])
                    if x[1][2] != None: removal.add(tile)
            
            if tile.other != None:
                tile_names = [m.name for m in tiles.flatten()]
                if tile.name in tile_names:
                    count = tile_names.count(tile.name) - 1
                    for _ in range(count):
                        tile.coin_value += tile.other
            
            if tile.dice != None:
                tile.coin_value += random.randint(1, tile.dice)

            if tile.self_destruct:
                removal.add(tile)


    coin = np.sum(np.vectorize(lambda m : (m.coin_value + m.bonus_coins) * (m.multiplier + m.bonus_mult))(tiles))

    if removal:
        for x in removal:
            symbols.remove(x)
            add.extend(x.on_destroy_add)
            coin += (x.destruction_coin_bonus + x.bonus_coins) * (x.multiplier + x.bonus_mult)

    symbols.extend([IDS["symbol"][y] for y in add])
   
    if layer != layers:
        return [coin] + predict_thread(symbols, layers, layer+1)
    return [coin]

def parse_save(last_save, last_info):
    try:
        with open(save_path, "r") as save:
            lines = save.readlines()
    except IOError:
        lines = []
        last_save = {}

    lines = list(map(json.loads, lines))
    info = dict()

    if last_save != {}:
        # TODO: Inventory Sorts Items value/rarity/alphabet

        symbols = []
        data = []
        for i in range(3, 8):
            symbols.extend(lines[i]["icon_types"])
            data.extend(lines[i]["saved_icon_data"])

        info["symbols"] = [(x[0], copy(IDS["symbol"][x[1]])) for x in list(filter(lambda a:  a[1] != "empty", zip(data, symbols)))]

        try:
            for x in info["symbols"]:
                x[1].bonus_coins = x[0]["permanent_bonus"]
                x[1].bonus_mult = x[0]["permanent_multiplier"]
                x[1].times_shown = x[0]["times_displayed"]
        except Exception as e:
            pass
        
        
        info["symbols"] = [x[1] for x in info["symbols"]]

        if not info["symbols"]:
            accept()
        
        info["choices"] = lines[9]["saved_card_types"]
        info["email"]   = lines[9]["emails"]
        info["remove"]  = lines[9]["removal_tokens"]
        info["reroll"]  = lines[9]["reroll_tokens"]

        info["coins"]   = lines[2]["coins"]

        rent = lines[9]["rent_values"]

        info["rentCost"]  = rent[0]
        info["turnsLeft"] = rent[1]

    else:
        info = last_info

    return lines, info


def bot():
    save = {}
    info = {}
    first_spin = True
    lass = ""

    while True:
        x, info = parse_save(save, info)
        if not x:
            continue
        save = x
        if not info:
            continue

        time.sleep(0.1)

        if info["email"]:
            first_spin = True
            email = info["email"][0]
            if email["replies"] == ["<icon_confirm>"]:
                accept()

            elif email["replies"] == ["skip"]:
                skip()

            elif email["type"] == "rent_due":
                accept()

            elif email["type"] == "add_tile":
                tile_num = 1
                layers = info["turnsLeft"] if info["coins"] < info["rentCost"] else max(10, info["turnsLeft"])
                adverage = predict_board(info["symbols"], nodes, layers)
                choices = [predict_board(info["symbols"] + [copy(IDS["symbol"][symbol])], nodes, layers) for symbol in info["choices"]]
                print(list(zip(info["choices"], [round(x, 2) for x in choices])))
                max_value = max(choices)

                if max_value >= adverage:
                    if choices.count(max(choices)) > 1:
                        indexes = [i for i, element in enumerate(choices) if element == max(choices)]      
                        max_interactions = -1

                        for x in indexes:
                            y = len(info["symbols"][x].interactions)
                            if y > max_interactions:
                                max_interactions = y
                                tile_num = x          
                    else:
                        tile_num = choices.index(max(choices))

                    add(tile_num + 1)

                    b = max_value, info["choices"][tile_num]
                else:
                    skip()
                    b = "Too Low: " + str(adverage)

                if lass != b:
                    print(b)
                    lass = b

            elif email["type"] == "add_item":
                print(info["choices"][0])
                add(1)

            elif email["type"] == "comfy_pillow_prompt" or email["type"] == "33":
                if info["coins"] > info["rentCost"]:
                    accept()
                else:
                    deny()

            elif email["type"] == "oil_can_prompt":
                deny()
            elif email["type"] == "swap_prompt_1":
                deny()
            elif email["type"] == "game_over":
                quit()
            else:
               print(email)

        else:
            if first_spin:
                spin()
                first_spin = False


#startup()
#new_game()
bot()
