# Ski guide controller: read the joystick, decide which motors buzz, show it.
# To change behaviour, edit config.py - not this file.

import time

import config
import device
import screen
import signals


def is_fake_disconnect_held(button_a, button_b):
    held = {"button_a": button_a, "button_b": button_b}
    return held.get(config.FAKE_DISCONNECT_BUTTON, False)


def run():
    device.start()

    motor_names = list(config.MOTORS)
    problems = signals.check_settings(config.SIGNALS, motor_names, config.STRENGTHS)
    if problems:
        screen.show_problems(problems)
        return

    controller = device.Controller()
    display = screen.Screen()
    pause_ms = 1000 // config.UPDATES_PER_SECOND

    while True:
        x, y, click, button_a, button_b, joystick_ok = controller.read()
        connected = joystick_ok and not is_fake_disconnect_held(button_a, button_b)

        inputs = signals.make_inputs(x, y, click, button_a, button_b, connected)
        motor_strengths, active_names = signals.decide(config.SIGNALS, motor_names, config.STRENGTHS, inputs)

        for name, strength in motor_strengths.items():
            device.set_motor(name, strength)
        display.update(motor_strengths, active_names, connected)

        time.sleep_ms(pause_ms)


run()
