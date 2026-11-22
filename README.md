# Ski Guide Controller

A guide holds an M5Stack **StickS3** with a **Joystick Hat**. Moving the joystick
tells vibration motors (buzzers) worn by the skier what to do.

The motors aren't wired up yet, so the StickS3 screen shows the wearer from
behind, with each motor drawn as a circle. The circles go from grey (off)
to bright red (full strength).

## Changing what the signals mean

**Only edit [`config.py`](config.py).** It has four sections:

1. **Strengths**: names for vibration levels (`weak`, `medium`, `strong`) and their numbers.
2. **Motors**: one line per motor and where it appears on screen. Add or delete lines to change the count.
3. **Signals**: "when the joystick does X, buzz these motors at this strength". Signals higher in the list win.
4. **Testing**: which button pretends the connection dropped.

If you make a typo (for example a motor name that doesn't exist), the StickS3
shows a "Fix config.py" message with what's wrong.

## Default behaviour

| Controller action             | Signal       | Motors                      |
|-------------------------------|--------------|-----------------------------|
| Connection lost / hold **B**  | EMERGENCY    | all, strong                 |
| Push joystick all the way up  | EMERGENCY    | all, strong                 |
| Press front button **A**      | STOP         | right arm, strong           |
| Pull joystick down            | SLOW DOWN    | left arm, strong            |
| Click joystick in             | SPEED UP     | left arm, weak              |
| Nothing (always)              | KEEP PACE    | left arm, medium            |
| Push left (a little / a lot)  | LEFT / SHARP LEFT  | left chest, weak / strong   |
| Push right (a little / a lot) | RIGHT / SHARP RIGHT | right chest, weak / strong |

There's no wireless link yet. For now, "connection lost" means the joystick
hat can't be read (e.g. it was unplugged) or the fake-disconnect button is held.

## Files

| File | What it does |
|------|--------------|
| `config.py`  | All settings. Edit this one. |
| `main.py`    | The main loop: read joystick, decide, show. |
| `signals.py` | Turns joystick input into motor strengths. Plain Python, no hardware. |
| `device.py`  | Reads the joystick and buttons. Real motor output goes in `set_motor()`. |
| `screen.py`  | Draws the body and motors. |
| `tests/`     | Laptop tests for `signals.py` and the default settings. |

## Putting it on the StickS3

The StickS3 needs **UIFlow2** firmware (tested on v2.4.8; flash it with M5Burner if it doesn't have it).
Plug it in over USB, then copy the files over with `mpremote`:

```bash
uvx mpremote resume cp config.py main.py signals.py device.py screen.py :/flash/
```

```bash
uvx mpremote reset
```

`resume` matters: without it, mpremote restarts UIFlow's startup app first and the copy fails.
After the reset the StickS3 starts the controller on its own.

## Running the tests on a laptop

```bash
python3 -m unittest discover tests
```
