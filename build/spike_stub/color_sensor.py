"""Stand-in for the SPIKE App 3 color_sensor module, used only by runcheck.py.

reflection(port) returns the next reading from a script that runcheck.py supplies in
the SPIKE_READINGS environment variable, then repeats the last one. The script is how
the guard tries each branch of a program: a floor that ends in a line, or a floor
with no reading that ever passes the test. No reading on any page comes from here.
"""
import json
import os

_SCRIPT = json.loads(os.environ.get("SPIKE_READINGS", "[50]"))
_i = 0


def reflection(port):
    global _i
    assert port in range(6), "not a port"
    v = _SCRIPT[min(_i, len(_SCRIPT) - 1)]
    _i += 1
    assert 0 <= v <= 100
    return v
