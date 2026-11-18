"""Turns one of the course's Python programs into the same program in Word Blocks.

Only the Python that sessions 1 to 4 use is understood. Anything else raises
Unsupported, and the page then shows the Python alone. Each block remembers the line
of the Python program it came from, so a page whose text says "line 12" still points
at one block.

How each Python line becomes a block. The block words are the SPIKE App's own, read
on 18 November 2026 from the program image on LEGO's lesson page "Training Camp 1:
Driving Around" (set movement motors to, set movement speed to, move ... for ...,
stop moving, repeat, wait) and from the Game Master and Grabbers programs.

  async def main():                         when program starts
  motor_pair.pair(PAIR_1, port.A, port.E)   set movement motors to A+E
  velocity=250                              set movement speed to 24 %, once, at the top
  await motor_pair.move_for_degrees(...)    move [straight: 0] for 720 [degrees]
  motor_pair.move(PAIR_1, 0, ...)           start moving [straight: 0]
  motor_pair.stop(PAIR_1)                   stop moving
  await runloop.until(lambda: a < b)        wait until <a < b>
  for count in range(4):                    repeat 4
  FORWARD = 360                             set FORWARD to 360
  color_sensor.reflection(port.B)           (B) reflected light
  print(...)                                write ... on the light matrix

The speed. Python gives the speed as degrees of motor turn each second. The block
gives it as a percent of the motor's top speed. The top speed of the large motor is
1050 degrees of motor turn each second (the range the SPIKE App's Python help gives
for velocity), so 250 is 250 / 1050 of top speed, which is 24 % to the nearest whole
percent. The two programs are about the same speed, not exactly the same.

These stacks were written from the Python, not built and run in the app.
"""
import re

import blocks as B

LARGE_MOTOR_TOP = 1050     # degrees of motor turn each second


class Unsupported(Exception):
    pass


def percent(velocity):
    return int(round(100.0 * velocity / LARGE_MOTOR_TOP))


def _steer(s):
    s = s.strip()
    if s == "____":
        return B.dd("____")
    n = int(s)
    if n == 0:
        return B.dd("straight: 0")
    return B.dd(("right: %d" % n) if n > 0 else ("left: %d" % -n))


def _value(s, consts):
    s = s.strip()
    if s in consts or re.fullmatch(r"[A-Z][A-Z_]*", s):
        return B.var(s)
    if re.fullmatch(r"-?\d+|____", s):
        return B.num(s)
    raise Unsupported(s)


def _reflect(arg, ports):
    arg = arg.strip()
    p = ports.get(arg) or (arg[5:] if arg.startswith("port.") else None)
    if not p:
        raise Unsupported(arg)
    return ("rep", "sensors", (B.port(p), "reflected light"))


MOVE = re.compile(r"await motor_pair\.move_for_degrees\(motor_pair\.PAIR_1, ([^,]+), ([^,]+), velocity=(\d+)\)$")
START = re.compile(r"motor_pair\.move\(motor_pair\.PAIR_1, ([^,]+), velocity=(\d+)\)$")
PAIR = re.compile(r"motor_pair\.pair\(motor_pair\.PAIR_1, port\.([A-F]), port\.([A-F])\)$")
UNTIL = re.compile(r"await runloop\.until\(lambda: color_sensor\.reflection\((\w+(?:\.\w+)?)\) ([<>]) (\w+)\)$")
FOR = re.compile(r"for count in range\((\d+|____)\):$")
PRINT = re.compile(r"print\(color_sensor\.reflection\((\w+(?:\.\w+)?)\)\)$")
CONST = re.compile(r"([A-Z_]+) = (-?\d+|____)$")
SENSOR = re.compile(r"([A-Z_]+) = port\.([A-F])$")
SKIP = re.compile(r"(from hub import .*|import \w+|runloop\.run\(main\(\)\))$")


def translate(code, context=None):
    """A list of blocks for B.stack, and whether the code was a whole program.

    context is the whole program when code is only a few lines of it, so a name such
    as FORWARD or LINE_SENSOR is known.
    """
    consts, ports = set(), {}
    for src in (context or "", code):
        for ln in src.split("\n"):
            m = CONST.match(ln)
            if m:
                consts.add(m.group(1))
            m = SENSOR.match(ln)
            if m:
                ports[m.group(1)] = m.group(2)
    whole = "async def main():" in code
    lines = code.split("\n")
    speeds = {int(v) for v in re.findall(r"velocity=(\d+)", code)}
    if len(speeds) > 1:
        raise Unsupported("more than one speed")

    top, sets, body = [], [], []
    stack = [(-1, body)]           # (indent, list to add to)
    base = None
    for i, raw in enumerate(lines, 1):
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        ln = i if whole else None
        if indent == 0 and whole:
            if SKIP.match(text):
                continue
            if text == "async def main():":
                top.append(dict(B.hat("events", "when program starts"), line=ln))
                continue
            m = CONST.match(text)
            if m:
                sets.append(dict(B.blk("variables", "set", B.dd(m.group(1)), "to", B.num(m.group(2))),
                                 line=ln))
                continue
            if SENSOR.match(text):
                continue
            raise Unsupported(text)
        if base is None:
            base = indent
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        out = stack[-1][1]
        m = CONST.match(text)
        if m:
            out.append(B.blk("variables", "set", B.dd(m.group(1)), "to", B.num(m.group(2))))
            continue
        if re.match(r"[A-Z_]+ = port\.(?:[A-F]|____)$", text):
            continue               # a sensor's port is chosen inside its block, not named
        m = PAIR.match(text)
        if m:
            top.append(dict(B.blk("movement", "set movement motors to", B.dd(m.group(1) + "+" + m.group(2))),
                            line=ln))
            if speeds:
                top.append(B.blk("movement", "set movement speed to", B.num(percent(speeds.pop())), "%"))
            continue
        m = MOVE.match(text)
        if m:
            out.append(dict(B.blk("movement", "move", _steer(m.group(2)), "for",
                                  _value(m.group(1), consts), B.dd("degrees")), line=ln))
            continue
        m = START.match(text)
        if m:
            out.append(dict(B.blk("movement", "start moving", _steer(m.group(1))), line=ln))
            continue
        if text == "motor_pair.stop(motor_pair.PAIR_1)":
            out.append(dict(B.blk("movement", "stop moving"), line=ln))
            continue
        m = UNTIL.match(text)
        if m:
            test = B.boolean("operators", _reflect(m.group(1), ports), m.group(2),
                             _value(m.group(3), consts))
            out.append(dict(B.blk("control", "wait until", test), line=ln))
            continue
        m = FOR.match(text)
        if m:
            inner = []
            out.append(dict(B.cblock("control", ("repeat", B.num(m.group(1))), inner), line=ln))
            stack.append((indent, inner))
            continue
        m = PRINT.match(text)
        if m:
            out.append(dict(B.blk("light", "write", _reflect(m.group(1), ports)), line=ln))
            continue
        raise Unsupported(text)
    blocks = top + sets + body
    if not blocks:
        raise Unsupported("nothing to draw")
    return blocks, whole
