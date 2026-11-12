"""Wheel arithmetic for the Advanced Driving Base. Every computed number on a page
comes from here, and runcheck.py recomputes each one on every build.

The wheel's circumference is the figure LEGO's own Python programs for this robot
give in a comment: 27.63 cm. One full turn of a drive motor is 360 degrees of motor
turn and is one full turn of its wheel.
"""

WHEEL_CM = 27.63          # cm moved by one full turn of the wheel (LEGO's figure)
FULL_TURN = 360           # degrees of motor turn in one full turn of the wheel


def turns(motor_degrees):
    """Full turns of the wheel for a number of degrees of motor turn."""
    return motor_degrees / FULL_TURN


def cm(motor_degrees):
    """Centimetres the robot moves, straight, for a number of degrees of motor turn."""
    return turns(motor_degrees) * WHEEL_CM


def whole_cm(motor_degrees):
    """The same distance in whole centimetres, as the pages print it."""
    return round(abs(cm(motor_degrees)))


def nearest5(x):
    """x to the nearest 5, the answer shape the prediction questions ask for."""
    return int(5 * round(abs(x) / 5.0))


def classroom_cm(motor_degrees):
    """The distance worked the way the page works it: whole turns times 28 cm.

    Students have whole centimetres only, so the page says one full turn is about
    28 cm and adds. The answer to the nearest 5 must match the exact arithmetic, or
    the page would teach a wrong number; asserted here.
    """
    by_hand = abs(turns(motor_degrees)) * round(WHEEL_CM)
    assert nearest5(by_hand) == nearest5(cm(motor_degrees)), (
        "whole-centimetre working disagrees with the exact figure for %s" % motor_degrees)
    return by_hand
