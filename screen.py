# Draws the wearer and their motors on the StickS3 screen.

from M5 import Lcd, Widgets

import config

WIDTH = 135
HEIGHT = 240
FONT = Widgets.FONTS.DejaVu18
LINE_HEIGHT = 22

# Screen areas for text: (x, y, width, height).
# The whole area is wiped before new text is drawn, so no old text is left behind.
STATUS_AREA = (0, 0, WIDTH, 28)                # "LINK OK" / "NO LINK" at the top
SIGNAL_AREA = (0, 172, WIDTH, HEIGHT - 172)    # active signal names under the body


def blend(color_a, color_b, fraction):
    """Mix two 0xRRGGBB colours. fraction 0.0 gives color_a, 1.0 gives color_b."""
    result = 0
    for shift in (16, 8, 0):
        a = (color_a >> shift) & 0xFF
        b = (color_b >> shift) & 0xFF
        result |= int(a + (b - a) * fraction) << shift
    return result


def motor_color(strength):
    return blend(config.MOTOR_OFF_COLOR, config.MOTOR_ON_COLOR, strength / 100)


def draw_body():
    """The wearer seen from behind: head, torso and arms."""
    Lcd.fillScreen(config.BACKGROUND_COLOR)
    c = config.BODY_OUTLINE_COLOR
    Lcd.drawCircle(67, 45, 15, c)                   # head
    Lcd.drawRoundRect(28, 64, 79, 106, 10, c)       # torso
    Lcd.drawLine(28, 70, 12, 135, c)                # left arm
    Lcd.drawLine(106, 70, 122, 135, c)              # right arm


def draw_motor(name, strength):
    spot = config.MOTORS[name]
    Lcd.fillCircle(spot["x"], spot["y"], config.MOTOR_RADIUS, motor_color(strength))
    Lcd.drawCircle(spot["x"], spot["y"], config.MOTOR_RADIUS, config.BODY_OUTLINE_COLOR)


def write_lines(lines, area, color):
    """Wipe a screen area, then write lines of text into it."""
    x, y, width, height = area
    Lcd.fillRect(x, y, width, height, config.BACKGROUND_COLOR)
    Lcd.setFont(FONT)
    Lcd.setTextSize(1)
    Lcd.setTextColor(color, config.BACKGROUND_COLOR)
    for row, line in enumerate(lines):
        Lcd.drawString(line, x + 3, y + 2 + row * LINE_HEIGHT)


def show_problems(problems):
    """Show config.py mistakes so they can be fixed without a computer log."""
    Lcd.fillScreen(config.BACKGROUND_COLOR)
    Lcd.setFont(Widgets.FONTS.DejaVu12)
    Lcd.setTextSize(1)
    Lcd.setTextColor(0xFF4040, config.BACKGROUND_COLOR)
    Lcd.drawString("Fix config.py:", 3, 3)
    Lcd.setTextColor(config.TEXT_COLOR, config.BACKGROUND_COLOR)
    y = 24
    for problem in problems:
        for start in range(0, len(problem), 14):   # wrap long lines
            Lcd.drawString(problem[start:start + 14], 3, y)
            y += 16
        y += 6


class Screen:
    """Only redraws what changed, so the screen doesn't flicker."""

    def __init__(self):
        Lcd.setRotation(0)
        draw_body()
        self.shown_strengths = {}
        self.shown_names = None
        self.shown_connected = None

    def update(self, motor_strengths, signal_names, connected):
        for name, strength in motor_strengths.items():
            if self.shown_strengths.get(name) != strength:
                draw_motor(name, strength)
                self.shown_strengths[name] = strength

        if signal_names != self.shown_names:
            write_lines(signal_names[:3], SIGNAL_AREA, config.TEXT_COLOR)
            self.shown_names = signal_names

        if connected != self.shown_connected:
            if connected:
                write_lines(["LINK OK"], STATUS_AREA, 0x00C000)
            else:
                write_lines(["NO LINK"], STATUS_AREA, 0xFF0000)
            self.shown_connected = connected
