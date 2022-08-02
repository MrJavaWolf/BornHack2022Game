first_introduction_npc = {
    "position": {"x": 85, "y": 60},
    "collision_size": {"width": 20, "height": 16},
    "sprite_sheet": "/game_data/big_npc_0.bmp",
    "sprite_offset": {"x": -16, "y": -26},
    "sprite_sheet_tile_size": {"width": 32, "height": 36},
    "default_animation": "idle",
    "default_flip_x": True,
    "default_flip_y": False,
    "animations": [
        {
            "name": "idle",
            "fps": 0.45,
            "frames": [1, 2],
        },
        {
            "name": "happy_jump",
            "fps": 0.25,
            "frames": [3, 5, 5, 7],
            "loop_animation": False,
        },
    ],
    "actions": [
        {
            "action_type": "talk",
            "text": "Welcome to this badge game.\nI am so excited!",
        },
        {
            "action_type": "play_animation",
            "animation": "happy_jump",
        },
        {"action_type": "wait", "time": 1},
        {
            "action_type": "camera_shake",
            "time": 1,
            "amount": 10,
            "decrease_factor": 1,
        },
        {
            "action_type": "play_animation",
            "animation": "happy_jump",
        },
        {"action_type": "wait", "time": 1},
        {
            "action_type": "camera_shake",
            "time": 1,
            "amount": 10,
            "decrease_factor": 1,
        },
        {
            "action_type": "play_animation",
            "animation": "idle",
        },
        {
            "action_type": "talk",
            "text": "The controls are:",
        },
		{
            "action_type": "talk",
            "text": "To move:\nAn analog stick connected to A2 and A3",
        },
		{
            "action_type": "talk",
            "text": "To Dash:\nB Button",
        },
		{
            "action_type": "talk",
            "text": "To interact or attack:\nX Button",
        },
        {
            "action_type": "talk",
            "text": "You can change everything.\nNow go and have fun!",
        },
    ],
}

hidden_treasure_1_npc = {
    "position": {"x": 150, "y": 74},
    "collision_size": {"width": 16, "height": 16},
    "sprite_sheet": "/game_data/items.bmp",
    "sprite_offset": {"x": -8, "y": -8},
    "sprite_sheet_tile_size": {"width": 16, "height": 16},
    "default_animation": "idle",
    "default_flip_x": False,
    "default_flip_y": False,
    "animations": [
        {
            "name": "idle",
            "fps": 1,
            "frames": [21],
        },
        {
            "name": "open",
            "fps": 0.5,
            "frames": [
                21,
                22,
                23,
                23,
                23,
                23,
                23,
                23,
                22,
                21,
                25,
                26,
                27,
                26,
                27,
                26,
                27,
                27,
                27,
                27,
                27,
                27,
                27,
                26,
                21,
            ],
            "loop_animation": False,
        },
    ],
    "actions": [
        {
            "action_type": "play_animation",
            "animation": "open",
        }
    ],
}


change_character_npc = {
    "position": {"x": 355, "y": 50},
    "collision_size": {"width": 24, "height": 16},
    "sprite_sheet": "/game_data/player_4.bmp",
    "sprite_offset": {"x": -8, "y": -26},
    "sprite_sheet_tile_size": {"width": 16, "height": 32},
    "default_animation": "idle",
    "default_flip_x": True,
    "default_flip_y": False,
    "animations": [
        {
            "name": "idle",
            "fps": 0.45,
            "frames": [0, 1],
        },
        {
            "name": "happy_jump",
            "fps": 0.25,
            "frames": [3, 5, 5, 7],
            "loop_animation": False,
        },
    ],
    "actions": [
        {
            "action_type": "talk",
            "text": "Psst!",
        },
        {"action_type": "wait", "time": 1},
        {"action_type": "flip_sprite_x", "value": False},
        {"action_type": "wait", "time": 1},
        {"action_type": "flip_sprite_x", "value": True},
        {"action_type": "wait", "time": 1},
        {
            "action_type": "talk",
            "text": "Open player.py and you can change your look",
        },
        {
            "action_type": "talk",
            "text": "Nobody knows!",
        },
    ],
}


world_changing_npc = {
    "position": {"x": 418, "y": 90},
    "collision_size": {"width": 24, "height": 16},
    "sprite_sheet": "/game_data/player_8.bmp",
    "sprite_offset": {"x": -8, "y": -26},
    "sprite_sheet_tile_size": {"width": 16, "height": 32},
    "default_animation": "idle",
    "default_flip_x": True,
    "default_flip_y": False,
    "animations": [
        {
            "name": "idle",
            "fps": 0.45,
            "frames": [0, 1],
        },
        {
            "name": "happy_jump",
            "fps": 0.25,
            "frames": [3, 5, 5, 7],
            "loop_animation": False,
        },
    ],
    "actions": [
        {
            "action_type": "talk",
            "text": "I found this magic hat and now I control the landscape",
        },
        {"action_type": "wait", "time": 1},
        {"action_type": "flip_sprite_x", "value": False},
        {"action_type": "wait", "time": 1},
        {
            "action_type": "talk",
            "text": "ABRA!- CADABRA!",
        },
        {
            "action_type": "talk",
            "text": "*Edits world_map.csv with his favorite text editor*",
        },
        {"action_type": "wait", "time": 1},
        {
            "action_type": "camera_shake",
            "time": 0.5,
            "amount": 10,
            "decrease_factor": 1,
        },
        {
            "action_type": "change_world_tile",
            "tile_x": 28,
            "tile_y": 6,
            "to_tile_type": 52,
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "change_world_tile",
            "tile_x": 28,
            "tile_y": 5,
            "to_tile_type": 128,
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "change_world_tile",
            "tile_x": 27,
            "tile_y": 5,
            "to_tile_type": 112,
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "change_world_tile",
            "tile_x": 28,
            "tile_y": 4,
            "to_tile_type": 52,
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "camera_shake",
            "time": 0.5,
            "amount": 10,
            "decrease_factor": 1,
        },
        {"action_type": "wait", "time": 1},
        {"action_type": "flip_sprite_x", "value": True},
        {"action_type": "wait", "time": 1},
        {
            "action_type": "talk",
            "text": "See, magic runs through my veins",
        },
        {"action_type": "wait", "time": 1},
        {
            "action_type": "camera_shake",
            "time": 0.5,
            "amount": 10,
            "decrease_factor": 1,
        },
        {"action_type": "flip_sprite_x", "value": False},
        {"action_type": "wait", "time": 1},
        {
            "action_type": "talk",
            "text": "O...oh...",
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "change_world_tile",
            "tile_x": 30,
            "tile_y": 8,
            "to_tile_type": 18,
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "change_world_tile",
            "tile_x": 30,
            "tile_y": 7,
            "to_tile_type": 18,
        },
        {"action_type": "wait", "time": 0.5},
        {
            "action_type": "change_world_tile",
            "tile_x": 30,
            "tile_y": 6,
            "to_tile_type": 102,
        },
        # Open the path behind the player
        {
            "action_type": "change_world_tile",
            "tile_x": 20,
            "tile_y": 9,
            "to_tile_type": 18,
        },
        {
            "action_type": "change_world_tile",
            "tile_x": 21,
            "tile_y": 9,
            "to_tile_type": 18,
        },
        {
            "action_type": "change_world_tile",
            "tile_x": 19,
            "tile_y": 9,
            "to_tile_type": 105,
        },
        {
            "action_type": "change_world_tile",
            "tile_x": 22,
            "tile_y": 9,
            "to_tile_type": 103,
        },
        {
            "action_type": "change_world_tile",
            "tile_x": 19,
            "tile_y": 8,
            "to_tile_type": 70,
        },
        {
            "action_type": "change_world_tile",
            "tile_x": 22,
            "tile_y": 8,
            "to_tile_type": 70,
        },
        {"action_type": "wait", "time": 1},
        {"action_type": "flip_sprite_x", "value": True},
        {
            "action_type": "talk",
            "text": "Well now I can get into my house again",
        },
    ],
}


no_more_game_npc = {
    "position": {"x": 300, "y": 230},
    "collision_size": {"width": 20, "height": 16},
    "sprite_sheet": "/game_data/big_npc_0.bmp",
    "sprite_offset": {"x": -16, "y": -26},
    "sprite_sheet_tile_size": {"width": 32, "height": 36},
    "default_animation": "idle",
    "default_flip_x": False,
    "default_flip_y": False,
    "animations": [
        {
            "name": "idle",
            "fps": 0.45,
            "frames": [1, 2],
        }
    ],
    "actions": [
        {
            "action_type": "talk",
            "text": "This is it, there is no more game.",
        },
        {
            "action_type": "talk",
            "text": "Thanks for playing",
        },
        {
            "action_type": "talk",
            "text": "Made by:\nJens JWolf Larsen\nhttps://github.com/MrJavaWolf",
        },
    ],
}


interactable_npcs = [
    first_introduction_npc,
    change_character_npc,
    world_changing_npc,
    no_more_game_npc,
    hidden_treasure_1_npc,
]
