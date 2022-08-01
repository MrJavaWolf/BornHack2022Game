interactable_npcs = [
    {
        "position": {"x": 60, "y": 30},
        "collision_size": {"width": 16, "height": 16},
        "sprite_sheet": "/game_data/big_npc_0.bmp",
        "sprite_offset": {"x": -16, "y": -26},
        "sprite_sheet_tile_size": {"width": 32, "height": 36},
        "default_animation": "idle",
        "animations": [
            {
                "name": "idle",
                "fps": 0.45,
                "frames": [1, 2],
            },
            #{"name": "run", "fps": 0.15, "frames": [4, 7]},
        ],
        "actions": [
            {
                "action_type": "talk",
                "text": "Hello greate adventur-y",
            },
            {
                "action_type": "talk",
                "text": "I am happy to see you",
            },
            {
                "action_type": "talk",
                "text": "I need you to write-y me some dialog",
            },
            {
                "action_type": "camera_shake",
                "time": 1.5,
                "amount": 10,
                "decrease_factor": 1,
            },
            {
                "action_type": "change_world_tile",
                "tile_x": 1,
                "tile_y": 1,
                "to_tile_type": 1,
            },
            {"action_type": "wait", "time": 0.5},
            {
                "action_type": "flip_sprite_x",
                "value": True,
            },
            {
                "action_type": "talk",
                "text": "Ohh-y~ I think the world just changed",
            },
            {
                "action_type": "flip_sprite_x",
                "value": False,
            },
        ],
    }
]
