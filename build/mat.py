"""The challenge mat: 24 sheets of letter paper taped into one space field for three robots.

Everything is in centimetres from the mat's top left corner, x to the right and y
down. The mat is 4 sheets wide and 6 sheets tall, each sheet upright, so it is
86.36 cm by 167.64 cm. It holds three lanes, one for each robot, one under the other.
A lane is two sheets tall, 55.88 cm, which leaves room for a robot to drive its
square and to park without reaching the next lane.

Each lane has one start, the launch line. The dock, the black line the colour sensor
has to find, is a different distance from the launch line in each lane: 55, 50, and
45 cm. A program that drives a set distance works in one lane only; a program that
waits for the colour sensor works in all three. That is what the lane swap in
mission 3 tests.

Nothing that matters is drawn within SAFE cm of a sheet's edge, because most printers
leave that strip blank. The sheets are taped edge to edge with no trimming. Each dock
sits wholly inside one sheet. No picture is drawn where the colour sensor passes
between the launch line and the dock, and the tinted launch pad ends 3.5 cm behind the
launch line.

Where the numbers come from:
  - 55 cm is the course's own far line (robot.FAR_CM), about two full turns of the wheel.
  - The moon base, the asteroid, and the home marks are placed from the wheel arithmetic
    (wheel.py) and a robot about 22 cm long and 20 cm wide whose wheels are about 11 cm
    behind its front edge. They have NOT been checked on a built robot.

The mat is for every driving robot the class builds, not only the Advanced Driving
Base: LEGO's Driving Base with no sensor, with the distance sensor, or with the colour
sensor, and a robot with a force sensor. Nothing printed on a sheet names one robot.
What differs from robot to robot is on the mat's page, not on the mat:
  - the number that moves a robot a given distance (ROBOT_WHEELS, degrees_for);
  - how a robot stops at the dock (DOCK_WAYS): by a number, by the colour sensor over
    the black dock, or by a wall that the distance sensor measures or the force sensor
    presses. The wall is a box, not a printed mark.
"""
import html
import math
import random

from robot import FAR_CM, CRATE_CM
from wheel import WHEEL_CM, whole_cm

SHEET_W, SHEET_H = 21.59, 27.94          # one letter sheet, upright
COLS, ROWS = 4, 6
W, H = SHEET_W * COLS, SHEET_H * ROWS
SAFE = 0.8                                # nothing is drawn this close to a sheet's edge

LANES = 3
LANE_H = 2 * SHEET_H                      # each lane is two sheets tall
LANE_Y = 17.0                             # the middle of the robot's path, from the lane's top
START = 23.0                              # the launch line
DOCK_CM = [FAR_CM, FAR_CM - 5, FAR_CM - 10]   # launch line to dock, lane by lane
PAST = 7                                  # the dashed line is this far past the dock
HOME = (START - 5, START + 5)             # the robot's front edge ends between these
ISLAND = (26.0, 31.0)                     # the asteroid: where the middle of the crate goes
ZONE_Y = (30.0, 52.5)                     # the moon base, top and bottom, in a lane
ZONE_W, ZONE_H = 27, int(ZONE_Y[1] - ZONE_Y[0])


# One full turn of the wheel, for each wheel a class robot can have. The big wheel is
# LEGO's own figure for the Advanced Driving Base (wheel.py). The small wheel, on LEGO's
# Driving Base, is 5.6 cm across, which is 17.6 cm around; 17.5 is the number the SPIKE
# App's own "set 1 motor rotation to ... cm moved" block starts with. Each crew still
# measures its own on the lane's ruler.
SMALL_WHEEL_CM = 17.5
ROBOT_WHEELS = [
    ("Big wheels", "the Advanced Driving Base", WHEEL_CM),
    ("Small wheels", "LEGO's Driving Base, every version", SMALL_WHEEL_CM),
]
SQUARE_CM = whole_cm(360)                 # one side of the orbit in mission 2

# The wall for a robot that stops by a distance sensor or a force sensor: a box or a
# thick book, not a printed mark. Its face is the same distance from the dock in every
# lane, so one program still works after a lane swap.
WALL_PAST = 10                            # distance sensor: the face is this far past the dashed red line
WALL_FIRST_TRY = 15                       # cm, a first try for "closer than"


def degrees_for(cm, wheel_cm=WHEEL_CM):
    """Degrees of motor turn that move a robot this many cm, for a wheel that moves
    wheel_cm in one full turn."""
    return int(round(cm / wheel_cm * 360))


def motor_degrees(cm):
    """Degrees of motor turn that move the Advanced Driving Base this many cm."""
    return degrees_for(cm)


def wall_from_edge(k):
    """Where the distance sensor's wall stands in lane k, in cm from the mat's right
    edge: more than 0 is off the mat, less than 0 is on it."""
    return dock_x(k) + PAST + WALL_PAST - W


def dock_x(k):
    return START + DOCK_CM[k]


def zone(k):
    """The moon base of lane k: x0, y0, x1, y1 in the lane's own y."""
    return (dock_x(k) - 21, ZONE_Y[0], dock_x(k) + 6, ZONE_Y[1])


INK, TEAL, OCHRE, SOFT, CLAY = "#17181B", "#0E4D52", "#8A5A00", "#4A4D53", "#9C2B22"
# each lane has a rocket colour, always named in words beside it
CREW = [("RED", "#B5362A", "#F6D8D2"), ("BLUE", "#1F5FA8", "#D6E5F6"), ("GREEN", "#2E7D46", "#D8EDDD")]

# Each mission scores for every robot that does it, and scores a team bonus when all
# three robots do it on the same run.
# How a robot stops at the dock, by what it has. The first three are sensors; the last
# is a robot with none. Each is (key, name, what the crew sets up, what the program does).
DOCK_WAYS = [
    ("colour", "A colour sensor that points down",
     "Nothing. The black dock is printed on the mat.",
     "Start the wheels, wait until the colour sensor is over the black dock, stop the wheels."),
    ("distance", "A distance sensor that points forward",
     "A wall, with its face %d cm past the dashed red line." % WALL_PAST,
     "Start the wheels, wait until the wall is closer than the crew's number, stop the wheels."),
    ("force", "A force sensor on the front",
     "A wall, with its face on the dashed red line.",
     "Start the wheels, wait until the force sensor is pressed, stop the wheels."),
    ("none", "No sensor",
     "Nothing.",
     "Move forward by a number. The crew reads the lane's ruler and works the number out."),
]

SWAP_RULE = ("A crew whose robot has a sensor changes nothing after the swap. A crew whose "
             "robot has no sensor reads the ruler of its new lane and changes one number. A "
             "wall moves with its robot to the new lane.")

MISSIONS = [
    dict(n=1, name="Fly to the space station", session=2, each=10, bonus=10,
         start="The launch line, each team in its own lane",
         goal="Each robot flies to its space station and stops with its front edge between "
              "the dock and the dashed red line.",
         rule="Use a number for the distance. Do not use a sensor yet, even if your robot has "
              "one. The three stations are %d, %d, and %d cm away, and robots with different "
              "wheels need different numbers, so each team reads its own ruler and works out "
              "its own number." % tuple(DOCK_CM),
         does="stops with its front edge between the dock and the dashed red line"),
    dict(n=2, name="Orbit the asteroid", session=2, each=10, bonus=10,
         start="The launch line, with a crate on each asteroid. The crate is the space rock.",
         goal="Each robot drives a square around its asteroid and comes back to the launch line.",
         rule="Each side of the square is about %d cm. That is one full turn of big wheels and "
              "more than one full turn of small wheels. A robot that touches the space rock "
              "does not score." % SQUARE_CM,
         does="goes around its asteroid without touching the space rock and ends with its "
              "front edge between the home marks"),
    dict(n=3, name="Swap ships", session=3, each=10, bonus=10,
         start="The launch line of a different lane. Every team moves one lane down, and the "
               "team in lane 3 moves to lane 1.",
         goal="Each robot stops at the dock of its new lane, with its front edge between the "
              "dock and the dashed red line.",
         rule=SWAP_RULE + " The docks are at different distances, so a number that worked in "
              "one lane does not work in the next. A program that waits for a sensor works in "
              "every lane.",
         does="stops with its front edge between the dock and the dashed red line",
         ways=True),
    dict(n=4, name="Moon landing", session=4, each=10, bonus=20,
         start="The launch line of any lane. The teacher may call a swap just before the run.",
         goal="Each robot stops at the dock, makes a quarter turn to the right, and lands on "
              "the moon base.",
         rule="A robot has landed when both big wheels are inside the moon base. The big "
              "wheels are the two wheels the motors turn. After a swap, the rule of mission 3 "
              "holds: a crew whose robot has a sensor changes nothing, and a crew whose robot "
              "has no sensor changes one number.",
         does="lands with both big wheels inside the moon base",
         ways=True),
    dict(n=5, name="Moon dance", session=4, each=5, bonus=5,
         start="This is a bonus. It is added to the end of the moon landing program.",
         goal="After it lands, each robot spins all the way around once, and ends with both "
              "big wheels still inside the moon base.",
         rule="A full spin is four quarter turns. Repeat one line four times.",
         does="spins all the way around and stays on the moon base"),
]
for _m in MISSIONS:
    _m["points"] = LANES * _m["each"] + _m["bonus"]
TOTAL = sum(m["points"] for m in MISSIONS)


def sheet_name(col, row):
    return "ABCD"[col] + str(row + 1)


def _t(x, y, s, size=0.7, fill=INK, weight=700, anchor="start", rot=None):
    tr = ' transform="rotate(%s %.2f %.2f)"' % (rot, x, y) if rot is not None else ""
    return ('<text x="%.2f" y="%.2f" font-family="DM Sans, Arial, Helvetica, sans-serif" '
            'font-size="%.2f" font-weight="%d" fill="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, size, weight, fill, anchor, tr, html.escape(s)))


def _line(x1, y1, x2, y2, stroke=INK, w=0.2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"%s/>'
            % (x1, y1, x2, y2, stroke, w, d))


def _ticks(x, lane, colour, label, anchor="middle"):
    """A launch or home mark: two short ticks well outside the robot's middle, so the
    colour sensor never passes over a mark."""
    return (_line(x, lane - 10.0, x, lane - 8.6, colour, 0.35)
            + _line(x, lane + 8.2, x, lane + 9.4, colour, 0.35)
            + _t(x, lane - 10.5, label, 0.62, colour, anchor=anchor))


def _star(x, y, r, fill="#F4D35E", stroke="#B8962E"):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append("%.2f,%.2f" % (x + rr * math.cos(a), y + rr * math.sin(a)))
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="0.06"/>' % (" ".join(pts), fill, stroke)


def _rocket(x, y, colour, tint):
    """A small rocket pointing right, its nose at x + 7."""
    return ('<g transform="translate(%.2f %.2f)">' % (x, y)
            + '<polygon points="0,-0.2 -1.6,-0.9 -1.0,0.75 -1.6,2.4 0,1.7" fill="#F4D35E" stroke="#B8962E" stroke-width="0.08"/>'
            + '<polygon points="0.6,-0.5 -0.4,-1.9 2.2,-0.5" fill="%s"/>' % colour
            + '<polygon points="0.6,2.0 -0.4,3.4 2.2,2.0" fill="%s"/>' % colour
            + '<path d="M0,-0.5 L4.6,-0.5 Q6.6,0 7,0.75 Q6.6,1.5 4.6,2 L0,2 Z" fill="%s" stroke="%s" stroke-width="0.14"/>' % (tint, colour)
            + '<path d="M4.6,-0.5 Q6.6,0 7,0.75 Q6.6,1.5 4.6,2 Z" fill="%s"/>' % colour
            + '<circle cx="2.9" cy="0.75" r="0.62" fill="#FFFFFF" stroke="%s" stroke-width="0.14"/>' % colour
            + '</g>')


def _station(far, lane):
    """A colourful space station around the dock. Its solar panels sit above the strip
    the colour sensor travels, and its hull sits past the dock, where the sensor only
    arrives after the black line has already stopped the robot."""
    p = []
    top = lane - 12.4
    # keep the panels and hub inside the dock's own sheet
    col0 = int(far // SHEET_W) * SHEET_W + SAFE + 0.2
    fx = far + max(0.0, col0 - (far - 8.2))
    # two solar panels on a yellow boom
    p.append(_line(fx - 8.2, top + 1.6, fx + 6.6, top + 1.6, "#E0A800", 0.3))
    for x0 in (fx - 8.2, fx + 2.0):
        p.append('<rect x="%.2f" y="%.2f" width="4.6" height="3.2" rx="0.2" fill="#2F7FD1" stroke="#17406E" stroke-width="0.14"/>'
                 % (x0, top))
        for i in (1, 2, 3):
            p.append(_line(x0 + i * 1.15, top, x0 + i * 1.15, top + 3.2, "#BFE0FF", 0.07))
        p.append(_line(x0, top + 1.6, x0 + 4.6, top + 1.6, "#BFE0FF", 0.07))
    # the hub between the panels, with a dish
    p.append('<rect x="%.2f" y="%.2f" width="4.6" height="3.2" rx="0.9" fill="#F28C28" stroke="#9A4E0A" stroke-width="0.16"/>'
             % (fx - 2.9, top))
    for dx, c in ((-1.8, "#E5484D"), (-0.6, "#F4D35E"), (0.6, "#3FB56B")):
        p.append('<circle cx="%.2f" cy="%.2f" r="0.42" fill="%s" stroke="#17181B" stroke-width="0.08"/>'
                 % (fx + dx, top + 1.6, c))
    p.append(_line(fx + 1.0, top, fx + 1.9, top - 1.0, "#7B3FA0", 0.16))
    p.append('<path d="M%.2f,%.2f a0.9,0.9 0 0 1 1.5,1.0 Z" fill="#C9A6E4" stroke="#7B3FA0" stroke-width="0.12"/>'
             % (fx + 1.2, top - 1.5))
    p.append(_t(fx - 0.6, lane - 8.4, "SPACE STATION", 0.6, TEAL, 800, "middle"))
    # the hull, past the dock: orange with purple bands and blue windows
    hx, hy, hw, hh = far + 2.25, lane - 7.8, 3.0, 15.4
    p.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.2" fill="#F9B66B" stroke="#9A4E0A" stroke-width="0.16"/>'
             % (hx, hy, hw, hh))
    for yy in (hy + 1.6, hy + hh - 2.4):
        p.append('<rect x="%.2f" y="%.2f" width="%.2f" height="0.8" fill="#7B3FA0"/>' % (hx + 0.08, yy, hw - 0.16))
    for i, c in enumerate(("#BDE3FF", "#FFE08A", "#BDE3FF", "#FFE08A", "#BDE3FF")):
        p.append('<circle cx="%.2f" cy="%.2f" r="0.75" fill="%s" stroke="#17406E" stroke-width="0.14"/>'
                 % (hx + hw / 2, hy + 3.9 + i * 1.9, c))
    return "".join(p)


def _planet(x, y, r, colour, tint):
    return ('<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="none" stroke="%s" stroke-width="0.25" '
            'transform="rotate(-18 %.2f %.2f)"/>' % (x, y, r * 1.75, r * 0.42, colour, x, y)
            + '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" stroke-width="0.2"/>' % (x, y, r, tint, colour)
            + '<path d="M%.2f,%.2f q%.2f,%.2f %.2f,0" fill="none" stroke="%s" stroke-width="0.18"/>'
            % (x - r * 0.8, y - r * 0.3, r * 0.8, r * 0.5, r * 1.6, colour)
            + '<path d="M%.2f,%.2f q%.2f,%.2f %.2f,0" fill="none" stroke="%s" stroke-width="0.18"/>'
            % (x - r * 0.9, y + r * 0.25, r * 0.9, r * 0.45, r * 1.8, colour))


def lane_features(k):
    """Every mark in lane k (0, 1, 2), as SVG in centimetres."""
    oy = k * LANE_H
    lane = oy + LANE_Y
    crew, colour, tint = CREW[k]
    far = dock_x(k)
    limit = far + PAST
    rnd = random.Random(40 + k)
    p = []
    # stars, kept out of the strip the robot's sensors pass along
    for _ in range(46):
        x, y = rnd.uniform(1.5, W - 1.5), rnd.uniform(3.4, LANE_H - 1.2)
        if abs(y - LANE_Y) < 11.5 and x > 14:
            continue
        p.append(_star(x, oy + y, rnd.choice([0.28, 0.36, 0.5])))
    p.append(_t(2.0, oy + 3.3, "LANE %d" % (k + 1), 1.4, TEAL, 800))
    p.append(_t(2.0, oy + 4.5, "%s ROCKET" % crew, 0.75, colour, 800))
    p.append(_rocket(12.6, oy + 2.0, colour, tint))
    # ruler along the top of the lane, in cm from the launch line
    for c in range(0, int(limit - START) + 1):
        x = START + c
        long_ = c % 5 == 0
        p.append(_line(x, oy + 1.0, x, oy + (1.9 if long_ else 1.5), SOFT, 0.12 if long_ else 0.08))
        if long_:
            p.append(_t(x, oy + 2.55, str(c), 0.5, SOFT, 500, "middle"))
    p.append(_t(START + 0.3, oy + 3.7, "the ruler counts cm from the launch line", 0.5, SOFT, 500))
    # the launch pad: where the robot sits, with a centre guide
    p.append('<rect x="2" y="%.2f" width="17.5" height="19.4" rx="1.2" fill="%s" stroke="%s" stroke-width="0.2" '
             'stroke-dasharray="0.9 0.6"/>' % (lane - 10, tint, colour))
    p.append(_line(2.6, lane, 19.0, lane, colour, 0.1, "0.6 0.5"))
    p.append(_t(3.0, lane - 0.5, "middle of the robot goes on this line", 0.5, SOFT, 500))
    p.append(_t(3.0, lane - 7.8, "LAUNCH PAD", 0.9, colour, 800))
    p.append(_line(3.0, lane + 5.4, 11.0, lane + 5.4, colour, 0.35))
    p.append('<polygon points="11,%.2f 12.6,%.2f 11,%.2f" fill="%s"/>' % (lane + 4.7, lane + 5.4, lane + 6.1, colour))
    p.append(_t(3.0, lane + 4.8, "forward", 0.7, colour))
    # launch line and home marks
    p.append(_ticks(HOME[0], lane, SOFT, "home"))
    p.append(_ticks(START, lane, colour, "LAUNCH LINE", "start"))
    p.append(_ticks(HOME[1], lane, SOFT, "home", "start"))
    # the dock, black, and the dashed limit
    p.append('<rect x="%.2f" y="%.2f" width="2" height="15.4" fill="%s"/>' % (far, lane - 7.8, INK))
    p.append(_station(far, lane))
    p.append(_t(far + 1.22, lane - 0.2, "DOCK  %d cm" % DOCK_CM[k], 0.62, "#FFFFFF", anchor="middle", rot=90))
    p.append(_line(limit, lane - 7.8, limit, lane + 7.6, CLAY, 0.25, "1 0.7"))
    p.append(_t(limit - 0.75, lane + 0.5, "DEEP SPACE", 0.55, CLAY, anchor="middle", rot=90))
    # the asteroid: a target for the middle of the crate, wholly inside one sheet
    ix, iy = ISLAND[0], oy + ISLAND[1]
    rock = [(-2.1, -0.4), (-1.2, -1.9), (0.5, -2.1), (1.9, -1.2), (2.2, 0.5), (1.1, 1.9), (-0.7, 2.1), (-1.9, 1.2)]
    p.append('<polygon points="%s" fill="#E3DED2" stroke="#6B6557" stroke-width="0.22"/>'
             % " ".join("%.2f,%.2f" % (ix + a, iy + b) for a, b in rock))
    p.append('<circle cx="%.2f" cy="%.2f" r="0.38" fill="none" stroke="#6B6557" stroke-width="0.12"/>' % (ix - 1.0, iy + 0.9))
    p.append('<circle cx="%.2f" cy="%.2f" r="0.3" fill="none" stroke="#6B6557" stroke-width="0.12"/>' % (ix + 1.1, iy - 1.0))
    p.append(_line(ix - 1.2, iy, ix + 1.2, iy, OCHRE, 0.2) + _line(ix, iy - 1.2, ix, iy + 1.2, OCHRE, 0.2))
    p.append(_t(ix, iy + 3.4, "ASTEROID", 0.8, OCHRE, 800, "middle"))
    p.append(_t(ix, iy + 4.4, "put the space rock on the cross", 0.5, OCHRE, 500, "middle"))
    # the moon base
    x0, y0, x1, y1 = zone(k)
    y0, y1 = oy + y0, oy + y1
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 1.4
    p.append('<circle cx="%.2f" cy="%.2f" r="8.6" fill="#F5F0DA" stroke="#B9AF96" stroke-width="0.2"/>' % (cx, cy))
    for dx, dy, r in ((-4.6, -3.2, 1.3), (3.9, -4.4, 0.9), (5.2, 2.6, 1.5), (-3.1, 4.6, 1.0), (0.6, 0.4, 0.7)):
        p.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#EAE3C8" stroke="#B9AF96" stroke-width="0.15"/>'
                 % (cx + dx, cy + dy, r))
    p.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" '
             'stroke-width="0.5"/>' % (x0, y0, x1 - x0, y1 - y0, TEAL))
    p.append(_t(cx, y0 + 2.4, "MOON BASE", 1.2, TEAL, 800, "middle"))
    p.append(_t(cx, y0 + 3.6, "land with both big wheels inside", 0.62, TEAL, 500, "middle"))
    # a planet in the lane's colour, in the empty corner
    p.append(_planet(10.5, oy + 43.5, 4.2, colour, tint))
    # where one lane ends and the next begins
    if k:
        p.append(_line(1.5, oy, W - 1.5, oy, "#B9AF96", 0.15, "0.3 0.6"))
    return "".join(p)


def features():
    return "".join(lane_features(k) for k in range(LANES))


def _wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + [cur]


def sheet_svg(col, row):
    """One sheet at its real size."""
    sx, sy = col * SHEET_W, row * SHEET_H
    cid = "clip%d%d" % (col, row)
    name = sheet_name(col, row)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="21.59cm" height="27.94cm" '
         'viewBox="%.2f %.2f %.2f %.2f">' % (sx, sy, SHEET_W, SHEET_H),
         '<defs><clipPath id="%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/></clipPath></defs>'
         % (cid, sx + SAFE, sy + SAFE, SHEET_W - 2 * SAFE, SHEET_H - 2 * SAFE),
         '<g clip-path="url(#%s)">' % cid, features(), '</g>']
    # the sheet's own name, its neighbours, and a bar to check the print size
    bx, by = sx + SHEET_W - SAFE - 0.3, sy + SHEET_H - SAFE - 0.3
    p.append(_t(bx, by, name, 0.9, SOFT, 800, "end"))
    nx, ny = sx + SAFE + 0.4, sy + SHEET_H - SAFE - 1.2
    if col + 1 < COLS:
        p.append(_t(nx, ny, "%s goes to the right" % sheet_name(col + 1, row), 0.42, SOFT, 500))
    if row + 1 < ROWS:
        p.append(_t(nx, ny - 0.6, "%s goes below" % sheet_name(col, row + 1), 0.42, SOFT, 500))
    cx, cy = sx + SAFE + 0.4, sy + SHEET_H - SAFE - 0.4
    p.append(_line(cx, cy, cx + 5, cy, SOFT, 0.08) + _line(cx, cy - 0.3, cx, cy + 0.3, SOFT, 0.08)
             + _line(cx + 5, cy - 0.3, cx + 5, cy + 0.3, SOFT, 0.08)
             + _t(cx + 5.4, cy + 0.17, "this bar is 5 cm long", 0.42, SOFT, 500))
    p.append('</svg>')
    return "".join(p)


def overview_svg(caption):
    """The whole mat from above, with its sheets marked."""
    pad = 1.5
    p = ['<div class="figwrap"><svg class="fig" viewBox="%.2f %.2f %.2f %.2f" role="img" '
         'aria-label="%s" xmlns="http://www.w3.org/2000/svg">'
         % (-pad, -pad, W + 2 * pad, H + 2 * pad, html.escape(caption)),
         '<rect x="0" y="0" width="%.2f" height="%.2f" fill="#FFFFFF" stroke="%s" stroke-width="0.25"/>'
         % (W, H, INK)]
    for c in range(1, COLS):
        p.append(_line(c * SHEET_W, 0, c * SHEET_W, H, "#B9AF96", 0.12, "0.8 0.6"))
    for r in range(1, ROWS):
        p.append(_line(0, r * SHEET_H, W, r * SHEET_H, "#B9AF96", 0.12, "0.8 0.6"))
    p.append(features())
    for c in range(COLS):
        for r in range(ROWS):
            p.append(_t((c + 1) * SHEET_W - 1.2, (r + 1) * SHEET_H - 1.1, sheet_name(c, r), 0.9,
                        "#8C836C", 800, "end"))
    p.append('</svg></div><p class="figcap">' + caption + '</p>')
    return "".join(p)


# ------------------------------------------------------------------ the programs
# One whole program for every mission and every kind of robot, in the course's own
# shape: the tool lines, names in capitals for the numbers, the frame, one move per
# line. The colour sensor lines are session 3's. The distance sensor and force sensor
# lines follow LEGO's own Python lessons: distance_sensor.distance(port) counts in
# tenths of a cm and gives -1 when nothing is measured, so the test asks for more than
# 0 as well; force_sensor.pressed(port) is True while the button is pressed.
#
# Every number is a first try for the Advanced Driving Base in lane 1. runcheck.py runs
# each program against the stand-in modules and checks the moves in EXPECT.
_MOVE = "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, %s, %s, velocity=250)"
_START = "    motor_pair.move(motor_pair.PAIR_1, 0, velocity=250)"
_STOP = "    motor_pair.stop(motor_pair.PAIR_1)"
QUARTER_FIRST = 180                        # session 2's first try for the quarter turn
BACK_FIRST = -90                           # a short move backward, off the wall
DARK_FIRST = 50                            # session 3's first try

# how each kind of robot gets to the dock: tool line, names, lines, moves
_TO_DOCK = {
    "none": (None, ["TO_DOCK = %d" % degrees_for(DOCK_CM[0])],
             ["    # Move to the dock. TO_DOCK is the number for your lane and your wheels.",
              _MOVE % ("TO_DOCK", 0)],
             [("move", degrees_for(DOCK_CM[0]), 0, 250)]),
    "colour": ("color_sensor", ["LINE_SENSOR = port.B", "DARK = %d" % DARK_FIRST],
               ["    # Start the wheels. Wait until the sensor is over the dock. Stop the wheels.",
                _START,
                "    await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) < DARK)",
                _STOP],
               [("start", 0, 250), ("stop",)]),
    "distance": ("distance_sensor", ["WALL_SENSOR = port.F", "NEAR = %d" % (WALL_FIRST_TRY * 10)],
                 ["    # Start the wheels. Wait until the wall is near. Stop the wheels.",
                  _START,
                  "    await runloop.until(lambda: 0 < distance_sensor.distance(WALL_SENSOR) < NEAR)",
                  _STOP],
                 [("start", 0, 250), ("stop",)]),
    "force": ("force_sensor", ["BUMPER = port.F"],
              ["    # Start the wheels. Wait until the wall presses the bumper. Stop the wheels.",
               _START,
               "    await runloop.until(lambda: force_sensor.pressed(BUMPER))",
               _STOP],
              [("start", 0, 250), ("stop",)]),
}
_LAND = ["    # Turn a quarter turn to the right, then land on the moon base.",
         _MOVE % ("QUARTER_TURN", 100), _MOVE % ("FORWARD", 0)]
_LAND_X = [("move", QUARTER_FIRST, 100, 250), ("move", 360, 0, 250)]
_BACK = ["    # Move backward a little, off the wall. The number has a minus sign.",
         _MOVE % ("BACK", 0)]
_DANCE = ["    # Moon dance: four quarter turns make one full spin.",
          "    for count in range(4):",
          "    " + _MOVE % ("QUARTER_TURN", 100)]


def _program(tool, names, body):
    tools = sorted(t for t in (tool, "motor_pair", "runloop") if t)
    lines = ["from hub import port"] + ["import " + t for t in tools]
    if names:
        lines += [""] + names
    lines += ["", "", "async def main():",
              "    # The left drive motor is in port A. The right drive motor is in port E.",
              "    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)", ""]
    return "\n".join(lines + body + ["", "", "runloop.run(main())"])


KIND = {"none": "A robot with no sensor", "colour": "A robot with a colour sensor",
        "distance": "A robot with a distance sensor", "force": "A robot with a force sensor",
        "any": "Every robot"}
_READINGS = [90, 90, 10]                   # white paper, white paper, the dock
_PAIRED = [("pair", "A", "E")]
PROGRAMS = []                              # dicts: key, mission, kind, code, expect, script


def _add(key, mission, kind, tool, names, body, expect):
    code = _program(tool, names, body)
    compile(code, key, "exec")
    PROGRAMS.append(dict(key=key, mission=mission, kind=kind, code=code,
                         expect=_PAIRED + expect, script=_READINGS if tool == "color_sensor" else None))


_tool, _nm, _bd, _ex = _TO_DOCK["none"]
_add("m1", 1, "any", _tool, _nm, _bd, _ex)
_add("m2", 2, "any", None, ["FORWARD = 360", "QUARTER_TURN = %d" % QUARTER_FIRST],
     ["    # One side of the square and one quarter turn, four times.",
      "    for count in range(4):", "    " + _MOVE % ("FORWARD", 0),
      "    " + _MOVE % ("QUARTER_TURN", 100)],
     [("move", 360, 0, 250), ("move", QUARTER_FIRST, 100, 250)] * 4)
for _k in ("colour", "distance", "force"):
    _tool, _nm, _bd, _ex = _TO_DOCK[_k]
    _add("m3-" + _k, 3, _k, _tool, _nm, _bd, _ex)
for _k in ("colour", "distance", "force", "none"):
    _tool, _nm, _bd, _ex = _TO_DOCK[_k]
    _names = _nm + ["FORWARD = 360", "QUARTER_TURN = %d" % QUARTER_FIRST]
    if _k == "force":
        _names.append("BACK = %d" % BACK_FIRST)
        _add("m4-" + _k, 4, _k, _tool, _names, _bd + [""] + _BACK + [""] + _LAND,
             _ex + [("move", BACK_FIRST, 0, 250)] + _LAND_X)
    else:
        _add("m4-" + _k, 4, _k, _tool, _names, _bd + [""] + _LAND, _ex + _LAND_X)
_tool, _nm, _bd, _ex = _TO_DOCK["colour"]
_add("m5", 5, "colour", _tool, _nm + ["FORWARD = 360", "QUARTER_TURN = %d" % QUARTER_FIRST],
     _bd + [""] + _LAND + [""] + _DANCE,
     _ex + _LAND_X + [("move", QUARTER_FIRST, 100, 250)] * 4)


def program(key):
    return [p for p in PROGRAMS if p["key"] == key][0]
