import gameworld
import player
import gamepad
import gametime
import npcmanager
import imagemanager
import uispeechbox
import framecounter

class GameState:
    """Keeps references to relevants parts of the game state"""
    player: player.Player
    npc_manager: npcmanager.NpcManager
    game_time: gametime.GameTime
    gamepad: gamepad.Gamepad
    game_world: gameworld.GameWorld
    image_manager: imagemanager.ImageManager
    ui_speech_box:uispeechbox.UISpeechBox
    frame_counter: framecounter.FrameCounter


