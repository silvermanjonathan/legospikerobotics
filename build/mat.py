"""The challenge mat: 24 sheets of letter paper taped into one field for three robots.

Everything is in centimetres from the mat's top left corner, x to the right and y
down. The mat is 4 sheets wide and 6 sheets tall, each sheet upright, so it is
86.36 cm by 167.64 cm. It holds three lanes, one for each robot, one under the other.
A lane is two sheets tall, 55.88 cm, which leaves room for a robot to drive its
square and to park without reaching the next lane.

Nothing that matters is drawn within SAFE cm of a sheet's edge, because most printers
leave that strip blank. The sheets are taped edge to edge with no trimming, and the
blank strips become part of the mat. Each far line, which the colour sensor has to
find, sits wholly inside one sheet.

Where the numbers come from:
  - 55 cm from start A to the far line is the course's own far line (robot.FAR_CM),
    about two full turns of the wheel (wheel.py).
  - Start B is 14 cm nearer the far line, about half a turn of the wheel.
  - The drop zone, the island, and the home marks are placed from the wheel arithmetic
    and a robot about 22 cm long and 20 cm wide whose wheels are about 11 cm behind its
    front edge. They have NOT been checked on a built robot.
"""
import html

from robot import FAR_CM, CRATE_CM
from wheel import WHEEL_CM, whole_cm

SHEET_W, SHEET_H = 21.59, 27.94          # one letter sheet, upright
COLS, ROWS = 4, 6
W, H = SHEET_W * COLS, SHEET_H * ROWS
SAFE = 0.8                                # nothing is drawn this close to a sheet's edge

LANES = 3
LANE_H = 2 * SHEET_H                      # each lane is two sheets tall
LANE_Y = 17.0                             # the middle of the robot's path, from the lane's top
START_A = 23.0
START_B = 37.0
FAR = START_A + FAR_CM                    # 78
LIMIT = FAR + 7                           # the dashed line: past this is too far
HOME = (START_A - 5, START_A + 5)         # the robot's front edge ends between these
ISLAND = (26.0, 31.0)                     # where the middle of the crate goes, in a lane
ZONE = (58.0, 30.0, 85.0, 52.5)           # the drop zone in a lane: x0, y0, x1, y1
ZONE_W, ZONE_H = int(ZONE[2] - ZONE[0]), int(round(ZONE[3] - ZONE[1]))

INK, TEAL, OCHRE, SOFT, CLAY = "#17181B", "#0E4D52", "#8A5A00", "#4A4D53", "#9C2B22"

# Each mission scores for every robot that does it, and scores a team bonus when all
# three robots do it on the same run.
MISSIONS = [
    dict(n=1, name="The dock", session=2, each=10, bonus=10,
         start="Start A, in all three lanes",
         goal="Each robot stops with its front edge between its far line and its dashed line.",
         rule="Use a number for the distance. Do not use the colour sensor yet.",
         does="stops with its front edge between the far line and the dashed line"),
    dict(n=2, name="Around the crate", session=2, each=10, bonus=10,
         start="Start A, with a crate on each island",
         goal="Each robot drives a square around its crate and comes back to where it started.",
         rule="Each side of the square is one full turn of the wheel, about %d cm. A robot "
              "that touches its crate does not score." % whole_cm(360),
         does="goes around its crate without touching it and ends with its front edge "
              "between the home marks"),
    dict(n=3, name="The dock that moves", session=3, each=10, bonus=10,
         start="Start A or start B. The teacher says which for each lane, just before the run.",
         goal="Each robot stops between its far line and its dashed line, from whichever "
              "start it was given.",
         rule="Start B is 14 cm nearer the far line, so a distance cannot work for both. "
              "Nobody changes a program after the teacher has spoken.",
         does="stops with its front edge between the far line and the dashed line"),
    dict(n=4, name="The delivery run", session=4, each=10, bonus=20,
         start="Start A or start B. The teacher says which for each lane, just before the run.",
         goal="Each robot finds its far line, makes a quarter turn to the right, and parks "
              "in its drop zone.",
         rule="A robot is parked when both big wheels are inside the drop zone.",
         does="parks with both big wheels inside its drop zone"),
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
    """A start or home mark: two short ticks at the edges of the robot's path. The
    middle stays blank, so the colour sensor never passes over a mark."""
    return (_line(x, lane - 7.8, x, lane - 5.2, colour, 0.35)
            + _line(x, lane + 5.2, x, lane + 7.8, colour, 0.35)
            + _t(x, lane - 8.5, label, 0.62, colour, anchor=anchor))


def lane_features(k):
    """Every mark in lane k (0, 1, 2), as SVG in centimetres."""
    oy = k * LANE_H
    lane = oy + LANE_Y
    p = [_t(2.2, oy + 4.6, "LANE %d" % (k + 1), 1.5, TEAL, 800)]
    # ruler along the top of the lane, in cm from start A
    for c in range(0, int(LIMIT - START_A) + 1):
        x = START_A + c
        long_ = c % 5 == 0
        p.append(_line(x, oy + 1.0, x, oy + (1.9 if long_ else 1.5), SOFT, 0.12 if long_ else 0.08))
        if long_:
            p.append(_t(x, oy + 2.55, str(c), 0.5, SOFT, 500, "middle"))
    p.append(_t(START_A + 12, oy + 3.6, "the ruler counts cm from start A", 0.5, SOFT, 500))
    # centre guide behind start A, to line the robot up
    p.append(_line(2.0, lane, START_A - 2.5, lane, SOFT, 0.08, "0.6 0.5"))
    p.append(_t(2.0, lane - 0.5, "middle of the robot goes on this line", 0.5, SOFT, 500))
    # forward arrow
    p.append(_line(3.0, lane + 3.4, 11.0, lane + 3.4, TEAL, 0.35))
    p.append('<polygon points="11,%.2f 12.6,%.2f 11,%.2f" fill="%s"/>'
             % (lane + 2.7, lane + 3.4, lane + 4.1, TEAL))
    p.append(_t(3.0, lane + 2.8, "forward", 0.7, TEAL))
    # starts and home marks
    p.append(_ticks(HOME[0], lane, SOFT, "home"))
    p.append(_ticks(START_A, lane, TEAL, "START A", "start"))
    p.append(_ticks(HOME[1], lane, SOFT, "home", "start"))
    p.append(_ticks(START_B, lane, OCHRE, "START B"))
    # the far line, black, and the dashed limit
    p.append('<rect x="%.2f" y="%.2f" width="2" height="16.6" fill="%s"/>' % (FAR, lane - 7.8, INK))
    p.append(_t(FAR + 2.9, lane + 0.5, "FAR LINE", 0.62, INK, anchor="middle", rot=90))
    p.append(_line(LIMIT, lane - 7.8, LIMIT, lane + 8.8, CLAY, 0.25, "1 0.7"))
    p.append(_t(LIMIT - 0.9, lane + 0.5, "TOO FAR", 0.62, CLAY, anchor="middle", rot=90))
    # the island: a target for the middle of the crate, wholly inside one sheet
    ix, iy = ISLAND[0], oy + ISLAND[1]
    p.append('<circle cx="%.2f" cy="%.2f" r="1.6" fill="none" stroke="%s" stroke-width="0.3"/>'
             % (ix, iy, OCHRE))
    p.append(_line(ix - 2.2, iy, ix + 2.2, iy, OCHRE, 0.2) + _line(ix, iy - 2.2, ix, iy + 2.2, OCHRE, 0.2))
    p.append(_t(ix, iy + 3.6, "ISLAND %d" % (k + 1), 0.8, OCHRE, 800, "middle"))
    p.append(_t(ix, iy + 4.6, "put the crate on the cross", 0.5, OCHRE, 500, "middle"))
    # the drop zone
    x0, y0, x1, y1 = ZONE[0], oy + ZONE[1], ZONE[2], oy + ZONE[3]
    p.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" '
             'stroke-width="0.5"/>' % (x0, y0, x1 - x0, y1 - y0, TEAL))
    p.append(_t((x0 + x1) / 2, y0 + 2.6, "DROP ZONE %d" % (k + 1), 1.2, TEAL, 800, "middle"))
    p.append(_t((x0 + x1) / 2, y0 + 3.9, "park with both big wheels inside", 0.62, TEAL, 500, "middle"))
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
