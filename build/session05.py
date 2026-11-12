"""Session 5 (part 2): sound, the light matrix, and counting lines.

Part 2 is for a class that finishes sessions 1 to 4 early or continues for another
term. It opens things part 1 never used: the hub's speaker and light matrix here,
the motion sensor in session 6, while and if in session 7, and the students' own
functions in session 8.

light_matrix.write and sound.beep are called without await inside the counting loop,
on purpose: the robot keeps moving while they happen, and a wait there could carry
the sensor past the next line.
"""

from robot import shelves_figure, SHELF_GAP_CM, SHELVES

C1 = '''from hub import light_matrix, sound
import runloop


async def main():
    light_matrix.write("3")
    await sound.beep(440, 500, 100)
    await sound.beep(880, 500, 100)


runloop.run(main())'''

HEAD = '''from hub import %sport%s
import color_sensor
import motor_pair
import runloop

LINE_SENSOR = port.B
DARK = 50
%s

async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

'''
END = '''


runloop.run(main())'''
UNDER = "await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) < DARK)"
OVER = "await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) > DARK)"

C2 = (HEAD % ("", "", "") + '''    # Start the wheels. Wait for the tape, then wait for the floor again. Stop.
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=250)
    ''' + UNDER + "\n    " + OVER + '''
    motor_pair.stop(motor_pair.PAIR_1)''' + END)


def counter(show):
    return (HEAD % ("light_matrix, ", ", sound", "SHELF = 3\n")
            + '''    # Start the wheels. Count the lines. Stop after the last one.
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=250)
    for count in range(SHELF):
        ''' + UNDER + '''
        light_matrix.write(str(''' + show + '''))
        sound.beep(440, 200, 100)
        ''' + OVER + '''
    motor_pair.stop(motor_pair.PAIR_1)''' + END)


C3 = counter("count")
MISSION = counter("count + 1")
HINGE = "    for count in range(SHELF):\n        light_matrix.write(str(count + 1))"

LINE = [80, 10, 80]
STARTED, STOPPED = ("start", 0, 250), ("stop",)


def crossing(shown):
    return [("show", shown), ("beep", 440, 200)]


SETUP = ("Setup: the robot is behind the start line with its front edge on the line, "
         "facing the shelf lines. It starts here on every run.")

SESSION05 = {
    "num": 5,
    "part": 2,
    "slug": "session05_count_the_lines",
    "title": "Beep, show a number, and count the lines",
    "subtitle": ("The hub makes sounds and shows numbers. The robot crosses a row of lines "
                 "and stops after the one you choose."),
    "new": ["sound.beep", "light_matrix.write", "str", ">"],
    "new_text": ("<code>sound.beep</code> plays a note on the hub's speaker. "
                 "<code>light_matrix.write</code> shows text on the hub's square of lights. "
                 "<code>str</code> turns a number into text. The sign <code>&gt;</code> "
                 "means \"is greater than\"."),
    "reuse": ("Moving until the line from session 3, and the <code>for</code> line from "
              "session 2. For the first time, the name <code>count</code> in the "
              "<code>for</code> line gets used."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. If it was taken apart, rebuild it from the "
            "five building books before anything else.",
            "Every cable is pushed all the way into its port.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session05</code>.",
            "Your ledger card is on the table, with your sensor's port letter and your "
            "number for <code>DARK</code>. If the room or the floor has changed, measure "
            "your two readings again with the program from session 3.",
        ],
        "after": ("The program in chunk 1 is today's test run. It needs no motors and no "
                  "sensor, only the hub."),
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from sessions 1 to 4?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("Three lines move the robot until a line of tape. What does each one do?",
             ["The first starts the wheels. The second waits until the reflected light is "
              "less than <code>DARK</code>. The third stops the wheels."]),
            ("Some lines start with <code>await</code> and some do not. What is the "
             "difference?",
             ["A line with <code>await</code> makes the hub finish that job before the next "
              "line starts. A line without it only starts the job, and the hub goes "
              "straight on."]),
            ("What does <code>for count in range(4):</code> do?",
             ["It runs the lines inside it 4 times."]),
            ("Why does each team have its own number for <code>DARK</code>?",
             ["Each team measured its own floor and its own tape. The number has to sit "
              "between those two readings."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "The hub can show and beep",
            "teach": [
                "Line 6 shows the text inside the quote marks on the <b>light matrix</b>, "
                "the square of 25 lights on the hub. Lines 7 and 8 each play one note.",
                "A beep has three numbers. The first is the pitch: a bigger number is a "
                "higher note. The second is how long the note lasts, counted in thousandths "
                "of a second, so 500 is half a second. The third is how loud, from 0 to 100.",
            ],
            "code": C1,
            "where": "Type the whole program. It uses no motors, so the robot stays still.",
            "parts_title": "The parts of line 7",
            "parts": [
                ("440", "The pitch of the note. A bigger number is a higher note."),
                ("500", "How long the note lasts: 500 thousandths of a second, which is half a second."),
                ("100", "How loud, from 0 to 100."),
            ],
            "figure": shelves_figure(caption="The field for today, from above. Chunk 1 does "
                                     "not use it yet."),
            "setup": "Setup: the robot sits anywhere on the table. It does not move in this program.",
            "predict": ("Which note is higher, the first or the second? Is the 3 already on "
                        "the light matrix while the first note plays?"),
            "hints": ["Compare the first number on line 7 with the first number on line 8.",
                      "Line 6 has no <code>await</code>. What does the hub do after it starts "
                      "line 6?"],
            "reveal": [
                "The first one: the second note is higher. Its pitch is 880 and the first "
                "note's pitch is 440.",
                "The second one: yes. Line 6 has no <code>await</code>, so the hub starts "
                "showing the 3 and goes straight on to line 7. Lines 7 and 8 have "
                "<code>await</code>, so the second note waits for the first to finish.",
            ],
            "computed": "the 3 shows\nfirst note, pitch 440, half a second\nsecond note, pitch 880, half a second, higher",
            "measure": ("Change one number on line 7 and say what you expect before you run "
                        "it. Try the second number first."),
            "unit": "which note is higher",
            "expect": [("show", "3"), ("beep", 440, 500), ("beep", 880, 500)],
        },
        {
            "key": "chunk2",
            "title": "Cross one line and stop after it",
            "teach": [
                "Line 16 is the wait you know: it waits until the reflected light is less "
                "than <code>DARK</code>, which happens when the sensor reaches the tape.",
                "Line 17 is new. The sign <code>&gt;</code> means \"is greater than\". "
                "Line 17 waits until the reflected light is greater than <code>DARK</code> "
                "again, which happens when the sensor has left the tape.",
            ],
            "code": C2,
            "where": ("Put your own port letter on line 6 and your own number on line 7 before "
                      "the first run."),
            "figure": shelves_figure(caption="The shelf lines from above. Chunk 2 uses the "
                                     "first one, %d cm from the start line." % SHELF_GAP_CM),
            "setup": SETUP,
            "predict": ("Where is the colour sensor when the wheels stop: before the first "
                        "shelf line, over it, or just past it?"),
            "hints": ["The hub reaches line 18 only after line 17 has finished waiting. What "
                      "was line 17 waiting for?"],
            "reveal": [
                "Just past it. Line 16 waits for the tape. Line 17 then waits for the pale "
                "floor on the far side of the tape. Only then does line 18 stop the wheels.",
                "Crossing a line takes two waits: one to reach it and one to leave it.",
            ],
            "computed": "start the wheels\nwait for the tape\nwait for the pale floor after the tape\nstop the wheels",
            "measure": ("Look under the robot after it stops. Is the tape just behind the "
                        "sensor?"),
            "unit": "sensor before, over, or past the line",
            "script": LINE,
            "expect": [("pair", "A", "E"), STARTED, STOPPED],
        },
        {
            "key": "chunk3",
            "title": "Count the lines",
            "teach": [
                "Line 8 names the shelf to stop after. The <code>for</code> line on line 17 "
                "runs the four lines inside it once for each shelf line: wait for the tape, "
                "show a number, beep, wait for the floor.",
                "Each time round, <code>count</code> holds a number. Line 19 turns that "
                "number into text with <code>str</code>, because the light matrix shows "
                "text. Lines 19 and 20 have no <code>await</code>, so the robot keeps "
                "moving while the hub shows and beeps.",
            ],
            "code": C3,
            "where": ("Lines 18 to 21 are inside the <code>for</code> line, eight spaces in. "
                      "Line 22 is back at four spaces, so it runs once, after the last line "
                      "has been counted."),
            "figure": shelves_figure(caption="The shelf lines from above: %d lines, %d cm apart."
                                     % (SHELVES, SHELF_GAP_CM)),
            "setup": SETUP,
            "predict": ("How many lines does the robot cross before it stops? What number is "
                        "on the light matrix as it crosses the first line: 0 or 1?"),
            "hints": ["Line 8 says <code>SHELF = 3</code>, and line 17 uses it.",
                      "Run it and watch the hub as the robot crosses the first line."],
            "reveal": [
                "The first one: 3 lines. <code>range(SHELF)</code> is <code>range(3)</code>, "
                "so the hub runs lines 18 to 21 three times, then line 22 stops the wheels.",
                "The second one: 0. Python starts counting at 0, so <code>count</code> is 0, "
                "then 1, then 2. The robot crosses three lines and the last number it shows "
                "is 2.",
                "To show 1, 2, 3, change line 19 so it shows <code>count + 1</code>. The "
                "mission program does that.",
            ],
            "computed": "line 1: shows 0, beeps\nline 2: shows 1, beeps\nline 3: shows 2, beeps\nthe wheels stop after line 3",
            "measure": "Count the beeps aloud with your team as the robot goes.",
            "unit": "lines crossed",
            "script": [80, 10, 80, 10, 80, 10, 80],
            "expect": ([("pair", "A", "E"), STARTED] + crossing("0") + crossing("1")
                       + crossing("2") + [STOPPED]),
        },
    ],
    "checks": [],

    "hinge": {
        "code": HINGE,
        "context": MISSION,
        "q": ("These two lines are from a program where line 8 says <code>SHELF = 4</code>. "
              "What numbers does the light matrix show, in order?"),
        "a": [
            "1, 2, 3, 4. <code>count</code> goes 0, 1, 2, 3, and the line shows "
            "<code>count + 1</code> each time.",
        ],
    },

    "brief": {
        "minutes": 33,
        "title": "Deliver to the right shelf",
        "intro": [
            "The warehouse has four shelves in a row, and each shelf has a line of tape in "
            "front of it. An order comes in for one shelf. The cart has to count the lines "
            "as it passes them and stop at the right one, showing the shelf number as it "
            "goes.",
            "Your teacher calls the shelf number. Your team changes one line of the program "
            "and nothing else.",
        ],
        "figure": shelves_figure(caption="The mission from above. Shelf 1 is %d cm from the "
                                 "start line and the shelves are %d cm apart."
                                 % (SHELF_GAP_CM, SHELF_GAP_CM)),
        "values": [
            ("Start", "Behind the start line, front edge on the line."),
            ("Shelves", "%d lines of black tape, %d cm apart." % (SHELVES, SHELF_GAP_CM)),
            ("Done means", "The robot stops past the line of the shelf that was called and "
                           "before the next line, and the last number it showed is that "
                           "shelf's number."),
            ("You may change", "Only line 8, once the program works."),
            ("Speed", "<code>velocity=250</code>."),
        ],
        "code": MISSION,
        "code_note": ("Start from this program. It is chunk 3 with line 19 changed to show "
                      "<code>count + 1</code>."),
        "steps": [
            "Run it with <code>SHELF = 3</code> and fill in row 1.",
            "Your teacher calls a shelf. Change line 8, fill in Expected, and run.",
            "If the robot miscounts, look at where it happened. Write down what you think "
            "went wrong before you change anything.",
        ],
        "sheet_head": ["Run", "Shelf called", "Expected: last number shown, and where it stops",
                       "Measured: last number shown", "Stopped at the right shelf?"],
        "sheet_rows": [["1", "3"], ["2", None], ["3", None], ["4", None]],
        "script": [80, 10, 80, 10, 80, 10, 80],
        "expect": ([("pair", "A", "E"), STARTED] + crossing("1") + crossing("2")
                   + crossing("3") + [STOPPED]),
    },

    "exits": {
        "floor": ("The robot crosses one line and stops just past it, and each builder can "
                  "say why crossing a line takes two waits."),
        "middle": ("The robot stops at the right shelf for 3 different shelf numbers, with "
                   "only line 8 changed, and shows 1, 2, 3 on the way."),
        "stretch": ("The cart comes home. After it stops, a second <code>for</code> line "
                    "moves it backward over the same number of lines to the start. "
                    "<code>velocity=-250</code> on a <code>motor_pair.move</code> line moves "
                    "the robot backward."),
    },

    "ledger_code": ("light_matrix.write(str(count + 1))\nsound.beep(440, 200, 100)\n"
                    "await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) > DARK)"),
    "ledger_context": MISSION,
    "ledger": ("Session 5. Show a number, play a note, and wait until the sensor has left "
               "the tape. Python starts counting at 0."),
    "stamp": ("To get today's stamp, tell your teacher why the first number the robot showed "
              "in chunk 3 was 0."),

    "teacher": {
        "before": [
            "If the robots were taken apart since session 4, the rebuild takes most of a "
            "session. Plan a build session before this one.",
            "Charge every hub. Turn the hub's volume up, and warn the room next door.",
            "Lay out one lane for every two teams: a start line and %d shelf lines of black "
            "tape, %d cm apart, on a pale floor." % (SHELVES, SHELF_GAP_CM),
            "Log three runs of each program on the reference robot. If it miscounts at "
            "%d cm, widen the gap and change the field page." % SHELF_GAP_CM,
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, show and beep", 10),
            ("0:25", "Chunk 2, cross one line", 10),
            ("0:35", "Chunk 3, count the lines", 12),
            ("0:47", "Hinge question", 3),
            ("0:50", "Mission", 33),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("Chunk 1 is loud and popular. Give it its ten minutes and then move on. "
                   "Stopping at the floor exit is a finish."),
        "misconceptions": [
            ("The robot stops on the first line instead of past it.",
             "Line 17 is missing or has <code>&lt;</code> where <code>&gt;</code> belongs. "
             "Read lines 16 and 17 aloud together."),
            ("The robot counts one line twice, or skips a line.",
             "Ask for the team's two readings and <code>DARK</code>. A <code>DARK</code> "
             "close to the floor reading makes the sensor flicker at the tape's edge."),
            ("A team puts <code>await</code> on the beep inside the loop and the robot "
             "miscounts.",
             "Ask what the robot does while the hub waits for the beep to finish. It keeps "
             "moving, and the sensor can pass the next line unread."),
            ("A student expects the first number to be 1.",
             "That is the prediction in chunk 3. Let the run answer it, then ask what "
             "<code>count + 1</code> does."),
            ("Line 22 is typed inside the <code>for</code> line.",
             "The robot stops after one line. Count the spaces in front of line 22 "
             "together: four."),
        ],
        "standards": ["3-5-ETS1-3", "NY-4.MD.2"],
        "routing": ("If time is short, skip the stretch and keep the mission to two called "
                    "shelves. Chunk 1 can shrink to one run."),
        "deliberate": ("Chunk 3 shows <code>count</code>, so the numbers start at 0, on "
                       "purpose. The mission program shows <code>count + 1</code>."),
    },
}
