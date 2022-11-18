import math
import random
import typing

def check_my_body(body_move_safe, directional_adjustments, game_state):
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_body = game_state['you']['body']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    for direction in body_move_safe:
        if body_move_safe[direction]:
            temp_move = {'x': my_head['x'] + directional_adjustments[direction][0], 'y': my_head['y'] + directional_adjustments[direction][1]}
            edge_check = temp_move['x'] < 0 or temp_move['y'] < 0 or temp_move['x'] > board_width -1 or temp_move['y'] > board_height -1
            if temp_move in my_body or ("wrapped" not in game_state['game']['ruleset']['name'] and edge_check):
                body_move_safe[direction] = 0
    
    return body_move_safe

def check_environment(envi_move_safe, directional_adjustments, game_state):
    opponents = game_state['board']['snakes']
    hazards = game_state['board']['hazards']
    my_head = game_state["you"]["body"][0]
    dangerous_locations = []
    for snake in opponents:
        for body_part in snake['body']:
            if body_part not in dangerous_locations:
                dangerous_locations.append(body_part)
    for hazard in hazards:
        if hazard not in dangerous_locations:
            dangerous_locations.append(hazard)

    for direction in envi_move_safe:
        if envi_move_safe[direction]:
            temp_move = {'x': my_head['x'] + directional_adjustments[direction][0], 'y': my_head['y'] + directional_adjustments[direction][1]}
            if temp_move in dangerous_locations:
                envi_move_safe[direction] = 0

    return envi_move_safe

def weight_food_moves(food_move_safe, directional_adjustments, game_state):
    food = game_state['board']['food']
    if len(food) > 0:
        my_head = game_state["you"]["body"][0]
        closest_food = determine_closest_food(food, my_head)
        x_distance = abs(closest_food['x'] - my_head['x'])
        y_distance = abs(closest_food['y'] - my_head['y'])

        for direction in food_move_safe:
            if food_move_safe[direction]:
                temp_move = {'x': my_head['x'] + directional_adjustments[direction][0], 'y': my_head['y'] + directional_adjustments[direction][1]}
                temp_x_distance = abs(closest_food['x'] - temp_move['x'])
                temp_y_distance = abs(closest_food['y'] - temp_move['y'])

                if temp_x_distance <= x_distance and temp_y_distance <= y_distance:
                    food_move_safe[direction] += 0.5

    return food_move_safe

def determine_closest_food(food_array, head):
    closest_food = food_array[0]
    x_distance = abs(closest_food['x'] - head['x'])
    y_distance = abs(closest_food['y'] - head['y'])

    for food in food_array:
        temp_x_distance = abs(food['x'] - head['x'])
        temp_y_distance = abs(food['y'] - head['y'])
        if temp_x_distance < x_distance and temp_y_distance < y_distance:
            closest_food = food
            y_distance = temp_y_distance
            x_distance = temp_x_distance
    return closest_food


def move(game_state: typing.Dict) -> typing.Dict:
    print(game_state)
    is_move_safe = {
      "up": 1, 
      "down": 1, 
      "left": 1, 
      "right": 1
    }
    direction_adjustments = {'left': (-1,0), 'right': (1,0), 'up': (0,1), 'down': (0,-1)}

    is_move_safe = check_my_body(is_move_safe, direction_adjustments, game_state)
    is_move_safe = check_environment(is_move_safe, direction_adjustments, game_state)
    is_move_safe = weight_food_moves(is_move_safe, direction_adjustments, game_state)

    print(is_move_safe)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe != 0:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    next_move = 'down'
    move_weight = 0
    for move, weight in is_move_safe.items():
        if weight > move_weight:
            next_move = move
            move_weight = weight

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}