# SPIKE Prime with Python

LEGO SPIKE Prime robotics for grades 4 and 5, written in Python for the SPIKE App 3.
The class robot is LEGO's Advanced Driving Base. The house style is the SPIKE Prime
Course Style Guide, snapshot of 12 November 2026.

Homepage: `spike_course_hub.html` at the repo root (there is no `index.html`).

## Pages

| File | What it is |
|---|---|
| `spike_course_hub.html` | Course home. The session list, how a session runs, a link to the robot page. |
| `session01_advanced_driving_base.html` | Session 1. A team of four builds the Advanced Driving Base, then moves it forward, backward, and through a turn with Python. Adapted from LEGO's lesson "Assembling an Advanced Driving Base". |
| `robot_advanced_driving_base.html` | The class robot: links to LEGO's five building books, the port map, the wheel table, and the test field drawn to scale. |
| `runs.csv` | The run log for the reference robot. Empty so far. |

## Build

Pages are generated, never edited by hand.

    python3 build/render.py              # writes the pages into the repo root
    python3 build/validate.py            # guard 1: structure, prose rules, links, 90 minutes
    python3 build/runcheck.py            # guard 2: programs, arithmetic, run log
    python3 build/runcheck.py --release  # also fails while a measured result is not logged

| Generator | Holds |
|---|---|
| `build/session01.py` | Session 1: its programs and every word on its page |
| `build/robot.py` | Port map, LEGO's links, the field and robot figures |
| `build/wheel.py` | Wheel arithmetic: degrees of motor turn to centimetres |
| `build/standards.py` | Standards, as retrieved, with CASE identifiers |
| `build/hl.py` | Python code colors, from the beginner Python course's build |
| `build/spike_stub/` | Stand-ins for the SPIKE App 3 modules, so the guard can run each program on a computer |

## Logging runs

Each measured result needs three runs on the reference robot. Add one row per run to
`runs.csv`, with the program id that the session's teacher panel and `runcheck.py`
print, then rebuild. A run counts only while its program id matches the program on
the page, so a result cannot outlive a change to its program.

    date,session,chunk,project,program_id,run,battery,result,unit,notes
    2026-11-16,1,chunk1,Jonathan_session01,95fe2ae2,1,100,54,cm,

## Locked decisions, 12 November 2026

1. **Python.** This course uses Python in the SPIKE App 3, by Jonathan's direction.
   The style guide's default (section 17) is Word Blocks only for grades 4 and 5;
   the guide needs that line changed, or this course named as the exception.
2. **The class robot is the Advanced Driving Base.** Port map: A is the left drive
   motor and E is the right drive motor, as LEGO's own programs for this robot say.
   The style guide's default port map is the Rhinobot's (A and B).
3. **One frame for every program.** `async def main():` at the top and
   `runloop.run(main())` at the bottom are handed over working in session 1 and are
   not explained yet. A later session takes them apart; it is not written.
4. **One wheel figure.** One full turn of the wheel moves the robot 27.63 cm, the
   figure in LEGO's Python programs. Pages print whole centimetres.
5. **One measuring point.** From the start line to the robot's front edge.
6. **Session 1 has no opener.** There is no earlier session to bring back. That time
   goes to building the robot.
7. **Standards.** New York science (engineering design) and New York mathematics
   only, retrieved through the Learning Commons Knowledge Graph on 12 November 2026.
   No computer science codes.

## Release log

### 12 November 2026, first printing (version pin 1)

What was made: the hub, session 1, and the robot page, with the build and both guards.

What was checked:

- `validate.py` passes on all three pages.
- `runcheck.py`: all five programs on the session page run cleanly against the
  stand-in modules and ask for exactly the moves the page says; the wheel arithmetic
  is recomputed and matches.
- Layout looked at in a browser at 1280px and 390px with every reveal open. No
  sideways scroll.
- Function signatures (`motor_pair.pair`, `motor_pair.move_for_degrees`,
  `runloop.run(main())`), a minus sign for backward, and the direction of positive
  steering were checked against published SPIKE App 3 references.

What is not done, so this is not release-ready under section 16 of the style guide:

- **Nothing has been run on a real hub or a real robot.** No measured result is on any
  page. Four results wait for three logged runs each: chunk 1, chunk 2, chunk 3, and
  the mission. Until then each reveal shows the computed result and asks students to
  measure their own run.
- **Ports B, C, D, and F on the robot page are not confirmed** against a built robot.
  Session 1 uses only A and E.
- The mission's 5 cm target zone is a first choice. If the reference robot's spread is
  wider, the zone or the program changes before release.
- The 45 minutes for the build is an estimate for grades 4 and 5. LEGO gives 30
  minutes for grades 6 to 8.
- Not built yet: a separate field page, the constraints page, the standards map, the
  ledger card, a starter project file, and extra cards. Dates are not set.
