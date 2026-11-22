# =====================================================================
#  SKI GUIDE - SETTINGS
#
#  This is the only file you should need to edit.
#  Change the values below, save, copy to the StickS3, and restart it.
#
#  Rules for editing:
#    - Keep the quotes around names, e.g. "left_arm"
#    - Keep the commas at the end of each line inside { } and [ ]
#    - Lines starting with # are notes and are ignored
# =====================================================================


# ---------------------------------------------------------------------
#  1. VIBRATION STRENGTHS
#     Give each strength level a name and a number.
#     0 = off, 100 = as strong as the motor can go.
# ---------------------------------------------------------------------
STRENGTHS = {
    "off": 0,
    "weak": 30,
    "medium": 60,
    "strong": 100,
}


# ---------------------------------------------------------------------
#  2. MOTORS (BUZZERS)
#     One line per motor. Add or remove lines to change how many there are.
#
#     The name on the left is what you use in the SIGNALS section below.
#     x and y say where the motor is drawn on the StickS3 screen.
#     The screen is 135 wide and 240 tall; (0, 0) is the top-left corner.
#     The picture shows the wearer from BEHIND, so their left is on the left.
# ---------------------------------------------------------------------
MOTORS = {
    "chest_left":   {"x": 40,  "y": 95},
    "chest_middle": {"x": 67,  "y": 95},
    "chest_right":  {"x": 94,  "y": 95},
    "left_arm":     {"x": 14,  "y": 150},
    "right_arm":    {"x": 120, "y": 150},
}


# ---------------------------------------------------------------------
#  3. SIGNALS
#     Each signal means: WHEN something happens, BUZZ some motors at a STRENGTH.
#
#     "name"      Text shown on the screen while the signal is active.
#
#     "when"      What triggers it. One of:
#                   "connection_lost"  the controller lost contact
#                   "up", "down", "left", "right"   joystick pushed that way
#                   "joystick_click"   joystick pressed in
#                   "button_a"         big button on the front of the StickS3
#                   "always"           all the time (useful as a default)
#
#     "how_far"   (optional, joystick directions only)
#                 How far the joystick must be pushed, from 0.0 (centre)
#                 to 1.0 (all the way). (0.3, 0.7) means "between 30% and 70%".
#                 If you leave it out, it means (0.5, 1.0): "at least halfway".
#
#     "buzz"      A list of motor names from section 2, or "all".
#
#     "strength"  A strength name from section 1.
#
#     ORDER MATTERS: if two signals want the same motor at the same time,
#     the one HIGHER UP in this list wins. Put the most important ones first.
# ---------------------------------------------------------------------
SIGNALS = [
    # --- Emergency: every motor on, full strength ---
    {"name": "EMERGENCY", "when": "connection_lost",                     "buzz": "all", "strength": "strong"},
    {"name": "EMERGENCY", "when": "up",              "how_far": (0.8, 1.0), "buzz": "all", "strength": "strong"},

    # --- Normal stop: right arm ---
    {"name": "STOP",      "when": "button_a",                            "buzz": ["right_arm"], "strength": "strong"},

    # --- Speed: left arm ---
    {"name": "SLOW DOWN", "when": "down",                                "buzz": ["left_arm"], "strength": "strong"},
    {"name": "SPEED UP",  "when": "joystick_click",                      "buzz": ["left_arm"], "strength": "weak"},
    {"name": "KEEP PACE", "when": "always",                              "buzz": ["left_arm"], "strength": "medium"},

    # --- Direction: across the chest. Push further for a sharper turn. ---
    {"name": "SHARP LEFT",  "when": "left",  "how_far": (0.7, 1.0), "buzz": ["chest_left"],  "strength": "strong"},
    {"name": "LEFT",        "when": "left",  "how_far": (0.2, 0.7), "buzz": ["chest_left"],  "strength": "weak"},
    {"name": "SHARP RIGHT", "when": "right", "how_far": (0.7, 1.0), "buzz": ["chest_right"], "strength": "strong"},
    {"name": "RIGHT",       "when": "right", "how_far": (0.2, 0.7), "buzz": ["chest_right"], "strength": "weak"},
]


# ---------------------------------------------------------------------
#  4. TESTING WITHOUT A WEARER
#     There is no wireless link yet, so hold this button to pretend the
#     connection dropped. Set to None to turn this off.
#     Unplugging the joystick also counts as a lost connection.
# ---------------------------------------------------------------------
FAKE_DISCONNECT_BUTTON = "button_b"


# =====================================================================
#  HARDWARE SETTINGS
#  You probably don't need to change anything below this line.
# =====================================================================

# Joystick Hat wiring on the StickS3 top connector.
JOYSTICK_I2C_ADDRESS = 0x38
JOYSTICK_SDA_PIN = 8
JOYSTICK_SCL_PIN = 0

# Joystick readings go from about -128 to 127. Movements smaller than
# JOYSTICK_DEADZONE (0.0 - 1.0) are ignored so a resting stick reads as centred.
JOYSTICK_MAX_READING = 127
JOYSTICK_DEADZONE = 0.1

# Set to True if a direction comes out backwards.
JOYSTICK_FLIP_X = False
JOYSTICK_FLIP_Y = False

# Screen colours (0xRRGGBB). A motor's colour fades from MOTOR_OFF_COLOR
# to MOTOR_ON_COLOR as its strength goes from 0 to 100.
BACKGROUND_COLOR = 0x000000
BODY_OUTLINE_COLOR = 0x444444
TEXT_COLOR = 0xFFFFFF
MOTOR_OFF_COLOR = 0x202020
MOTOR_ON_COLOR = 0xFF2000
MOTOR_RADIUS = 11

# How many times per second to check the joystick and update the motors.
UPDATES_PER_SECOND = 30
