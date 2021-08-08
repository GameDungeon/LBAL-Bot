import os
import time
from pydirectinput import click, press
import json
from copy import copy
from collections import Counter

from tiles import IDS
from simulator import predict_board

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
                tile_num = 0
                layers = 20
                adverage = predict_board(info["symbols"], nodes, layers)
                choices = [predict_board(info["symbols"] + [copy(IDS["symbol"][symbol])], nodes, layers) for symbol in info["choices"]]
                print(f"adverage: {str(round(adverage, 2))}, " + ", ".join([f"{x[0]}: {x[1]}" for x in list(zip(info["choices"], [round(x, 2) for x in choices]))]))
                max_value = max(choices)

                if max_value >= adverage:
                    tile_num = choices.index(max(choices))
                    print(f"Picked: {info['choices'][tile_num]}")
                    add(tile_num + 1)
                else:
                    if info["reroll"] >= 1:
                        press("r")
                    else:
                        skip()

            elif email["type"] == "add_item":
                print("Picked: " + str(info["choices"][0]))
                if "guillotine_essence" in info["choices"]:
                    skip()
                else:
                    add(1)

            elif email["type"] == "comfy_pillow_prompt" or email["type"] == "comfy_pillow_essence_prompt":
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
                print(str(dict(Counter([x.name for x in info["symbols"]])))[1:-1].replace("'", ""))
                spin()
                first_spin = False


if __name__=="__main__":
    #startup()
    #new_game()
    bot()
