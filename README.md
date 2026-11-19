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
| `spike_course_hub.html` | Course home. The sessions, how a session runs, links to everything else. |
| `session01_advanced_driving_base.html` | Session 1. A team of four builds the robot, then moves it forward, backward, and through a turn. Adapted from LEGO's lesson "Assembling an Advanced Driving Base". |
| `session02_quarter_turn_and_square.html` | Session 2. Names for numbers, the quarter turn found by testing, a square the long way and with a `for` line. Tells students the final mission. |
| `session03_stop_at_the_line.html` | Session 3. The colour sensor's reflected light, and moving until a line. |
| `session04_delivery_run_and_demo.html` | Session 4. No new Python. The delivery run, then the demo for families. |
| `session05_count_the_lines.html` | Session 5, part 2. The hub beeps and shows numbers; the robot counts shelf lines and stops at the one called. |
| `session06_turns_that_measure_themselves.html` | Session 6. The motion sensor; a turn that ends on a measurement; counted and measured turns compared on the square. |
| `session07_follow_the_line.html` | Session 7. `if`, `else`, `while`, and a line follower with a stop bar, then timed runs. |
| `session08_your_own_functions_and_mission.html` | Session 8. The students' own functions; each team writes and runs its own mission; second demo. |
| `builds_word_blocks.html` | More builds, in Word Blocks: the Game Master and the Grabbers, five block snippets each, with a prediction on each and a sheet to fill in. |
| `challenge_mat.html`, `challenge_mat.pdf` | The challenge mat for three robots: 24 sheets of letter paper to print and tape, three lanes, four missions, and the match. For every driving robot the class builds, with a colour, distance, or force sensor or with none. |
| `pieces_of_the_builds.html` | Every LEGO piece the three builds use, 61 of them: a drawing, a plain name, LEGO's own name and part number, and the builds that use it. Buttons show the pieces of one build. |
| `robot_advanced_driving_base.html` | The class robot: links to LEGO's five building books, the port map, the wheel table. |
| `field_test_field.html` | The test field for every session, drawn to scale. |
| `course_constraints.html` | What the course uses and when each thing is first taught, what it never uses, the locked decisions. Dated. |
| `standards_map.html` | Every standards code used, its full statement, CASE identifiers, and sessions. |
| `course_ledger_card.html` | The printable card: four stamps, the team's numbers, a reference strip, the port map, a fault table. |
| `runs.csv` | The run log for the reference robot. Empty so far. |
| `parts/` | One PNG drawing for each piece on the pieces page, made by `build/ldraw_render.py`. |

## Build

Pages are generated, never edited by hand.

    python3 build/render.py              # writes the pages into the repo root
    python3 build/validate.py            # guard 1: structure, prose rules, links, 90 minutes
    python3 build/runcheck.py            # guard 2: programs, arithmetic, run log
    python3 build/runcheck.py --release  # also fails while a measured result is not logged

| Generator | Holds |
|---|---|
| `build/session01.py` to `build/session08.py` | One session each: its programs and every word on its page |
| `build/blocks.py` | Draws Word Block stacks in HTML and CSS; holds the app's block colours and checks every one at 7:1 |
| `build/builds.py` | The Game Master and Grabbers snippets and the words on their page |
| `build/py2blocks.py` | Turns each Python program of sessions 1 to 4 into the same program in Word Blocks |
| `build/mat.py`, `build/mat_pdf.py` | The challenge mat's geometry and missions; the tool that writes its PDF |
| `build/parts.py` | Every piece the three builds use: plain name, LEGO's name and numbers, sets, builds, and how it is drawn |
| `build/ldraw_render.py` | A tool, run by hand: draws each piece from the LDraw parts library into `parts/`. The page build does not need it or the library. |
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

### 19 November 2026, version pin 13: the mat is for every version of the robot

What changed: the challenge mat's missions, numbers, and programs now fit every driving
robot the class builds, not only the Advanced Driving Base. The 24 sheets did not
change, only page 1 of the PDF, so a printed mat is still right.

- **Which robot is yours?** A table on the mat page: a robot with a colour sensor stops
  at the black dock; a robot with a distance sensor or a force sensor stops at a wall (a
  box, not a printed mark); a robot with no sensor stops by a number. It also lists
  LEGO's versions: Driving Base, Driving Base with the distance sensor, Driving Base
  with the colour sensor, Advanced Driving Base.
- **Find your robot's numbers.** One full turn measured on the lane's ruler, and first
  tries in degrees of motor turn for big wheels (27.63 cm) and small wheels (17.5 cm).
- **Stop at the dock with a sensor.** Session 3's colour sensor program, and two new
  programs, each in Python and Word Blocks: `distance_sensor.distance` and
  `force_sensor.pressed` in the same start, wait, stop shape.
- **Missions 3 and 4.** After a lane swap a crew with a sensor changes nothing and a
  crew with no sensor changes one number. A wall moves with its robot. Points are the
  same for every kind of robot, 190 in all.
- The constraints page has a new section 9 for these exceptions.

Where the facts came from: LEGO's lesson pages name the three Driving Base versions (no
sensors, with the Distance Sensor, with the Color Sensor). The small wheel figure is
arithmetic from a wheel 5.6 cm across.

What was checked: both guards pass. Three sheets of the new PDF were compared with the
old one and are identical.

What is not done: the distance and force sensor programs and their block stacks have
not been run on a hub or built in the SPIKE App. The Driving Base's ports are not named
because they were not read from a robot. No robot of any version has run on the mat.

### 19 November 2026, version pin 12: colourful space stations

Each dock now has a space station drawn in colour: blue solar panels and an orange hub
above the dock, and an orange hull with purple bands and windows just past it. The
panels sit above the strip the colour sensor travels, and the hull is past the black
line, so the sensor reaches colour only after the dock has already stopped the robot.
Not yet read with a colour sensor.

### 19 November 2026, tenth printing (version pin 11): space mat

What changed: the challenge mat has a space theme and one start in each lane.

- Each lane is a rocket (red, blue, green) with a launch pad, a space station with a
  black dock line, an asteroid, and a moon base, plus stars and a planet as decoration.
- Start B is gone. The docks are 55, 50, and 45 cm from the launch line instead, so a
  set distance works in one lane only. Mission 3, Swap ships, moves every team one lane
  down with no change to the program, which only a program that waits for the colour
  sensor passes.
- A bonus mission, Moon dance: after landing, spin all the way around with four quarter
  turns. 190 points in all.
- The mat page's teacher panel has the computed degrees of motor turn for each lane.

What was checked: both guards pass. The 24 sheets were rendered and laid side by side.
No picture is printed where the middle of the robot passes between the launch line and
the dock, and each dock sits inside one sheet.

What is not done: nobody has run a robot on the mat, and no colour sensor has been read
over the printed dock or the tinted launch pad.


### 19 November 2026, ninth printing (version pin 10)

What changed:

- **A Word Blocks panel under every program.** Python stays on screen for everyone.
  Under each Python program on all eight session pages is a closed panel marked Word
  Blocks; opening it shows the same program as blocks, so a builder who works in blocks
  follows the same lesson as the Python builders beside them. 55 panels in all. A box
  at the top of each session page explains the panels and has a button that opens or
  closes every panel at once; with them open, the pager carries the choice to the next
  page (`#wb`). Closed panels do not print. This replaces the seventh printing's
  Python / Word Blocks switch, which hid the Python.
- **Sessions 5 to 8 now have blocks too.** `build/py2blocks.py` now draws beeps, the
  light matrix, the motion sensor, waits in seconds, `if` and `else`, `while`, the
  count in a `for` loop, more than one speed, and My Blocks for the students' own
  functions. Each panel's note says where the two languages count differently (speed
  as a percent, the turn in whole ones not tenths, seconds not thousandths, note
  numbers not pitches). The build stops if a program on a session page has no panel.
- **Fix:** a left turn is now drawn as `left: -100`, the way LEGO's own images show it,
  not `left: 100`.
- The constraints page has a new section 8 on the panels; the hub says they are there.

Where the facts came from:

- **Block words**: LEGO lesson images for Training Camp 3 (if then else, start moving
  left: -50, reflected light), My Code, Our Program (define and call blocks, and the My
  Blocks colour, #FF6680), and Mission Ready; LEGO coach slides and FLLCasts tutorials
  for set yaw angle to 0 and the yaw angle reporter; FLLCasts for the beep blocks.
- **Note numbers**: 440 Hz is note 69 and 880 Hz is note 81 (`py2blocks.midi`).

What was checked: both guards pass. Every panel was read against its Python program.

What is not done: the Part 2 stacks were written from the Python and have not been
built and run in the SPIKE App. The beep and yaw block wordings come from tutorials, not
from a LEGO lesson image. Build one Part 2 stack in the app before the class uses it.

### 18 November 2026, eighth printing (version pin 9)

What changed: the challenge mat is now for three robots at once. It is 24 upright letter
sheets, 4 across and 6 down, about 86 cm by 168 cm, with three identical lanes, each two
sheets tall. Each lane has its own starts, far line, island, and drop zone, so one
program works in any lane and each team can tape its own lane. The class has one score:
each mission gives 10 points to every robot that does it and a bonus when all three do
it on the same run, 170 points in all. The match is 3 minutes with all three robots on
the mat. The PDF is 25 pages.

What was checked: both guards pass. The 24 sheets were rendered and laid side by side to
check that no label is cut off and no mark a mission needs falls in a sheet's blank edge.

What is not done: nobody has run a robot on the mat. The space between lanes assumes a
robot about 22 cm long and 20 cm wide. Tape one lane and try it before printing all three.


### 18 November 2026, seventh printing (version pin 8)

What changed:

- **Python or Word Blocks.** Sessions 1 to 4 have two buttons under the masthead, Python
  and Word Blocks. Word Blocks draws every program on the page as a block stack, 42
  programs and snippets in all. Each block shows the number of the Python line it
  matches, so the page's text ("line 12") still points at one block. A link ending in
  `#wb` opens a page in Word Blocks, and the pager carries the choice to the next page.
  Sessions 5 to 8 are Python only.
- **`build/py2blocks.py`** turns each Python program into its block stack, so the two
  cannot drift apart. The build stops if a program on a session 1 to 4 page has no stack.
- **Challenge mat.** `challenge_mat.html` and `challenge_mat.pdf`: 12 sheets of letter
  paper, taped 4 across and 3 down into a mat about 112 cm by 65 cm, with four missions
  worth 80 points, one or two for each of sessions 2, 3, and 4, and a 2 minute match.
  The hub and the three session pages link to it. `build/mat.py` draws it and
  `build/mat_pdf.py` writes the PDF.

Where the facts came from:

- **Block words and the Movement colour**: read and sampled on 18 November 2026 from the
  program image on LEGO's lesson page Training Camp 1: Driving Around.
- **The speed**: Python's `velocity=250` is 250 degrees of motor turn each second. The
  large motor's top speed is 1050, so the block is `set movement speed to 24 %`
  (250 / 1050, to the nearest whole percent). About the same speed, not exactly.
- **The mat**: the far line is 55 cm from start A (`robot.FAR_CM`); every other distance
  comes from `build/wheel.py`.

What was checked: both guards pass on all 17 pages. The PDF has 13 letter pages. The
twelve sheets were rendered and laid side by side to check that no mark a mission needs
falls in the blank strip at a sheet's edge. Pages were looked at at 1280px and 390px.

What is not done:

- **No block stack was built or run in the SPIKE App**, and no Python program has logged
  runs either. In particular, a negative number of degrees in a move block (session 1,
  moving backward) is assumed to move the robot backward, as it does in Python.
- **Nobody has run a robot on the mat.** The drop zone, island, and home marks assume a
  robot about 22 cm long with its wheels about 11 cm behind its front edge. The mat
  page's teacher panel says what to test first.
- **The page text still names Python lines** when Word Blocks is chosen.


### 13 November 2026, sixth printing (version pin 7)

What changed: a new page, `pieces_of_the_builds.html`, with a card for each of the 61
LEGO pieces that the Advanced Driving Base, the Game Master, and the Grabbers use.
Each card has a drawing, a plain name, the colour, LEGO's own name and part number,
and the builds that use the piece. Buttons show one build's pieces; a link ending in
`#adb`, `#gm`, or `#gr` opens the page already filtered. The hub, the robot page, and
the Word Block page link to it. The teacher panel has a table with LEGO's name, part
number, element number, the set each piece comes in, and LDraw's name for it.

Where the facts came from:

- **Which pieces each build uses**: read from LEGO's ten building books, page by page
  in a browser, on 13 November 2026 (the first four pages of book 3 on 18 November). Pieces that look alike at page size (black peg
  and black axle peg, grey long peg with a stop, the cross blocks, the rubber joiner)
  were read again at twice the size.
- **LEGO's names, part numbers, and element numbers**: LEGO's parts lists for sets
  45678 and 45681 as Brickset publishes them. Names are copied letter for letter.
- **Second check**: every part number was looked up in the LDraw parts library and
  its name there had to describe the same piece. Every piece and colour read from a
  book also had to be on the parts list of a set that build needs. All 61 passed, and
  `build/parts.py` stops the build if a Game Master or Grabbers piece is not in the
  SPIKE Prime set.
- **Drawings**: made by `build/ldraw_render.py` from LDraw geometry (CC BY 4.0), not
  copied from LEGO.

What was checked: both guards pass on all 16 pages. `validate.py` now also checks that
every picture has alt text and its file, and that the cards match `build/parts.py`. The
page was looked at in a browser at 1280px and 390px with the teacher panel open, and
the filter buttons and `#gm` link were tried.

What is not done:

- **No counts.** The page says which pieces a build uses, not how many.
- **Not checked against a built model.** Check the list against the reference robot
  when it is built.


### 12 November 2026, fifth printing (version pin 6)

What changed: a new page, `builds_word_blocks.html`, with Word Block snippets for two
more LEGO models, the Game Master and the Grabbers, five each. These are SPIKE App
Word Blocks, not Python, by Jonathan's direction. The hub has a new section and pill
for it, and the constraints page has a new section 7 listing the blocks it uses.

How the blocks are drawn: in HTML and CSS by `build/blocks.py`, as section 9 of the
style guide asks. Each category keeps the SPIKE App's own hue, sampled from LEGO's
program images for these two models, lightened toward white only as far as black
block words need to clear 7:1. The validator recomputes every ratio and checks every
C block's arm.

What came from LEGO: the ports (Game Master A and B, Grabbers A and E), the 2.1
seconds and 95 degrees of motor turn on the Game Master, the motor directions on the
Grabbers, the block words, and the sound names, all from LEGO's own block programs
on its lesson pages. The snippets themselves are written for this course.

What was checked: both guards pass on all 15 pages; the page was looked at in a
browser at 1280px and 390px.

What is not done:

- **The snippets have not been run on a hub.** There is no runner for Word Blocks
  here, so each stack was checked by hand against LEGO's published blocks.
- **Check on a built Grabbers model that counterclockwise closes the claw**, and in
  the app that the force sensor's question block offers "released".
- **Check on a built Game Master that 95 degrees of motor turn moves the candy stick
  one brick.**

### 12 November 2026, fourth printing (version pin 5)

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
