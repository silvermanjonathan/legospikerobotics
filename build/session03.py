"""Session 3: the colour sensor, and moving until a line.

One way to move until a sensor says stop, used in every program from here on:

    motor_pair.move(...)              start the wheels
    await runloop.until(lambda: ...)  wait until the sensor test is true
    motor_pair.stop(...)              stop the wheels

The word lambda is handed over as part of the frame of that line and is not
explained. With four sessions there is no later session to take it apart.

No reflected light reading is printed on the page as a fact: each team measures its
own floor and its own tape and chooses DARK between them. The reference robot's two
readings go in runs.csv.
"""

from robot import field_figure, FAR_CM

READ = '''from hub import port
import color_sensor
import runloop

LINE_SENSOR = port.B


async def main():
    print(color_sensor.reflection(LINE_SENSOR))


runloop.run(main())'''


def drive(dark):
    return '''from hub import port
import color_sensor
import motor_pair
import runloop

LINE_SENSOR = port.B
DARK = %d


async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Start the wheels. Wait until the sensor is over the line. Stop the wheels.
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=250)
    await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) < DARK)
    motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())''' % dark


C2 = drive(50)
C3 = drive(0)
C3_HIGH = drive(101)
UNTIL = "    await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) < DARK)"

# Readings the guard feeds the stand-in sensor: a pale floor, then a dark line. They
# are test inputs for the build only and appear on no page.
FLOOR_THEN_LINE = [80, 80, 80, 80, 10]
FLOOR_ONLY = [80]

STARTED, STOPPED, NEVER = ("start", 0, 250), ("stop",), ("never",)

SETUP = ("Setup: the robot is behind the start line with its front edge on the line, "
         "facing the far line. It starts here on every run.")

SESSION03 = {
    "num": 3,
    "slug": "session03_stop_at_the_line",
    "title": "Stop at the line with the colour sensor",
    "subtitle": ("The colour sensor measures the floor. The program waits for that "
                 "measurement to change, then stops the wheels."),
    "new": ["color_sensor.reflection", "print", "motor_pair.move", "runloop.until",
            "motor_pair.stop"],
    "new_text": ("<code>color_sensor.reflection</code> gives the sensor's measurement as a "
                 "number. <code>print</code> shows a number on the screen. "
                 "<code>motor_pair.move</code> starts the wheels, "
                 "<code>runloop.until</code> waits, and <code>motor_pair.stop</code> stops "
                 "the wheels."),
    "reuse": ("Names in capitals at the top of the program, and one change per run, from "
              "session 2."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. Nothing is loose and nothing is missing.",
            "Every cable is pushed all the way into its port. Port A holds the left wheel's "
            "motor and port E holds the right wheel's motor.",
            "Find a colour sensor on your robot and follow its cable to the hub. Write down "
            "the letter of its port. Today's programs need it.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session03</code>.",
        ],
        "after": ("The program in chunk 1 is today's test run. If it prints nothing, come "
                  "back to this list and check the sensor's port letter."),
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from session 2?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("A program has a name in capitals at the top, such as <code>FORWARD</code>. "
             "Why give a number a name?",
             ["You change the number in one place, and every line that uses the name "
              "changes with it. The name also says what the number is for."]),
            ("What does the line <code>for count in range(4):</code> do to the lines inside "
             "it?",
             ["It runs them 4 times, in order, one after another."]),
            ("The turn line counts degrees of motor turn. A quarter turn is 90 degrees of "
             "the robot's turn. Are those the same number?",
             ["No. Your team found its own number of degrees of motor turn for a quarter "
              "turn by testing."]),
            ("How did your team find its number for <code>QUARTER_TURN</code>?",
             ["By testing: change the one number, run, and write down what the robot did, "
              "until it faced along the second strip."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "The colour sensor measures reflected light",
            "teach": [
                "The colour sensor shines a light at the floor and measures how much of the "
                "light comes back. That measurement is called <b>reflected light</b>. It is "
                "a number from 0 to 100. More light coming back gives a bigger number.",
                "Line 5 names the port of the colour sensor. Line 9 measures the reflected "
                "light once and prints the number in the console, the part of the SPIKE App "
                "that shows what a program prints.",
            ],
            "code": READ,
            "where": ("Line 5 says <code>port.B</code>. If your colour sensor's cable goes to "
                      "a different port, change the letter on line 5 to your port's letter."),
            "figure": field_figure(far=True, caption="The field from above. Hold the robot so "
                                   "the colour sensor is over the pale floor for one run, and "
                                   "over the black tape of the far line for the next."),
            "setup": ("Setup: for run 1, the colour sensor is over the pale floor. For run 2, "
                      "the colour sensor is over the black tape. The robot does not move in "
                      "this program."),
            "predict": ("Which run prints the bigger number: the run over the pale floor, or "
                        "the run over the black tape?"),
            "hints": ["Which one sends more of the sensor's light back, a pale floor or black "
                      "tape?"],
            "reveal": [
                "The run over the pale floor prints the bigger number. A pale floor sends "
                "more of the light back to the sensor. Black tape sends less of it back.",
                "Write your own two numbers in the sheet below. Every floor and every tape "
                "is a little different, so your numbers are your own.",
            ],
            "computed": "pale floor: more light comes back, the bigger number\nblack tape: less light comes back, the smaller number",
            "measure": ("Run each one twice. If the two numbers for the floor are far apart, "
                        "check that the sensor is the same height above the floor each time."),
            "unit": "reflected light, floor then tape",
            "sheet": {
                "title": "Your two readings",
                "intro": "Write what the console prints.",
                "head": ["Where the sensor is", "Reflected light, run 1", "Reflected light, run 2"],
                "rows": [["Over the pale floor", None, None], ["Over the black tape", None, None]],
            },
            "script": [80],
            "expect": [],
            "prints": ["80"],
        },
        {
            "key": "chunk2",
            "title": "Move until the line",
            "teach": [
                "Choose a number between your two readings and put it on line 7. Its name is "
                "<code>DARK</code>. A reading less than <code>DARK</code> means the sensor "
                "is over the tape.",
                "Line 15 starts the wheels, and they keep turning. It has no "
                "<code>await</code>, because it only starts the move. Line 16 waits until "
                "the reflected light is less than <code>DARK</code>. The sign "
                "<code>&lt;</code> means \"is less than\". Line 17 stops the wheels.",
            ],
            "code": C2,
            "where": ("The 50 on line 7 is a first try. Replace it with your own number before "
                      "the first run. The word <code>lambda</code> and the colon after it are "
                      "part of the frame of line 16. Type them exactly."),
            "parts_title": "The three lines that move until the line",
            "parts": [
                ("motor_pair.move", "Line 15. Starts the wheels, straight, and does not wait."),
                ("runloop.until", "Line 16. Waits until the test after it is true."),
                ("< DARK", "The test: the reflected light is less than DARK."),
                ("motor_pair.stop", "Line 17. Stops the wheels."),
            ],
            "figure": field_figure(far=True, caption="The field from above for chunk 2. The far "
                                   "line is %d cm from the start line for run 1." % FAR_CM),
            "setup": SETUP,
            "predict": ("Run 1 has the far line %d cm from the start line. For run 2 you move "
                        "the far line to 30 cm and change nothing in the program. Does the "
                        "robot stop in the same place both times, or at the far line both "
                        "times?" % FAR_CM),
            "hints": ["Read line 16. What is the hub waiting for: a number of degrees of motor "
                      "turn, or a reading from the sensor?"],
            "reveal": [
                "At the far line both times. No line in this program says how far to move. "
                "Line 16 waits for the sensor's reading to drop below <code>DARK</code>, and "
                "that happens when the sensor reaches the tape, wherever the tape is.",
                "The robot stops with the far line somewhere under it, not with its front "
                "edge on the line. The sensor is not at the front edge.",
            ],
            "computed": "run 1: the wheels stop when the sensor reaches the far line\nrun 2: the wheels stop when the sensor reaches the far line\nthe program is the same; the place is different",
            "measure": ("Measure from the start line to the robot's front edge after each run "
                        "and write both numbers down."),
            "unit": "cm, far line at 55",
            "script": FLOOR_THEN_LINE,
            "expect": [("pair", "A", "E"), STARTED, STOPPED],
        },
        {
            "key": "chunk3",
            "title": "When DARK is the wrong number",
            "teach": [
                "The test on line 16 only works if <code>DARK</code> is between your two "
                "readings. This program has <code>DARK = 0</code>. Reflected light is never "
                "less than 0.",
                "Before you run it, find the large button in the middle of the hub. Pressing "
                "it stops a program. One builder keeps a hand ready beside the robot.",
            ],
            "code": C3,
            "where": "Change only line 7.",
            "figure": field_figure(far=True, caption="The field from above for chunk 3. One "
                                   "builder waits past the far line, ready to stop the program."),
            "setup": SETUP,
            "predict": ("With <code>DARK = 0</code>, does the robot stop at the far line? Then "
                        "think about <code>DARK = 101</code>: how far does the robot move?"),
            "hints": ["Line 16 waits until the reading is less than <code>DARK</code>. Can a "
                      "reading from 0 to 100 be less than 0? Can it be less than 101?"],
            "reveal": [
                "The first one: no. The robot moves over the far line and keeps moving, "
                "because no reading is less than 0. The test on line 16 is never true, so "
                "the hub never reaches line 17. Press the button in the middle of the hub.",
                "The second one: it hardly moves at all. Every reading is less than 101, so "
                "the test on line 16 is true at once and line 17 stops the wheels straight "
                "away.",
                "Put your own number back on line 7 before the mission.",
            ],
            "computed": "DARK = 0: the test is never true, the wheels are never stopped\nDARK = 101: the test is true at once, the wheels stop straight away",
            "measure": "Try <code>DARK = 101</code> as well and watch what the robot does.",
            "unit": "stops at the line, yes or no",
            "script": FLOOR_THEN_LINE,
            "expect": [("pair", "A", "E"), STARTED, NEVER],
        },
    ],
    "checks": [("DARK 101", C3_HIGH, [("pair", "A", "E"), STARTED, STOPPED], FLOOR_ONLY),
               ("DARK 50, no line", C2, [("pair", "A", "E"), STARTED, NEVER], FLOOR_ONLY)],

    "hinge": {
        "code": UNTIL,
        "context": C2,
        "q": ("Suppose a team measured 80 over its floor and 10 over its tape. These two "
              "numbers are made up for this question. Which value of <code>DARK</code> "
              "makes the robot stop at the line: 5, 40, or 95?"),
        "a": [
            "40. It is between the two readings. Over the floor the reading is 80, which is "
            "not less than 40, so the hub keeps waiting. Over the tape the reading is 10, "
            "which is less than 40, so the hub goes on to the stop line.",
            "With 5 the robot never stops, because 10 is not less than 5. With 95 it stops "
            "at once, because 80 is already less than 95.",
        ],
    },

    "brief": {
        "minutes": 31,
        "title": "The dock that moves",
        "intro": [
            "Your robot is a cart that brings parts to a loading dock. The dock's edge is "
            "the far line. The dock is moved every day, so the cart cannot count on a "
            "distance. It has to stop at the dock's edge wherever the edge is.",
            "Between runs, a builder from another team moves your far line.",
        ],
        "figure": field_figure(far=True, far_sub="black tape, 40 to 70 cm",
                               caption="The mission from above. The far line is put somewhere "
                               "from 40 to 70 cm from the start line."),
        "values": [
            ("Start", "Behind the start line, front edge on the line, facing the far line."),
            ("Far line", "40, 55, or 70 cm from the start line. It changes between runs."),
            ("Speed", "<code>velocity=250</code>."),
            ("Target", "The robot stops with the far line under it."),
            ("You may not", "Change the program between the three runs."),
        ],
        "code": C2,
        "code_note": ("Start from the program in chunk 2, with your own port letter on line 6 "
                      "and your own number on line 7."),
        "steps": [
            "Fill in the Expected column for all three rows before the first run.",
            "Run 1, with the far line at 55 cm. Measure and fill in the row.",
            "Ask a builder from another team to move the far line. Run again without "
            "changing the program.",
            "When all three rows say yes, add a line under line 17 that moves the robot "
            "backward by 360 degrees of motor turn after it stops.",
        ],
        "sheet_head": ["Run", "Far line, cm from the start line", "Expected: stops at the line?",
                       "Measured: front edge, cm from the start line", "Line under the robot?"],
        "sheet_rows": [["1", "55"], ["2", "40"], ["3", "70"]],
        "script": FLOOR_THEN_LINE,
        "expect": [("pair", "A", "E"), STARTED, STOPPED],
    },

    "exits": {
        "floor": ("Your sheet has your own readings for the floor and the tape, your "
                  "<code>DARK</code> is between them, and the robot stops at the far line "
                  "at 55 cm."),
        "middle": ("The robot stops with the far line under it at 40, 55, and 70 cm, with no "
                   "change to the program between runs."),
        "stretch": ("After it stops, the robot moves backward by 360 degrees of motor turn. "
                    "Then put lines 15 to 17 and your backward line inside a "
                    "<code>for</code> line, so the robot visits the far line 3 times."),
    },

    "ledger_code": ("motor_pair.move(motor_pair.PAIR_1, 0, velocity=250)\n"
                    "await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) < DARK)\n"
                    "motor_pair.stop(motor_pair.PAIR_1)"),
    "ledger_context": C2,
    "ledger": ("Session 3. Start the wheels, wait until the reflected light is less than "
               "DARK, stop the wheels. Write your sensor's port letter and your number for "
               "DARK beside it."),
    "stamp": ("To get today's stamp, tell your teacher your two readings and why your "
              "<code>DARK</code> is between them."),

    "teacher": {
        "before": [
            "Keep the robots built between sessions and charge every hub.",
            "Check which ports the two colour sensors use on the reference robot and how "
            "high they sit above the floor. The programs name port B as a first try.",
            "Use a pale, plain floor or table and black tape. A dark or patterned floor "
            "gives readings too close to the tape's.",
            "Lay out one lane for every two teams: a start line, and a far line that can be "
            "lifted and moved. Mark 40, 55, and 70 cm beside the lane with small pieces of "
            "tape.",
            "Log the reference robot's readings over the floor and over the tape, and three "
            "runs of each program on this page.",
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, reflected light", 12),
            ("0:27", "Chunk 2, move until the line", 13),
            ("0:40", "Chunk 3, when DARK is wrong", 8),
            ("0:48", "Hinge question", 4),
            ("0:52", "Mission", 31),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("Chunk 3 needs space past the far line and one adult watching each lane. "
                   "If the room is tight, run it once at the front as a class. Stopping at "
                   "the floor exit is a finish."),
        "misconceptions": [
            ("Chunk 1 prints nothing, or the program stops.",
             "Follow the sensor's cable to the hub together and read the port letter aloud. "
             "Compare it with line 5."),
            ("The two readings are close together.",
             "Look at the floor: a dark or shiny floor does this. Move the lane to a paler "
             "surface, or lay white paper under the lane and tape the line onto it."),
            ("A student says the robot can tell where the line is by itself.",
             "Point at line 16. The hub is waiting for one number to drop below another. "
             "Ask what number the sensor gives over the floor, and over the tape."),
            ("The robot stops as soon as it starts.",
             "Ask for the floor reading and the number on line 7. The number on line 7 is "
             "higher than the floor reading, as in chunk 3."),
            ("The robot does not stop at the line.",
             "Ask for the tape reading and the number on line 7. Either line 7 is lower "
             "than the tape reading, or line 6 names a port with no colour sensor in it."),
            ("A team types <code>await</code> in front of <code>motor_pair.move</code>.",
             "Ask what line 15 has to finish. It only starts the wheels, so there is "
             "nothing to wait for."),
        ],
        "standards": ["3-5-ETS1-3", "3-5-ETS1-1"],
        "routing": ("If time is short, drop chunk 3's own run and talk its two cases through "
                    "from the page, then give the time to the mission. The floor exit is "
                    "what session 4 needs: every team must leave with a working "
                    "<code>DARK</code>."),
        "deliberate": ("Chunk 3's <code>DARK = 0</code> is wrong on purpose. The 50 on line 7 "
                       "of chunk 2 and <code>port.B</code> on line 6 are first tries that "
                       "each team replaces."),
    },
}
