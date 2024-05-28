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
import numpy


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
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
    map = Map.Map(11)
    map.fillMap(game_state)
    map.evaluateMap()
    my_head = map.head
    moves = []
    if my_head[0] > 0:
        moves.append([map.array[my_head[0]-1][my_head[1]], "left"])
    if my_head[0] < map.dimension:
        moves.append([map.array[my_head[0]+1][my_head[1]], "right"])
    if my_head[1] > 0:
        moves.append([map.array[my_head[0]][my_head[1]-1], "down"])
    if my_head[1] < map.dimension:
        moves.append([map.array[my_head[0]][my_head[1]+1], "up"])
    while len(moves) > 1:
        if moves[0][0] <= moves[1][0]:
            moves.pop(0)
        else:
            moves.pop(1)
    next_move = moves[0][1]
    print(f"MOVE {game_state['turn']}: {next_move}")
    result = numpy.flip(map.array, axis=0)
    print(map.array)
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    nextmove = move({
        "game": {
            "id": "totally-unique-game-id",
            "ruleset": {
                "name": "standard",
                "version": "v1.1.15",
                "settings": {
                    "foodSpawnChance": 15,
                    "minimumFood": 1,
                    "hazardDamagePerTurn": 14
                }
            },
            "map": "standard",
            "source": "league",
            "timeout": 500
        },
        "turn": 14,
        "board": {
            "height": 11,
            "width": 11,
            "food": [
                {"x": 5, "y": 5},
                {"x": 9, "y": 0},
                {"x": 2, "y": 6}
            ],
            "hazards": [
                {"x": 3, "y": 2}
            ],
            "snakes": [
                {
                    "id": "snake-508e96ac-94ad-11ea-bb37",
                    "name": "My Snake",
                    "health": 54,
                    "body": [
                        {"x": 0, "y": 0},
                        {"x": 1, "y": 0},
                        {"x": 2, "y": 0}
                    ],
                    "latency": "111",
                    "head": {"x": 0, "y": 0},
                    "length": 3,
                    "shout": "why are we shouting??",
                    "customizations":{
                        "color":"#FF0000",
                        "head":"pixel",
                        "tail":"pixel"
                    }
                },
                {
                    "id": "snake-b67f4906-94ae-11ea-bb37",
                    "name": "Another Snake",
                    "health": 16,
                    "body": [
                        {"x": 5, "y": 4},
                        {"x": 5, "y": 3},
                        {"x": 6, "y": 3},
                        {"x": 6, "y": 2}
                    ],
                    "latency": "222",
                    "head": {"x": 5, "y": 4},
                    "length": 4,
                    "shout": "I'm not really sure...",
                    "customizations":{
                        "color":"#26CF04",
                        "head":"silly",
                        "tail":"curled"
                    }
                }
            ]
        },
        "you": {
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [
                {"x": 0, "y": 0},
                {"x": 1, "y": 0},
                {"x": 2, "y": 0}
            ],
            "latency": "111",
            "head": {"x": 0, "y": 0},
            "length": 3,
            "shout": "why are we shouting??",
            "customizations": {
                "color":"#FF0000",
                "head":"pixel",
                "tail":"pixel"
            }
        }
    })
    #from server import run_server

    #run_server({"info": info, "start": start, "move": move, "end": end})
