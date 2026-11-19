"""Stand-in for the SPIKE App 3 distance_sensor module, used only by runcheck.py.

distance(port) gives the next reading from a short script, then repeats the last one.
As in the SPIKE App, a reading is in tenths of a cm, and -1 means nothing was measured.
The script starts with -1 so the guard shows that a program does not stop on it. No
distance on any page comes from here.
"""
import json
import os

_SCRIPT = json.loads(os.environ.get("SPIKE_DISTANCES", "[-1, 600, 300, 100]"))
_i = [0]


def distance(port):
    assert port in range(6), "not a port"
    k = _i[0]
    _i[0] = k + 1
    return _SCRIPT[min(k, len(_SCRIPT) - 1)]
