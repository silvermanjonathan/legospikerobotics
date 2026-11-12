# SPIKE Prime with Python

LEGO SPIKE Prime robotics for grades 4 and 5, in four sessions of 90 minutes, written
in Python for the SPIKE App 3. The class robot is LEGO's Advanced Driving Base. The
house style is the SPIKE Prime Course Style Guide, snapshot of 12 November 2026.

Homepage: `spike_course_hub.html` at the repo root (there is no `index.html`).

## Pages

| File | What it is |
|---|---|
| `spike_course_hub.html` | Course home. The four sessions, how a session runs, links to everything else. |
| `session01_advanced_driving_base.html` | Session 1. A team of four builds the robot, then moves it forward, backward, and through a turn. Adapted from LEGO's lesson "Assembling an Advanced Driving Base". |
| `session02_quarter_turn_and_square.html` | Session 2. Names for numbers, the quarter turn found by testing, a square the long way and with a `for` line. Tells students the final mission. |
| `session03_stop_at_the_line.html` | Session 3. The colour sensor's reflected light, and moving until a line. |
| `session04_delivery_run_and_demo.html` | Session 4. No new Python. The delivery run, then the demo for families. |
| `robot_advanced_driving_base.html` | The class robot: links to LEGO's five building books, the port map, the wheel table. |
| `field_test_field.html` | The test field for every session, drawn to scale. |
| `course_constraints.html` | What the course uses and when each thing is first taught, what it never uses, the locked decisions. Dated. |
| `standards_map.html` | Every standards code used, its full statement, CASE identifiers, and sessions. |
| `course_ledger_card.html` | The printable card: four stamps, the team's numbers, a reference strip, the port map, a fault table. |
| `runs.csv` | The run log for the reference robot. Empty so far. |

## Build

Pages are generated, never edited by hand.

    python3 build/render.py              # writes the pages into the repo root
    python3 build/validate.py            # guard 1: structure, prose rules, links, 90 minutes
    python3 build/runcheck.py            # guard 2: programs, arithmetic, run log
    python3 build/runcheck.py --release  # also fails while a measured result is not logged

| Generator | Holds |
|---|---|
| `build/session01.py` to `build/session04.py` | One session each: its programs and every word on its page |
| `build/robot.py` | Port map, LEGO's links, every field and robot figure |
| `build/wheel.py` | Wheel arithmetic: degrees of motor turn to centimetres |
| `build/standards.py` | Standards, as retrieved, with CASE identifiers |
| `build/hl.py` | Python code colors, from the beginner Python course's build |
| `build/spike_stub/` | Stand-ins for the SPIKE App 3 modules, so the guard can run each program on a computer |
| `build/render.py` | Writes every page; holds the constraints, standards, ledger, field, and hub pages |

## Logging runs

Each measured result needs three runs on the reference robot. Add one row per run to
`runs.csv`, with the program id that the session's teacher panel and `runcheck.py`
print, then rebuild. A run counts only while its program id matches the program on
the page, so a result cannot outlive a change to its program.

    date,session,chunk,project,program_id,run,battery,result,unit,notes
    2026-11-16,1,chunk1,Jonathan_session01,95fe2ae2,1,100,54,cm,

## Locked decisions, 12 November 2026

The constraints page carries the full list. The ones that differ from the style guide:

1. **Python.** This course uses Python in the SPIKE App 3, by Jonathan's direction.
   The style guide's default (section 17) is Word Blocks only for grades 4 and 5.
2. **The class robot is the Advanced Driving Base**, one for each team of four. Port
   map: A left drive motor, E right drive motor, as LEGO's own programs for this robot
   say. The style guide's default port map is the Rhinobot's (A and B).
3. **Four sessions.** Session 4 is the demo for families. The final mission is told
   to students in session 2, because session 1 is the build.
4. **Machinery handed over and never opened**, because four sessions leave no room:
   the frame (`async def main():`, `runloop.run(main())`) and the word `lambda`.
5. **Teams fill in their own numbers.** No turn number, sensor port letter, or
   reflected light reading is printed as a fact. The programs carry first tries (180,
   `port.B`, 50) that each team replaces by testing.
6. **Session 1 has no opener.** That time goes to building the robot.
7. **Standards.** New York science (engineering design) and New York mathematics
   only, retrieved through the Learning Commons Knowledge Graph on 12 November 2026.

## Release log

### 12 November 2026, second printing (version pin 2)

What changed: sessions 2, 3, and 4 added; the field page, constraints page, standards
map, and ledger card added; the hub rewritten for four sessions; session 1 now says
"Session 1 of 4" and links to the new pages. Session 1's programs did not change.

What was checked:

- `validate.py` passes on all ten pages.
- `runcheck.py`: all 21 programs run cleanly against the stand-in modules and ask for
  exactly the moves their pages say. The sensor programs were run against a scripted
  floor-then-line and a floor with no line, so each branch a page describes was tried.
  The wheel arithmetic is recomputed and found on the built pages.
- Layout looked at in a browser at 1280px and 390px with every reveal open. No
  sideways scroll.
- Every function used was checked against published SPIKE App 3 references:
  `motor_pair.pair`, `move_for_degrees`, `move`, `stop`, `color_sensor.reflection`,
  `runloop.until` with a lambda, `runloop.run(main())`.

What is not done, so this is not release-ready under section 16 of the style guide:

- **Nothing has been run on a real hub or a real robot.** No measured result is on any
  page. Fifteen results wait for three logged runs each. Until then each reveal shows
  what the page works out and asks students to measure their own run.
- **The colour sensors are unconfirmed.** Which ports they use, and whether they sit
  low enough to read reflected light off the floor, has to be checked on a built
  robot before session 3. The session 3 robot check has each team read its own port
  letter.
- **Target zones are first choices:** 5 cm (session 1), 10 cm (session 2), the line
  under the robot (session 3), a 40 cm drop zone laid from the reference robot
  (session 4). A reference spread wider than a zone means the zone changes.
- **Timings are estimates.** The 45 minutes for the build in particular: LEGO gives
  30 minutes for grades 6 to 8.
- Dates are not set. The SPIKE App and hub version numbers are not yet written on the
  constraints page.
- Not built: starter project files, extra cards, worksheets, and photos of the
  reference robot.

### 12 November 2026, first printing (version pin 1)

Session 1, the hub, and the robot page, with the build and both guards.
