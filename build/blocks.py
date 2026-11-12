"""Word Block stacks drawn in HTML and CSS (style guide, section 9).

A stack is drawn, not screenshotted, so its words are real text that prints, scales,
and reads aloud. Each block keeps the SPIKE App's own category hue. The hues below
were sampled on 12 November 2026 from the block program images on LEGO's lesson
pages for the Game Master and the Grabbers. Block words are ink (#17181B). Where a
hue is too dark for ink to clear 7:1, it is lightened toward white in the same hue
until it does, so it still matches the tablet. The edge of each block is a darker
shade of the app's own hue.

check() is called by validate.py. It recomputes every contrast ratio and stops the
build if one falls short, and checks that every C block's arm is at least 16px wide.

Shapes follow the app: a hat block starts a stack, a stack block snaps under another,
a C block holds blocks, a round reporter gives a value, and a six-sided block gives
true or false.
"""
import html

INK = "#17181B"
MIN_RATIO = 7.0
ARM_PX = 20               # width of a C block's left arm; the guide asks for 16 or more

# The app's hue for each category, sampled from LEGO's program images.
APP_HUE = {
    "events":    ("#F5C400", "a 'when' block on LEGO's Grabbers and Game Master programs"),
    "motors":    ("#0090F5", "a motor 'run' block on the same two programs"),
    "light":     ("#935DF5", "a 'turn off pixels' block on the Game Master program"),
    "sound":     ("#BF70E7", "a 'play sound' block on the Game Master program"),
    "control":   ("#FFB515", "a 'repeat' block on the Game Master program"),
    "sensors":   ("#1DCCF0", "a colour sensor block on the Game Master program"),
    "operators": ("#00B94D", "an '=' block on the Game Master program"),
    "variables": ("#FF693C", "a list block in the Variables category on the Game Master program"),
}

NAMES = {
    "events": "Events", "motors": "Motors", "light": "Light", "sound": "Sound",
    "control": "Control", "sensors": "Sensors", "operators": "Operators",
    "variables": "Variables",
}


# ---------------------------------------------------------------- colour arithmetic

def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def _lum(h):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _mix(h, t):
    """h moved a fraction t of the way to white."""
    return _hex(tuple(c + (255 - c) * t for c in _rgb(h)))


def _shade(h, k):
    return _hex(tuple(c * k for c in _rgb(h)))


def fill_for(hue):
    """The lightest step needed for ink to clear MIN_RATIO, in the same hue."""
    for step in range(0, 101):
        f = _mix(hue, step / 100.0)
        if ratio(INK, f) >= MIN_RATIO:
            return f, step
    raise ValueError("no fill clears %s:1 for %s" % (MIN_RATIO, hue))


COLOURS = {}
for _cat, (_hue, _src) in APP_HUE.items():
    _fill, _step = fill_for(_hue)
    COLOURS[_cat] = {"hue": _hue, "fill": _fill, "lightened": _step,
                     "edge": _shade(_hue, 0.72), "field": _mix(_fill, 0.55),
                     "source": _src}


def check():
    """Recompute every contrast the stacks depend on. Returns a list of faults."""
    faults = []
    for cat, c in COLOURS.items():
        for part in ("fill", "field"):
            r = ratio(INK, c[part])
            if r < MIN_RATIO:
                faults.append("%s %s %s gives %.2f:1, under %s:1" % (cat, part, c[part], r, MIN_RATIO))
    if ratio(INK, "#FFFFFF") < MIN_RATIO:
        faults.append("number fields fail contrast")
    if ARM_PX < 16:
        faults.append("C block arms are %dpx, under 16px" % ARM_PX)
    return faults


# ---------------------------------------------------------------- block data

def hat(cat, *parts):
    return {"kind": "hat", "cat": cat, "parts": parts}


def blk(cat, *parts):
    return {"kind": "stack", "cat": cat, "parts": parts}


def cblock(cat, head, body, else_body=None):
    return {"kind": "c", "cat": cat, "head": head, "body": body, "else": else_body}


def num(v):
    return ("num", str(v))


def txt(v):
    return ("txt", str(v))


def dd(v):
    return ("dd", str(v))


def port(v):
    return ("port", str(v))


def cw():
    return ("dir", "cw")


def ccw():
    return ("dir", "ccw")


def boolean(cat, *parts):
    return ("bool", cat, parts)


def var(name):
    return ("rep", "variables", (name,))


DIR_GLYPH = {"cw": ("↻", "clockwise"), "ccw": ("↺", "counterclockwise")}


# ---------------------------------------------------------------- drawing

def _parts(parts):
    out = []
    for p in parts:
        if isinstance(p, str):
            out.append('<span class="w">' + html.escape(p) + '</span>')
        elif p[0] == "num":
            out.append('<span class="fd n">' + html.escape(p[1]) + '</span>')
        elif p[0] == "txt":
            out.append('<span class="fd t">' + html.escape(p[1]) + '</span>')
        elif p[0] == "dd":
            out.append('<span class="fd dd">' + html.escape(p[1]) + '</span>')
        elif p[0] == "port":
            out.append('<span class="fd pt">' + html.escape(p[1]) + '</span>')
        elif p[0] == "dir":
            g, word = DIR_GLYPH[p[1]]
            out.append('<span class="fd dd dir" title="' + word + '"><span aria-hidden="true">'
                       + g + '</span><span class="sr">' + word + '</span></span>')
        elif p[0] == "bool":
            out.append('<span class="bool cat-' + p[1] + '"><span class="bin">'
                       + _parts(p[2]) + '</span></span>')
        elif p[0] == "rep":
            out.append('<span class="rep cat-' + p[1] + '">' + _parts(p[2]) + '</span>')
    return "".join(out)


def _block(b):
    if b["kind"] == "hat":
        return '<div class="bk hat cat-' + b["cat"] + '">' + _parts(b["parts"]) + '</div>'
    if b["kind"] == "stack":
        return '<div class="bk cat-' + b["cat"] + '">' + _parts(b["parts"]) + '</div>'
    cat = b["cat"]
    out = ['<div class="cb cat-' + cat + '">',
           '<div class="bk chead">' + _parts(b["head"]) + '</div>',
           '<div class="cbody"><div class="carm"></div><div class="cin">'
           + "".join(_block(x) for x in b["body"]) + '</div></div>']
    if b["else"] is not None:
        out.append('<div class="bk cmid"><span class="w">else</span></div>')
        out.append('<div class="cbody"><div class="carm"></div><div class="cin">'
                   + "".join(_block(x) for x in b["else"]) + '</div></div>')
    out.append('<div class="bk cfoot"></div></div>')
    return "".join(out)


def _uses_dir(blocks):
    def walk(bs):
        for b in bs:
            parts = b.get("parts") or b.get("head") or ()
            if any(isinstance(p, tuple) and p[0] == "dir" for p in parts):
                return True
            if b["kind"] == "c" and (walk(b["body"]) or (b["else"] and walk(b["else"]))):
                return True
        return False
    return walk(blocks)


def _cats(blocks, found=None):
    found = found if found is not None else []

    def add(c):
        if c not in found:
            found.append(c)

    for b in blocks:
        add(b["cat"])
        for p in (b.get("parts") or ()) + tuple(b.get("head") or ()):
            if isinstance(p, tuple) and p[0] in ("bool", "rep"):
                add(p[1])
        if b["kind"] == "c":
            _cats(b["body"], found)
            if b["else"]:
                _cats(b["else"], found)
    return found


def stack(blocks, label=""):
    """One drawn stack, with a key that names its categories and any arrows."""
    key = ['<p class="bkey">']
    key.append("Colours: " + ", ".join(
        '<span class="chip cat-' + c + '">' + NAMES[c] + '</span>' for c in _cats(blocks)) + ".")
    if _uses_dir(blocks):
        key.append(" <span class=\"dirkey\">↻</span> means clockwise and "
                   "<span class=\"dirkey\">↺</span> means counterclockwise.")
    key.append('</p>')
    return ('<figure class="blocks"' + (' aria-label="' + html.escape(label) + '"' if label else '')
            + '><div class="stackwrap"><div class="stack">'
            + "".join(_block(b) for b in blocks) + '</div></div>' + "".join(key) + '</figure>')


def chip(cat, words):
    """A block named inside a sentence: its words, with an edge in its category colour."""
    return '<span class="bchip cat-' + cat + '">' + html.escape(words) + '</span>'


def css():
    vars_ = "".join(".cat-%s{--f:%s;--e:%s;--fd:%s}\n" % (c, v["fill"], v["edge"], v["field"])
                    for c, v in COLOURS.items())
    return vars_ + """
figure.blocks{margin:0 0 18px}
.stackwrap{overflow-x:auto; padding:4px 2px 8px}
.stack{display:inline-flex; flex-direction:column; align-items:flex-start; min-width:max-content}
.bk{position:relative; display:inline-flex; align-items:center; gap:7px; flex-wrap:nowrap;
  background:var(--f); border:2px solid var(--e); border-radius:7px;
  padding:6px 14px 6px 12px; min-height:46px; color:#17181B;
  font-family:'DM Sans',sans-serif; font-weight:600; font-size:19px; line-height:1.3;
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.stack>*+*, .cin>*+*{margin-top:-2px}
.bk.hat{border-radius:28px 28px 7px 7px; padding-top:18px; min-width:220px}
.cb{display:flex; flex-direction:column; align-items:flex-start; min-width:max-content}
.cb>.bk.chead{border-radius:7px 7px 7px 0}
.cb>.bk.cmid{border-radius:0 7px 7px 0; min-height:34px; margin-top:-2px}
.cb>.bk.cfoot{border-radius:0 7px 7px 7px; min-height:24px; min-width:150px; padding:0; margin-top:-2px}
.cbody{display:flex; align-items:stretch; margin-top:-2px}
.carm{width:""" + str(ARM_PX) + """px; flex:none; background:var(--f);
  border-left:2px solid var(--e); border-right:2px solid var(--e);
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.cin{display:flex; flex-direction:column; align-items:flex-start; padding:3px 0 3px 0; min-height:28px}
.fd{display:inline-flex; align-items:center; gap:4px; border:2px solid var(--e);
  border-radius:999px; padding:0 11px; min-height:32px; color:#17181B;
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.fd.n,.fd.t{background:#FFFFFF; font-family:'JetBrains Mono',monospace; font-weight:700;
  font-variant-ligatures:none}
.fd.dd,.fd.pt{background:var(--fd); font-weight:700}
.fd.dd{border-radius:7px}
.fd.dd::after{content:"\\25BE"; font-size:13px; margin-left:2px}
.fd.pt{font-family:'JetBrains Mono',monospace; min-width:38px; justify-content:center}
.fd.dir{font-size:21px}
.sr{position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0)}
.rep{display:inline-flex; align-items:center; gap:6px; background:var(--f);
  border:2px solid var(--e); border-radius:999px; padding:2px 13px; min-height:34px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.bool{display:inline-flex; background:var(--e); padding:2px;
  clip-path:polygon(16px 0,calc(100% - 16px) 0,100% 50%,calc(100% - 16px) 100%,16px 100%,0 50%);
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.bool .bin{display:inline-flex; align-items:center; gap:6px; background:var(--f);
  padding:3px 22px; min-height:36px;
  clip-path:polygon(15px 0,calc(100% - 15px) 0,100% 50%,calc(100% - 15px) 100%,15px 100%,0 50%);
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.bkey{font-size:15.5px; color:var(--ink-soft); margin:4px 0 0}
.chip{display:inline-block; background:var(--f); border-left:6px solid var(--e);
  padding:0 8px; border-radius:3px; color:#17181B; font-weight:600;
  -webkit-print-color-adjust:exact; print-color-adjust:exact}
.dirkey{font-size:19px}
.bchip{display:inline; background:#EDE7D9; border-left:4px solid var(--e); padding:1px 7px;
  border-radius:3px; font-family:'DM Sans',sans-serif; font-weight:600; font-size:.9em; color:#17181B}
@media (max-width:760px){
  .bk{font-size:15px; min-height:38px; padding:5px 10px}
  .fd{min-height:26px; padding:0 8px}
  .bk.hat{min-width:170px}
}
@media print{
  .bk{font-size:15.5px}
  .stackwrap{overflow:visible}
  figure.blocks{break-inside:avoid}
}
"""
