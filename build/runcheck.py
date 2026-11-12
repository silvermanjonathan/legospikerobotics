"""Guard 2: programs, arithmetic, and the run log.

    python3 build/runcheck.py             report; fails on any wrong program or number
    python3 build/runcheck.py --release   also fails while a measured result is not logged

What it checks:
  1. Every program on a page is real Python and runs to the end against the stand-in
     SPIKE modules in build/spike_stub, and asks for exactly the moves its page says,
     in order. A move line without await, a wrong port, or steering out of range fails.
     A program that reads the colour sensor is run against a scripted list of readings,
     once for each branch its page describes.
  2. Every computed number is recomputed from wheel.py and found on the built page.
  3. Every measured result has at least three runs in runs.csv, logged against the
     current text of its program. Until it does, the page prints no measured box for
     it and this guard lists it as pending.

The stand-in modules are not a simulator. No distance, turn, or sensor reading on a
page comes from them.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render
import wheel
import robot

FAIL = []
STUB = os.path.join(HERE, "spike_stub")


def run_program(tag, code, script):
    env = dict(os.environ, PYTHONPATH=STUB, PYTHONWARNINGS="error")
    if script:
        env["SPIKE_READINGS"] = json.dumps(script)
    p = subprocess.run([sys.executable, "-X", "dev", "-c", code], capture_output=True,
                       text=True, env=env, timeout=30)
    if p.returncode != 0 or "never awaited" in p.stderr:
        FAIL.append("%s: program did not run cleanly: %s" % (tag, p.stderr.strip()[-300:]))
        return None, None
    lines = p.stdout.strip().splitlines()
    return json.loads(lines[-1]), lines[:-1]


def as_expect(calls):
    out = []
    for c in calls:
        if c["call"] == "pair":
            out.append(("pair", c["left"], c["right"]))
        elif c["call"] == "move_for_degrees":
            out.append(("move", c["degrees"], c["steering"], c["velocity"]))
        elif c["call"] == "start":
            out.append(("start", c["steering"], c["velocity"]))
        else:
            out.append((c["call"],))
    return out


def check_program(tag, code, expect, script=None, prints=None):
    calls, printed = run_program(tag, code, script)
    if calls is None:
        return
    got = as_expect(calls)
    if got != [tuple(e) for e in expect]:
        FAIL.append("%s: the program asks for %s, the page says %s" % (tag, got, list(expect)))
    elif prints is not None and printed != prints:
        FAIL.append("%s: the program prints %s, expected %s" % (tag, printed, prints))
    else:
        print("  ok  %-22s %s  %d calls match the page" % (tag, render.program_id(code), len(got)))
    for c in got:
        if c[0] == "pair" and (c[1], c[2]) != (robot.DRIVE_LEFT, robot.DRIVE_RIGHT):
            FAIL.append("%s: pairs ports %s+%s, the port map says %s+%s"
                        % (tag, c[1], c[2], robot.DRIVE_LEFT, robot.DRIVE_RIGHT))
        if c[0] in ("move", "start") and abs(c[-1]) != 250:
            FAIL.append("%s: a speed other than velocity=250" % tag)


def main():
    release = "--release" in sys.argv
    pending = 0
    for s in render.SESSIONS:
        n = s["num"]
        page = open(os.path.join(render.OUT, s["slug"] + ".html")).read()
        print("session %d programs:" % n)
        for ch in s["chunks"]:
            check_program("s%d-%s" % (n, ch["key"]), ch["code"], ch["expect"],
                          ch.get("script"), ch.get("prints"))
            if ch.get("start"):
                compile(ch["start"], "start", "exec")
        br = s["brief"]
        check_program("s%d-mission" % n, br["code"], br["expect"], br.get("script"))
        for name, code, expect, script in s.get("checks", []):
            check_program("s%d-%s" % (n, name), code, expect, script)

        for name, on_page, needle, deg in s.get("arith", []):
            exact = wheel.cm(deg)
            want = wheel.whole_cm(deg) if "whole" in name else wheel.nearest5(exact)
            if on_page != want:
                FAIL.append("s%d arithmetic: %s is %s on the page, %s computed" % (n, name, on_page, want))
            elif needle not in page:
                FAIL.append("s%d arithmetic: the built page does not say %r; rebuild" % (n, needle))
            else:
                print("  ok  %-32s %s" % (name, on_page))

        for key, code in render.session_programs(s):
            rows = render.runs_for(n, key, code)
            stale = [r for r in render.RUNS if r["session"] == str(n) and r["chunk"] == key
                     and r["program_id"] != render.program_id(code)]
            ok = len(rows) >= render.RUNS_NEEDED
            pending += not ok
            print("  %-8s %-8s program id %s  %d of %d runs%s"
                  % ("logged" if ok else "PENDING", key, render.program_id(code), len(rows),
                     render.RUNS_NEEDED,
                     ("  (%d older runs no longer count)" % len(stale)) if stale else ""))

    # the port map is the same wherever it is printed
    for name in (render.ROBOT, render.LEDGER, render.CONSTRAINTS):
        text = open(os.path.join(render.OUT, name + ".html")).read()
        if "left" not in text or ">" + robot.DRIVE_LEFT + "<" not in text.replace("port " + robot.DRIVE_LEFT, ">A<"):
            FAIL.append("port map: %s does not show port %s as the left drive motor" % (name, robot.DRIVE_LEFT))

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
