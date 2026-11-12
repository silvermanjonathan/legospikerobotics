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
import robot
import wheel

SESSIONS = [SESSION01]

# Paths are relative to this file, so the repo builds from any clone.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get("SPIKE_OUT", ROOT)
VERSION = "1"
COURSE = "SPIKE Prime with Python"
HUB = "spike_course_hub"
ROBOT = "robot_advanced_driving_base"
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
            '<p>' + COURSE + ', grades 4 and 5. The class robot is LEGO\'s Advanced Driving '
            'Base. LEGO\'s building instructions are linked, not copied.</p>'
            '<p>Mapped to the New York State P-12 Science Learning Standards and the New York '
            'Next Generation Mathematics Learning Standards. Codes retrieved through the '
            + CONNECTOR + ' on ' + RESOLVED_ON + '. Pages built ' + PUBLISHED + '.</p>'
            '<p>LEGO and SPIKE are trademarks of the LEGO Group, which does not sponsor or '
            'endorse this course.</p></div></footer>')


# --------------------------------------------------------------- session pages

def render_session(s, prev_s, next_s):
    n = s["num"]
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">' + COURSE + ' &middot; Grades 4 and 5 &middot; Session '
             + str(n) + '</p>')
    b.append('<h1>' + html.escape(s["title"]) + '</h1>')
    b.append('<p class="sub">' + html.escape(s["subtitle"]) + '</p>')
    b.append('<div class="dates">')
    b.append('<span class="pill"><b>Length</b> 90 minutes</span>')
    b.append('<span class="pill"><b>Team</b> 4 builders, 1 robot</span>')
    b.append('<span class="pill"><b>New</b> ' + str(len(s["new"])) + ' items</span>')
    b.append('</div></div></header>')
    b.append('<main><div class="wrap">')

    b.append('<section><h2>What is new today</h2><p>' + s["new_text"] + '</p>')
    b.append('<p><b>Deliberately re-used:</b> ' + s["reuse"] + '</p>')
    b.append('<p><a href="' + link(ROBOT) + '">Open the robot page</a></p></section>')

    # ---- the build (session 1 only: it stands where the opener stands later)
    bd = s["build"]
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
        b.append(reveal_block(tag, ch["predict"], ans, hints=ch.get("hints")))
        b.append('</section>')

    # ---- hinge
    h = s["hinge"]
    b.append('<section class="hinge"><p class="chunk-no">Hinge question &middot; from '
             'today\'s chunks</p><h2>Before the mission</h2>')
    b.append(code_block(h["code"], context=s["chunks"][0]["code"]))
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
    b.append('<p>' + br["code_note"] + '</p>')
    b.append(code_block(br["code"]))
    b.append('<ol>' + "".join('<li>' + x + '</li>' for x in br["steps"]) + '</ol>')
    b.append('<h3>Expected and measured</h3><p>Fill in the Expected column before each run. '
             'Fill in the rest of the row after it. One change per run.</p>')
    b.append('<table><tr>' + "".join('<th>' + x + '</th>' for x in br["sheet_head"]) + '</tr>')
    for row in br["sheet_rows"]:
        first = ('<td class="mono">' + row[1] + '</td>' if row[1]
                 else blank("Run " + row[0] + ", first number on line 14"))
        b.append('<tr><td class="mono">' + row[0] + '</td>' + first
                 + blank("Run " + row[0] + ", expected") + blank("Run " + row[0] + ", measured")
                 + blank("Run " + row[0] + ", faces home, yes or no") + '</tr>')
    b.append('</table>')
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

    b.append('<section><h2>Ledger card</h2><p>Copy this onto your card.</p>'
             + code_block(s["ledger_code"], context=s["chunks"][0]["code"]) + '<p>'
             + s["ledger"] + '</p><p>' + s["stamp"] + '</p></section>')

    # ---- teacher panel
    t = s["teacher"]
    b.append('<details class="teacher"><summary>Teacher panel</summary>')
    b.append('<h3>Before class</h3><ul>' + "".join('<li>' + x + '</li>' for x in t["before"]) + '</ul>')
    b.append('<h3>Timing, 90 minutes</h3><ul>')
    for clock, what, mins in t["timing"]:
        b.append('<li>' + clock + ' ' + html.escape(what) + ', ' + str(mins) + ' min</li>')
    b.append('</ul><p class="note">' + t["pacing"] + '</p>')
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
             '<a href="runs.csv?v=' + VERSION + '">Run log, runs.csv</a> &middot; '
             '<a href="' + robot.LEGO_LESSON + '">LEGO\'s lesson this session is adapted from</a></p>')
    b.append('<p>Log each run on the reference robot in <code>runs.csv</code> with the '
             'program id below, then rebuild. A run counts only while its program id matches '
             'the program on this page.</p>')
    b.append('<table><tr><th>Result</th><th>Program id</th><th>Runs logged</th><th>On the page?</th></tr>')
    progs = [(c["key"], c["code"]) for c in s["chunks"]] + [("mission", br["code"])]
    for key, code in progs:
        got = len(runs_for(n, key, code))
        b.append('<tr><td>' + key + '</td><td class="mono">' + program_id(code) + '</td><td>'
                 + str(got) + ' of ' + str(RUNS_NEEDED) + '</td><td>'
                 + ('Yes' if got >= RUNS_NEEDED else 'Not yet') + '</td></tr>')
    b.append('</table></details>')
    b.append('</div></main>')

    b.append('<nav class="pager">')
    b.append('<a href="' + link(prev_s["slug"]) + '">&larr; ' + html.escape(prev_s["title"]) + '</a>'
             if prev_s else '<span></span>')
    b.append('<a href="' + link(HUB) + '">Course home</a>')
    b.append('<a href="' + link(next_s["slug"]) + '">' + html.escape(next_s["title"]) + ' &rarr;</a>'
             if next_s else '<span></span>')
    b.append('</nav>')
    b.append(footer())
    return page(s["title"] + " | " + COURSE, "".join(b))


# -------------------------------------------------------------------- hub page

def render_hub():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">LEGO SPIKE Prime &middot; Python &middot; Grades 4 and 5</p>')
    b.append('<h1>' + COURSE + '</h1>')
    b.append('<p class="sub">Read a robot program and say what the robot will do before it runs.</p>')
    b.append('</div></header><main><div class="wrap">')
    b.append('<section><h2>Sessions</h2><ul class="sessionlist">')
    for s in SESSIONS:
        b.append('<li><span class="n">' + str(s["num"]) + '</span><span><a href="'
                 + link(s["slug"]) + '">' + html.escape(s["title"]) + '</a><span class="meta">'
                 '90 minutes &middot; date to be set</span></span></li>')
    b.append('</ul></section>')
    b.append('<section><h2>How a session runs</h2><div class="grid2">'
             '<div class="card"><h3>Predict, then run</h3><p>Each part of a session shows a '
             'program and where the robot starts. You say what the robot will do. Then you '
             'run the program and check.</p></div>'
             '<div class="card"><h3>One change per run</h3><p>When you test, change one number, '
             'run the program, and write down what the robot did. Then you know what that one '
             'change does.</p></div></div></section>')
    b.append('<section><h2>The robot</h2><p>Every session uses the same robot, built the same '
             'way, with each cable in the same port.</p><div class="toolbar"><a class="btn" href="'
             + link(ROBOT) + '">Open the robot page</a></div></section>')
    b.append('</div></main>' + footer())
    return page(COURSE, "".join(b))


# ------------------------------------------------------------------ robot page

def render_robot():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">' + COURSE + ' &middot; The class robot</p>')
    b.append('<h1>The Advanced Driving Base</h1>')
    b.append('<p class="sub">The robot, its ports, its wheel, and the test field.</p>')
    b.append('</div></header><main><div class="wrap">')

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

    b.append('<section><h2>The test field</h2><p>Two lines of black tape on a flat floor or '
             'table. The far line is ' + str(robot.FAR_CM) + ' cm from the start line. The '
             'robot starts behind the start line with its front edge on the line, facing '
             'the far line. Every distance is measured with a ruler from the start line to '
             'the robot\'s front edge.</p>')
    b.append(robot.field_figure(far=True, caption="The test field from above, drawn to scale."))
    b.append('</section>')

    b.append('<details class="teacher"><summary>Teacher panel</summary>'
             '<h3>Where each fact on this page comes from</h3>'
             '<table><tr><th>Port</th><th>Source</th></tr>')
    for letter, what, where, src in robot.PORT_MAP:
        b.append('<tr><td class="mono">' + letter + '</td><td>' + src + '</td></tr>')
    b.append('</table><p>' + robot.WHEEL_NOTE + ' <a href="' + robot.LEGO_PYTHON
             + '">LEGO\'s Python programs (PDF)</a>.</p>'
             '<p>Before the first session, build the reference robot and check every row of '
             'the port map against it. Ports B, C, D, and F are not used by session 1.</p>'
             '<p>LEGO stopped selling SPIKE Prime on 30 June 2026 and supports the SPIKE App '
             'until 30 June 2031 (<a href="' + robot.LEGO_UPDATE + '">LEGO Education</a>). '
             'Keep a spare of every part this robot needs, and an unpublished copy of the '
             'five building books.</p></details>')
    b.append('</div></main>')
    b.append('<nav class="pager"><span></span><a href="' + link(HUB) + '">Course home</a><span></span></nav>')
    b.append(footer())
    return page("The Advanced Driving Base | " + COURSE, "".join(b))


def main():
    files = {}
    for i, s in enumerate(SESSIONS):
        prev_s = SESSIONS[i - 1] if i > 0 else None
        next_s = SESSIONS[i + 1] if i < len(SESSIONS) - 1 else None
        files[s["slug"] + ".html"] = render_session(s, prev_s, next_s)
        print("rendered", s["slug"])
    files[HUB + ".html"] = render_hub()
    files[ROBOT + ".html"] = render_robot()
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(text)
    print("\nwrote", len(files), "files to", OUT)
    if PENDING:
        print("\nmeasured results not on the pages yet (fewer than %d logged runs):" % RUNS_NEEDED)
        for session, key, pid, got in PENDING:
            print("   session %s %-8s program id %s  %d runs logged" % (session, key, pid, got))


if __name__ == "__main__":
    main()
