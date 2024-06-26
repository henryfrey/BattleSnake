# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import Map
import time 
import numpy

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Henry Freyschmidt",  # TODO: Your Battlesnake Username
        "color": "#3E338F",  # TODO: Choose color
        "head": "tongue",  # TODO: Choose head
        "tail": "mlh-gene",  # TODO: Choose tail
    } 


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    starttime = time.time()
    map = Map.Map(11)
    map.fillMapData(game_state)
    map.findStrat()
    map.finalMapAdjustment()
    my_head = map.body[0]
    moves = []
    if my_head[0] > 0:
        moves.append([map.array[my_head[0]-1][my_head[1]], "left"])
    if my_head[0] < map.dimension -1:
        moves.append([map.array[my_head[0]+1][my_head[1]], "right"])
    if my_head[1] > 0:
        moves.append([map.array[my_head[0]][my_head[1]-1], "down"])
    if my_head[1] < map.dimension -1:
        moves.append([map.array[my_head[0]][my_head[1]+1], "up"])
    while len(moves) > 1:
        if moves[0][0] <= moves[1][0]:
            moves.pop(0)
        else:
            moves.pop(1)
    next_move = moves[0][1]
    print(f"MOVE {game_state['turn']}: {next_move}")
    print(f"Time: {time.time() - starttime}")
    print(numpy.rot90(map.array, 1, (0,1)))
    #print(map.snakeData)
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
