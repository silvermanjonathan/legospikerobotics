"""The class robot and the test field: figures, the port map, and LEGO's links.

The robot is LEGO's Advanced Driving Base. LEGO's building instructions are linked,
never copied or redrawn (style guide, section 2). The robot figure here is a plain
outline that shows left, right, forward, and the measuring point; it is not a drawing
of the model.
"""

from wheel import WHEEL_CM

# ------------------------------------------------------------------ the port map
# Ports A and E are named in a comment in LEGO's own Python programs for this robot:
# "The drive motors are in port A (left) and port E (right)." LEGO's later programs
# for the same robot name medium motors in ports C and D. LEGO's lesson page lists two
# large motors, two medium motors, and two colour sensors, which leaves ports B and F
# for the sensors. Only A and E are used by this session's programs.
PORT_MAP = [
    ("A", "Large motor", "Turns the left wheel", "Named in LEGO's programs for this robot"),
    ("B", "Colour sensor", "Check on the built robot", "The port left over; confirm on the reference robot"),
    ("C", "Medium motor", "Check on the built robot", "Named in LEGO's later programs for this robot"),
    ("D", "Medium motor", "Check on the built robot", "Named in LEGO's later programs for this robot"),
    ("E", "Large motor", "Turns the right wheel", "Named in LEGO's programs for this robot"),
    ("F", "Colour sensor", "Check on the built robot", "The port left over; confirm on the reference robot"),
]
DRIVE_LEFT, DRIVE_RIGHT = "A", "E"

# ------------------------------------------------------------------ LEGO's files
_ASSET = "https://assets.education.lego.com/v3/assets/blt293eea581807678a/"
BOOKS = [
    (1, "Front", _ASSET + "blt9d23fa8f579e63ea/5f8802346c54ba0f72c2081e/advanced-driving-base-bi-pdf-book1of5.pdf?locale=en-us"),
    (2, "Right side", _ASSET + "blt0ee7fdaec9e58ae1/5f88021925f8972408a02fde/advanced-driving-base-bi-pdf-book2of5.pdf?locale=en-us"),
    (3, "Left side", _ASSET + "blt493de8c0e8747730/5f88021dce1f390e99419eca/advanced-driving-base-bi-pdf-book3of5.pdf?locale=en-us"),
    (4, "Rear", _ASSET + "blt31204a16915d90ff/5f88023d0fa6ca0be8c8d3bd/advanced-driving-base-bi-pdf-book4of5.pdf?locale=en-us"),
    (5, "Assembly", _ASSET + "blt12341bbb85ea4318/5f8802c42792080f77214054/advanced-driving-base-bi-pdf-book5of5.pdf?locale=en-us"),
]
LEGO_LESSON = ("https://education.lego.com/en-us/lessons/prime-competition-ready/"
               "assembling-an-advanced-driving-base/")
LEGO_INDEX = ("https://education.lego.com/en-us/product-resources/spike-prime/downloads/"
              "building-instructions/")
LEGO_PYTHON = (_ASSET + "blt02bcbffa2bf460b5/65df44a50f1d35dffdca4995/"
               "EN-US-SPIKE-Prime-Python-Programs_Feb-2024.pdf?locale=en-us")
LEGO_UPDATE = "https://education.lego.com/en-us/spike-update-2026/"

# ------------------------------------------------------------------ the field
START_CM = 0
FAR_CM = 55               # the far line, in cm from the start line
ZONE_CM = 5               # how close each wheel must end to its wheel marker

INK = "#17181B"
TEAL = "#0E4D52"
CARD = "#FFFDF7"
SOFT = "#4A4D53"
TAPE = "#17181B"          # both lines are black tape

PX = 8                    # pixels per cm in every field figure
LEFT_CM = -30             # the figure starts 30 cm behind the start line


def _x(cm):
    return (cm - LEFT_CM) * PX + 20


def _text(x, y, s, size=15, weight=700, fill=INK, anchor="start"):
    return ('<text x="%d" y="%d" font-family="DM Sans, sans-serif" font-size="%d" '
            'font-weight="%d" fill="%s" text-anchor="%s">%s</text>'
            % (x, y, size, weight, fill, anchor, s))


def _tape(cm, label, sub):
    x = _x(cm)
    return ('<rect x="%d" y="62" width="10" height="176" fill="%s" stroke="%s" stroke-width="2"/>'
            % (x - 5, TAPE, INK)
            + _text(x, 34, label, anchor="middle")
            + _text(x, 52, sub, size=13, weight=500, fill=SOFT, anchor="middle"))


def field_figure(far=False, markers=False, caption="", far_cm=None, far_sub=None):
    """The test field from above, to scale: 8 pixels to 1 cm.

    The start line is always drawn. far adds the far line, markers adds the two wheel
    markers. The robot is an outline only and is labelled as not to scale, because
    its real size is on the reference robot, not in this file.
    """
    far_cm = FAR_CM if far_cm is None else far_cm
    right_cm = max(FAR_CM, far_cm) + 12
    w = _x(right_cm) + 20
    h = 318
    p = ['<div class="figwrap"><svg class="fig" viewBox="0 0 %d %d" role="img" '
         'aria-label="%s" xmlns="http://www.w3.org/2000/svg">' % (w, h, caption),
         '<rect x="1" y="1" width="%d" height="%d" fill="%s" stroke="#D3CBB8" stroke-width="2"/>'
         % (w - 2, h - 2, CARD)]
    # the robot outline, behind the start line, front edge on the line
    rx, rw = _x(-22), 22 * PX - 5
    p.append('<rect x="%d" y="100" width="%d" height="100" fill="none" stroke="%s" '
             'stroke-width="3"/>' % (rx, rw, INK))
    p.append(_text(rx + rw // 2, 146, "robot", anchor="middle"))
    p.append(_text(rx + rw // 2, 164, "(outline, not to scale)", size=13, weight=500,
                   fill=SOFT, anchor="middle"))
    if markers:
        for y, name in ((84, "wheel marker"), (216, "wheel marker")):
            p.append('<rect x="%d" y="%d" width="22" height="8" fill="%s" stroke="%s" '
                     'stroke-width="2"/>' % (rx + rw // 2 - 11, y - 4, "#FFFDF7", INK))
        p.append(_text(rx + rw // 2, 76, "wheel marker", size=13, anchor="middle"))
        p.append(_text(rx + rw // 2, 236, "wheel marker", size=13, anchor="middle"))
    p.append(_tape(START_CM, "start line", "black tape, 0 cm"))
    if far:
        p.append(_tape(far_cm, "far line", far_sub or "black tape, %d cm" % far_cm))
    # the measuring point: the robot's front edge
    fx = _x(0) - 8
    p.append('<circle cx="%d" cy="150" r="6" fill="%s"/>' % (fx, TEAL))
    # forward arrow
    ax = _x(6)
    p.append('<line x1="%d" y1="150" x2="%d" y2="150" stroke="%s" stroke-width="5"/>'
             % (ax, ax + 92, TEAL))
    p.append('<polygon points="%d,138 %d,150 %d,162" fill="%s"/>' % (ax + 92, ax + 116, ax + 92, TEAL))
    p.append(_text(ax + 4, 136, "forward", fill=TEAL))
    # scale bar, 10 cm
    sx = _x(-28)
    p.append('<line x1="%d" y1="286" x2="%d" y2="286" stroke="%s" stroke-width="4"/>'
             % (sx, sx + 10 * PX, INK))
    for t in (sx, sx + 10 * PX):
        p.append('<line x1="%d" y1="278" x2="%d" y2="294" stroke="%s" stroke-width="4"/>' % (t, t, INK))
    p.append(_text(sx + 10 * PX + 10, 291, "10 cm", size=14))
    p.append(_text(sx + 150, 291, "Teal dot: the robot's front edge. Every distance is "
                   "measured from the start line to it.", size=13, weight=500, fill=SOFT))
    p.append('</svg></div>')
    if caption:
        p.append('<p class="figcap">' + caption + '</p>')
    return "".join(p)


def turn_figure(caption=""):
    """The robot from above with its own left and right, and the two drive wheels."""
    w, h = 720, 300
    p = ['<div class="figwrap"><svg class="fig" viewBox="0 0 %d %d" role="img" '
         'aria-label="%s" xmlns="http://www.w3.org/2000/svg">' % (w, h, caption),
         '<rect x="1" y="1" width="%d" height="%d" fill="%s" stroke="#D3CBB8" stroke-width="2"/>'
         % (w - 2, h - 2, CARD)]
    p.append('<rect x="250" y="100" width="190" height="100" fill="none" stroke="%s" '
             'stroke-width="3"/>' % INK)
    p.append(_text(345, 146, "robot", anchor="middle"))
    p.append(_text(345, 164, "(outline, not to scale)", size=13, weight=500, fill=SOFT,
                   anchor="middle"))
    for y in (78, 204):
        p.append('<rect x="305" y="%d" width="80" height="18" fill="%s" stroke="%s" '
                 'stroke-width="2"/>' % (y, "#EDE7D9", INK))
    p.append(_text(345, 66, "left wheel, motor in port %s" % DRIVE_LEFT, anchor="middle"))
    p.append(_text(345, 246, "right wheel, motor in port %s" % DRIVE_RIGHT, anchor="middle"))
    p.append(_text(345, 36, "the robot's left", size=14, fill=SOFT, anchor="middle"))
    p.append(_text(345, 276, "the robot's right", size=14, fill=SOFT, anchor="middle"))
    p.append('<line x1="460" y1="150" x2="560" y2="150" stroke="%s" stroke-width="5"/>' % TEAL)
    p.append('<polygon points="560,138 584,150 560,162" fill="%s"/>' % TEAL)
    p.append(_text(464, 136, "forward", fill=TEAL))
    p.append(_text(244, 154, "back", size=14, fill=SOFT, anchor="end"))
    p.append('</svg></div>')
    if caption:
        p.append('<p class="figcap">' + caption + '</p>')
    return "".join(p)


# ------------------------------------------------------------------ session 2 figures
SQUARE_ZONE_CM = 10       # how close each wheel must end to its marker after a square
CRATE_CM = 10             # the crate is no more than this across


def _arrow(x1, y1, x2, y2, color=TEAL, width=5):
    """A straight arrow along the x or the y direction."""
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 22 * math.cos(ang), y2 - 22 * math.sin(ang)
    px, py = 11 * math.sin(ang), -11 * math.cos(ang)
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%d"/>'
            % (x1, y1, hx, hy, color, width)
            + '<polygon points="%d,%d %d,%d %d,%d" fill="%s"/>'
            % (x2, y2, hx + px, hy + py, hx - px, hy - py, color))


def _open(w, h, caption):
    return ['<div class="figwrap"><svg class="fig" viewBox="0 0 %d %d" role="img" '
            'aria-label="%s" xmlns="http://www.w3.org/2000/svg">' % (w, h, caption),
            '<rect x="1" y="1" width="%d" height="%d" fill="%s" stroke="#D3CBB8" stroke-width="2"/>'
            % (w - 2, h - 2, CARD)]


def _close(p, caption):
    p.append('</svg></div>')
    if caption:
        p.append('<p class="figcap">' + caption + '</p>')
    return "".join(p)


def cross_figure(caption=""):
    """The turn cross: two strips of black tape that cross at a right angle."""
    w, h = 720, 360
    p = _open(w, h, caption)
    cx, cy = 300, 180
    p.append('<rect x="80" y="%d" width="440" height="10" fill="%s" stroke="%s" stroke-width="2"/>'
             % (cy - 5, TAPE, INK))
    p.append('<rect x="%d" y="30" width="10" height="300" fill="%s" stroke="%s" stroke-width="2"/>'
             % (cx - 5, TAPE, INK))
    p.append('<rect x="%d" y="%d" width="150" height="90" fill="%s" fill-opacity="0.9" stroke="%s" '
             'stroke-width="3"/>' % (cx - 75, cy - 45, CARD, INK))
    p.append(_text(cx, cy - 8, "robot", anchor="middle"))
    p.append(_text(cx, cy + 12, "(outline, not to scale)", size=13, weight=500, fill=SOFT,
                   anchor="middle"))
    p.append(_arrow(cx + 85, cy - 24, cx + 200, cy - 24))
    p.append(_text(cx + 90, cy - 38, "before the turn: forward", fill=TEAL))
    p.append(_arrow(cx + 30, cy + 55, cx + 30, cy + 140, color=INK))
    p.append(_text(cx + 48, cy + 110, "after a quarter turn to the right:", size=14))
    p.append(_text(cx + 48, cy + 128, "the robot faces along this strip", size=14))
    p.append(_text(90, cy - 16, "strip 1, black tape", size=13, fill=SOFT))
    p.append(_text(cx - 14, 48, "strip 2, black tape", size=13, fill=SOFT, anchor="end"))
    return _close(p, caption)


def square_figure(side_cm, crate=False, caption=""):
    """The square the robot drives, from above, to scale: 4 pixels to 1 cm."""
    s4 = 4
    side = side_cm * s4
    w, h = 720, side + 150
    p = _open(w, h, caption)
    x0, y0 = 250, 70
    # the four sides, in the order the robot drives them
    pts = [(x0, y0), (x0 + side, y0), (x0 + side, y0 + side), (x0, y0 + side), (x0, y0)]
    for i in range(4):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        p.append(_arrow(x1, y1, x2, y2, width=4))
    p.append(_text(x0 + side // 2, y0 - 12, "side 1, forward", fill=TEAL, anchor="middle"))
    p.append(_text(x0 + side + 12, y0 + side // 2, "side 2", fill=TEAL))
    p.append(_text(x0 + side // 2, y0 + side + 22, "side 3", fill=TEAL, anchor="middle"))
    p.append(_text(x0 - 12, y0 + side // 2, "side 4", fill=TEAL, anchor="end"))
    # start: the robot outline behind the first corner, and the wheel markers
    p.append('<rect x="%d" y="%d" width="70" height="56" fill="none" stroke="%s" stroke-width="3"/>'
             % (x0 - 78, y0 - 28, INK))
    p.append(_text(x0 - 86, y0 - 2, "robot starts here", size=14, anchor="end"))
    p.append(_text(x0 - 86, y0 + 16, "(outline, not to scale)", size=13, weight=500, fill=SOFT,
                   anchor="end"))
    for yy in (y0 - 42, y0 + 34):
        p.append('<rect x="%d" y="%d" width="22" height="8" fill="%s" stroke="%s" stroke-width="2"/>'
                 % (x0 - 54, yy, CARD, INK))
    p.append(_text(x0 - 43, y0 - 50, "wheel markers", size=13, anchor="middle"))
    if crate:
        c = CRATE_CM * s4
        p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#EDE7D9" stroke="%s" '
                 'stroke-width="3"/>' % (x0 + side // 2 - c // 2, y0 + side // 2 - c // 2, c, c, INK))
        p.append(_text(x0 + side // 2, y0 + side // 2 + c // 2 + 20, "crate", anchor="middle"))
        p.append(_text(x0 + side // 2, y0 + side // 2 + c // 2 + 38,
                       "no more than %d cm across" % CRATE_CM, size=13, weight=500, fill=SOFT,
                       anchor="middle"))
    sx, sy = 30, h - 30
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
             % (sx, sy, sx + 10 * s4, sy, INK))
    for t in (sx, sx + 10 * s4):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
                 % (t, sy - 8, t, sy + 8, INK))
    p.append(_text(sx + 10 * s4 + 10, sy + 5, "10 cm", size=14))
    p.append(_text(sx + 120, sy + 5, "Each side is about %d cm. Every turn is a quarter turn "
                   "to the robot's right." % side_cm, size=13, weight=500, fill=SOFT))
    return _close(p, caption)


# ------------------------------------------------------------------ session 4 figure
DROP_CM = 40              # the drop zone is a square of tape this many cm on a side
FAR_MIN, FAR_MAX = 40, 70 # the teacher puts the far line somewhere in this range


def delivery_figure(leg_cm, caption=""):
    """The delivery run from above, to scale: 5 pixels to 1 cm, far line drawn at 55 cm."""
    k = 5
    w, h = 760, 480
    p = _open(w, h, caption)
    x0, y0 = 190, 110
    xf = x0 + FAR_CM * k
    for x, name, sub in ((x0, "start line", "black tape, 0 cm"),
                         (xf, "far line", "black tape, %d to %d cm" % (FAR_MIN, FAR_MAX))):
        p.append('<rect x="%d" y="50" width="10" height="130" fill="%s" stroke="%s" stroke-width="2"/>'
                 % (x - 5, TAPE, INK))
        p.append(_text(x, 24, name, anchor="middle"))
        p.append(_text(x, 42, sub, size=13, weight=500, fill=SOFT, anchor="middle"))
    p.append('<rect x="%d" y="%d" width="120" height="70" fill="none" stroke="%s" stroke-width="3"/>'
             % (x0 - 128, y0 - 35, INK))
    p.append(_text(x0 - 68, y0 - 2, "robot", anchor="middle"))
    p.append(_text(x0 - 68, y0 + 16, "(not to scale)", size=13, weight=500, fill=SOFT, anchor="middle"))
    p.append(_arrow(x0 + 14, y0, xf - 14, y0))
    p.append(_text(x0 + 24, y0 - 12, "1. move until the far line", fill=TEAL))
    p.append(_arrow(xf - 30, y0 + 20, xf - 30, y0 + 20 + leg_cm * k))
    p.append(_text(xf - 44, y0 + 44, "2. quarter turn to the right", fill=TEAL, anchor="end"))
    p.append(_text(xf - 44, y0 + 64, "3. forward about %d cm" % leg_cm, fill=TEAL, anchor="end"))
    d = DROP_CM * k
    zx, zy = xf - 30 - d // 2, y0 + 20 + leg_cm * k - 40
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="4" '
             'stroke-dasharray="14 8"/>' % (zx, zy, d, d, INK))
    p.append(_text(zx + d + 12, zy + d // 2 - 6, "drop zone"))
    p.append(_text(zx + d + 12, zy + d // 2 + 14, "%d cm by %d cm, tape" % (DROP_CM, DROP_CM),
                   size=13, weight=500, fill=SOFT))
    sx, sy = 30, h - 30
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
             % (sx, sy, sx + 10 * k, sy, INK))
    for t in (sx, sx + 10 * k):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
                 % (t, sy - 8, t, sy + 8, INK))
    p.append(_text(sx + 10 * k + 10, sy + 5, "10 cm", size=14))
    return _close(p, caption)



# ------------------------------------------------------------------ part 2 figures
SHELF_GAP_CM = 20         # the shelf lines are this far apart
SHELVES = 4
TRACK_CM = 70             # the line to follow runs this far to the stop bar


def shelves_figure(caption=""):
    """The shelf lines from above, to scale: 7 pixels to 1 cm."""
    k = 7
    w, h = 30 * k + SHELVES * SHELF_GAP_CM * k + 110, 300
    p = _open(w, h, caption)
    x0 = 30 * k
    p.append('<rect x="%d" y="100" width="%d" height="90" fill="none" stroke="%s" stroke-width="3"/>'
             % (x0 - 150, 145, INK))
    p.append(_text(x0 - 78, 142, "robot", anchor="middle"))
    p.append(_text(x0 - 78, 160, "(not to scale)", size=13, weight=500, fill=SOFT, anchor="middle"))
    p.append('<rect x="%d" y="70" width="10" height="150" fill="%s" stroke="%s" stroke-width="2"/>'
             % (x0 - 5, TAPE, INK))
    p.append(_text(x0, 44, "start line", anchor="middle"))
    p.append(_text(x0, 60, "0 cm", size=13, weight=500, fill=SOFT, anchor="middle"))
    for i in range(1, SHELVES + 1):
        x = x0 + i * SHELF_GAP_CM * k
        p.append('<rect x="%d" y="70" width="10" height="150" fill="%s" stroke="%s" stroke-width="2"/>'
                 % (x - 5, TAPE, INK))
        p.append(_text(x, 44, "shelf %d" % i, anchor="middle"))
        p.append(_text(x, 60, "%d cm" % (i * SHELF_GAP_CM), size=13, weight=500, fill=SOFT,
                       anchor="middle"))
    p.append(_arrow(x0 + 16, 145, x0 + 110, 145))
    p.append(_text(x0 + 18, 132, "forward", fill=TEAL))
    sx, sy = 30, h - 30
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
             % (sx, sy, sx + 10 * k, sy, INK))
    for t in (sx, sx + 10 * k):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
                 % (t, sy - 8, t, sy + 8, INK))
    p.append(_text(sx + 10 * k + 10, sy + 5, "10 cm", size=14))
    p.append(_text(sx + 150, sy + 5, "Every line is black tape. The lines are %d cm apart."
                   % SHELF_GAP_CM, size=13, weight=500, fill=SOFT))
    return _close(p, caption)


def track_figure(bend=False, caption=""):
    """The line to follow and its stop bar, from above, to scale: 7 pixels to 1 cm."""
    k = 7
    w, h = 30 * k + TRACK_CM * k + 200, (440 if bend else 340)
    p = _open(w, h, caption)
    x0, y0 = 30 * k, 150
    xe = x0 + TRACK_CM * k
    ye = y0 + (15 * k if bend else 0)
    if bend:
        xm = x0 + 35 * k
        pts = "%d,%d %d,%d %d,%d" % (x0 - 60, y0, xm, y0, xe, ye)
    else:
        pts = "%d,%d %d,%d" % (x0 - 60, y0, xe, ye)
    p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="14" stroke-linejoin="round"/>'
             % (pts, TAPE))
    p.append('<rect x="%d" y="%d" width="14" height="%d" fill="%s" stroke="%s" stroke-width="2"/>'
             % (xe - 7, ye - 100, 200, TAPE, INK))
    p.append(_text(xe + 16, ye - 70, "stop bar"))
    p.append(_text(xe + 16, ye - 52, "black tape, 30 cm long", size=13, weight=500, fill=SOFT))
    p.append(_text(x0 - 40, y0 - 22, "the line to follow, black tape"))
    p.append('<rect x="%d" y="%d" width="140" height="90" fill="%s" fill-opacity="0.85" stroke="%s" '
             'stroke-width="3"/>' % (x0 - 200, y0 - 45, CARD, INK))
    p.append(_text(x0 - 130, y0 - 4, "robot", anchor="middle"))
    p.append(_text(x0 - 130, y0 + 14, "(not to scale)", size=13, weight=500, fill=SOFT, anchor="middle"))
    p.append(_arrow(x0 - 50, y0 + 40, x0 + 50, y0 + 40))
    p.append(_text(x0 - 48, y0 + 66, "forward", fill=TEAL))
    if bend:
        p.append(_text(x0 + 35 * k + 10, y0 - 22, "the bend", size=14, fill=SOFT))
    sx, sy = 30, h - 30
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
             % (sx, sy, sx + 10 * k, sy, INK))
    for t in (sx, sx + 10 * k):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'
                 % (t, sy - 8, t, sy + 8, INK))
    p.append(_text(sx + 10 * k + 10, sy + 5, "10 cm", size=14))
    p.append(_text(sx + 150, sy + 5, "At the start the line sensor is over the tape.",
                   size=13, weight=500, fill=SOFT))
    return _close(p, caption)



WHEEL_NOTE = ("One full turn of the wheel moves the robot %.2f cm. LEGO's Python programs "
              "for this robot give that figure in a comment." % WHEEL_CM)
