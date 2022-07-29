import displayio
from adafruit_display_text import label
from adafruit_display_text import wrap_text_to_pixels
import terminalio
from adafruit_display_shapes.roundrect import RoundRect

class UISpeechBox:

    def __init__(self):
        # UI speech box
        screen_width = 128
        screen_height = 160
        border_size = 4
        speech_box_height = 56
        roundiness = 2
        line_height = 12
        self.sprite_ui = displayio.Group()
        self.speech_box_ui = displayio.Group()
        self.max_line_width = screen_width - border_size * 4
        roundrect = RoundRect(
            border_size,
            screen_height - border_size - speech_box_height,
            screen_width - border_size,
            speech_box_height,
            roundiness,
            fill=0xDDDDDD,
            outline=0x111111,
            stroke=2,
        )
        self.speech_box_ui.append(roundrect)
        label_group = displayio.Group(
            scale=1,
            x=border_size + 4,
            y=screen_height - speech_box_height + border_size,
        )
        self.text_line_1 = label.Label(terminalio.FONT, text="", color=0x111111)
        self.text_line_2 = label.Label(
            terminalio.FONT, text="", color=0x111111, y=line_height * 1
        )
        self.text_line_3 = label.Label(
            terminalio.FONT, text="", color=0x111111, y=line_height * 2
        )
        self.text_line_4 = label.Label(
            terminalio.FONT, text="", color=0x111111, y=line_height * 3
        )
        label_group.append(self.text_line_1)
        label_group.append(self.text_line_2)
        label_group.append(self.text_line_3)
        label_group.append(self.text_line_4)
        self.speech_box_ui.append(label_group)

    def show(self, text:str):
        texts = wrap_text_to_pixels(text, self.max_line_width, terminalio.FONT)
        if len(texts) > 0:
            self.text_line_1.text = texts[0]
        if len(texts) > 1:
            self.text_line_2.text = texts[1]
        if len(texts) > 2:
            self.text_line_3.text = texts[2]
        if len(texts) > 3:
            self.text_line_4.text = texts[3]
        self.sprite_ui.append(self.speech_box_ui)

    def hide(self):
        self.text_line_1.text = ""
        self.text_line_2.text = ""
        self.text_line_3.text = ""
        self.text_line_4.text = ""
        self.sprite_ui.remove(self.speech_box_ui)