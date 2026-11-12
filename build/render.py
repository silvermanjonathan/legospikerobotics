"""Writes every page of the site from the generator files. Pages are never edited by
hand: an edit made to the HTML is overwritten by the next build.

    python3 build/render.py      write the pages into the repo root
    python3 build/validate.py    guard 1: structure, prose rules, links, timing
    python3 build/runcheck.py    guard 2: programs, arithmetic, the run log

The page styling (Lecture Light), the Python code colors, the indent guides, and the
reveal and hint helpers are carried over unchanged from the beginner Python course's
build, as the SPIKE Prime Course Style Guide asks (sections 8 and 9).
"""
import csv
import hashlib
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from standards import STANDARDS, RESOLVED_ON, CONNECTOR
from hl import highlight
from session01 import SESSION01
from session02 import SESSION02
from session03 import SESSION03
from session04 import SESSION04
from session05 import SESSION05
from session06 import SESSION06
from session07 import SESSION07
from session08 import SESSION08
import robot
import wheel

SESSIONS = [SESSION01, SESSION02, SESSION03, SESSION04,
            SESSION05, SESSION06, SESSION07, SESSION08]
PART1 = [x for x in SESSIONS if x.get("part", 1) == 1]
PART2 = [x for x in SESSIONS if x.get("part", 1) == 2]

# Paths are relative to this file, so the repo builds from any clone.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get("SPIKE_OUT", ROOT)
VERSION = "3"
COURSE = "SPIKE Prime with Python"
HUB = "spike_course_hub"
ROBOT = "robot_advanced_driving_base"
FIELD = "field_test_field"
CONSTRAINTS = "course_constraints"
STDMAP = "standards_map"
LEDGER = "course_ledger_card"
PUBLISHED = "12 November 2026"
RUNS_NEEDED = 3

# ------------------------------------------------------------------ code colors
# The hues VS Code's light theme gives Python tokens, each darkened until it clears
# 7:1 contrast on the white code background (WCAG AAA for body text), so the code
# reads when it is projected in a room with the lights on. The same colors print.
CODE_BG = "#FFFFFF"
CODE_INK = "#1F1F1F"
CODE_COLORS = {
    "hk": "#8A00B0",  # control words: if, for, while, return, import
    "hs": "#0000FF",  # def, True, False, None, and, or, not, in, is, the f of an f-string
    "hf": "#6A4E14",  # functions and methods
    "hc": "#135C70",  # classes, types, modules
    "hv": "#001080",  # variables and parameters
    "hn": "#00579A",  # CAPITAL constants
    "hq": "#A31515",  # strings
    "he": "#B00000",  # escapes inside strings
    "hd": "#035F3E",  # numbers
    "hm": "#006400",  # comments
}


def _luminance(hex_color):
    """Relative luminance of a #RRGGBB color, as WCAG defines it."""
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(fg, bg):
    """WCAG contrast ratio between two #RRGGBB colors, from 1 to 21."""
    a, b = _luminance(fg), _luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# VS Code draws a thin light-grey line down each step of indentation. On these pages
# the same lines are drawn 6px wide and dark, because a 1px light-grey line vanishes on
# a projector with the lights on. The grey clears 7:1 on white, like the code colors.
GUIDE = "#595959"
GUIDE_WIDTH = "6px"

for _cls, _hex in list(CODE_COLORS.items()) + [("ink", CODE_INK), ("guide", GUIDE)]:
    _ratio = contrast(_hex, CODE_BG)
    assert _ratio >= 7.0, "code color %s %s is only %.2f:1 on %s" % (_cls, _hex, _ratio, CODE_BG)
# ---------------------------------------------------------------------- styling

CSS = """
/* Lecture Light: built for a projector in a room with the lights on.
   Light ground, near-black text, few accents, no hairlines. */
:root{
  --paper:#F4F0E6;
  --card:#FFFDF7;
  --ink:#17181B;
  --ink-soft:#4A4D53;
  --rule:#D3CBB8;
  --teal:#0E4D52;
  --teal-deep:#0A3A3E;
  --clay:#9C2B22;
  --ochre:#8A5A00;
  --ochre-line:#D99B12;
  --ochre-tint:#FBF2DC;
  --green:#1D5B39;
  --green-tint:#E8F1E9;
  --green-ink:#122B1C;
  --code-bg:#EDE7D9;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'DM Sans',system-ui,sans-serif; font-size:18px; font-weight:500;
  line-height:1.65;
}
header.top{
  background:var(--teal); color:#FFFDF7;
  border-bottom:6px solid var(--ochre-line); padding:30px 22px 26px;
}
.wrap{max-width:1080px; margin:0 auto}
/* prose lines stay at reading length inside the wider column; code gets the width */
p,li{max-width:72ch}
.dates,.sessionlist li,.toolbar,.legend,.exits p,.card p,.stamp,.pill{max-width:none}
.eyebrow{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.14em;
  text-transform:uppercase; color:#F2D89B; margin:0 0 10px; font-weight:700;
}
h1{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:800;
  font-size:clamp(29px,4.8vw,44px); line-height:1.1; margin:0 0 10px;
}
h2{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:25px; line-height:1.2; margin:0 0 12px; color:var(--teal-deep);
}
h3{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:20px; margin:0 0 8px; color:var(--teal-deep);
}
header.top h1,header.top h2{color:#FFFDF7}
.sub{color:#EAE3D2; margin:0 0 16px; font-size:19px; font-weight:400}
.dates{
  display:flex; flex-wrap:wrap; gap:10px; margin-top:16px;
  font-family:'JetBrains Mono',monospace; font-size:13.5px;
}
.pill{
  border:2px solid rgba(255,253,247,.4); border-radius:999px; padding:5px 13px;
  background:rgba(255,253,247,.08);
}
.pill b{color:#F2D89B; font-weight:700}
main{padding:28px 22px 12px}
section{
  background:var(--card); border:2px solid var(--rule); border-radius:6px;
  padding:22px 24px; margin:0 0 20px;
}
section.opener{border-left:8px solid var(--green)}
section.chunk{border-left:8px solid var(--ochre-line)}
section.hinge{border-left:8px solid var(--clay)}
section.brief{border-left:8px solid var(--teal)}
section.extension{border-left:8px solid var(--clay)}
.chunk-no{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ochre); margin:0 0 8px; font-weight:700;
}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px; padding-left:24px}
li{margin:0 0 8px}
.sessionlist li{max-width:none}
code,pre{
  /* JetBrains Mono ligatures turn != into a slashed equals and <= into a single
     glyph; students then type a character that does not exist. Keep every
     operator as the keys that produce it. */
  font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0,"dlig" 0;
}
code{
  font-family:'JetBrains Mono',monospace; font-size:.9em; font-weight:700;
  background:var(--code-bg); color:#1E2A2B;
  padding:2px 6px; border-radius:3px;
}
pre{
  /* 19px, a little over the 18px prose, so code reads from the back of the room */
  font-family:'JetBrains Mono',monospace; font-size:19px; line-height:1.6;
  background:var(--code-bg); color:var(--ink); border:2px solid var(--rule);
  border-left:6px solid #B9AF96; border-radius:4px;
  padding:16px 18px; overflow-x:auto; margin:0 0 16px; font-weight:500;
}
pre code{background:none; padding:0; border-radius:0; font-size:inherit; font-weight:inherit; color:inherit}
/* Python code, colored the way VS Code's light theme colors it, on white. Each color
   clears 7:1 on white (render.py checks), and the same colors print. Color only, never
   bold or italic, so every character keeps its width. */
pre.py{background:CODE_BG_HEX; color:CODE_INK_HEX}
CODE_COLOR_RULES
/* Indent guides on every code block, the lines VS Code draws down each step of
   indentation, so even a line shown on its own shows how far in it goes. Each
   four-space step is one box with a thick dark bar down its left edge. The box holds
   the step's four spaces, or on a blank line one space drawn by the CSS and not part
   of the text, so it is exactly as tall as a line wherever it sits and the bars join
   up from line to line. The spaces never wrap, even where the printed worksheets let
   code wrap. A border rather than a shadow, so the bars print. */
pre.py .ig{
  display:inline-block; width:4ch; vertical-align:top; white-space:pre;
  border-left:GUIDE_WIDTH solid GUIDE_HEX;
}
pre.py .ig:empty::before{content:" "}
pre.anatomy{background:#FFFDF7; border-left:6px solid var(--teal)}
pre.anatomy .cond{background:#FBF2DC; border-bottom:3px solid var(--ochre-line); padding:1px 2px}
pre.anatomy .blk{background:#E8F1E9; border-left:3px solid var(--green); padding:1px 2px}
pre.anatomy .nm{background:#E3EDEE; border-bottom:3px solid var(--teal); padding:1px 2px}
pre.anatomy .arg{background:#F7E4E1; border-bottom:3px solid var(--clay); padding:1px 2px}
pre.anatomy .lbl{color:var(--ink-soft); font-weight:700}
pre.anatomy .lbl-n{color:var(--teal)}
pre.anatomy .lbl-a{color:var(--clay)}
.legend i.n{background:#E3EDEE; border-bottom:3px solid var(--teal)}
.legend i.a{background:#F7E4E1; border-bottom:3px solid var(--clay)}
pre.anatomy .lbl-c{color:var(--ochre)}
pre.anatomy .lbl-b{color:var(--green)}
.legend{display:flex; flex-wrap:wrap; gap:10px 22px; font-size:16px; margin:0 0 16px}
.legend span{display:inline-flex; align-items:center; gap:8px; margin-right:18px}
.legend i{display:inline-block; width:22px; height:16px; border-radius:2px; margin-right:8px}
.legend i.c{background:#FBF2DC; border-bottom:3px solid var(--ochre-line)}
.legend i.b{background:#E8F1E9; border-left:3px solid var(--green)}
pre.out{
  background:var(--green-tint); border-color:#A9C6B2;
  border-left:6px solid var(--green); color:var(--green-ink);
}
.outlabel{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--green); margin:0 0 7px; font-weight:700;
}
.predict{
  border:2px dashed var(--ochre); border-radius:5px;
  padding:16px 18px; margin:0 0 16px; background:var(--ochre-tint);
}
.predict p{margin:0 0 12px}
.predict .q{font-weight:700}
button.rev{
  font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700;
  background:var(--teal); color:#FFFDF7; border:0; border-radius:4px;
  padding:10px 18px; cursor:pointer;
}
button.rev:hover{background:var(--teal-deep)}
button.rev.hint{background:var(--card); color:var(--ochre); border:2px solid var(--ochre-line); margin:0 10px 10px 0}
button.rev.hint:hover{background:var(--ochre-tint)}
.hints .ans{margin:0 0 12px; padding-top:10px; border-top:2px solid var(--ochre-line)}
.ladder .ans{margin:12px 0 0; padding-top:12px; border-top:2px solid var(--ochre-line)}
.ladder .ans p{margin:0 0 12px}
.ladder .ans pre{margin:0 0 12px}
.ladder .q b{color:var(--clay)}
.sofar,.whole{margin:0 0 16px}
.sofar .ans,.whole .ans{margin-top:12px; padding-top:0; border-top:0}
.ans{display:none; margin-top:16px; padding-top:16px; border-top:2px solid var(--rule)}
.ans.open{display:block}
table{border-collapse:collapse; width:100%; margin:0 0 16px; font-size:16.5px}
th,td{border:2px solid var(--rule); padding:9px 11px; text-align:left; vertical-align:top}
th{background:#EFE9DA; font-weight:700; font-size:15px; color:var(--teal-deep)}
td.fill{background:#FBF9F3; min-width:100px}
.exits{display:grid; gap:14px; grid-template-columns:1fr}
@media(min-width:760px){.exits{grid-template-columns:repeat(3,1fr)}}
.exit{border:2px solid var(--rule); border-radius:5px; padding:16px}
.exit .tag{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; margin:0 0 8px; font-weight:700;
}
.exit.floor{border-top:6px solid var(--green)}
.exit.floor .tag{color:var(--green)}
.exit.middle{border-top:6px solid var(--ochre-line)}
.exit.middle .tag{color:var(--ochre)}
.exit.stretch{border-top:6px solid var(--clay)}
.exit.stretch .tag{color:var(--clay)}
details.teacher{
  background:var(--card); border:2px solid var(--rule);
  border-left:8px solid var(--clay); border-radius:6px;
  padding:18px 22px; margin:0 0 20px;
}
details.teacher summary{
  cursor:pointer; font-family:'Bricolage Grotesque','DM Sans',sans-serif;
  font-weight:700; font-size:21px; color:var(--clay);
}
details.teacher[open] summary{margin-bottom:14px}
.note{
  font-size:16.5px; color:var(--ink-soft); border-left:4px solid var(--rule);
  padding-left:14px; margin:0 0 14px;
}
.pager{
  max-width:1080px; margin:0 auto; padding:8px 22px 34px;
  display:flex; justify-content:space-between; gap:12px;
  font-family:'JetBrains Mono',monospace; font-size:14px;
}
.pager a{
  color:var(--teal); text-decoration:none; font-weight:700;
  border:2px solid var(--rule); background:var(--card);
  border-radius:4px; padding:10px 14px;
}
.pager a:hover{background:#EFE9DA}
footer{
  background:#EAE4D5; border-top:4px solid var(--teal); padding:22px 22px 36px;
  font-size:15px; color:var(--ink-soft);
}
footer a{color:var(--teal); font-weight:700}
a{color:var(--teal)}
.toolbar{display:flex; gap:12px; flex-wrap:wrap; margin:0 0 20px}
a.btn{
  display:inline-block; font-family:'DM Sans',sans-serif; font-size:17px; font-weight:700;
  background:var(--teal); color:#FFFDF7; text-decoration:none; border-radius:4px;
  padding:12px 20px; border:2px solid var(--teal);
}
a.btn:hover{background:var(--teal-deep)}
a.btn.quiet{background:var(--card); color:var(--teal)}
a.btn.quiet:hover{background:#EFE9DA}
.grid2{display:grid; gap:16px; grid-template-columns:1fr}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}}
.card{border:2px solid var(--rule); border-radius:5px; padding:16px; background:#FFFDF7}
.card h3{margin-bottom:8px}
.sessionlist{list-style:none; padding:0; margin:0}
.sessionlist li{
  border:2px solid var(--rule); border-left:8px solid var(--teal);
  border-radius:5px; margin:0 0 12px; padding:14px 16px;
  display:flex; gap:16px; align-items:flex-start; background:#FFFDF7;
}
.sessionlist .n{
  font-family:'JetBrains Mono',monospace; font-size:24px; font-weight:700;
  color:var(--teal); min-width:38px;
}
.sessionlist a{font-weight:700; text-decoration:none; font-size:19px}
.sessionlist .meta{
  font-family:'JetBrains Mono',monospace; font-size:13px; color:var(--ink-soft);
  display:block; margin-top:4px;
}
.bonus{border-left-color:var(--clay)}
.bonus .n{color:var(--clay)}
.flag{
  background:#F7E4E1; border:2px solid var(--clay); border-left:8px solid var(--clay);
  border-radius:5px; padding:14px 16px; margin:0 0 18px; font-size:16.5px;
  color:#3A1512;
}
.stamp{
  border:3px dashed #BFB49A; border-radius:5px; padding:14px;
  font-size:15px; min-height:100px; background:#FFFDF7;
}
.stampgrid{display:grid; gap:12px; grid-template-columns:1fr 1fr}
@media(min-width:820px){.stampgrid{grid-template-columns:repeat(3,1fr)}}
.stamp .no{
  font-family:'JetBrains Mono',monospace; color:var(--ochre); font-size:12.5px;
  letter-spacing:.1em; text-transform:uppercase; display:block; margin-bottom:6px;
  font-weight:700;
}
@media (max-width:760px){
  pre{font-size:15px}
  /* a wide table scrolls inside itself instead of widening the page */
  table{display:block; overflow-x:auto; max-width:100%}
  table tbody{display:table; width:100%}
}
@media print{
  body{background:#fff; font-size:11pt}
  header.top{background:#fff; color:#111; border-bottom:3px solid #111}
  header.top h1,header.top .sub,header.top .eyebrow,.pill b{color:#111}
  .pill{border-color:#666}
  footer,.pager,details.teacher{background:#fff}
  section,.stamp,.card{background:#fff; break-inside:avoid}
  .noprint,.toolbar{display:none}
  a{color:#111}
  /* printed code keeps its old size, so printed pages and PDFs do not reflow */
  pre{font-size:15.5px}
  pre.py{background:#fff; border:1px solid #999}
}
"""

CSS = (CSS.replace("CODE_BG_HEX", CODE_BG).replace("CODE_INK_HEX", CODE_INK)
       .replace("GUIDE_HEX", GUIDE).replace("GUIDE_WIDTH", GUIDE_WIDTH)
       .replace("CODE_COLOR_RULES", " ".join("pre.py .%s{color:%s}" % kv for kv in CODE_COLORS.items())))

JS = """
document.addEventListener('click', function(e){
  var b = e.target.closest('button.rev');
  if(!b) return;
  var t = document.getElementById(b.getAttribute('data-target'));
  if(!t) return;
  var open = t.classList.toggle('open');
  b.setAttribute('aria-expanded', open ? 'true' : 'false');
  b.textContent = open ? b.getAttribute('data-hide') : b.getAttribute('data-show');
});
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Bricolage+Grotesque:opsz,wght@12..96,400..800&'
         'family=DM+Sans:wght@400;500;700&'
         'family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">')

# ------------------------------------------------- added for the robot and the field
CSS += """
.figwrap{overflow-x:auto; margin:0 0 6px}
svg.fig{display:block; width:100%; min-width:560px; height:auto}
.figcap{font-size:15.5px; color:var(--ink-soft); margin:0 0 16px}
.outsrc{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.06em;
  color:var(--green-ink); margin:-2px 0 7px; font-weight:700;
}
.setup{border-left:6px solid var(--teal); padding:2px 0 2px 14px; margin:0 0 16px; font-weight:700}
td.fill input{
  width:100%; min-width:90px; border:0; border-bottom:2px solid #B9AF96; background:transparent;
  font:inherit; color:var(--ink); padding:4px 2px;
}
td.fill input:focus{outline:3px solid var(--ochre-line); outline-offset:1px}
ul.checklist{list-style:none; padding-left:0}
ul.checklist li{padding-left:34px; position:relative}
ul.checklist li::before{
  content:""; position:absolute; left:0; top:4px; width:20px; height:20px;
  border:3px solid var(--teal); border-radius:3px; background:#FFFDF7;
}
table.strip td:last-child,table.strip th:last-child{min-width:230px}
table.strip pre{margin:0}
td.mono,th.mono{font-family:'JetBrains Mono',monospace; font-weight:700}
@media print{ td.fill input{border-bottom:1px solid #666} }
"""

def page(title, body, hub_label="Course home", head_extra=""):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + html.escape(title) + '</title>\n'
        + FONTS + '\n<style>' + CSS + '</style>\n' + head_extra + '</head>\n<body>\n'
        + body +
        '\n<script>' + JS + '</script>\n</body>\n</html>\n'
    )


def link(slug):
    return slug + ".html?v=" + VERSION


def code_block(code, context=None):
    """A block of Python, colored the way VS Code colors it.

    context is the whole program when code is only the part being added, so a name
    is colored by what it is in the whole program. Output boxes (out_block) and the
    expected/got sheets stay plain: they are not code.
    """
    return '<pre class="py"><code>' + indent_guides(highlight(code, context)) + '</code></pre>'


def indent_guides(colored):
    """Put each four-space step of indentation in its own guide span.

    colored is code that hl.py has colored, one line of code per line of text. Each
    step's four spaces go inside <span class="ig">, which the CSS draws as a thick
    bar down its left edge: the indent guides VS Code shows. A blank
    line inside an indented block gets empty guide spans, as many steps as the lines
    above and below it share, so the bars run through it unbroken the way they do in
    VS Code. The spaces stay spaces and nothing is added to the text, so code copied
    from a page pastes with its indentation as it was.
    """
    lines = colored.split("\n")
    steps = [(len(ln) - len(ln.lstrip(" "))) // 4 if ln.strip() else None for ln in lines]
    out = []
    for i, ln in enumerate(lines):
        n = steps[i]
        if n is None:
            above = next((s for s in reversed(steps[:i]) if s is not None), 0)
            below = next((s for s in steps[i + 1:] if s is not None), 0)
            out.append('<span class="ig"></span>' * min(above, below) + ln)
        else:
            out.append('<span class="ig">    </span>' * n + ln[4 * n:])
    return "\n".join(out)


def strip_block(text, width=24):
    """The ledger card's reference strip: code in the left column, a plain gloss in the right.

    Only the code column is colored. The gloss is English, so its words stay in ink
    rather than being read as keywords.
    """
    lines = []
    for ln in text.split("\n"):
        code, gloss = ln[:width], ln[width:]
        lines.append(highlight(code) + html.escape(gloss, quote=False))
    return '<pre class="py"><code>' + "\n".join(lines) + '</code></pre>'


def out_block(text, label="What actually happens"):
    return ('<p class="outlabel">' + label + '</p><pre class="out">'
            + html.escape(text) + '</pre>')


def nest_hints(idx, hints, inner, prefix="-hint", word="Hint"):
    """Wrap inner (a button and its block) in hints that open one inside the next.

    Hint 2's button sits inside hint 1's box, hint 3's inside hint 2's, and inner,
    which is usually the button that shows the answer, sits inside the last hint. So
    the hints come out in order, and the answer cannot be opened before the hints.
    With one hint, its button reads "Show a hint" rather than "Hint 1".
    """
    if not hints:
        return inner
    if isinstance(hints, str):
        hints = [hints]
    for n in range(len(hints), 0, -1):
        hid = idx + prefix + str(n)
        low = word.lower()
        if len(hints) == 1:
            show, hide = "Show a " + low, "Hide the " + low
        else:
            show, hide = word + " " + str(n), "Hide " + low + " " + str(n)
        inner = ('<button class="rev hint" data-target="' + hid + '" aria-controls="' + hid + '" '
                 'aria-expanded="false" data-show="' + show + '" data-hide="' + hide + '">'
                 + show + '</button>'
                 '<div class="ans" id="' + hid + '">' + hint_html(hints[n - 1]) + inner + '</div>')
    return '<div class="hints">' + inner + '</div>'


def hint_html(h):
    """A hint is a string of HTML, or a dict with "text" and/or "code"."""
    if isinstance(h, str):
        return '<p>' + h + '</p>'
    out = ""
    if h.get("text"):
        out += '<p>' + h["text"] + '</p>'
    if h.get("code"):
        out += code_block(h["code"])
    return out


def toggle(idx, show, hide, inner):
    """One button that opens one block."""
    return ('<button class="rev" data-target="' + idx + '" aria-controls="' + idx + '" '
            'aria-expanded="false" data-show="' + show + '" data-hide="' + hide + '">'
            + show + '</button><div class="ans" id="' + idx + '">' + inner + '</div>')


def ladder(idx, question, hints, answer_html, label="What goes next?",
           show="Show the lines", hide="Hide the lines"):
    """A question for the room, with hints that open one inside the next.

    Hint 2's button sits inside hint 1's box, hint 3's inside hint 2's, and the button
    that shows the answer sits inside the last hint, so the hints come out in order and
    nothing below the question is on screen until it is asked for.
    """
    inner = toggle(idx + "-lines", show, hide, answer_html)
    return ('<div class="predict ladder"><p class="q"><b>' + label + '</b> ' + question + '</p>'
            + nest_hints(idx, hints, inner, prefix="-h") + '</div>')


def check_step(step, code, tag):
    """A step's line must be in the chunk's program, at the line number its label names.

    The label is "Line 7", "Lines 18, 21, and 24", or "Lines 9 to 13"; every number in
    it is checked against the program, so a label cannot drift from the code.
    """
    lines = code.split("\n")
    wanted = [ln for ln in step["line"].split("\n") if ln.strip()]
    for ln in wanted:
        assert ln in lines, "%s: step line not in the program: %r" % (tag, ln)
    label = step["label"]
    m = re.fullmatch(r"Lines (\d+) to (\d+)", label)
    if m:
        nums = list(range(int(m.group(1)), int(m.group(2)) + 1))
        assert [lines[n - 1] for n in nums] == wanted, "%s: %s does not match" % (tag, label)
        return
    nums = [int(x) for x in re.findall(r"\d+", label)]
    assert nums, "%s: step label needs a line number: %r" % (tag, label)
    for n in nums:
        assert lines[n - 1] in wanted, "%s: %s names line %d, which is %r" % (tag, label, n, lines[n - 1])


def line_ladders(tag, program, steps, start=None, whole="Show the whole program"):
    """One question per new line of a program, each behind a ladder of hints.

    The program so far sits behind a button, then each step is a What goes next?
    ladder whose last button shows the line, then the whole program sits behind a
    button. Every step's line is checked against the program at the line its label
    names, so a label cannot drift from the code.
    """
    out = []
    if start:
        out.append('<div class="sofar">' + toggle(tag + "-start", "Show the program so far",
                   "Hide the program so far", code_block(start)) + '</div>')
    for j, st in enumerate(steps):
        check_step(st, program, tag)
        sid = tag + "-l" + str(j + 1)
        ans = code_block(st["line"], context=program)
        if st.get("note"):
            ans += '<p>' + st["note"] + '</p>'
        low = st["label"][0].lower() + st["label"][1:]
        out.append(ladder(sid, st["q"], st["hints"], ans,
                          label=st["label"] + ". What goes next?",
                          show="Show " + low, hide="Hide " + low))
    out.append('<div class="whole">' + toggle(tag + "-whole", whole,
               whole.replace("Show", "Hide", 1), code_block(program)) + '</div>')
    return "".join(out)


def reveal(idx, question, answer, qlabel="Predict", extra="",
           show="Show the answer", hide="Hide the answer", hints=None):
    inner = toggle(idx, show, hide, extra + '<p>' + answer + '</p>')
    return ('<div class="predict"><p class="q">' + qlabel + ': ' + question + '</p>'
            + nest_hints(idx, hints, inner) + '</div>')


# ------------------------------------------------------------------ the run log
# runs.csv holds every run on the reference robot. A measured result is printed only
# when the log holds RUNS_NEEDED runs for it, and only runs logged against the current
# text of the program count, so a result cannot outlive a change to its program.

def program_id(code):
    """A short fingerprint of a program's text. It changes when the program changes."""
    return hashlib.sha1(code.encode("utf-8")).hexdigest()[:8]


def load_runs():
    path = os.path.join(ROOT, "runs.csv")
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


RUNS = load_runs()
PENDING = []       # (session, key, program id) for results with too few logged runs


def runs_for(session, key, code):
    pid = program_id(code)
    return [r for r in RUNS if r["session"] == str(session) and r["chunk"] == key
            and r["program_id"] == pid]


def result_block(text, label, source):
    """A result box. label says what it is, source says where it came from."""
    return ('<p class="outlabel">' + label + '</p><p class="outsrc">' + source + '</p>'
            '<pre class="out">' + html.escape(text) + '</pre>')


def measured_block(session, key, code, unit):
    """The measured result for a program, from the run log, or nothing yet."""
    rows = runs_for(session, key, code)
    if len(rows) < RUNS_NEEDED:
        PENDING.append((session, key, program_id(code), len(rows)))
        return ""
    vals = [r["result"] for r in rows]
    try:
        nums = [float(v) for v in vals]
        lo, hi = min(nums), max(nums)
        text = ("%g to %g %s" % (lo, hi, unit)) if lo != hi else ("%g %s" % (lo, unit))
    except ValueError:
        text = ", ".join(sorted(set(vals)))
    return result_block(text, "What actually happens",
                        "On the reference robot, %d runs" % len(rows))


def paras(items):
    return "".join('<p>' + x + '</p>' for x in items)


def reveal_block(idx, question, answer_html, qlabel="Predict", hints=None,
                 show="Run it first, then check here", hide="Hide"):
    """A question with nested hints, then one button that shows the whole answer."""
    inner = toggle(idx, show, hide, answer_html)
    return ('<div class="predict"><p class="q">' + qlabel + ': ' + question + '</p>'
            + nest_hints(idx, hints, inner) + '</div>')


def blank(label):
    return '<td class="fill"><input type="text" aria-label="' + html.escape(label) + '"></td>'


def standards_table(codes):
    rows = ""
    for c in codes:
        s = STANDARDS[c]
        ids = "<br>".join(g + ": <code>" + u + "</code>" for g, u in s["uuids"])
        st = html.escape(s["statement"])
        if s["deviation"]:
            st += '<br><i>' + html.escape(s["deviation"]) + '</i>'
        rows += ('<tr><td><code>' + c + '</code></td><td>' + s["framework"] + '</td><td>'
                 + s["grades"] + '</td><td>' + st + '</td><td>' + ids + '</td><td>'
                 + html.escape(s["why"]) + '</td></tr>')
    return ('<table class="std"><tr><th>Code</th><th>Framework</th><th>Grade</th>'
            '<th>Statement, as retrieved</th><th>CASE identifier</th><th>Mapped because</th></tr>'
            + rows + '</table>')


def footer():
    return ('<footer><div class="wrap">'
            '<p>' + COURSE + ', grades 4 and 5. Part 1 is sessions 1 to 4. Part 2 is sessions 5 '
            'to 8, for a class that continues. The class robot is LEGO\'s '
            'Advanced Driving Base. LEGO\'s building instructions are linked, not copied.</p>'
            '<p>Mapped to the New York State P-12 Science Learning Standards and the New York '
            'Next Generation Mathematics Learning Standards. Codes retrieved through the '
            + CONNECTOR + ' on ' + RESOLVED_ON + '. <a href="' + link(STDMAP) + '">Full '
            'standards map</a> &middot; <a href="' + link(CONSTRAINTS) + '">Course '
            'constraints, published ' + PUBLISHED + '</a></p>'
            '<p>LEGO and SPIKE are trademarks of the LEGO Group, which does not sponsor or '
            'endorse this course.</p></div></footer>')


# --------------------------------------------------------------- session pages

def sheet_table(head, rows, tag):
    """An expected and measured sheet. A cell given as text is printed; the rest are blanks."""
    out = ['<table><tr>' + "".join('<th>' + x + '</th>' for x in head) + '</tr>']
    for r, row in enumerate(rows):
        cells = list(row) + [None] * (len(head) - len(row))
        out.append('<tr>')
        for c, cell in enumerate(cells):
            if cell:
                out.append('<td' + (' class="mono"' if cell.isdigit() or len(cell) == 1 else '') + '>' + cell + '</td>')
            else:
                out.append(blank(re.sub(r"<[^>]+>", "", head[c]) + ", row " + str(r + 1)))
        out.append('</tr>')
    out.append('</table>')
    return "".join(out)


def session_programs(s):
    """Every program whose result is measured on the reference robot: (key, code)."""
    return [(c["key"], c["code"]) for c in s["chunks"]] + [("mission", s["brief"]["code"])]


def render_session(s, prev_s, next_s):
    n = s["num"]
    first_code = s["chunks"][0]["code"]
    b = ['<header class="top"><div class="wrap">']
    part2 = s.get("part", 1) == 2
    b.append('<p class="eyebrow">' + COURSE + ' &middot; Grades 4 and 5 &middot; '
             + ('Part 2 &middot; Session ' + str(n) + ' of ' + str(len(SESSIONS)) if part2
                else 'Part 1 &middot; Session ' + str(n) + ' of ' + str(len(PART1))) + '</p>')
    b.append('<h1>' + html.escape(s["title"]) + '</h1>')
    b.append('<p class="sub">' + html.escape(s["subtitle"]) + '</p>')
    b.append('<div class="dates">')
    b.append('<span class="pill"><b>Date</b> to be set</span>')
    b.append('<span class="pill"><b>Length</b> 90 minutes</span>')
    b.append('<span class="pill"><b>Team</b> 4 builders, 1 robot</span>')
    b.append('<span class="pill"><b>New</b> ' + (str(len(s["new"])) + ' items' if s["new"]
                                                else 'nothing new') + '</span>')
    b.append('</div></div></header>')
    b.append('<main><div class="wrap">')

    b.append('<section><h2>What is new today</h2><p>' + s["new_text"] + '</p>')
    b.append('<p><b>Deliberately re-used:</b> ' + s["reuse"] + '</p>')
    b.append('<p><a href="' + link(ROBOT) + '">Robot page</a> &middot; <a href="' + link(FIELD)
             + '">Field page</a></p></section>')

    # ---- the build (session 1 only: it stands where the opener stands later)
    bd = s.get("build")
    if bd:
        b.append('<section class="opener"><p class="chunk-no">Build &middot; '
                 + str(bd["minutes"]) + ' minutes</p><h2>' + html.escape(bd["title"]) + '</h2>')
        b.append(paras(bd["intro"]))
        b.append('<p>' + bd["words"] + '</p>')
        b.append('<table><tr><th>Builder</th><th>Building book</th><th>Part of the robot</th></tr>')
        for num, part, url in robot.BOOKS:
            who = "Builder " + str(num) if num < 5 else "The whole team"
            b.append('<tr><td>' + who + '</td><td><a href="' + html.escape(url) + '">Book '
                     + str(num) + ' of 5</a></td><td>' + part + '</td></tr>')
        b.append('</table>')
        b.append('<p class="note">The building books are LEGO\'s own files. Each link opens a '
                 'PDF on LEGO\'s site.</p>')
        b.append('<ol>' + "".join('<li>' + x + '</li>' for x in bd["steps"]) + '</ol>')
        b.append('<h3>Your port map</h3><p>' + bd["portmap_intro"] + '</p>')
        b.append('<table><tr><th>Port</th><th>What is plugged in</th><th>Where it is on the robot</th></tr>')
        for letter in "ABCDEF":
            b.append('<tr><td class="mono">' + letter + '</td>' + blank("Port " + letter + ", what is plugged in")
                     + blank("Port " + letter + ", where it is on the robot") + '</tr>')
        b.append('</table>')
        b.append('<div class="predict"><p class="q">Check: which two ports hold the motors that '
                 'turn the wheels?</p>'
                 + toggle("s%d-portmap" % n, "Fill in your port map first, then check here", "Hide",
                          paras(bd["portmap_check"])) + '</div>')
        b.append('</section>')

    # ---- robot check
    ck = s["check"]
    b.append('<section class="opener"><p class="chunk-no">Robot check &middot; '
             + str(ck["minutes"]) + ' minutes</p><h2>Before the first run</h2>')
    b.append('<ul class="checklist">' + "".join('<li>' + x + '</li>' for x in ck["items"]) + '</ul>')
    b.append('<p>' + ck["after"] + '</p></section>')

    # ---- opener
    op = s.get("opener")
    if op:
        b.append('<section class="opener"><p class="chunk-no">Opener &middot; '
                 + str(op["minutes"]) + ' minutes</p><h2>' + html.escape(op["title"]) + '</h2>')
        b.append('<p>' + op["body"] + '</p>')
        for i, (q, a) in enumerate(op["questions"]):
            b.append(reveal_block("s%d-op%d" % (n, i + 1), q, paras(a), "Question",
                                  show="Show the answer", hide="Hide the answer"))
        b.append('</section>')

    # ---- chunks
    for i, ch in enumerate(s["chunks"]):
        tag = "s%d-c%d" % (n, i + 1)
        b.append('<section class="chunk"><p class="chunk-no">Chunk ' + str(i + 1)
                 + ' of ' + str(len(s["chunks"])) + '</p>')
        b.append('<h2>' + html.escape(ch["title"]) + '</h2>')
        b.append(paras(ch["teach"]))
        if ch.get("steps"):
            b.append(line_ladders(tag, ch["code"], ch["steps"], ch["start"]))
        else:
            b.append(code_block(ch["code"]))
        if ch.get("parts"):
            b.append('<h3>' + ch["parts_title"] + '</h3><table><tr><th>Part</th>'
                     '<th>What it says</th></tr>')
            for part, says in ch["parts"]:
                b.append('<tr><td><code>' + html.escape(part) + '</code></td><td>' + says + '</td></tr>')
            b.append('</table>')
        if ch.get("where"):
            b.append('<p class="note">' + ch["where"] + '</p>')
        b.append(ch["figure"])
        b.append('<p class="setup">' + ch["setup"] + '</p>')
        ans = result_block(ch["computed"], "What the page works out", "Computed, not measured")
        ans += measured_block(n, ch["key"], ch["code"], ch["unit"])
        ans += paras(ch["reveal"]) + '<p>' + ch["measure"] + '</p>'
        b.append(reveal_block(tag, ch["predict"], ans, hints=ch.get("hints"),
                              show=ch.get("show", "Run it first, then check here")))
        sh = ch.get("sheet")
        if sh:
            b.append('<h3>' + sh["title"] + '</h3><p>' + sh["intro"] + '</p>'
                     + sheet_table(sh["head"], sh["rows"], tag))
        b.append('</section>')

    # ---- hinge
    h = s["hinge"]
    b.append('<section class="hinge"><p class="chunk-no">Hinge question &middot; from '
             'today\'s chunks</p><h2>Before the mission</h2>')
    b.append(code_block(h["code"], context=h.get("context", first_code)))
    b.append(reveal_block("s%d-hinge" % n, h["q"], paras(h["a"]), "Question",
                          show="Show the answer", hide="Hide the answer"))
    b.append('</section>')

    # ---- mission
    br = s["brief"]
    b.append('<section class="brief"><p class="chunk-no">Mission &middot; '
             + str(br["minutes"]) + ' minutes</p><h2>' + html.escape(br["title"]) + '</h2>')
    b.append(paras(br["intro"]))
    b.append(br["figure"])
    b.append('<table>' + "".join('<tr><th>' + k + '</th><td>' + v + '</td></tr>'
                                for k, v in br["values"]) + '</table>')
    if br.get("plan_head"):
        b.append('<h3>' + br.get("plan_title", "Two plans") + '</h3><p>'
                 + br.get("plan_intro", "Write both plans before you type anything.") + '</p>'
                 + sheet_table(br["plan_head"], br["plan_rows"], "plan"))
    b.append('<p>' + br["code_note"] + '</p>')
    b.append(code_block(br["code"]))
    b.append('<ol>' + "".join('<li>' + x + '</li>' for x in br["steps"]) + '</ol>')
    b.append('<h3>Expected and measured</h3><p>Fill in the Expected column before each run. '
             'Fill in the rest of the row after it. One change per run.</p>')
    b.append(sheet_table(br["sheet_head"], br["sheet_rows"], "mission"))
    # the mission's runs are logged too; its result shows in the teacher panel only
    measured_block(n, "mission", br["code"], "runs inside the target")
    b.append('</section>')

    # ---- exits
    ex = s["exits"]
    b.append('<section><h2>Where you can stop</h2>'
             '<p>All three are real places to stop. Nobody is behind for finishing at the floor.</p>'
             '<div class="exits">')
    for k in ("floor", "middle", "stretch"):
        b.append('<div class="exit ' + k + '"><p class="tag">' + k.capitalize() + '</p><p>'
                 + ex[k] + '</p></div>')
    b.append('</div></section>')

    dm = s.get("demo")
    if dm:
        b.append('<section class="brief"><p class="chunk-no">Demo &middot; ' + str(dm["minutes"])
                 + ' minutes</p><h2>' + html.escape(dm["title"]) + '</h2>' + paras(dm["body"])
                 + '<ol>' + "".join('<li>' + x + '</li>' for x in dm["steps"]) + '</ol></section>')

    pv = s.get("preview")
    if pv:
        b.append('<section class="hinge"><p class="chunk-no">Looking ahead &middot; '
                 + str(pv["minutes"]) + ' minutes</p><h2>' + html.escape(pv["title"]) + '</h2>'
                 + paras(pv["body"]) + '</section>')

    b.append('<section><h2>Ledger card</h2><p>Copy this onto your card.</p>'
             + code_block(s["ledger_code"], context=s.get("ledger_context", first_code)) + '<p>'
             + s["ledger"] + '</p><p>' + s["stamp"] + '</p><p><a href="' + link(LEDGER)
             + '">Open the ledger card</a></p></section>')

    # ---- teacher panel
    t = s["teacher"]
    b.append('<details class="teacher"><summary>Teacher panel</summary>')
    b.append('<h3>Before class</h3><ul>' + "".join('<li>' + x + '</li>' for x in t["before"]) + '</ul>')
    b.append('<h3>Timing, 90 minutes</h3><ul>')
    for clock, what, mins in t["timing"]:
        b.append('<li>' + clock + ' ' + html.escape(what) + ', ' + str(mins) + ' min</li>')
    b.append('</ul><p class="note">' + t["pacing"] + '</p>')
    if bd:
        b.append('<p class="note">Locked exception: session 1 has no opener, because there is no '
                 'earlier session to bring back. That time goes to building the robot.</p>')
    b.append('<h3>What you will see, and what to do</h3>'
             '<table><tr><th>In the room</th><th>Redirect</th></tr>')
    for a, r in t["misconceptions"]:
        b.append('<tr><td>' + a + '</td><td>' + r + '</td></tr>')
    b.append('</table>')
    b.append('<h3>Mapped to</h3>' + standards_table(t["standards"]))
    b.append('<h3>If time runs out</h3><p>' + t["routing"] + '</p>')
    b.append('<h3>Deliberate</h3><p>' + t["deliberate"] + '</p>')
    b.append('<h3>Files</h3><p><a href="' + link(ROBOT) + '">Robot page</a> &middot; '
             '<a href="' + link(FIELD) + '">Field page</a> &middot; '
             '<a href="' + link(CONSTRAINTS) + '">Course constraints</a> &middot; '
             '<a href="runs.csv?v=' + VERSION + '">Run log, runs.csv</a>'
             + (' &middot; <a href="' + robot.LEGO_LESSON + '">LEGO\'s lesson this session is '
                'adapted from</a>' if bd else '') + '</p>')
    b.append('<p>Log each run on the reference robot in <code>runs.csv</code> with the '
             'program id below, then rebuild. A run counts only while its program id matches '
             'the program on this page.</p>')
    b.append('<table><tr><th>Result</th><th>Program id</th><th>Runs logged</th><th>On the page?</th></tr>')
    for key, code in session_programs(s):
        got = len(runs_for(n, key, code))
        b.append('<tr><td>' + key + '</td><td class="mono">' + program_id(code) + '</td><td>'
                 + str(got) + ' of ' + str(RUNS_NEEDED) + '</td><td>'
                 + ('Yes' if got >= RUNS_NEEDED else 'Not yet') + '</td></tr>')
    b.append('</table></details>')
    b.append('</div></main>')

    b.append('<nav class="pager">')
    b.append('<a href="' + link(prev_s["slug"]) + '">&larr; Session ' + str(prev_s["num"]) + '</a>'
             if prev_s else '<span></span>')
    b.append('<a href="' + link(HUB) + '">Course home</a>')
    b.append('<a href="' + link(next_s["slug"]) + '">Session ' + str(next_s["num"]) + ' &rarr;</a>'
             if next_s else '<span></span>')
    b.append('</nav>')
    b.append(footer())
    return page(s["title"] + " | " + COURSE, "".join(b))


def simple_page(eyebrow, title, sub, body, teacher=""):
    b = ['<header class="top"><div class="wrap">',
         '<p class="eyebrow">' + eyebrow + '</p>', '<h1>' + title + '</h1>',
         '<p class="sub">' + sub + '</p>', '</div></header><main><div class="wrap">',
         body, teacher, '</div></main>',
         '<nav class="pager noprint"><span></span><a href="' + link(HUB) + '">Course home</a><span></span></nav>',
         footer()]
    return page(title + " | " + COURSE, "".join(b))


# -------------------------------------------------------------------- hub page

def render_hub():
    def listing(group):
        out = ['<ul class="sessionlist">']
        for s in group:
            new = (", ".join(s["new"]) if s["new"] else "nothing new")
            out.append('<li><span class="n">' + str(s["num"]) + '</span><span><a href="'
                       + link(s["slug"]) + '">' + html.escape(s["title"]) + '</a><span class="meta">'
                       '90 minutes &middot; date to be set &middot; new: ' + html.escape(new)
                       + '</span></span></li>')
        out.append('</ul>')
        return "".join(out)

    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">LEGO SPIKE Prime &middot; Python &middot; Grades 4 and 5</p>')
    b.append('<h1>' + COURSE + '</h1>')
    b.append('<p class="sub">Sessions of ninety minutes. You read a robot program, say '
             'what the robot will do, and then run it.</p>')
    b.append('<div class="dates"><span class="pill"><b>Part 1</b> sessions 1 to 4</span>'
             '<span class="pill"><b>Part 2</b> sessions 5 to 8</span>'
             '<span class="pill"><b>Dates</b> to be set</span>'
             '<span class="pill"><b>Teams</b> 4 builders, 1 robot</span>'
             '<span class="pill"><b>Demo days</b> sessions 4 and 8</span></div>')
    b.append('</div></header><main><div class="wrap">')
    b.append('<section><h2>Part 1: sessions 1 to 4</h2><p>Build the robot, move it, turn it, '
             'stop it at a line, and make a delivery. Session 4 ends with a demo for '
             'families.</p>' + listing(PART1) + '</section>')
    b.append('<section><h2>Part 2: sessions 5 to 8</h2><p>For a class that finishes part 1 '
             'early or keeps going. The hub beeps and shows numbers, the robot measures its '
             'own turns and follows a line, and each team writes its own mission. Session 8 '
             'ends with a second demo.</p>' + listing(PART2) + '</section>')
    b.append('<section><h2>How a session runs</h2><div class="grid2">'
             '<div class="card"><h3>Robot check, then opener</h3><p>A week passes between '
             'sessions. Each session starts by checking the robot against the robot page, '
             'then brings back last week\'s ideas with a few questions.</p></div>'
             '<div class="card"><h3>Predict, then run</h3><p>Each chunk shows a program and '
             'where the robot starts. You say what the robot will do. Then you run the '
             'program and check.</p></div>'
             '<div class="card"><h3>One change per run</h3><p>When you test, change one '
             'thing, run the program, and write down what the robot did. Then you know what '
             'that one change does.</p></div>'
             '<div class="card"><h3>Three places to stop</h3><p>Every mission has a floor, a '
             'middle, and a stretch exit. All three are a finish.</p></div></div></section>')
    b.append('<section><h2>Everything else</h2><div class="toolbar">'
             '<a class="btn" href="' + link(ROBOT) + '">Robot page</a>'
             '<a class="btn" href="' + link(FIELD) + '">Field page</a>'
             '<a class="btn quiet" href="' + link(LEDGER) + '">Ledger card</a>'
             '<a class="btn quiet" href="' + link(CONSTRAINTS) + '">Course constraints</a>'
             '<a class="btn quiet" href="' + link(STDMAP) + '">Standards map</a>'
             '</div></section>')
    b.append('</div></main>' + footer())
    return page(COURSE, "".join(b))


# ------------------------------------------------------------------ robot page

def render_robot():
    b = []
    b.append('<section><h2>Building instructions</h2><p>The robot is built from five of '
             'LEGO\'s building books. It needs the SPIKE Prime set and the SPIKE Prime '
             'Expansion Set.</p><table><tr><th>Book</th><th>Part of the robot</th></tr>')
    for num, part, url in robot.BOOKS:
        b.append('<tr><td><a href="' + html.escape(url) + '">Book ' + str(num)
                 + ' of 5</a></td><td>' + part + '</td></tr>')
    b.append('</table><p class="note">These are LEGO\'s own files, linked from '
             '<a href="' + robot.LEGO_INDEX + '">LEGO\'s building instructions page</a>. '
             'They are not copied here.</p></section>')
    b.append('<section><h2>Port map</h2><p>The port map is the same in every session. Left and '
             'right are the robot\'s left and right, as if you were sitting in the robot '
             'facing forward.</p>')
    b.append('<table><tr><th>Port</th><th>What is plugged in</th><th>Where it is</th></tr>')
    for letter, what, where, _ in robot.PORT_MAP:
        b.append('<tr><td class="mono">' + letter + '</td><td>' + what + '</td><td>' + where + '</td></tr>')
    b.append('</table>')
    b.append(robot.turn_figure(caption="The robot from above: its left, its right, and the "
                               "two wheels the programs turn."))
    b.append('</section>')
    b.append('<section><h2>The wheel</h2><p>One full turn of a drive motor is 360 degrees of '
             'motor turn. It turns the wheel one full turn, and the robot moves about '
             + str(wheel.whole_cm(360)) + ' cm.</p>')
    b.append('<table><tr><th>Degrees of motor turn</th><th>Full turns of the wheel</th>'
             '<th>The robot moves about</th></tr>')
    for deg in (180, 360, 720, 1080):
        t = wheel.turns(deg)
        b.append('<tr><td class="mono">' + str(deg) + '</td><td>'
                 + ("half a turn" if t == 0.5 else ("%d" % t)) + '</td><td>'
                 + str(wheel.whole_cm(deg)) + ' cm</td></tr>')
    b.append('</table><p class="note">Computed by the build from the wheel, not measured. '
             'Whole centimetres.</p></section>')
    t = ['<details class="teacher"><summary>Teacher panel</summary>'
         '<h3>Where each fact on this page comes from</h3>'
         '<table><tr><th>Port</th><th>Source</th></tr>']
    for letter, what, where, src in robot.PORT_MAP:
        t.append('<tr><td class="mono">' + letter + '</td><td>' + src + '</td></tr>')
    t.append('</table><p>' + robot.WHEEL_NOTE + ' <a href="' + robot.LEGO_PYTHON
             + '">LEGO\'s Python programs (PDF)</a>.</p>'
             '<p>Before the first session, build the reference robot and check every row of '
             'the port map against it. Sessions 1 and 2 use only ports A and E. Sessions 3 '
             'and 4 use one colour sensor; their programs name port B as a first try, and '
             'each team replaces it with the letter on its own robot.</p>'
             '<p>LEGO stopped selling SPIKE Prime on 30 June 2026 and supports the SPIKE App '
             'until 30 June 2031 (<a href="' + robot.LEGO_UPDATE + '">LEGO Education</a>). '
             'Keep a spare of every part this robot needs, and an unpublished copy of the '
             'five building books.</p></details>')
    return simple_page(COURSE + ' &middot; The class robot', 'The Advanced Driving Base',
                       'The robot, its ports, and its wheel.', "".join(b), "".join(t))


# ------------------------------------------------------------------ field page

def render_field():
    one, side = wheel.whole_cm(360), wheel.nearest5(wheel.cm(720))
    b = []
    b.append('<section><h2>The rules of the field</h2><ul>'
             '<li>A pale, plain, flat floor or table. Every line is black tape.</li>'
             '<li>The robot starts behind the start line with its front edge on the line, '
             'facing forward. It starts there on every run.</li>'
             '<li>Every distance is in cm, measured with a ruler from the start line to the '
             'robot\'s front edge.</li>'
             '<li>A wheel marker is a small piece of tape on the floor beside a wheel, put '
             'down before the first run.</li></ul></section>')
    b.append('<section><h2>Sessions 1 and 3: the lane</h2><p>A start line and a far line. The '
             'far line is ' + str(robot.FAR_CM) + ' cm from the start line. In session 3 it is '
             'lifted and moved to 40 cm and 70 cm as well.</p>'
             + robot.field_figure(far=True, markers=True, caption="The lane from above, drawn "
                                  "to scale, with the far line at %d cm." % robot.FAR_CM)
             + '</section>')
    b.append('<section><h2>Session 2: the turn cross</h2><p>Two strips of black tape that '
             'cross at a right angle, like a plus sign. The robot starts over the middle, '
             'facing along strip 1. After a quarter turn it faces along strip 2.</p>'
             + robot.cross_figure(caption="The turn cross from above.") + '</section>')
    b.append('<section><h2>Session 2: the square</h2><p>The robot drives four sides and four '
             'quarter turns to its right. In chunk 3 each side is about ' + str(one)
             + ' cm. In the mission each side is about ' + str(side) + ' cm and a crate no more '
             'than ' + str(robot.CRATE_CM) + ' cm across sits in the middle.</p>'
             + robot.square_figure(side, crate=True, caption="The mission square from above, "
                                   "drawn to scale.") + '</section>')
    b.append('<section><h2>Session 4: the delivery run</h2><p>The lane, with the far line '
             'somewhere from ' + str(robot.FAR_MIN) + ' to ' + str(robot.FAR_MAX) + ' cm from '
             'the start line, and a drop zone: a square of tape ' + str(robot.DROP_CM)
             + ' cm on each side, to the right of the far line.</p>'
             + robot.delivery_figure(one, caption="The delivery run from above, drawn to scale "
                                     "with the far line at %d cm." % robot.FAR_CM) + '</section>')
    b.append('<section><h2>Session 5: the shelf lines</h2><p>A start line and '
             + str(robot.SHELVES) + ' shelf lines, ' + str(robot.SHELF_GAP_CM) + ' cm apart.</p>'
             + robot.shelves_figure(caption="The shelf lines from above, drawn to scale.")
             + '</section>')
    b.append('<section><h2>Session 6: the turn cross and the square</h2><p>The same turn '
             'cross and the same square as session 2, with the crate in the middle.</p></section>')
    b.append('<section><h2>Sessions 7 and 8: the line and its stop bar</h2><p>A line of black '
             'tape ' + str(robot.TRACK_CM) + ' cm long, ending at a stop bar: a strip of tape '
             '30 cm long laid across the end of the line. The mission line has one gentle '
             'bend.</p>' + robot.track_figure(caption="The straight line from above, drawn to scale.")
             + robot.track_figure(bend=True, caption="The line with a bend, from above, drawn "
                                  "to scale.") + '</section>')
    t = ('<details class="teacher"><summary>Teacher panel</summary>'
         '<p>The drop zone is laid from the reference robot: run session 4\'s chunk 1 program '
         'with the far line at ' + str(robot.FAR_CM) + ' cm and centre the square of tape on '
         'where the wheels end. Its place in the figure is a sketch of that, not a '
         'measurement.</p><p>The robot outline in every figure is not to scale. The lines, '
         'the square, and the scale bars are.</p></details>')
    return simple_page(COURSE + ' &middot; The test field', 'The test field',
                       'Every line, its distance in cm, and where the robot starts.',
                       "".join(b), t)


# ------------------------------------------------------------- constraints page

FIRST_TAUGHT = [
    ("<code>from hub import port</code>, <code>import motor_pair</code>, <code>import runloop</code>",
     1, "The three tool lines at the top of every program."),
    ("<code>async def main():</code> and <code>runloop.run(main())</code>", 1,
     "The frame every program sits in. Handed over working and not explained."),
    ("<code>motor_pair.pair</code>", 1, "Says which two motors turn the wheels."),
    ("<code>await motor_pair.move_for_degrees</code>", 1, "One move, counted in degrees of motor turn."),
    ("A minus sign on the first number", 1, "Backward."),
    ("Steering: 0, 100, and -100", 1, "Straight, turn right on the spot, turn left on the spot."),
    ("<code>#</code> notes", 1, "A line for the reader. The hub skips it."),
    ("A name in capitals for a number", 2, "Every number the behaviour depends on, set once at the top."),
    ("<code>for count in range(4):</code>", 2, "Arrives after the square is written the long way."),
    ("<code>import color_sensor</code>, <code>color_sensor.reflection</code>", 3, "Reflected light, 0 to 100."),
    ("<code>print</code>", 3, "Shows one reading in the console."),
    ("<code>motor_pair.move</code>, <code>await runloop.until(lambda: ...)</code>, <code>motor_pair.stop</code>",
     3, "The one way to move until a sensor says stop. The word lambda is handed over and not explained."),
    ("<code>&lt;</code>", 3, "Is less than."),
    ("<code>sound.beep</code>, <code>light_matrix.write</code>, <code>str</code>", 5,
     "The hub reports what the robot is doing. Part 2 starts here."),
    ("<code>&gt;</code>", 5, "Is greater than. Crossing a line takes two waits."),
    ("The name <code>count</code> in a <code>for</code> line", 5, "It starts at 0."),
    ("<code>motion_sensor.reset_yaw</code>, <code>motion_sensor.tilt_angles()[0]</code>, <code>abs</code>",
     6, "A turn that ends on a measurement, in tenths of a degree of the robot's turn."),
    ("<code>await runloop.sleep_ms</code>", 6, "Wait for a set time, in thousandths of a second."),
    ("<code>velocity=100</code> and <code>velocity=150</code>", 6, "Slower moves for measured turns and line following."),
    ("<code>if</code> and <code>else</code>", 7, "Choose between two moves."),
    ("<code>while</code>", 7, "Only with a test the student can name as its stop."),
    ("The second colour sensor", 7, "The stop sensor."),
    ("<code>async def name():</code> and <code>await name()</code>", 8,
     "The students' own functions. This opens the frame handed over in session 1."),
]

NEVER_PART1 = [
    "<code>if</code>, <code>while</code>, and functions the students define. They arrive in sessions 7 and 8.",
    "The hub's speaker, light matrix, and motion sensor, and the second colour sensor. They arrive in sessions 5 to 7.",
    "Any speed other than <code>velocity=250</code>. Part 2 adds 100 and 150, and lets teams tune the speed.",
]

NEVER = [
    "Word Blocks. This course is written in Python throughout.",
    "<code>while True</code> or any loop with no stop the student can name.",
    "<code>if</code> inside <code>if</code>. One <code>if</code> may sit inside one <code>while</code>, as in the line follower.",
    "Lists, and variables that change while the program runs.",
    "A second task running at the same time.",
    "Seconds as the unit of a move. Moves are counted in degrees of motor turn or ended by a sensor.",
    "Any distance unit other than cm.",
    "The medium motors and any part not on the port map.",
]


def render_constraints():
    b = ['<section class="flag">Published ' + PUBLISHED + '. Changing anything on this page '
         'means publishing it again with a new date.</section>']
    b.append('<section><h2>1. What the course uses, and where each thing is first taught</h2>'
             '<table><tr><th>Python</th><th>Session</th><th>Why</th></tr>')
    for what, sess, why in FIRST_TAUGHT:
        b.append('<tr><td>' + what + '</td><td class="mono">' + str(sess) + '</td><td>' + why + '</td></tr>')
    b.append('</table><p>Nothing is used before the session that teaches it.</p></section>')
    b.append('<section><h2>2. What the course never uses</h2><ul>'
             + "".join('<li>' + x + '</li>' for x in NEVER) + '</ul>'
             '<h3>What part 1 leaves for part 2</h3><ul>'
             + "".join('<li>' + x + '</li>' for x in NEVER_PART1) + '</ul></section>')
    b.append('<section><h2>3. One way to do each thing</h2><p>One frame, at the top and bottom '
             'of every program:</p>'
             + code_block(SESSION01["chunks"][0]["code"])
             + '<p>One way to move until the sensor says stop:</p>'
             + code_block(SESSION03["ledger_code"], context=SESSION03["chunks"][1]["code"])
             + '<p>One start, one forward direction, one measuring point: behind the start '
             'line, front edge on the line, and every distance measured to the front edge.</p></section>')
    b.append('<section><h2>4. Standing rules</h2><ul>'
             '<li>One change per run.</li><li>Predict before you run.</li>'
             '<li>The Expected column is filled in before the run.</li>'
             '<li>The robot starts in the same place, facing forward, every run.</li>'
             '<li>Names say what they do: <code>QUARTER_TURN</code>, not <code>x</code>.</li>'
             '<li>The frame at the top and bottom of every program.</li></ul></section>')
    b.append('<section><h2>5. Locked hardware and software</h2><ul>'
             '<li>The robot: LEGO\'s Advanced Driving Base, one for each team of four, built '
             'from the SPIKE Prime set and the SPIKE Prime Expansion Set.</li>'
             '<li>The port map: port ' + robot.DRIVE_LEFT + ' left drive motor, port '
             + robot.DRIVE_RIGHT + ' right drive motor. See the robot page.</li>'
             '<li>The wheel: one full turn moves the robot about ' + str(wheel.whole_cm(360)) + ' cm.</li>'
             '<li>The field: see the field page.</li>'
             '<li>The SPIKE App, version 3, and the hub\'s software, frozen at the versions on '
             'the reference robot. Write both version numbers here when the reference robot '
             'is set up.</li></ul>'
             '<p>LEGO adds no new features to the SPIKE App after 30 June 2026 and supports it '
             'until 30 June 2031 (<a href="' + robot.LEGO_UPDATE + '">LEGO Education</a>).</p></section>')
    b.append('<section><h2>6. Locked decisions</h2><ul>'
             '<li>Part 1 is four sessions and stands on its own. Session 4 is its demo for '
             'families. Part 2 is four more, for a class that continues, and session 8 is a '
             'second demo.</li>'
             '<li>Session 1 has no opener. That time goes to building the robot.</li>'
             '<li>The final mission of part 1 is told to students in session 2.</li>'
             '<li>Machinery handed over, then opened: the frame (<code>async def main():</code>, '
             '<code>runloop.run(main())</code>) is handed over in session 1 and explained in '
             'session 8. A class that stops after part 1 never sees it opened.</li>'
             '<li>Machinery handed over and not opened: the word <code>lambda</code>, from '
             'session 3, and <code>[0]</code> after <code>tilt_angles()</code>, from session 6.</li>'
             '<li>Deliberate errors: <code>DARK = 0</code> in session 3, chunk 3, and two '
             'lines in the wrong order in session 4, chunk 2. First tries that every team '
             'replaces: 180 for the turn, 50 for <code>DARK</code>, <code>port.B</code> and '
             '<code>port.F</code>, 900 for <code>QUARTER</code>, and 30 and 150 in the line '
             'follower. Session 5, chunk 3, shows numbers that start at 0 on purpose.</li>'
             '<li>Standards: New York science (engineering design) and New York mathematics '
             'only. No computer science codes: the graph returned none for New York on '
             + RESOLVED_ON + '.</li></ul></section>')
    return simple_page(COURSE + ' &middot; Constraints', 'Course constraints',
                       'What the course uses, what it never uses, and what is locked.', "".join(b))


# ------------------------------------------------------------- standards map

def render_standards():
    used = {}
    for s in SESSIONS:
        for c in s["teacher"]["standards"]:
            used.setdefault(c, []).append(s["num"])
    b = ['<section><h2>How to read this page</h2><p>Each session is mapped to at most three '
         'standards. Every code was retrieved through the ' + CONNECTOR + ' on ' + RESOLVED_ON
         + ' and is printed with its CASE identifier, so it can be checked. A 3-5 science '
         'code has one identifier for each grade; this course is for grades 4 and 5, so both '
         'are printed.</p></section>']
    b.append('<section><h2>Codes used</h2><table class="std"><tr><th>Code</th><th>Framework</th>'
             '<th>Grade</th><th>Statement, as retrieved</th><th>CASE identifier</th>'
             '<th>Sessions mapped to it</th></tr>')
    for c in STANDARDS:
        if c not in used:
            continue
        st = STANDARDS[c]
        ids = "<br>".join(g + ": <code>" + u + "</code>" for g, u in st["uuids"])
        text = html.escape(st["statement"])
        if st["deviation"]:
            text += '<br><i>' + html.escape(st["deviation"]) + '</i>'
        b.append('<tr><td><code>' + c + '</code></td><td>' + st["framework"] + '</td><td>'
                 + st["grades"] + '</td><td>' + text + '</td><td>' + ids + '</td><td>'
                 + ", ".join(str(x) for x in used[c]) + '</td></tr>')
    b.append('</table></section>')
    b.append('<section><h2>By session</h2><table><tr><th>Session</th><th>Mapped to</th></tr>')
    for s in SESSIONS:
        b.append('<tr><td><a href="' + link(s["slug"]) + '">' + str(s["num"]) + '. '
                 + html.escape(s["title"]) + '</a></td><td>'
                 + ", ".join('<code>' + c + '</code>' for c in s["teacher"]["standards"]) + '</td></tr>')
    b.append('</table><p class="note">No CSTA code and no New York Computer Science and '
             'Digital Fluency code appears anywhere on this site. The graph returned no New '
             'York computer science codes on ' + RESOLVED_ON + '.</p></section>')
    return simple_page(COURSE + ' &middot; Standards', 'Standards map',
                       'Every code used, its full statement, and the sessions mapped to it.',
                       "".join(b))


# ---------------------------------------------------------------- ledger card

def render_ledger():
    b = ['<section class="noprint"><h2>How to use it</h2><ul>'
         '<li>Print one card for each student before session 1 and keep the stack in the room.</li>'
         '<li>Two minutes at the end of each session. The student writes, not the teacher.</li>'
         '<li>The card comes out again in the next session\'s opener.</li></ul></section>']
    b.append('<section><h2>Stamps</h2><div class="stampgrid">')
    for s in SESSIONS:
        b.append('<div class="stamp"><span class="no">Stamp ' + str(s["num"]) + ' &middot; '
                 + html.escape(s["title"]) + '</span></div>')
    b.append('</div></section>')
    b.append('<section><h2>My team\'s numbers</h2><table>'
             '<tr><th>Name</th><th>What it is</th><th>Our value</th></tr>'
             '<tr><td><code>QUARTER_TURN</code></td><td>Degrees of motor turn for a quarter '
             'turn of the robot. Session 2.</td>' + blank("QUARTER_TURN") + '</tr>'
             '<tr><td><code>LINE_SENSOR</code></td><td>The port letter of our colour sensor. '
             'Session 3.</td>' + blank("LINE_SENSOR") + '</tr>'
             '<tr><td>Floor reading</td><td>Reflected light over the pale floor. Session 3.</td>'
             + blank("Floor reading") + '</tr>'
             '<tr><td>Tape reading</td><td>Reflected light over the black tape. Session 3.</td>'
             + blank("Tape reading") + '</tr>'
             '<tr><td><code>DARK</code></td><td>A number between the two readings. Session 3.</td>'
             + blank("DARK") + '</tr>'
             '<tr><td><code>QUARTER</code></td><td>The motion sensor\'s count for a quarter turn. '
             'Session 6.</td>' + blank("QUARTER") + '</tr>'
             '<tr><td><code>STOP_SENSOR</code></td><td>The port letter of our other colour '
             'sensor. Session 7.</td>' + blank("STOP_SENSOR") + '</tr>'
             '<tr><td>Steering and speed</td><td>Our line follower\'s two numbers. Session 7.</td>'
             + blank("Steering and speed") + '</tr></table></section>')
    b.append('<section><h2>Reference strip</h2>')
    strip = [
        ("motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)", "The left motor is in port A, the right motor in port E."),
        ("await motor_pair.move_for_degrees(motor_pair.PAIR_1, 720, 0, velocity=250)",
         "One move: how far, the steering, and the speed."),
        ("-720", "A minus sign on the first number: backward."),
        ("100", "Steering 100: turn right on the spot. Steering -100: turn left."),
        ("FORWARD = 360", "A name for a number, at the top of the program."),
        ("for count in range(4):", "Runs the lines inside it 4 times."),
        ("color_sensor.reflection(LINE_SENSOR)", "Reflected light, from 0 to 100."),
        (SESSION03["ledger_code"], "Start the wheels, wait until the test is true, stop the wheels."),
        ("sound.beep(440, 500, 100)", "Part 2. A note: pitch, how long in thousandths of a second, how loud."),
        ("light_matrix.write(str(count + 1))", "Show a number on the light matrix. Python counts from 0."),
        (SESSION06["ledger_code"], "A measured turn. The sensor counts in tenths of a degree of the robot's turn."),
        (SESSION07["ledger_code"], "A line follower: keep choosing until the stop sensor is over the stop bar."),
        ("async def quarter_turn():", "Give the lines inside a name. Run them with await quarter_turn()."),
    ]
    ctx = SESSION08["chunks"][1]["code"]
    b.append('<table class="strip"><tr><th>Python</th><th>What it does</th></tr>')
    for code, gloss in strip:
        b.append('<tr><td>' + code_block(code, context=ctx) + '</td><td>' + gloss + '</td></tr>')
    b.append('</table>')
    b.append('<p class="note">360 degrees of motor turn is one full turn of the wheel, about '
             + str(wheel.whole_cm(360)) + ' cm. One change per run.</p></section>')
    b.append('<section><h2>Port map</h2><table><tr><th>Port</th><th>What is plugged in</th></tr>'
             '<tr><td class="mono">' + robot.DRIVE_LEFT + '</td><td>Large motor, left wheel</td></tr>'
             '<tr><td class="mono">' + robot.DRIVE_RIGHT + '</td><td>Large motor, right wheel</td></tr>'
             '<tr><td>Our colour sensor</td>' + blank("Colour sensor port") + '</tr></table></section>')
    b.append('<section><h2>When something goes wrong</h2><table><tr><th>What you call it</th>'
             '<th>What it looks like</th><th>Check first</th></tr>'
             '<tr><td>Wrong way</td><td>The robot moves backward when the program says forward.</td>'
             '<td>The port map. The two large motors\' cables may be swapped.</td></tr>'
             '<tr><td>No go</td><td>The program stops and the robot does not move.</td>'
             '<td>The robot check list, then capitals and <code>await</code> on the move lines.</td></tr>'
             '<tr><td>Curve</td><td>The robot curves when the steering is 0.</td>'
             '<td>A cable rubbing a wheel, or a wheel not pushed fully onto its axle.</td></tr>'
             '<tr><td>Runs past</td><td>The robot does not stop at the line.</td>'
             '<td>Is <code>DARK</code> above the tape reading? Is the port letter right?</td></tr>'
             '<tr><td>Stops at once</td><td>The robot stops as soon as it starts.</td>'
             '<td>Is <code>DARK</code> below the floor reading?</td></tr>'
             '</table></section>')
    return simple_page('One page &middot; print it &middot; one stamp a session', 'Ledger card',
                       'One stamp a session, written by hand, in the student\'s own words.',
                       "".join(b))


def main():
    files = {}
    for i, s in enumerate(SESSIONS):
        prev_s = SESSIONS[i - 1] if i > 0 else None
        next_s = SESSIONS[i + 1] if i < len(SESSIONS) - 1 else None
        files[s["slug"] + ".html"] = render_session(s, prev_s, next_s)
        print("rendered", s["slug"])
    files[HUB + ".html"] = render_hub()
    files[ROBOT + ".html"] = render_robot()
    files[FIELD + ".html"] = render_field()
    files[CONSTRAINTS + ".html"] = render_constraints()
    files[STDMAP + ".html"] = render_standards()
    files[LEDGER + ".html"] = render_ledger()
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(text)
    print("\nwrote", len(files), "files to", OUT)
    if PENDING:
        print("\nmeasured results not on the pages yet (fewer than %d logged runs): %d"
              % (RUNS_NEEDED, len(PENDING)))


if __name__ == "__main__":
    main()
