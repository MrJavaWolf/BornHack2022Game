import time
import json
from collections import OrderedDict


class GameTime:
    """Keeps track of the game time"""

    total_time: float = 0
    """Total time in seconds since the start of the game"""

    delta_time: float = 0
    """The interval in seconds from the last frame to the current one"""

    last_frame_time: float = 0
    """The interval in seconds from the last frame to the current one"""

    def __init__(self):
        self.last_frame_time = time.monotonic()

    def loop(self):
        current_time = time.monotonic()
        self.delta_time = current_time - self.last_frame_time
        self.total_time += self.delta_time
        self.last_frame_time = current_time

    def print_state(self):
        print(
            json.dumps(
                OrderedDict(
                    {
                        "total_time": self.total_time,
                        "delta_time": self.delta_time,
                    }
                )
            )
        )
