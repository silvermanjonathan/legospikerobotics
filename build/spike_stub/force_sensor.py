"""Stand-in for the SPIKE App 3 force_sensor module, used only by runcheck.py.

pressed(port) gives False twice and then True, which is a robot that reaches the wall.
"""
_i = [0]


def pressed(port):
    assert port in range(6), "not a port"
    _i[0] += 1
    return _i[0] > 2
