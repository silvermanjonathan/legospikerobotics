"""A stand-in for the SPIKE App 3 hub module, used only by runcheck.py.

It lets a page's program be run on a computer so the build can see which moves the
program asks for, in which order. It is not a simulator: no distance, time, turn, or
reading on any page comes from it. Those are computed in wheel.py or measured on the
reference robot and logged in runs.csv.
"""
import motor_pair


class _Port:
    A, B, C, D, E, F = range(6)


class _Done:
    """What light_matrix.write and sound.beep give back: it can be awaited or not."""
    def __await__(self):
        return iter(())


class _LightMatrix:
    def write(self, text):
        assert isinstance(text, str), "light_matrix.write needs text, so use str() on a number"
        motor_pair.CALLS.append({"call": "show", "text": text})
        return _Done()


class _Sound:
    def beep(self, freq=440, duration=500, volume=100):
        assert 100 <= freq <= 10000 and 0 <= volume <= 100 and duration > 0
        motor_pair.CALLS.append({"call": "beep", "freq": freq, "duration": duration})
        return _Done()


class _MotionSensor:
    """Yaw, in tenths of a degree. Each reading after a reset is 100 more than the
    last, so a turn-until test passes after a few readings. A test input only."""
    def __init__(self):
        self._yaw = 0

    def reset_yaw(self, angle):
        self._yaw = angle
        motor_pair.CALLS.append({"call": "reset"})

    def tilt_angles(self):
        self._yaw -= 100          # one direction reads as a minus number
        return (self._yaw, 0, 0)


port = _Port()
light_matrix = _LightMatrix()
sound = _Sound()
motion_sensor = _MotionSensor()
