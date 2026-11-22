# Draws the wearer and their motors on the StickS3 screen.

from M5 import Lcd

import config

WIDTH = 135
HEIGHT = 240


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
    Lcd.drawRoundRect(28, 64, 79, 110, 10, c)       # torso
    Lcd.drawLine(28, 70, 12, 135, c)                # left arm
    Lcd.drawLine(106, 70, 122, 135, c)              # right arm


def draw_motor(name, strength):
    spot = config.MOTORS[name]
    Lcd.fillCircle(spot["x"], spot["y"], config.MOTOR_RADIUS, motor_color(strength))
    Lcd.drawCircle(spot["x"], spot["y"], config.MOTOR_RADIUS, config.BODY_OUTLINE_COLOR)


def draw_text_line(text, y, color=None):
    Lcd.fillRect(0, y, WIDTH, 16, config.BACKGROUND_COLOR)
    Lcd.setTextColor(color if color is not None else config.TEXT_COLOR, config.BACKGROUND_COLOR)
    Lcd.drawString(text, 4, y)


def draw_connection(connected):
    if connected:
        draw_text_line("LINK OK", 4, 0x00C000)
    else:
        draw_text_line("NO LINK", 4, 0xFF0000)


def draw_signal_names(names):
    """List the active signals under the body (up to 3 lines)."""
    for row in range(3):
        text = names[row] if row < len(names) else ""
        draw_text_line(text, 186 + row * 17)


def show_problems(problems):
    """Show config.py mistakes so they can be fixed without a computer log."""
    Lcd.fillScreen(config.BACKGROUND_COLOR)
    Lcd.setTextColor(0xFF4040, config.BACKGROUND_COLOR)
    Lcd.drawString("Fix config.py:", 4, 4)
    Lcd.setTextColor(config.TEXT_COLOR, config.BACKGROUND_COLOR)
    y = 24
    for problem in problems:
        for start in range(0, len(problem), 20):   # wrap long lines
            Lcd.drawString(problem[start:start + 20], 4, y)
            y += 14
        y += 6


class Screen:
    """Only redraws what changed, so the screen doesn't flicker."""

    def __init__(self):
        Lcd.setRotation(0)
        Lcd.setTextSize(1.5)
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
            draw_signal_names(signal_names)
            self.shown_names = signal_names

        if connected != self.shown_connected:
            draw_connection(connected)
            self.shown_connected = connected
