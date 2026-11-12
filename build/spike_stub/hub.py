"""A stand-in for the SPIKE App 3 hub module, used only by runcheck.py.

It lets a page's program be run on a computer so the build can see which moves the
program asks for, in which order. It is not a simulator: no distance, time, or turn
on any page comes from it. Those are computed in wheel.py or measured on the
reference robot and logged in runs.csv.
"""


class _Port:
    A, B, C, D, E, F = range(6)


port = _Port()
