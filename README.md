# SPIKE Prime with Python

LEGO SPIKE Prime robotics for grades 4 and 5, in sessions of 90 minutes, written in
Python for the SPIKE App 3. Part 1 is sessions 1 to 4 and stands on its own. Part 2 is
sessions 5 to 8, for a class that finishes early or continues for another term. The class robot is LEGO's Advanced Driving Base. The
house style is the SPIKE Prime Course Style Guide, snapshot of 12 November 2026.

**Open the course: [silvermanjonathan.github.io/legospikerobotics/spike_course_hub.html](https://silvermanjonathan.github.io/legospikerobotics/spike_course_hub.html)**

The homepage is `spike_course_hub.html` at the repo root (there is no `index.html`).
The site is served by GitHub Pages from the root of the `main` branch.

## Pages

| File | What it is |
|---|---|
| `spike_course_hub.html` | Course home. The four sessions, how a session runs, links to everything else. |
| `session01_advanced_driving_base.html` | Session 1. A team of four builds the robot, then moves it forward, backward, and through a turn. Adapted from LEGO's lesson "Assembling an Advanced Driving Base". |
| `session02_quarter_turn_and_square.html` | Session 2. Names for numbers, the quarter turn found by testing, a square the long way and with a `for` line. Tells students the final mission. |
| `session03_stop_at_the_line.html` | Session 3. The colour sensor's reflected light, and moving until a line. |
| `session04_delivery_run_and_demo.html` | Session 4. No new Python. The delivery run, then the demo for families. |
| `session05_count_the_lines.html` | Session 5, part 2. The hub beeps and shows numbers; the robot counts shelf lines and stops at the one called. |
| `session06_turns_that_measure_themselves.html` | Session 6. The motion sensor; a turn that ends on a measurement; counted and measured turns compared on the square. |
| `session07_follow_the_line.html` | Session 7. `if`, `else`, `while`, and a line follower with a stop bar, then timed runs. |
| `session08_your_own_functions_and_mission.html` | Session 8. The students' own functions; each team writes and runs its own mission; second demo. |
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
| `build/session01.py` to `build/session08.py` | One session each: its programs and every word on its page |
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
3. **Two parts of four sessions.** Part 1 stands alone and session 4 is its demo for
   families; its final mission is told to students in session 2. Part 2 opens what
   part 1 never used: sound and the light matrix, the motion sensor, `if` and `while`,
   the second colour sensor, slower speeds, and the students' own functions.
4. **Machinery handed over.** The frame (`async def main():`, `runloop.run(main())`)
   is handed over in session 1 and opened in session 8. The word `lambda` and the
   `[0]` after `tilt_angles()` are never opened.
5. **Teams fill in their own numbers.** No turn number, sensor port letter, or
   reflected light reading is printed as a fact. The programs carry first tries (180,
   `port.B`, 50) that each team replaces by testing.
6. **Session 1 has no opener.** That time goes to building the robot.
7. **Standards.** New York science (engineering design) and New York mathematics
   only, retrieved through the Learning Commons Knowledge Graph on 12 November 2026.

## Release log

### 12 November 2026, fourth printing (version pin 4)

What changed: on the hub, the Part 1 and Part 2 pills at the top are now links that
jump to their lists of sessions. Nothing else changed.

What was checked: both guards pass.

### 12 November 2026, third printing (version pin 3)

What changed: part 2 added, sessions 5 to 8. The hub, field page, constraints page,
standards map, and ledger card now cover both parts. Sessions 1 to 4 say "Part 1" in
their mastheads; their programs did not change, so their program ids are the same.

What was checked:

- `validate.py` passes on all 14 pages. It now also checks that each mission's minutes
  match its timing row.
- `runcheck.py`: all 38 programs run cleanly against the stand-in modules and ask for
  what their pages say, in order. Both branches of the `if` and both edges of the line
  follower were run against scripted readings.
- Layout looked at in a browser at 1280px and 390px with every reveal open.
- The new functions were checked against published SPIKE App 3 material:
  `await sound.beep(450, 500, 100)` and `await light_matrix.write(str(...))` appear in
  LEGO's own Python lessons, `light_matrix.write` without `await` in a published
  tutorial, and `motion_sensor.reset_yaw(0)` followed by a short wait and
  `abs(motion_sensor.tilt_angles()[0])` in a published turn test. That test also
  measured the robot ending past its target angle, which session 6 teaches.

What is not done, on top of the list under the second printing:

- **Thirty measured results are pending now**, fifteen of them in part 2.
- **Part 2 leans harder on the two colour sensors.** Session 7 needs them far enough
  apart for one to sit over the tape while the other is over the floor. Check that on
  a built robot before planning part 2.
- **Session 5's line spacing (20 cm) is a first choice.** If the reference robot
  miscounts, widen it.
- **Session 7's first tries (steering 30, speed 150) come from a published follower
  for a different robot.** They may need changing before the first class.

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
