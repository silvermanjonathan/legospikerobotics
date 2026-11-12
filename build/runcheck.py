"""Guard 2: programs, arithmetic, and the run log.

    python3 build/runcheck.py             report; fails on any wrong program or number
    python3 build/runcheck.py --release   also fails while a measured result is not logged

What it checks:
  1. Every program on a page is real Python and runs to the end against the stand-in
     SPIKE modules in build/spike_stub, and asks for exactly the moves its page says,
     in order. A move line without await, a wrong port, or steering out of range fails.
  2. Every computed number is recomputed from wheel.py.
  3. Every measured result has at least three runs in runs.csv, logged against the
     current text of its program. Until it does, the page prints no measured box for
     it and this guard lists it as pending.

The stand-in modules are not a simulator. No distance or turn on a page comes from them.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render
import wheel
from session01 import SESSION01, HINGE, TOP, END, ONE_TURN, TWO_TURNS, HINGE_CM
import robot

FAIL = []
STUB = os.path.join(HERE, "spike_stub")


def run_program(tag, code):
    env = dict(os.environ, PYTHONPATH=STUB, PYTHONWARNINGS="error")
    p = subprocess.run([sys.executable, "-X", "dev", "-c", code], capture_output=True,
                       text=True, env=env, timeout=30)
    if p.returncode != 0 or "never awaited" in p.stderr:
        FAIL.append("%s: program did not run cleanly: %s" % (tag, p.stderr.strip()[-300:]))
        return None
    return json.loads(p.stdout.strip().splitlines()[-1])


def as_expect(calls):
    out = []
    for c in calls:
        if c["call"] == "pair":
            out.append(("pair", c["left"], c["right"]))
        else:
            out.append(("move", c["degrees"], c["steering"], c["velocity"]))
    return out


def check_program(tag, code, expect):
    calls = run_program(tag, code)
    if calls is None:
        return
    got = as_expect(calls)
    if got != list(expect):
        FAIL.append("%s: the program asks for %s, the page says %s" % (tag, got, expect))
    else:
        print("  ok  %-16s %s  %d calls match the page" % (tag, render.program_id(code), len(got)))
    for c in got:
        if c[0] == "pair" and (c[1], c[2]) != (robot.DRIVE_LEFT, robot.DRIVE_RIGHT):
            FAIL.append("%s: pairs ports %s+%s, the port map says %s+%s"
                        % (tag, c[1], c[2], robot.DRIVE_LEFT, robot.DRIVE_RIGHT))


def main():
    release = "--release" in sys.argv
    s = SESSION01
    print("programs:")
    for ch in s["chunks"]:
        check_program("s1-" + ch["key"], ch["code"], ch["expect"])
    check_program("s1-mission", s["brief"]["code"], s["brief"]["expect"])
    check_program("s1-hinge", TOP + "\n    " + HINGE + END, [("pair", "A", "E"), ("move", -360, 0, 250)])

    print("arithmetic:")
    checks = [
        ("one full turn, whole cm", ONE_TURN, round(wheel.WHEEL_CM)),
        ("720 degrees of motor turn, nearest 5", TWO_TURNS, wheel.nearest5(wheel.cm(720))),
        ("360 degrees of motor turn, nearest 5", HINGE_CM, wheel.nearest5(wheel.cm(360))),
        ("far line", robot.FAR_CM, wheel.nearest5(wheel.cm(720))),
    ]
    for name, on_page, computed in checks:
        if on_page != computed:
            FAIL.append("arithmetic: %s is %s on the page, %s computed" % (name, on_page, computed))
        else:
            print("  ok  %-40s %s" % (name, on_page))
    # the numbers must also be in the built page
    page = open(os.path.join(render.OUT, s["slug"] + ".html")).read()
    for needle in ("about %d cm" % ONE_TURN, "that is %d cm" % TWO_TURNS, "that is %d cm" % HINGE_CM):
        if needle not in page:
            FAIL.append("arithmetic: the built page does not say %r; rebuild" % needle)

    print("run log:")
    pending = 0
    progs = [(c["key"], c["code"]) for c in s["chunks"]] + [("mission", s["brief"]["code"])]
    for key, code in progs:
        rows = render.runs_for(1, key, code)
        stale = [r for r in render.RUNS if r["session"] == "1" and r["chunk"] == key
                 and r["program_id"] != render.program_id(code)]
        state = "logged" if len(rows) >= render.RUNS_NEEDED else "PENDING"
        pending += state == "PENDING"
        print("  %-8s %-8s program id %s  %d of %d runs%s"
              % (state, key, render.program_id(code), len(rows), render.RUNS_NEEDED,
                 ("  (%d older runs no longer count)" % len(stale)) if stale else ""))
        if len(rows) >= render.RUNS_NEEDED and 'On the reference robot' not in page:
            FAIL.append("run log: %s is logged but the page was not rebuilt" % key)

    if FAIL:
        print("\n%d FAILURES" % len(FAIL))
        for f in FAIL:
            print("   -> " + f)
        sys.exit(1)
    if pending:
        print("\n%d measured result(s) pending: not release-ready (style guide, section 16, "
              "item 3). Programs and arithmetic pass." % pending)
        if release:
            sys.exit(1)
    else:
        print("\nall checks passed")


if __name__ == "__main__":
    main()
