"""The challenge mat: twelve sheets of letter paper taped into one field.

Everything is in centimetres from the mat's top left corner, x to the right and y
down. The mat is 4 sheets wide and 3 sheets tall, each sheet on its side, so it is
111.76 cm by 64.77 cm.

Nothing that matters is drawn within SAFE cm of a sheet's edge, because most printers
leave that strip blank. The sheets are taped edge to edge with no trimming, and the
blank strips become part of the mat. The far line, which the colour sensor has to
find, sits wholly inside one sheet.

Where the numbers come from:
  - 55 cm from start A to the far line is the course's own far line (robot.FAR_CM),
    about two full turns of the wheel (wheel.py).
  - Start B is 14 cm nearer the far line, about half a turn of the wheel.
  - The drop zone and the home marks are placed from the wheel arithmetic and a robot
    about 22 cm long. They have NOT been checked on a built robot. The drop zone is
    21 cm by 38 cm so that a robot a few cm off still parks inside it.
"""
import html

from robot import FAR_CM, CRATE_CM
from wheel import WHEEL_CM, whole_cm

SHEET_W, SHEET_H = 27.94, 21.59          # one letter sheet on its side
COLS, ROWS = 4, 3
W, H = SHEET_W * COLS, SHEET_H * ROWS
SAFE = 0.8                                # nothing is drawn this close to a sheet's edge

LANE_Y = 10.8                             # the middle of the lane, along the top row
START_A = 22.0
START_B = 36.0
FAR = START_A + FAR_CM                    # 79
LIMIT = FAR + 12                          # the dashed line: past this is too far
HOME = (START_A - 5, START_A + 5)         # the robot's front edge ends between these
ISLAND = (24.5, 25.0)                     # where the middle of the crate goes
ZONE = (58.5, 24.0, 79.5, 62.0)           # the drop zone: x0, y0, x1, y1
LEGEND = (85.2, 23.2)

INK, TEAL, OCHRE, SOFT, CLAY = "#17181B", "#0E4D52", "#8A5A00", "#4A4D53", "#9C2B22"

MISSIONS = [
    dict(n=1, name="The dock", session=2, points=10,
         start="Start A",
         goal="The robot stops with its front edge between the far line and the dashed line.",
         rule="Use a number for the distance. Do not use the colour sensor yet.",
         score=[("Front edge between the far line and the dashed line", 10)]),
    dict(n=2, name="Around the crate", session=2, points=20,
         start="Start A, with a crate on the island",
         goal="The robot drives a square around the crate and comes back to where it started.",
         rule="Each side of the square is one full turn of the wheel, about %d cm."
              % whole_cm(360),
         score=[("The robot goes all the way around and never touches the crate", 10),
                ("Its front edge ends between the two home marks", 10)]),
    dict(n=3, name="The dock that moves", session=3, points=20,
         start="Start A or start B. The teacher says which, just before the run.",
         goal="The same program stops the robot between the far line and the dashed line "
              "from both starts.",
         rule="Start B is 14 cm nearer the far line, so a distance cannot work for both.",
         score=[("Stops in the right place from start A", 10),
                ("Stops in the right place from start B, with no change to the program", 10)]),
    dict(n=4, name="The delivery run", session=4, points=30,
         start="Start A or start B. The teacher says which, just before the run.",
         goal="The robot finds the far line, makes a quarter turn to the right, and parks "
              "in the drop zone.",
         rule="The robot is parked when both big wheels are inside the drop zone.",
         score=[("Both big wheels inside the drop zone", 20),
                ("It parks from start A and from start B, with no change to the program", 10)]),
]
TOTAL = sum(m["points"] for m in MISSIONS)
for _m in MISSIONS:
    assert sum(p for _, p in _m["score"]) == _m["points"], _m["name"]


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


def _ticks(x, colour, label, anchor="middle"):
    """A start or home mark: two short ticks at the lane's edges. The middle of the
    lane stays blank, so the colour sensor never passes over a mark."""
    return (_line(x, 3.0, x, 5.6, colour, 0.35) + _line(x, 16.0, x, 18.6, colour, 0.35)
            + _t(x, 19.6, label, 0.62, colour, anchor=anchor))


def features():
    """Every mark on the mat, as SVG in centimetres."""
    p = []
    # ruler along the top of the lane, in cm from start A
    for c in range(0, int(LIMIT - START_A) + 1):
        x = START_A + c
        long_ = c % 5 == 0
        p.append(_line(x, 1.0, x, 1.9 if long_ else 1.5, SOFT, 0.08 if not long_ else 0.12))
        if long_:
            p.append(_t(x, 2.55, str(c), 0.5, SOFT, 500, "middle"))
    p.append(_t(START_A - 0.6, 1.75, "cm from start A", 0.5, SOFT, 500, "end"))
    # centre guide behind start A, to line the robot up
    p.append(_line(2.0, LANE_Y, START_A - 2.5, LANE_Y, SOFT, 0.08, "0.6 0.5"))
    p.append(_t(2.0, LANE_Y - 0.5, "middle of the robot goes on this line", 0.5, SOFT, 500))
    # forward arrow
    p.append(_line(3.0, 14.2, 11.0, 14.2, TEAL, 0.35))
    p.append('<polygon points="11,13.5 12.6,14.2 11,14.9" fill="%s"/>' % TEAL)
    p.append(_t(3.0, 13.6, "forward", 0.7, TEAL))
    # starts and home marks
    p.append(_ticks(HOME[0], SOFT, "home"))
    p.append(_ticks(START_A, TEAL, "START A"))
    p.append(_ticks(HOME[1], SOFT, "home", "end"))
    p.append(_ticks(START_B, OCHRE, "START B"))
    # the far line, black, and the dashed limit
    p.append('<rect x="%.2f" y="3.0" width="2" height="16.6" fill="%s"/>' % (FAR, INK))
    p.append(_t(FAR + 2.9, 11.3, "FAR LINE", 0.62, INK, anchor="middle", rot=90))
    p.append(_line(LIMIT, 3.0, LIMIT, 19.6, CLAY, 0.25, "1 0.7"))
    p.append(_t(LIMIT + 1.0, 11.3, "TOO FAR PAST THIS LINE", 0.62, CLAY, anchor="middle", rot=90))
    # the island: a target for the middle of the crate, wholly inside sheet A2
    ix, iy = ISLAND
    p.append('<circle cx="%.2f" cy="%.2f" r="1.6" fill="none" stroke="%s" stroke-width="0.3"/>'
             % (ix, iy, OCHRE))
    p.append(_line(ix - 2.2, iy, ix + 2.2, iy, OCHRE, 0.2) + _line(ix, iy - 2.2, ix, iy + 2.2, OCHRE, 0.2))
    p.append(_t(ix, iy + 3.6, "ISLAND", 0.8, OCHRE, 800, "middle"))
    p.append(_t(ix, iy + 4.6, "put the crate on the cross", 0.5, OCHRE, 500, "middle"))
    # the drop zone
    x0, y0, x1, y1 = ZONE
    p.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" '
             'stroke-width="0.5"/>' % (x0, y0, x1 - x0, y1 - y0, TEAL))
    p.append(_t((x0 + x1) / 2, y0 + 2.6, "DROP ZONE", 1.3, TEAL, 800, "middle"))
    p.append(_t((x0 + x1) / 2, y0 + 4.0, "park with both big wheels inside", 0.62, TEAL, 500, "middle"))
    # the missions, printed on the mat
    lx, ly = LEGEND
    p.append(_t(lx, ly + 1.2, "CHALLENGE MAT", 1.25, TEAL, 800))
    p.append(_t(lx, ly + 2.3, "%d points in all" % TOTAL, 0.7, SOFT, 500))
    y = ly + 4.4
    for m in MISSIONS:
        lines = sum(len(_wrap(w, 40)) for w, _ in m["score"])
        seam = SHEET_H * 2
        if y - 1 < seam + SAFE and y + 1.0 + 0.75 * lines > seam - SAFE:
            y = seam + SAFE + 1.6          # this mission would cross a seam: start it on the next sheet
        p.append(_t(lx, y, "%d  %s" % (m["n"], m["name"]), 0.85, INK, 800))
        p.append(_t(lx + 25.4, y, "%d" % m["points"], 0.85, TEAL, 800, "end"))
        y += 1.0
        for words, pts in m["score"]:
            for k, ln in enumerate(_wrap(words, 40)):
                p.append(_t(lx + 0.6, y, ("%d: " % pts if k == 0 else "     ") + ln, 0.52, SOFT, 500))
                y += 0.75
        y += 1.0
    return "".join(p)


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
    """One sheet at its real size: 11 by 8.5 in the printer's units."""
    sx, sy = col * SHEET_W, row * SHEET_H
    cid = "clip%d%d" % (col, row)
    name = sheet_name(col, row)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="27.94cm" height="21.59cm" '
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
    """The whole mat from above, with its twelve sheets marked."""
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
