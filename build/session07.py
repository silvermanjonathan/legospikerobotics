"""Session 7 (part 2): if, else, while, and following a line.

The follower is the standard one-sensor edge follower: over the tape, steer one way;
over the floor, steer the other way. It runs inside a while line whose stop the
student can name: the second colour sensor reaching the stop bar.

Part 2 lets teams change the speed. The follower starts at velocity=150.
"""

from robot import track_figure, TRACK_CM

C1 = '''from hub import light_matrix, port
import color_sensor
import runloop

LINE_SENSOR = port.B
DARK = 50


async def main():
    if color_sensor.reflection(LINE_SENSOR) < DARK:
        light_matrix.write("T")
    else:
        light_matrix.write("F")
    await runloop.sleep_ms(3000)


runloop.run(main())'''


def follower(on_tape, on_floor, velocity=150):
    return '''from hub import port
import color_sensor
import motor_pair
import runloop

LINE_SENSOR = port.B
STOP_SENSOR = port.F
DARK = 50


async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Follow the edge of the line until the stop sensor reaches the stop bar.
    while color_sensor.reflection(STOP_SENSOR) > DARK:
        if color_sensor.reflection(LINE_SENSOR) < DARK:
            motor_pair.move(motor_pair.PAIR_1, %d, velocity=%d)
        else:
            motor_pair.move(motor_pair.PAIR_1, %d, velocity=%d)
    motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())''' % (on_tape, velocity, on_floor, velocity)


C2 = follower(30, -30)
C3 = follower(-30, 30)
HINGE = ('''    while color_sensor.reflection(STOP_SENSOR) > DARK:
        if color_sensor.reflection(LINE_SENSOR) < DARK:
            motor_pair.move(motor_pair.PAIR_1, 30, velocity=150)
        else:
            motor_pair.move(motor_pair.PAIR_1, -30, velocity=150)''')

# Test inputs for the guard: the stop sensor reads floor four times and then the bar,
# while the line sensor reads tape, floor, tape, floor. They appear on no page.
WIGGLE = {"F": [80, 80, 80, 80, 10], "B": [10, 80, 10, 80]}
RIGHT, LEFT = ("start", 30, 150), ("start", -30, 150)

SETUP = ("Setup: the robot is at the start of the line, facing along it, with the line "
         "sensor over the tape. It starts here on every run.")

SESSION07 = {
    "num": 7,
    "part": 2,
    "slug": "session07_follow_the_line",
    "title": "Follow the line",
    "subtitle": ("The program chooses between two moves, again and again, and the robot "
                 "follows a line of tape to the end."),
    "new": ["if", "else", "while"],
    "new_text": ("<code>if</code> runs its lines only when its test is true. "
                 "<code>else</code> runs its lines when the test is false. "
                 "<code>while</code> runs the lines inside it again and again, for as long "
                 "as its test stays true."),
    "reuse": ("The tests <code>&lt; DARK</code> and <code>&gt; DARK</code> from sessions 3 and "
              "5, steering from session 1, and the second colour sensor on your port map."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. Nothing is loose and nothing is missing.",
            "Follow both colour sensors' cables to the hub and write down both port "
            "letters. Today uses both sensors.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session07</code>.",
            "Your ledger card is on the table, with your number for <code>DARK</code>.",
        ],
        "after": "The program in chunk 1 is today's test run. It uses one sensor and no motors.",
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from session 6?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("What does the motion sensor count, and in what size of step?",
             ["How far the hub has turned since the count was set to 0, in tenths of a "
              "degree of the robot's turn."]),
            ("Why did the measured turn end a little past the angle it waited for?",
             ["The wheels were still turning when the test became true, and they took a "
              "moment to stop."]),
            ("Your team compared two ways of turning. How did you decide which was better?",
             ["By running each one three times from the same start and measuring how far "
              "the wheels ended from their markers."]),
            ("A reading is less than <code>DARK</code>. Is the sensor over the tape or over "
             "the floor?",
             ["Over the tape. Black tape sends less light back, so it gives the smaller "
              "number."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "Choose between two things: if and else",
            "teach": [
                "Line 10 is a test. If the reflected light is less than <code>DARK</code>, "
                "the hub runs line 11 and skips line 13. If it is not, the hub skips line "
                "11 and runs line 13. It never runs both.",
                "Line 11 is inside the <code>if</code> line and line 13 is inside the "
                "<code>else</code> line, so each starts four more spaces in. Line 14 is "
                "back at four spaces. It runs either way and keeps the letter on the light "
                "matrix for 3 seconds.",
            ],
            "code": C1,
            "where": ("Put your own port letter on line 5 and your own number on line 6. Lines "
                      "10 and 12 each end with a colon."),
            "figure": track_figure(caption="The line from above. For chunk 1, hold the robot "
                                   "so the line sensor is over the tape, then over the floor."),
            "setup": ("Setup: for run 1 the line sensor is over the black tape. For run 2 it "
                      "is over the pale floor. The robot does not move in this program."),
            "predict": ("What letter does the light matrix show in run 1, over the tape? What "
                        "letter in run 2, over the floor?"),
            "hints": ["Over the tape, is the reading less than <code>DARK</code>? Then which "
                      "of lines 11 and 13 runs?"],
            "reveal": [
                "The first one: T. Over the tape the reading is less than <code>DARK</code>, "
                "so the test on line 10 is true and line 11 runs.",
                "The second one: F. Over the floor the reading is not less than "
                "<code>DARK</code>, so the test is false and line 13 runs.",
            ],
            "computed": "over the tape: the test is true, line 11 runs, shows T\nover the floor: the test is false, line 13 runs, shows F",
            "measure": "Run it over each one and check both letters.",
            "unit": "letter shown, tape then floor",
            "script": [10],
            "expect": [("show", "T"), ("wait", 3000)],
        },
        {
            "key": "chunk2",
            "title": "Keep choosing: while",
            "teach": [
                "To follow a line, the robot follows its edge. Over the tape, it steers a "
                "little to the right, off the tape. Over the floor, it steers a little to "
                "the left, back onto the tape. It wiggles along the right edge.",
                "One choice is not enough. Line 16 is a <code>while</code> line: it runs "
                "lines 17 to 20 again and again, for as long as its own test is true. Its "
                "test reads the other colour sensor, the stop sensor. When the stop sensor "
                "reaches the stop bar, the test is false, the repeating ends, and line 21 "
                "stops the wheels.",
            ],
            "code": C2,
            "where": ("Put your two port letters on lines 6 and 7. The line sensor is the one "
                      "that starts over the tape. Lines 17 to 20 are inside the "
                      "<code>while</code> line, and lines 18 and 20 are eight more spaces in "
                      "than line 16. The speed here is 150, slower than before."),
            "parts_title": "The parts of the follower",
            "parts": [
                ("while ... > DARK:", "Line 16. Keep going while the stop sensor is over pale floor."),
                ("if ... < DARK:", "Line 17. Is the line sensor over the tape?"),
                ("30", "Line 18. Over the tape: steer a little to the right."),
                ("-30", "Line 20. Over the floor: steer a little to the left."),
            ],
            "figure": track_figure(caption="The line and its stop bar from above. The line is "
                                   "%d cm long." % TRACK_CM),
            "setup": SETUP,
            "predict": ("What makes this robot stop: a number of degrees of motor turn, the "
                        "line sensor, or the stop sensor? Does the robot move in a straight "
                        "line or does it wiggle?"),
            "hints": ["Line 21 is the stop. Which line has to finish before the hub gets to "
                      "line 21, and what is its test?"],
            "reveal": [
                "The first one: the stop sensor. Line 16 keeps the choosing going while the "
                "stop sensor reads more than <code>DARK</code>. Over the stop bar it reads "
                "less, the <code>while</code> line ends, and line 21 stops the wheels.",
                "The second one: it wiggles. Every time round, the hub picks steering 30 or "
                "steering -30. It never picks 0.",
            ],
            "computed": "over the tape: steer right\nover the floor: steer left\nagain and again, until the stop sensor is over the stop bar\nthen stop",
            "measure": ("If the robot stops at once, or never stops, swap the two port letters "
                        "on lines 6 and 7 and say why that might help."),
            "unit": "reaches the stop bar, yes or no",
            "script": WIGGLE,
            "expect": [("pair", "A", "E"), RIGHT, LEFT, RIGHT, LEFT, ("stop",)],
        },
        {
            "key": "chunk3",
            "title": "The other edge",
            "teach": [
                "This program swaps the two steering numbers. Over the tape the robot now "
                "steers to the left, and over the floor it steers to the right.",
            ],
            "code": C3,
            "where": "Change only the steering numbers on lines 18 and 20.",
            "figure": track_figure(caption="The line and its stop bar from above."),
            "setup": SETUP,
            "predict": ("The line sensor starts over the tape. Which way does the robot steer "
                        "first? Which edge of the tape does it end up following, the left "
                        "edge or the right edge?"),
            "hints": ["Over the tape, line 18 runs. Read its steering number."],
            "reveal": [
                "The first one: to the left. The line sensor starts over the tape, so line "
                "18 runs, and its steering is now -30.",
                "The second one: the left edge. The robot steers left until the sensor is "
                "over the floor on the left of the tape, then right until it is over the "
                "tape again, and so on along the left edge.",
                "Both programs work. They follow different edges. Which one suits your "
                "robot depends on where its stop sensor sits.",
            ],
            "computed": "over the tape: steer left\nover the floor: steer right\nthe robot follows the left edge of the tape",
            "measure": ("Watch which side of the tape the line sensor ends up on. Then choose "
                        "the edge your team will use in the mission."),
            "unit": "edge followed, left or right",
            "script": WIGGLE,
            "expect": [("pair", "A", "E"), LEFT, RIGHT, LEFT, RIGHT, ("stop",)],
        },
    ],
    "checks": [("if, over the floor", C1, [("show", "F"), ("wait", 3000)], [80])],

    "hinge": {
        "code": HINGE,
        "context": C2,
        "q": ("The robot is half way along the line. A builder covers the stop sensor with "
              "a strip of black tape. What does the robot do, and which line of the "
              "program decides that?"),
        "a": [
            "It stops. The stop sensor now reads less than <code>DARK</code>, so the test on "
            "the <code>while</code> line is false. The repeating ends and the next line "
            "stops the wheels.",
            "The <code>while</code> line decides. The program cannot tell a stop bar from a "
            "strip of tape held under the sensor. It has only the reading.",
        ],
    },

    "brief": {
        "minutes": 34,
        "title": "The winding aisle",
        "intro": [
            "The warehouse has a new aisle with a bend in it, marked by a line of tape on "
            "the floor. The cart has to follow the line round the bend to the stop bar "
            "without losing it. Then the warehouse wants it faster.",
            "Two numbers set how the cart follows: how hard it steers and how fast it "
            "goes. Change one of them per run.",
        ],
        "figure": track_figure(bend=True, caption="The mission from above: a line of tape with "
                               "one bend, ending at the stop bar."),
        "values": [
            ("Start", "At the start of the line, facing along it, line sensor over the tape."),
            ("Done means", "The robot follows the line round the bend and stops at the stop "
                           "bar, in 3 runs out of 3."),
            ("You may change", "The steering numbers on lines 18 and 20 and the speed on "
                               "both lines. Keep the two speeds the same as each other."),
            ("You may not", "Touch the robot after the program starts."),
            ("Then", "Time each run with a stopwatch and try to beat your own best time."),
        ],
        "code": C2,
        "code_note": ("Start from the follower in chunk 2, or chunk 3 if your team chose the "
                      "left edge, with your own port letters and your own <code>DARK</code>."),
        "steps": [
            "Run it as it is and fill in row 1. Where does the robot lose the line, if it "
            "does?",
            "Change one number. Fill in Expected, then run.",
            "When it passes 3 runs out of 3, start timing. Raise the speed one step at a "
            "time and write down each time in seconds.",
        ],
        "sheet_head": ["Run", "The one thing changed", "Expected", "Measured: reached the "
                       "stop bar?", "Time, in seconds"],
        "sheet_rows": [["1", "Nothing yet"], ["2", None], ["3", None], ["4", None],
                       ["5", None], ["6", None]],
        "script": WIGGLE,
        "expect": [("pair", "A", "E"), RIGHT, LEFT, RIGHT, LEFT, ("stop",)],
    },

    "exits": {
        "floor": ("The robot follows the straight line to the stop bar and stops there, and "
                  "each builder can say what the <code>while</code> line waits for."),
        "middle": "The robot follows the line round the bend to the stop bar in 3 runs out of 3.",
        "stretch": ("Your sheet shows your team's fastest time that still passes 3 runs out "
                    "of 3, and the steering and speed that gave it."),
    },

    "ledger_code": HINGE.replace("    while", "while", 1).replace("\n    ", "\n"),
    "ledger_context": C2,
    "ledger": ("Session 7. A line follower: while the stop sensor is over the floor, steer "
               "one way over the tape and the other way over the floor. Write your team's "
               "steering and speed beside it."),
    "stamp": ("To get today's stamp, tell your teacher what would happen if the line had no "
              "stop bar."),

    "teacher": {
        "before": [
            "Check on the reference robot that the two colour sensors sit far enough apart "
            "for one to be over the tape while the other is over the floor. If they do "
            "not, this session needs a wider gap or a different stop.",
            "Lay out one straight line with a stop bar for every two teams, %d cm long, and "
            "one line with a gentle bend. Use black tape on a pale floor. Keep bends "
            "gentle: a sharp corner needs harder steering than the first try." % TRACK_CM,
            "Have one stopwatch for each team.",
            "Charge every hub, and log three runs of each program on the reference robot.",
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, if and else", 10),
            ("0:25", "Chunk 2, while and the follower", 14),
            ("0:39", "Chunk 3, the other edge", 7),
            ("0:46", "Hinge question", 3),
            ("0:49", "Mission", 34),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("Typing the follower takes time: three levels of spaces. Let teams check "
                   "each other's lines 16 to 21 before the first run. Stopping at the floor "
                   "exit is a finish."),
        "misconceptions": [
            ("The robot stops at once.",
             "The stop sensor is over the tape at the start. Swap the two port letters, or "
             "follow the other edge, so the stop sensor starts over pale floor."),
            ("The robot turns away from the line and circles.",
             "The line sensor started over the floor on the wrong side for this program's "
             "edge. Start it over the tape."),
            ("The robot loses the line at the bend.",
             "Ask which number sets how hard it steers. One change: a bigger steering "
             "number, or a slower speed, not both."),
            ("Line 21 is typed inside the <code>while</code> line.",
             "The robot stops and starts in jerks. Count the spaces in front of line 21 "
             "together: four."),
            ("A student says the robot can tell where the line goes.",
             "Ask what the hub reads. One number, many times a second, and each time it "
             "picks one of two steering numbers."),
        ],
        "standards": ["3-5-ETS1-3", "3-5-ETS1-1"],
        "routing": ("If time is short, drop chunk 3 and tell teams there are two edges. Keep "
                    "the timing part of the mission for teams at the stretch exit only."),
        "deliberate": ("The first tries are 30, -30, and 150. They are meant to be changed."),
    },
}
