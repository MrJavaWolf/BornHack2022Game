import displayio
from adafruit_display_text import label
import terminalio
import time
import json
from collections import OrderedDict

SHOW_FRAME_COUNT = True
SHOW_FRAMES_PER_SECOND = True
FRAMES_PER_SECOND_UPDATE_SPEED = 0.1


class FrameCounter:
    """A frame counter to calculate Frames Per Second and total number of frames"""

    total_frames: int = 0
    """The total number of frames rendered"""

    frames_per_second: float = 0
    """Number of frames rendered a second"""

    frames_per_second_counter: float = 0
    """Used to calculate the FPS"""

    frames_per_second_time = 0
    """Used to calculate the FPS"""

    def __init__(self):
        self.sprite = displayio.Group(scale=1, x=1, y=3)

        # Total frames
        self.total_frames_label = label.Label(
            terminalio.FONT, text=str(self.total_frames), color=0xFF0000
        )
        self.sprite.append(self.total_frames_label)

        # FPS
        self.frames_per_second_time = time.monotonic()
        self.frames_per_second_label = label.Label(
            terminalio.FONT, y=10, text=str(int(self.frames_per_second)), color=0xFF0000
        )
        self.sprite.append(self.frames_per_second_label)

    def loop(self):
        # Total frames
        self.total_frames += 1
        self.total_frames_label.text = str(self.total_frames)

        # Frames per second
        self.frames_per_second_counter += 1
        current_time = time.monotonic()
        if (
            current_time - self.frames_per_second_time
        ) > FRAMES_PER_SECOND_UPDATE_SPEED:
            self.frames_per_second = self.frames_per_second_counter / (
                current_time - self.frames_per_second_time
            )
            self.frames_per_second_label.text = str(int(self.frames_per_second))
            self.frames_per_second_counter = 0
            self.frames_per_second_time = current_time

    def print_state(self):
        print(
            json.dumps(
                OrderedDict(
                    {
                        "total_frames": self.total_frames,
                        "frames_per_second": self.frames_per_second,
                    }
                )
            )
        )
