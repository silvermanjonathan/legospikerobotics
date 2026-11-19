"""Turns one of the course's Python programs into the same program in Word Blocks.

Every session page puts a Word Blocks panel under each Python program, so a builder
who works in blocks follows the same lesson. This file writes those panels' stacks.
Only the Python the course uses is understood. Anything else raises Unsupported, and
render.py stops the build: every program on a session page must have its panel.
Each block remembers the line of the Python program it came from, so a page whose
text says "line 12" still points at one block.

How each Python line becomes a block. The words are the SPIKE App's own, read from
the program images on LEGO's lesson pages Training Camp 1, Training Camp 3, My Code,
Our Program, and Mission Ready, and from the Game Master and Grabbers programs. The
yaw blocks follow LEGO coach slides and FLLCasts tutorials; the beep block follows
the SPIKE App's Sound palette as FLLCasts describes it.

  async def main():                         when program starts
  async def quarter_turn():                 define quarter_turn  (a My Block)
  await quarter_turn()                      quarter_turn         (the My Block)
  motor_pair.pair(PAIR_1, port.A, port.E)   set movement motors to A+E
  velocity=250                              set movement speed to 24 %
  await motor_pair.move_for_degrees(...)    move [straight: 0] for 720 [degrees]
  motor_pair.move(PAIR_1, -30, ...)         start moving [left: -30]
  motor_pair.stop(PAIR_1)                   stop moving
  await runloop.until(lambda: a < b)        wait until <a < b>
  await runloop.sleep_ms(100)               wait 0.1 seconds
  for count in range(4):                    repeat 4
  while a > b:                              repeat until <not <a > b>>
  if a < b: ... else: ...                   if <a < b> then ... else ...
  FORWARD = 360                             set FORWARD to 360
  color_sensor.reflection(port.B)           (B) reflected light
  motion_sensor.reset_yaw(0)                set yaw angle to 0
  abs(motion_sensor.tilt_angles()[0])       abs of (yaw angle)
  sound.beep(440, 500, 100)                 play beep 69 for 0.5 seconds
  light_matrix.write(str(count + 1))        write (count + 1)
  print(...)                                write ... on the light matrix

The speed. Python gives the speed as degrees of motor turn each second. The block
gives it as a percent of the motor's top speed. The top speed of the large motor is
1050 degrees of motor turn each second (the range the SPIKE App's Python help gives
for velocity), so 250 is 24 %, 150 is 14 %, and 100 is 10 %, each to the nearest
whole percent. A program with one speed sets it once, under the motors block. A
program with more than one sets it again before any move whose speed is not the
speed already set, and again inside a loop whose moves change speed.

The turn. Python's motion sensor counts the robot's turn in tenths; the yaw angle
block counts whole ones. A number the program compares with the turn, such as
QUARTER = 900, is 90 in the blocks.

The count. Python's for loop counts its repeats in count. The repeat block does not,
so when a loop uses count, the blocks set count to 0 before the repeat and change it
by 1 at the end of each repeat.

These stacks were written from the Python, not built and run in the app.
"""
import math
import re

import blocks as B

LARGE_MOTOR_TOP = 1050     # degrees of motor turn each second


class Unsupported(Exception):
    pass


def percent(velocity):
    return int(round(100.0 * velocity / LARGE_MOTOR_TOP))


def midi(freq):
    """The note number the beep block takes, from Python's pitch in Hz."""
    n = 69 + 12 * math.log2(freq / 440.0)
    if abs(n - round(n)) > 0.01:
        raise Unsupported("a beep that is not on a note: %s Hz" % freq)
    return int(round(n))


def seconds(ms):
    return "%g" % (int(ms) / 1000.0)


def _steer(s):
    s = s.strip()
    if s == "____":
        return B.dd("____")
    n = int(s)
    if n == 0:
        return B.dd("straight: 0")
    # LEGO's own images write a left turn as "left: -50"
    return B.dd(("right: %d" % n) if n > 0 else ("left: %d" % n))


def _num(v):
    return B.num(v)


def _yaw_num(v):
    q, r = divmod(int(v), 10)
    return str(q) if r == 0 else "%g" % (int(v) / 10.0)


MOVE = re.compile(r"await motor_pair\.move_for_degrees\(motor_pair\.PAIR_1, ([^,]+), ([^,]+), velocity=(\d+)\)$")
START = re.compile(r"motor_pair\.move\(motor_pair\.PAIR_1, ([^,]+), velocity=(\d+)\)$")
PAIR = re.compile(r"motor_pair\.pair\(motor_pair\.PAIR_1, port\.([A-F]), port\.([A-F])\)$")
UNTIL = re.compile(r"await runloop\.until\(lambda: (.+)\)$")
SLEEP = re.compile(r"await runloop\.sleep_ms\((\d+)\)$")
FOR = re.compile(r"for count in range\(([A-Z_]+|\d+|____)\):$")
WHILE = re.compile(r"while (.+):$")
IF = re.compile(r"if (.+):$")
PRINT = re.compile(r"print\((.+)\)$")
WRITE = re.compile(r"light_matrix\.write\((.+)\)$")
BEEP = re.compile(r"(?:await )?sound\.beep\((\d+), (\d+), (\d+)\)$")
CALL = re.compile(r"await ([a-z_]+)\(\)$")
DEF = re.compile(r"async def ([a-z_]+)\(\):$")
CONST = re.compile(r"([A-Z_]+) = (-?\d+|____)$")
SENSOR = re.compile(r"([A-Z_]+) = port\.([A-F]|____)$")
SKIP = re.compile(r"(from hub import .*|import \w+|runloop\.run\(main\(\)\)|\.\.\.)$")
REFLECT = re.compile(r"color_sensor\.reflection\((\w+(?:\.\w+)?)\)$")
YAW = "motion_sensor.tilt_angles()[0]"
TEST = re.compile(r"(.+?) ([<>]) ([A-Z_]+|-?\d+|____)$")


class Program:
    """What the whole program says, so a few lines of it can be drawn on their own."""

    def __init__(self, code, context):
        full = context or code
        self.consts, self.ports, self.yaw_names = set(), {}, set()
        for src in (context or "", code):
            for ln in src.split("\n"):
                t = ln.strip()
                m = CONST.match(t)
                if m:
                    self.consts.add(m.group(1))
                m = SENSOR.match(t)
                if m:
                    self.ports[m.group(1)] = m.group(2)
                m = re.search(r"abs\(motion_sensor\.tilt_angles\(\)\[0\]\) [<>] ([A-Z_]+)", t)
                if m:
                    self.yaw_names.add(m.group(1))
        self.speeds = sorted({int(v) for v in re.findall(r"velocity=(\d+)", full)})
        self.many = len(self.speeds) > 1
        self.used = set()          # what this panel's note has to explain
        self.speeds_drawn = set()
        self.sleeps, self.pitches = [], []

    # ------------------------------------------------------------ values

    def value(self, s, yaw=False):
        s = s.strip()
        if re.fullmatch(r"[A-Z][A-Z_]*", s):
            if yaw:
                self.used.add("yaw")
            return B.var(s)
        if re.fullmatch(r"-?\d+", s):
            if yaw:
                self.used.add("yaw")
                return B.num(_yaw_num(s))
            return B.num(s)
        if s == "____":
            return B.num(s)
        raise Unsupported(s)

    def reporter(self, s):
        """A Python value that is a reading or a sum: the round block for it."""
        s = s.strip()
        m = REFLECT.match(s)
        if m:
            arg = m.group(1)
            p = self.ports.get(arg) or (arg[5:] if arg.startswith("port.") else None)
            if not p:
                raise Unsupported(arg)
            return ("rep", "sensors", (B.port(p), "reflected light"))
        if s == YAW:
            self.used.add("yaw")
            return ("rep", "sensors", (B.dd("yaw"), "angle"))
        if s == "abs(" + YAW + ")":
            self.used.add("yaw")
            return ("rep", "operators", (B.dd("abs"), "of", ("rep", "sensors", (B.dd("yaw"), "angle"))))
        if s == "count":
            return B.var("count")
        m = re.fullmatch(r"count \+ (\d+)", s)
        if m:
            return ("rep", "operators", (B.var("count"), "+", B.num(m.group(1))))
        raise Unsupported(s)

    def test(self, s):
        m = TEST.match(s.strip())
        if not m:
            raise Unsupported(s)
        left = self.reporter(m.group(1))
        yaw = YAW in m.group(1)
        return B.boolean("operators", left, m.group(2), self.value(m.group(3), yaw=yaw))

    # ------------------------------------------------------------ speed

    def speed_block(self, v):
        self.speeds_drawn.add(v)
        return B.blk("movement", "set movement speed to", B.num(percent(v)), "%")

    def speeds_in(self, node):
        found = set(int(v) for v in re.findall(r"velocity=(\d+)", node["text"]))
        for k in node["kids"]:
            found |= self.speeds_in(k)
        return found


def _tree(code):
    """The program's lines as a tree: each line holds the lines indented under it."""
    root = {"text": "", "ln": 0, "ind": -1, "kids": []}
    path = [root]
    for i, raw in enumerate(code.split("\n"), 1):
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        ind = len(raw) - len(raw.lstrip())
        while len(path) > 1 and ind <= path[-1]["ind"]:
            path.pop()
        node = {"text": text, "ln": i, "ind": ind, "kids": []}
        path[-1]["kids"].append(node)
        path.append(node)
    return root["kids"]


def translate(code, context=None):
    """The stacks for one panel, whether the code was a whole program, and its note.

    Returns (stacks, whole, notes), notes a list of short HTML items. stacks is a list of block lists, one for each stack
    the app would hold: one per My Block, then the main stack. context is the whole
    program when code is only a few lines of it, so a name such as FORWARD or
    LINE_SENSOR is known.
    """
    P = Program(code, context)
    whole = "async def main():" in code

    def at(node, block):
        if whole:
            block = dict(block, line=node["ln"])
        return block

    def run(nodes, out, cur):
        """Draw nodes into out. cur is the speed already set, or None. Returns cur."""
        i = 0
        while i < len(nodes):
            node = nodes[i]
            t = node["text"]
            i += 1
            if SKIP.match(t) or SENSOR.match(t):
                continue
            m = CONST.match(t)
            if m:
                name, v = m.group(1), m.group(2)
                if name in P.yaw_names and v != "____":
                    P.used.add("yaw")
                    v = _yaw_num(v)
                out.append(at(node, B.blk("variables", "set", B.dd(name), "to", B.num(v))))
                continue
            m = PAIR.match(t)
            if m:
                out.append(at(node, B.blk("movement", "set movement motors to",
                                          B.dd(m.group(1) + "+" + m.group(2)))))
                if P.speeds and not P.many:
                    out.append(P.speed_block(P.speeds[0]))
                    cur = P.speeds[0]
                continue
            m = MOVE.match(t) or START.match(t)
            if m:
                v = int(m.group(m.lastindex))
                if P.many and cur != v:
                    out.append(P.speed_block(v))
                    cur = v
                if MOVE.match(t):
                    blk = B.blk("movement", "move", _steer(m.group(2)), "for",
                                P.value(m.group(1)), B.dd("degrees"))
                else:
                    blk = B.blk("movement", "start moving", _steer(m.group(1)))
                out.append(at(node, blk))
                continue
            if t == "motor_pair.stop(motor_pair.PAIR_1)":
                out.append(at(node, B.blk("movement", "stop moving")))
                continue
            m = UNTIL.match(t)
            if m:
                out.append(at(node, B.blk("control", "wait until", P.test(m.group(1)))))
                continue
            m = SLEEP.match(t)
            if m:
                P.used.add("sleep")
                P.sleeps.append(int(m.group(1)))
                out.append(at(node, B.blk("control", "wait", B.num(seconds(m.group(1))), "seconds")))
                continue
            if t == "motion_sensor.reset_yaw(0)":
                P.used.add("yaw")
                out.append(at(node, B.blk("sensors", "set yaw angle to", B.num("0"))))
                continue
            m = BEEP.match(t)
            if m:
                if m.group(3) != "100":
                    raise Unsupported("a beep at a volume other than 100")
                P.used.add("beep")
                if int(m.group(1)) not in P.pitches:
                    P.pitches.append(int(m.group(1)))
                if not t.startswith("await"):
                    P.used.add("beep-nowait")
                out.append(at(node, B.blk("sound", "play beep", B.num(midi(int(m.group(1)))), "for",
                                          B.num(seconds(m.group(2))), "seconds")))
                continue
            m = WRITE.match(t) or PRINT.match(t)
            if m:
                arg = m.group(1).strip()
                sm = re.fullmatch(r'"([^"]*)"', arg)
                if sm:
                    shown = B.txt(sm.group(1))
                else:
                    sm = re.fullmatch(r"str\((.+)\)", arg)
                    shown = P.reporter(sm.group(1) if sm else arg)
                out.append(at(node, B.blk("light", "write", shown)))
                continue
            m = CALL.match(t)
            if m and m.group(1) != "main":
                P.used.add("myblock")
                out.append(at(node, B.blk("myblocks", m.group(1))))
                cur = None                 # the My Block may have set another speed
                continue
            # ---- blocks that hold blocks
            m = FOR.match(t)
            if m:
                counted = any(re.search(r"\bcount\b", k["text"]) for k in _walk(node["kids"]))
                if counted:
                    P.used.add("count")
                    out.append(B.blk("variables", "set", B.dd("count"), "to", B.num("0")))
                inner = []
                cur = _loop(node, inner, cur, out)
                if counted:
                    inner.append(B.blk("variables", "change", B.dd("count"), "by", B.num("1")))
                n = m.group(1)
                rep = B.var(n) if re.fullmatch(r"[A-Z_]+", n) else B.num(n)
                out.append(at(node, B.cblock("control", ("repeat", rep), inner)))
                continue
            m = WHILE.match(t)
            if m:
                P.used.add("while")
                inner = []
                cur = _loop(node, inner, cur, out)
                test = B.boolean("operators", "not", P.test(m.group(1)))
                out.append(at(node, B.cblock("control", ("repeat until", test), inner)))
                continue
            m = IF.match(t)
            if m:
                else_node = nodes[i] if i < len(nodes) and nodes[i]["text"] == "else:" else None
                if else_node:
                    i += 1
                both = set(P.speeds_in(node))
                if else_node:
                    both |= P.speeds_in(else_node)
                if P.many and len(both) == 1 and cur not in both:
                    cur = both.pop()
                    out.append(P.speed_block(cur))
                body, other = [], ([] if else_node else None)
                a = run(node["kids"], body, cur)
                b = run(else_node["kids"], other, cur) if else_node else cur
                cur = a if a == b else None
                out.append(at(node, B.cblock("control", ("if", P.test(m.group(1)), "then"), body, other)))
                continue
            raise Unsupported(t)
        return cur

    def _loop(node, inner, cur, out):
        """The body of a repeat. Its first move runs after its last one, so a speed
        set inside cannot be counted on at the top: draw it with no speed known,
        unless every move in it has the one speed, which is then set before it."""
        inside = P.speeds_in(node)
        if P.many and len(inside) == 1:
            v = next(iter(inside))
            if cur != v:
                out.append(P.speed_block(v))
            run(node["kids"], inner, v)
            return v
        run(node["kids"], inner, None)
        return None if inside else cur

    stacks, main_stack, loose = [], None, []
    for node in _tree(code):
        t = node["text"]
        m = DEF.match(t)
        if m:
            name = m.group(1)
            if name == "main":
                main_stack = [at(node, B.hat("events", "when program starts"))]
                stacks.append(main_stack)
                run(node["kids"], main_stack, None)
            else:
                P.used.add("myblock")
                st = [at(node, B.hat("myblocks", "define " + name))]
                run(node["kids"], st, None)
                stacks.append(st)
            continue
        if SKIP.match(t) or SENSOR.match(t):
            continue
        if whole and CONST.match(t):
            loose.append(node)     # drawn under the main stack's motors block
            continue
        if whole:
            raise Unsupported(t)
        if not stacks or stacks[-1] is main_stack or (stacks[-1] and stacks[-1][0]["kind"] == "hat"):
            stacks.append([])
        run([node], stacks[-1], None)

    if whole and loose:
        sets = []
        run(loose, sets, None)
        # the motors and speed blocks come first, as in the app, then the names
        k = 1
        while k < len(main_stack) and main_stack[k]["cat"] == "movement" and (
                "set movement" in (main_stack[k].get("parts") or ("",))[0]):
            k += 1
        main_stack[k:k] = sets

    stacks = [st for st in stacks if st]
    if not stacks:
        raise Unsupported("nothing to draw")
    return stacks, whole, _note(P, whole)


def _walk(nodes):
    for n in nodes:
        yield n
        yield from _walk(n["kids"])


def _note(P, whole):
    """The notes under one panel's stacks, one item each: only what they need."""
    out = []
    if whole:
        out.append("The small numbers are the lines of the Python program.")
    if P.speeds_drawn and P.many:
        out.append("This program has more than one speed, so the blocks set the speed "
                   "before a move that needs a new one: "
                   + ", ".join("%d is %d&nbsp;%%" % (v, percent(v)) for v in sorted(P.speeds_drawn)) + ".")
    if "yaw" in P.used:
        out.append("Python counts the robot's turn in tenths. The yaw angle block counts "
                   "whole ones, so 900 in Python is 90 in the blocks.")
    if "sleep" in P.used:
        ms = P.sleeps[0]
        out.append("The wait block counts seconds. Python's sleep_ms counts thousandths of "
                   "a second, so sleep_ms(%d) is wait %s seconds." % (ms, seconds(ms)))
    if "beep" in P.used:
        out.append("The beep block takes a note number, not a pitch: "
                   + " and ".join("%d is note %d" % (f, midi(f)) for f in P.pitches) + ".")
    if "beep-nowait" in P.used:
        out.append("A Python beep without await plays while the program goes on; the play "
                   "beep block waits until its beep ends.")
    if "count" in P.used:
        out.append("The repeat block does not count by itself, so the blocks set count to 0 "
                   "and change it by 1 at the end of each repeat.")
    if "while" in P.used:
        out.append("Python's while keeps going while its test is true. The repeat until "
                   "block keeps going until its test is true, so the test sits inside a not "
                   "block.")
    if "myblock" in P.used:
        out.append("A function is a My Block: make it in the My Blocks part of the app. Its "
                   "define block holds the lines inside the function.")
    return out
