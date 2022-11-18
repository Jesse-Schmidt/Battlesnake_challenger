
import random
import typing

def check_my_body(is_move_safe, game_state):
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_body = game_state['you']['body']

    for body_part in my_body:
        if body_part['x'] + 1 == my_head['x']:
            is_move_safe['left'] = False
        elif body_part['x'] - 1 == my_head['x']:
            is_move_safe['right'] = False
        elif body_part['y'] + 1 == my_head['y']:
            is_move_safe['down'] = False
        elif body_part['y'] - 1 == my_head['y']:
            is_move_safe['up'] = False
    return is_move_safe

def check_environment(is_move_safe, game_state):
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    #avoid hitting the walls
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    elif my_head["x"] == board_width-1:
        is_move_safe['right'] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    elif my_head["y"] == board_height-1:
        is_move_safe['up'] = False
    return is_move_safe

def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }
    is_move_safe = check_my_body(is_move_safe, game_state)
    is_move_safe = check_environment(is_move_safe, game_state)


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}