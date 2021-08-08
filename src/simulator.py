import numpy as np
import random
from copy import copy, deepcopy

from numba import njit

import time

from tiles import IDS

#@njit
def predict_board(symbols, nodes, layers):
    returned = []
    for _ in range(nodes):
        out = predict_thread(symbols, layers)
        returned.append(sum(out) / len(out))

    return sum(returned) / len(returned)

#@njit
def predict_thread(symbols, layers, layer=1):
    coin = 0
    removal = set()
    add = []

    symbols = deepcopy(symbols)
    tiles = copy(symbols)

    tiles.extend([IDS["symbol"]["empty"]] * max(0, 20 - len(tiles)))
    tiles = np.reshape(random.sample(tiles, 20), (4, 5))

    for row in tiles:
        for tile in row:
            tile.calc_value = tile.coin_value
            tile.multiplier = 1
            tile.times_shown += 1

            for x in tile.chance:
                if x[0] >= random.random():
                    tile.calc_value += x[1][0]
                    if x[1][1] != None: add.extend(x[1][1]) #TODO Add instantly and handle empty properly
                    if x[1][2] != None: removal.add(tile)

            if tile.timed is not None:
                if tile.times_shown % tile.timed[0] == 0:
                    tile.calc_value += tile.timed[1][0]
                    if tile.timed[1][1]: removal.add(tile)

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            
            
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
                        tile.calc_value += interaction[0][0]
                        tile.calc_value += interaction[0][1] * z.calc_value if interaction[0][1] != 0 else 0
                        if interaction[0][2]: removal.add(tile)
                        if interaction[0][3]: tile.bonus_coins += 1
                        interaction = interaction[1]

                    z.calc_value += interaction[0]
                    z.multiplier *= interaction[1]
                    if interaction[2]: removal.add(z)
            
            if tile.other != None:
                tile_names = [m.name for m in tiles.flatten()]
                if tile.name in tile_names:
                    tile.calc_value += tile.other * (tile_names.count(tile.name) - 1)
                    

            if tile.self_destruct:
                removal.add(tile)


    coin = np.sum(np.vectorize(lambda m : (m.calc_value + m.bonus_coins) * (m.multiplier * m.bonus_mult))(tiles))

    if removal:
        for x in removal:
            symbols.remove(x)
            add.extend(x.on_destroy_add)
            coin += x.destruction_coin_bonus  * (x.multiplier * x.bonus_mult)

    symbols.extend([IDS["symbol"][y] for y in add])
   
    if layer != layers:
        return [coin] + predict_thread(symbols, layers, layer+1)
    return [coin]


if __name__ == '__main__':
    a = ["archaeologist","archaeologist","d5","d5","d5","d5","d5","d5","d5","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl","pearl",]
    a = [copy(IDS["symbol"][x]) for x in a]

    start = time.perf_counter()
    print(predict_board(a, 1000, 20))
    print(time.perf_counter()-start)