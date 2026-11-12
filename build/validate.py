import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("SPIKE_OUT", os.path.dirname(HERE))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
# the span classes hl.py writes inside <pre class="py"><code> blocks
CODE_CLASSES = {"hk", "hs", "hf", "hc", "hv", "hn", "hq", "he", "hd", "hm"}
BANNED_WORDS = ["genuinely", "delve", "tapestry", "testament to", "at its core",
                "dial worth turning", "earns its keep", "unleash", "supercharge",
                # no page refers to a camp, another course or term, or a competition
                # the students are not in
                "summer", "camp", "last term", "previous term", "competition",
                # privacy: no employer name or workplace address on a public page
                "robofun", "vemny", "jerseystem", "west end avenue",
                # the robot is not a person and the hub is not a brain
                "the robot sees", "the robot knows", "the robot wants", "the robot decides",
                "the robot remembers", "the robot thinks", "brain", "smart"]
# cm is the only distance unit
BANNED_UNITS = [r"\binch(?:es)?\b", r"\bfeet\b", r"\bfoot\b", r"\d\s?mm\b", r"\bmillimet"]
FAILURES = []
NOTES = []


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("closing </%s> with nothing open at %s" % (tag, self.getpos()))
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append("expected </%s> (opened %s) but found </%s> at %s"
                               % (open_tag, pos, tag, self.getpos()))


def visible(text, keep_code=False):
    """The words a reader sees, without tags. Code and the quoted standards go too,
    unless keep_code is set, because their wording is not ours to change."""
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S)
    if not keep_code:
        t = re.sub(r"<pre\b.*?</pre>", " ", t, flags=re.S)
        t = re.sub(r"<code\b.*?</code>", " ", t, flags=re.S)
        t = re.sub(r'<table class="std">.*?</table>', " ", t, flags=re.S)
        # drawn Word Block stacks: their words are the app's own, not ours to change
        t = re.sub(r'<figure class="blocks".*?</figure>', " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


class Boxes(HTMLParser):
    """Finds any result box that is not inside a hidden reveal."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.loose = 0

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "") or ""
        if tag == "pre" and "out" in cls.split():
            if not any("ans" in c.split() for t, c in self.stack):
                self.loose += 1
        if tag not in VOID:
            self.stack.append((tag, cls))

    def handle_endtag(self, tag):
        if tag not in VOID and self.stack:
            self.stack.pop()


def check(name, text, all_names):
    fail = []

    p = Balance()
    p.feed(text)
    p.close()
    for e in p.errors:
        fail.append("tag balance: " + e)
    if p.stack:
        fail.append("unclosed tags: " + ", ".join(t for t, _ in p.stack))

    buttons = re.findall(r'<button class="rev(?: hint)?" data-target="([^"]+)"', text)
    answers = re.findall(r'<div class="ans" id="([^"]+)">', text)
    if sorted(buttons) != sorted(answers):
        fail.append("reveal parity: %d buttons, %d answer blocks; unmatched %s"
                    % (len(buttons), len(answers),
                       set(buttons) ^ set(answers)))
    if len(set(buttons)) != len(buttons):
        fail.append("duplicate reveal ids")
    # every reveal button names the block it controls and starts collapsed
    controls = re.findall(r'<button class="rev(?: hint)?" data-target="([^"]+)" aria-controls="([^"]+)" '
                          r'aria-expanded="false"', text)
    if len(controls) != len(buttons) or any(a != b for a, b in controls):
        fail.append("reveal buttons missing aria-controls/aria-expanded or mismatched target")

    # teacher panel timing rows must sum to exactly 90 minutes, with rows for the
    # robot check, packing away, and the ledger stamp
    rows = re.findall(r'<li>\d+:\d\d [^<]*?, (\d+) min', text)
    if rows and sum(int(r) for r in rows) != 90:
        fail.append("timing rows sum to %d minutes, not 90" % sum(int(r) for r in rows))
    for need in ("robot check", "pack away", "ledger stamp"):
        if rows and not re.search(r'<li>\d+:\d\d [^<]*' + need + r'[^<]*, \d+ min', text, re.I):
            fail.append("teacher panel has no %s row" % need)

    # the mission's minutes on the student side match its row in the teacher panel
    m_page = re.search(r'Mission &middot; (\d+) minutes', text)
    m_row = re.search(r'<li>\d+:\d\d Mission, (\d+) min', text)
    if m_page and m_row and m_page.group(1) != m_row.group(1):
        fail.append("the mission says %s minutes, its timing row says %s"
                    % (m_page.group(1), m_row.group(1)))

    # a result box sits inside a hidden reveal and says where its result came from
    bx = Boxes()
    bx.feed(text)
    if bx.loose:
        fail.append("%d result box(es) outside a hidden reveal" % bx.loose)
    n_out = len(re.findall(r'<pre class="out">', text))
    n_src = len(re.findall(r'<p class="outsrc">(?:On the reference robot, \d+ runs|Computed, not measured)</p>'
                           r'<pre class="out">', text))
    if n_out != n_src:
        fail.append("%d result box(es) without a source label" % (n_out - n_src))

    prose = visible(text)
    # "degrees" never stands alone: it is degrees of motor turn or of the robot's turn
    for m in re.finditer(r"\bdegrees\b(?! of motor turn| of the robot's turn)", prose):
        fail.append("degrees on its own: ..." + prose[max(0, m.start() - 40):m.end() + 20] + "...")
    for pat in BANNED_UNITS:
        if re.search(pat, prose, re.I):
            fail.append("a distance unit other than cm: " + pat)
    # every chunk has a prediction and a setup line
    for sec in re.findall(r'<section class="chunk">(.*?)</section>', text, re.S):
        if 'class="predict"' not in sec or "Predict:" not in sec:
            fail.append("a chunk has no prediction")
        if 'class="setup"' not in sec:
            fail.append("a chunk does not say where the robot starts")
        if '<pre class="py">' not in sec:
            fail.append("a chunk shows no program")
    if re.search(r"\b(aligned with|meets the standard|teaches the standard)\b", prose, re.I):
        fail.append("standards wording: use 'mapped to'")

    # a pre block holds code or output, so once its color spans and the code tag are
    # stripped, no tag may remain; the anatomy figures are the one exception and
    # carry their own labelled spans
    for attrs, block in re.findall(r'<pre([^>]*)>(.*?)</pre>', text, re.S):
        if 'class="anatomy"' in attrs:
            inner = re.sub(r'</?(?:span|b|em|code)\b[^>]*>', '', block)
        else:
            inner = re.sub(r'</?span\b[^>]*>|</?code>', '', block)
        if re.search(r'<[a-zA-Z/]', inner):
            fail.append("unescaped angle bracket inside a pre block: "
                        + block[:60].replace("\n", " "))
    # every colored code block is <pre class="py"><code>, and uses only hl.py's classes
    for block in re.findall(r'<pre class="py"><code>(.*?)</code></pre>', text, re.S):
        for cls in re.findall(r'<span class="([^"]+)">', block):
            if cls not in CODE_CLASSES and cls != "ig":
                fail.append("unknown code color class: " + cls)
        # every step of indentation sits in an indent guide span, so the hints can
        # draw VS Code's guides; a guide span holds four spaces or, on a blank line,
        # nothing
        for ln in block.split("\n"):
            if ln.startswith("    "):
                fail.append("indentation without indent guides: " + ln.strip()[:60])
        for inner in re.findall(r'<span class="ig">(.*?)</span>', block):
            if inner not in ("    ", ""):
                fail.append("an indent guide span holds %r, not four spaces" % inner)
    for attrs in re.findall(r'<pre([^>]*)><code>', text):
        if 'class="py"' not in attrs:
            fail.append("a <pre><code> block without the py class: <pre" + attrs + ">")
    if re.search(r'<pre class="py">(?!<code>)', text):
        fail.append("a pre.py block without a code tag inside it")
    # prose and output are never colored
    for attrs, block in re.findall(r'<pre([^>]*)>(.*?)</pre>', text, re.S):
        if 'class="out"' in attrs or 'class="want"' in attrs:
            if re.search(r'<span class="h[a-z]"', block):
                fail.append("an output box carries code color spans")

    for api in ("localStorage", "sessionStorage", "indexedDB"):
        if api in text:
            fail.append("storage API present: " + api)

    dashes = text.count("\u2014") + text.count("\u2013")
    if dashes:
        fail.append("dash characters found: %d" % dashes)

    low = visible(text, keep_code=True).lower()
    for w in BANNED_WORDS:
        if re.search(r"\b" + re.escape(w), low):
            fail.append("banned phrase: " + w)

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith("http") or href.startswith("#"):
            continue
        target = href.split("?")[0]
        if target not in all_names:
            fail.append("dead link: " + href)

    if "<h1>" not in text:
        fail.append("no h1")
    if "<title>" not in text:
        fail.append("no title")

    return fail


def main():
    names = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    # links may point at any file in the site, such as a worksheet's PDF
    targets = set(os.listdir(SITE))
    for n in names:
        text = open(os.path.join(SITE, n)).read()
        fails = check(n, text, targets)
        status = "PASS" if not fails else "FAIL"
        kb = len(text) / 1024.0
        print("%-44s %s  %6.1f kB" % (n, status, kb))
        for f in fails:
            print("      -> " + f)
            FAILURES.append(n + ": " + f)

    print("\nfiles: %d" % len(names))
    revs = sum(len(re.findall(r'<button class="rev(?: hint)?"', open(os.path.join(SITE, n)).read()))
               for n in names)
    outs = sum(len(re.findall(r'<pre class="out">', open(os.path.join(SITE, n)).read()))
               for n in names)
    pys = sum(len(re.findall(r'<pre class="py"><code>', open(os.path.join(SITE, n)).read()))
              for n in names)
    print("reveal buttons: %d" % revs)
    print("result boxes: %d" % outs)
    print("colored code blocks: %d" % pys)

    # Word Block stacks: every colour clears 7:1, every C arm is 16px or wider, and
    # every block inside a C block is drawn inside its arm
    sys.path.insert(0, HERE)
    import blocks
    for f in blocks.check():
        FAILURES.append("blocks: " + f)
        print("      -> blocks: " + f)
    stacks = 0
    for n in names:
        text = open(os.path.join(SITE, n)).read()
        stacks += len(re.findall(r'<figure class="blocks"', text))
        for cb in re.findall(r'<div class="cbody">(.*?)</div></div>', text, re.S):
            if not cb.startswith('<div class="carm"></div><div class="cin">'):
                FAILURES.append(n + ": a block inside a C block is drawn outside its arm")
    print("word block stacks: %d" % stacks)
    if FAILURES:
        print("\n%d FAILURES" % len(FAILURES))
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
