"""Stand-in for the SPIKE App 3 motor_pair module, used only by runcheck.py.

Signatures follow the SPIKE App 3 API: pair(pair, left_motor, right_motor) and
move_for_degrees(pair, degrees, steering, *, velocity=360, stop=motor.BRAKE,
acceleration=1000, deceleration=1000), which is awaitable. Each call is recorded so
runcheck.py can compare the program with what its page says the program does.
"""
import json
import motor

PAIR_1, PAIR_2, PAIR_3 = range(3)
CALLS = []
_PAIRS = {}
LARGE_MOTOR_MAX = 1050   # degrees of motor turn each second


def pair(pair, left_motor, right_motor):
    assert pair in (PAIR_1, PAIR_2, PAIR_3), "not a pair slot"
    assert left_motor in range(6) and right_motor in range(6), "not a port"
    assert left_motor != right_motor, "the two drive motors share a port"
    _PAIRS[pair] = (left_motor, right_motor)
    CALLS.append({"call": "pair", "left": "ABCDEF"[left_motor], "right": "ABCDEF"[right_motor]})


async def move_for_degrees(pair, degrees, steering, *, velocity=360, stop=motor.BRAKE,
                           acceleration=1000, deceleration=1000):
    assert pair in _PAIRS, "move_for_degrees before motor_pair.pair"
    assert isinstance(degrees, int), "degrees is a whole number"
    assert -100 <= steering <= 100, "steering runs from -100 to 100"
    assert -LARGE_MOTOR_MAX <= velocity <= LARGE_MOTOR_MAX, "velocity out of range"
    CALLS.append({"call": "move_for_degrees", "degrees": degrees, "steering": steering,
                  "velocity": velocity})


def dump():
    print(json.dumps(CALLS))
