# BornHack2022Game

Game made for the [BornHack 2022 Game On Badge](https://github.com/bornhack/badge2022).

## Requirements

- A `BornHack 2022 Game On Badge` 
- The badge running [CircetPython](https://circuitpython.org/).
- An analog stick connected to your badge using pins: `A2` and `A3` 
    - Or simular that works with [AnalogIn](https://learn.adafruit.com/circuitpython-essentials/circuitpython-analog-in)
    - The pins is set in `gamepad.py`

## Installation

*Remember to backup your current badge*

1. Copy the files from the `src/` onto your `BornHack 2022 Game On Badge`
2. Reboot the badge

## Todo

- Proper welcome into the game. Tell the player:
  - How the controls work
  - They can edit their character by editing the code
- Enemy to fight back
- Enemys to be set in a xxx_data.py file and not hardcoded
- Dedicated NPC/PlayerRenderer, there is alot of dublicate code between Player
- A prober "Game"
- More dialog NPC actions
