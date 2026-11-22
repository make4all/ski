# Run on a laptop:  python3 -m unittest discover tests
import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config
import signals

MOTORS = list(config.MOTORS)


def run(x=0.0, y=0.0, click=False, a=False, b=False, connected=True):
    inputs = signals.make_inputs(x, y, click, a, b, connected)
    return signals.decide(config.SIGNALS, MOTORS, config.STRENGTHS, inputs)


class TestDefaultSettings(unittest.TestCase):
    def test_settings_have_no_typos(self):
        self.assertEqual(signals.check_settings(config.SIGNALS, MOTORS, config.STRENGTHS), [])

    def test_idle_keeps_pace(self):
        strengths, names = run()
        self.assertEqual(names, ["KEEP PACE"])
        self.assertEqual(strengths["left_arm"], config.STRENGTHS["medium"])
        self.assertEqual(sum(strengths.values()), config.STRENGTHS["medium"])

    def test_connection_lost_is_emergency(self):
        strengths, names = run(connected=False)
        self.assertEqual(names, ["EMERGENCY"])
        self.assertTrue(all(s == 100 for s in strengths.values()))

    def test_push_up_is_emergency(self):
        strengths, names = run(y=0.9)
        self.assertEqual(names, ["EMERGENCY"])

    def test_emergency_beats_everything(self):
        strengths, names = run(y=1.0, a=True, click=True)
        self.assertEqual(names, ["EMERGENCY"])

    def test_stop(self):
        strengths, names = run(a=True)
        self.assertEqual(strengths["right_arm"], 100)
        self.assertIn("STOP", names)

    def test_slow_down_and_speed_up(self):
        self.assertEqual(run(y=-0.8)[0]["left_arm"], config.STRENGTHS["strong"])
        self.assertEqual(run(click=True)[0]["left_arm"], config.STRENGTHS["weak"])

    def test_turns_scale_with_distance(self):
        self.assertEqual(run(x=-0.4)[0]["chest_left"], config.STRENGTHS["weak"])
        self.assertEqual(run(x=-0.9)[0]["chest_left"], config.STRENGTHS["strong"])
        self.assertEqual(run(x=0.9)[0]["chest_right"], config.STRENGTHS["strong"])
        self.assertEqual(run(x=0.1)[0]["chest_right"], 0)


class TestCustomSettings(unittest.TestCase):
    def test_order_decides_who_wins(self):
        rules = [
            {"name": "A", "when": "always", "buzz": ["m"], "strength": "weak"},
            {"name": "B", "when": "always", "buzz": ["m"], "strength": "strong"},
        ]
        strengths, names = signals.decide(rules, ["m"], config.STRENGTHS, signals.make_inputs(0, 0, False, False, False, True))
        self.assertEqual((strengths["m"], names), (config.STRENGTHS["weak"], ["A"]))

    def test_typos_are_reported(self):
        rules = [
            {"name": "X", "when": "sideways", "buzz": ["nose"], "strength": "loud"},
            {"name": "Y", "when": "up"},
        ]
        problems = signals.check_settings(rules, MOTORS, config.STRENGTHS)
        self.assertEqual(len(problems), 4)

    def test_deadzone(self):
        self.assertEqual(signals.to_amount(5, 127, 0.1), 0.0)
        self.assertEqual(signals.to_amount(-200, 127, 0.1), -1.0)


if __name__ == "__main__":
    unittest.main()
