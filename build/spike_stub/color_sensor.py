"""Stand-in for the SPIKE App 3 color_sensor module, used only by runcheck.py.

reflection(port) returns the next reading from a script that runcheck.py supplies in
the SPIKE_READINGS environment variable, then repeats the last one. The script is a
list (one sensor) or a table of lists by port letter (two sensors). It is how the
guard tries each branch of a program. No reading on any page comes from here.
"""
import json
import os

_SCRIPT = json.loads(os.environ.get("SPIKE_READINGS", "[50]"))
_i = {}


def reflection(port):
    assert port in range(6), "not a port"
    letter = "ABCDEF"[port]
    seq = _SCRIPT[letter] if isinstance(_SCRIPT, dict) else _SCRIPT
    k = _i.get(letter, 0)
    _i[letter] = k + 1
    v = seq[min(k, len(seq) - 1)]
    assert 0 <= v <= 100
    return v
