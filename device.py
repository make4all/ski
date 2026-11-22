# Talks to the StickS3 and the Joystick Hat.
# Everything that only works on the real device lives here.

import M5
from M5 import BtnA, BtnB, Power
from hardware import I2C, Pin
from hat import JoystickHat

import config
from signals import to_amount


def start():
    M5.begin()
    # The hat connector's 5V power is off by default on the StickS3.
    Power.setExtOutput(True)


class Controller:
    """The joystick hat plus the two StickS3 buttons."""

    def __init__(self):
        self.i2c = I2C(0, scl=Pin(config.JOYSTICK_SCL_PIN), sda=Pin(config.JOYSTICK_SDA_PIN), freq=100000)
        self.joystick = None

    def read(self):
        """
        Returns (x, y, joystick_click, button_a, button_b, joystick_ok).
        x and y go from -1.0 to 1.0, right and up positive.
        If the joystick can't be read, it reports centred and joystick_ok=False.
        """
        M5.update()
        button_a = BtnA.isPressed()
        button_b = BtnB.isPressed()

        try:
            if self.joystick is None:
                self.joystick = JoystickHat(self.i2c, config.JOYSTICK_I2C_ADDRESS)
            raw_x = self.joystick.get_x()
            raw_y = self.joystick.get_y()
            click = self.joystick.get_button_status()
        except Exception:
            self.joystick = None  # try to reconnect next time
            return 0.0, 0.0, False, button_a, button_b, False

        x = to_amount(raw_x, config.JOYSTICK_MAX_READING, config.JOYSTICK_DEADZONE)
        y = to_amount(raw_y, config.JOYSTICK_MAX_READING, config.JOYSTICK_DEADZONE)
        if config.JOYSTICK_FLIP_X:
            x = -x
        if config.JOYSTICK_FLIP_Y:
            y = -y
        return x, y, click, button_a, button_b, True


def set_motor(name, strength):
    """
    Placeholder for the real motors: set motor `name` to `strength` (0-100).
    For now the screen shows what each motor would be doing.
    When motors arrive, drive them from here (e.g. a PWM pin per motor).
    """
    pass
