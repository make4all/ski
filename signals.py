# Decides how strongly each motor should vibrate.
#
# Everything here is plain Python with no hardware, so it can be tested
# on a laptop. The flow is:
#
#   raw joystick + buttons  ->  make_inputs()  ->  "how much" each trigger is active (0.0 - 1.0)
#   inputs + SIGNALS        ->  decide()       ->  strength for every motor, plus active signal names

DEFAULT_HOW_FAR = (0.5, 1.0)

TRIGGERS = (
    "connection_lost",
    "up", "down", "left", "right",
    "joystick_click",
    "button_a",
    "button_b",
    "always",
)


def to_amount(reading, max_reading, deadzone):
    """Turn a raw joystick reading into a number from -1.0 to 1.0, ignoring tiny wobbles."""
    amount = max(-1.0, min(1.0, reading / max_reading))
    if abs(amount) < deadzone:
        return 0.0
    return amount


def make_inputs(x, y, joystick_click, button_a, button_b, connected):
    """
    Describe the controller state as {trigger: how much, from 0.0 to 1.0}.
    x and y go from -1.0 to 1.0 (right and up are positive).
    """
    return {
        "connection_lost": 0.0 if connected else 1.0,
        "up": max(0.0, y),
        "down": max(0.0, -y),
        "right": max(0.0, x),
        "left": max(0.0, -x),
        "joystick_click": 1.0 if joystick_click else 0.0,
        "button_a": 1.0 if button_a else 0.0,
        "button_b": 1.0 if button_b else 0.0,
        "always": 1.0,
    }


def is_active(signal, inputs):
    low, high = signal.get("how_far", DEFAULT_HOW_FAR)
    return low <= inputs[signal["when"]] <= high


def motors_for(signal, all_motor_names):
    if signal["buzz"] == "all":
        return list(all_motor_names)
    return signal["buzz"]


def decide(signals, motor_names, strengths, inputs):
    """
    Work out the strength (0-100) for every motor.

    Signals are checked from top to bottom. The first active signal that
    asks for a motor gets it; later signals can't change that motor.

    Returns (motor_strengths, active_signal_names).
    """
    motor_strengths = {name: 0 for name in motor_names}
    already_set = set()
    active_names = []

    for signal in signals:
        if not is_active(signal, inputs):
            continue

        free_motors = [m for m in motors_for(signal, motor_names) if m not in already_set]
        if not free_motors:
            continue

        for motor in free_motors:
            motor_strengths[motor] = strengths[signal["strength"]]
            already_set.add(motor)

        if signal["name"] not in active_names:
            active_names.append(signal["name"])

    return motor_strengths, active_names


def check_settings(signals, motor_names, strengths):
    """
    Look for typos in config.py. Returns a list of plain-English problems
    (empty if everything looks fine).
    """
    problems = []
    for number, signal in enumerate(signals, start=1):
        where = "Signal #{} ({})".format(number, signal.get("name", "no name"))

        missing = [key for key in ("name", "when", "buzz", "strength") if key not in signal]
        if missing:
            problems.append('{} is missing "{}"'.format(where, missing[0]))
            continue

        if signal["when"] not in TRIGGERS:
            problems.append('{}: unknown "when" value "{}"'.format(where, signal["when"]))

        if signal["strength"] not in strengths:
            problems.append('{}: unknown strength "{}"'.format(where, signal["strength"]))

        if signal["buzz"] != "all":
            for motor in signal["buzz"]:
                if motor not in motor_names:
                    problems.append('{}: unknown motor "{}"'.format(where, motor))

        low, high = signal.get("how_far", DEFAULT_HOW_FAR)
        if not 0.0 <= low <= high <= 1.0:
            problems.append('{}: "how_far" must be two numbers from 0.0 to 1.0, smallest first'.format(where))

    return problems
