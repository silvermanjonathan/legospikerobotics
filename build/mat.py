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


def motor_degrees(cm):
    """Degrees of motor turn that move the robot this many cm."""
    return int(round(cm / WHEEL_CM * 360))


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
MISSIONS = [
    dict(n=1, name="Fly to the space station", session=2, each=10, bonus=10,
         start="The launch line, each team in its own lane",
         goal="Each robot flies to its space station and stops with its front edge between "
              "the dock and the dashed red line.",
         rule="Use a number for the distance. Do not use the colour sensor yet. The three "
              "stations are %d, %d, and %d cm away, so each team reads its own ruler and "
              "works out its own number." % tuple(DOCK_CM),
         does="stops with its front edge between the dock and the dashed red line"),
    dict(n=2, name="Orbit the asteroid", session=2, each=10, bonus=10,
         start="The launch line, with a crate on each asteroid. The crate is the space rock.",
         goal="Each robot drives a square around its asteroid and comes back to the launch line.",
         rule="Each side of the square is one full turn of the wheel, about %d cm. A robot "
              "that touches the space rock does not score." % whole_cm(360),
         does="goes around its asteroid without touching the space rock and ends with its "
              "front edge between the home marks"),
    dict(n=3, name="Swap ships", session=3, each=10, bonus=10,
         start="The launch line of a different lane. Every team moves one lane down, and the "
               "team in lane 3 moves to lane 1.",
         goal="Each robot stops at the dock of its new lane, with its front edge between the "
              "dock and the dashed red line.",
         rule="Nobody changes a program after the swap. The docks are at different distances, "
              "so only a program that waits for the colour sensor works in every lane.",
         does="stops with its front edge between the dock and the dashed red line"),
    dict(n=4, name="Moon landing", session=4, each=10, bonus=20,
         start="The launch line of any lane. The teacher may call a swap just before the run.",
         goal="Each robot finds the dock, makes a quarter turn to the right, and lands on the "
              "moon base.",
         rule="A robot has landed when both big wheels are inside the moon base.",
         does="lands with both big wheels inside the moon base"),
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
    p.append(_t(far + 2.9, lane + 0.5, "DOCK  %d cm" % DOCK_CM[k], 0.62, INK, anchor="middle", rot=90))
    p.append(_t(far + 1, lane - 8.6, "SPACE STATION", 0.7, TEAL, 800, "middle"))
    p.append(_line(limit, lane - 7.8, limit, lane + 7.6, CLAY, 0.25, "1 0.7"))
    p.append(_t(limit - 0.9, lane + 0.5, "DEEP SPACE", 0.62, CLAY, anchor="middle", rot=90))
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
