"""Session 2: names for numbers, the quarter turn, and a square with a for line.

The shortcut arrives after the long way: the square is first written as four copies
of the same two lines, then as one for line with the two lines inside it.

The final mission is told to students here, two sessions before the end. With four
sessions there is no earlier place for it: session 1 is the build.
"""

from robot import cross_figure, square_figure, field_figure, FAR_CM, SQUARE_ZONE_CM, CRATE_CM
from wheel import whole_cm, nearest5, classroom_cm, cm

HEAD = '''from hub import port
import motor_pair
import runloop

'''

PAIR = '''

async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

'''

END = '''


runloop.run(main())'''

FWD = "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, FORWARD, 0, velocity=250)"
TURN = "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, QUARTER_TURN, 100, velocity=250)"

C1 = HEAD + "FORWARD = 360\n" + PAIR + FWD + "\n" + FWD + END
C2 = HEAD + "FORWARD = 360\nQUARTER_TURN = 180\n" + PAIR + FWD + "\n" + TURN + "\n" + FWD + END
LONG = (HEAD + "FORWARD = 360\nQUARTER_TURN = 180\n" + PAIR
        + "\n".join([FWD, TURN] * 4) + END)
LOOP_LINES = ("    for count in range(4):\n    " + FWD + "\n    " + TURN)
C3 = HEAD + "FORWARD = 360\nQUARTER_TURN = 180\n" + PAIR + LOOP_LINES + END
MISSION = HEAD + "FORWARD = 720\nQUARTER_TURN = 180\n" + PAIR + LOOP_LINES + END
HINGE = "    for count in range(3):\n    " + FWD
HINGE_PROGRAM = HEAD + "FORWARD = 360\n" + PAIR + HINGE + END

ONE = whole_cm(360)                               # 28
TWO_BY_HAND = int(classroom_cm(720))              # 56
TWO = nearest5(classroom_cm(720))                 # 55
THREE_BY_HAND = int(classroom_cm(1080))           # 84
THREE = nearest5(classroom_cm(1080))              # 85
SIDE = nearest5(cm(720))                          # the mission square's side, 55

MOVE_F, MOVE_T = ("move", 360, 0, 250), ("move", 180, 100, 250)

SETUP_LINE = ("Setup: the robot is behind the start line with its front edge on the line. It "
              "faces forward, across the field. It starts here on every run.")
SETUP_CROSS = ("Setup: the robot sits over the middle of the turn cross and faces along "
               "strip 1. It starts here on every run.")
SETUP_SQUARE = ("Setup: the robot starts at the first corner of the square, facing along "
                "side 1, with a wheel marker beside each wheel. It starts here on every run.")

SESSION02 = {
    "num": 2,
    "slug": "session02_quarter_turn_and_square",
    "title": "Name the numbers, find the quarter turn, drive a square",
    "subtitle": ("A number gets a name at the top of the program. Then one line makes the "
                 "robot repeat two moves four times."),
    "new": ["a name for a number", "for count in range(4):"],
    "new_text": ("A number can have a name, such as <code>FORWARD = 360</code>, written once "
                 "at the top of the program. The line <code>for count in range(4):</code> "
                 "runs the lines inside it 4 times."),
    "reuse": ("<code>motor_pair.move_for_degrees</code>, <code>await</code>, and steering, "
              "from session 1."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. Nothing is loose and nothing is missing.",
            "Every cable is pushed all the way into its port. Port A holds the left wheel's "
            "motor and port E holds the right wheel's motor.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session02</code>.",
        ],
        "after": ("The program in chunk 1 is today's test run. If the robot does not move "
                  "forward in chunk 1, come back to this list."),
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from session 1?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("Why does the robot start in the same place, facing the same way, on every run?",
             ["Then every run starts the same. If the robot ends somewhere new, the change "
              "came from the program, not from where the robot started."]),
            ("What does <code>motor_pair.pair</code> tell the hub?",
             ["It tells the hub which two motors turn the wheels, and which one is on the "
              "left and which one is on the right."]),
            ("A move line starts with <code>await</code>. What does <code>await</code> do?",
             ["It makes the hub finish that move before it starts the next line."]),
            ("When you test, why do you change only one number for each run?",
             ["Then you know which change made the difference. With two changes in one run "
              "you cannot tell which one did it."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "A name for a number",
            "teach": [
                "Line 5 gives the number 360 a name: <code>FORWARD</code>. Wherever the "
                "program says <code>FORWARD</code>, the hub uses 360.",
                "A name in capitals at the top of the program is for a number you may want "
                "to change. You change it once, on line 5, and every line that uses the "
                "name changes with it.",
            ],
            "code": C1,
            "where": ("Type the whole program into your new project. Line 5 starts at the left "
                      "edge. It sits above line 8, so the name exists before any line uses it."),
            "figure": field_figure(caption="The field from above for chunk 1. The robot is "
                                           "behind the start line, facing forward."),
            "setup": SETUP_LINE,
            "predict": ("How many times does the robot move? About how many cm does it move in "
                        "all, to the nearest 5?"),
            "hints": ["Lines 12 and 13 both say <code>FORWARD</code>. What number does the hub "
                      "use there?",
                      "360 degrees of motor turn is one full turn of the wheel, about %d cm." % ONE],
            "reveal": [
                "The first one: 2 times. Line 12 is one move and line 13 is another, and "
                "<code>await</code> makes the hub finish line 12 before line 13 starts.",
                "The second one: about %d cm. Each move is 360 degrees of motor turn, which "
                "is about %d cm, and %d + %d = %d. To the nearest 5, that is %d cm."
                % (TWO, ONE, ONE, ONE, TWO_BY_HAND, TWO),
            ],
            "computed": "2 moves, each 1 full turn of the wheel\n%d cm + %d cm = %d cm\nto the nearest 5: %d cm"
                        % (ONE, ONE, TWO_BY_HAND, TWO),
            "measure": ("Measure your own run from the start line to the robot's front edge. "
                        "Then change line 5 to <code>FORWARD = 180</code>, say what you expect, "
                        "and run it again."),
            "unit": "cm",
            "expect": [("pair", "A", "E"), MOVE_F, MOVE_F],
        },
        {
            "key": "chunk2",
            "title": "Find your quarter turn",
            "teach": [
                "A quarter turn is 90 degrees of the robot's turn. After a quarter turn to "
                "the right, the robot faces to the right of where it faced before, like the "
                "corner of a square.",
                "The number in the program does not count that. It counts degrees of motor "
                "turn, and that is a different number. Line 6 gives it a name, "
                "<code>QUARTER_TURN</code>, and a first try of 180. Your team finds the "
                "real number by testing.",
            ],
            "code": C2,
            "start": C1,
            "steps": [
                {"label": "Line 14",
                 "q": ("Line 13 moves the robot forward. Line 14 turns it to its right on the "
                       "spot, by <code>QUARTER_TURN</code> degrees of motor turn. What is "
                       "line 14?"),
                 "hints": ["It is a move line, like line 13.",
                           "The first number is the name from line 6. The steering for a turn "
                           "to the right on the spot is 100.",
                           {"text": "Here is line 14 with two parts left blank.",
                            "code": "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, ____, ____, velocity=250)"}],
                 "line": TURN,
                 "note": ("Add line 6 under line 5 first. Then put this line between the two "
                          "forward lines, in line with them.")},
            ],
            "figure": cross_figure(caption="The turn cross from above: two strips of black tape "
                                   "that cross like a plus sign."),
            "setup": SETUP_CROSS,
            "predict": ("In what order does the robot do its three moves? After the turn, does "
                        "it face to the left or to the right of the way it faced at the start?"),
            "hints": ["Read lines 13, 14, and 15 from the top down."],
            "reveal": [
                "The first one: forward, then the turn, then forward again. The hub runs lines "
                "13, 14, and 15 in that order.",
                "The second one: to the right. The steering on line 14 is 100, so the left "
                "wheel turns forward and the right wheel turns backward.",
                "Whether 180 gives a quarter turn is what you test now. For the test, put "
                "<code>#</code> at the start of lines 13 and 15 so the hub skips them. Start "
                "the robot on the turn cross, facing along strip 1. Change line 6, one change "
                "per run, until the robot faces along strip 2 after the turn. Use one row "
                "of the sheet below for each run.",
            ],
            "sheet": {
                "title": "Expected and measured: the quarter turn",
                "intro": "Fill in the Expected column before each run. One change per run.",
                "head": ["Run", "Number on line 6", "Expected: less than a quarter turn, a "
                         "quarter turn, or more", "Measured: what the robot did",
                         "Faces along strip 2?"],
                "rows": [["1", "180"], ["2", None], ["3", None], ["4", None], ["5", None], ["6", None]],
            },
            "computed": "forward, turn to the right, forward\nthe robot ends facing to the right of the way it started",
            "measure": ("Write your team's number for <code>QUARTER_TURN</code> on your ledger "
                        "card. Every program after this one uses it."),
            "unit": "degrees of motor turn for a quarter turn",
            "expect": [("pair", "A", "E"), MOVE_F, MOVE_T, MOVE_F],
        },
        {
            "key": "chunk3",
            "title": "A square, the long way and the short way",
            "teach": [
                "A square is four sides and four quarter turns. The long way is to write the "
                "forward line and the turn line four times: eight move lines. Open the "
                "program so far to see it.",
                "The short way is the line <code>for count in range(4):</code>. It runs the "
                "lines inside it 4 times. The lines inside it start four more spaces in, so "
                "they are eight spaces from the left edge.",
            ],
            "code": C3,
            "start": LONG,
            "steps": [
                {"label": "Lines 13 to 15",
                 "q": ("The long way has the same two lines four times over. Which three lines "
                       "do the same job?"),
                 "hints": ["The first of the three lines says how many times to run the other "
                           "two.",
                           "The other two are one forward line and one turn line, each four "
                           "more spaces in.",
                           {"text": "Here are the three lines with the count left blank.",
                            "code": "    for count in range(____):\n    " + FWD + "\n    " + TURN}],
                 "line": LOOP_LINES,
                 "note": ("Delete the eight move lines and type these three in their place. "
                          "Line 13 ends with a colon.")},
            ],
            "figure": square_figure(ONE, caption="The square from above. Each side is about "
                                    "%d cm." % ONE),
            "setup": SETUP_SQUARE,
            "predict": ("How many forward moves does the robot make, and how many turns? If "
                        "<code>QUARTER_TURN</code> is your team's number, where does the robot "
                        "end and which way does it face?"),
            "hints": ["Line 13 says <code>range(4)</code>. How many lines are inside it?"],
            "reveal": [
                "The first one: 4 forward moves and 4 turns. Lines 14 and 15 are inside line "
                "13, so the hub runs that pair of lines 4 times.",
                "The second one: back at the first corner, or close to it, facing the way it "
                "started. Four sides of the same length and four quarter turns close a "
                "square, and four quarter turns make one full turn.",
            ],
            "computed": "forward, turn, forward, turn, forward, turn, forward, turn\n4 quarter turns = 1 full turn of the robot\nthe robot ends where it started, facing the way it started",
            "measure": ("Measure how far each wheel ends from its wheel marker. A small miss on "
                        "each turn adds up over four turns, so this is a hard test of your "
                        "number."),
            "unit": "cm from the wheel marker",
            "expect": [("pair", "A", "E")] + [MOVE_F, MOVE_T] * 4,
        },
    ],
    "arith": [("one full turn, whole cm", ONE, "about %d cm" % ONE, 360),
              ("two full turns, nearest 5", TWO, "that is %d cm" % TWO, 720),
              ("three full turns, nearest 5", THREE, "that is %d cm" % THREE, 1080),
              ("mission side, nearest 5", SIDE, "about %d cm" % SIDE, 720)],
    "checks": [("long way", LONG, [("pair", "A", "E")] + [MOVE_F, MOVE_T] * 4, None),
               ("hinge", HINGE_PROGRAM, [("pair", "A", "E")] + [MOVE_F] * 3, None)],

    "hinge": {
        "code": HINGE,
        "context": HINGE_PROGRAM,
        "q": ("These two lines are the only move lines in a program, and line 5 says "
              "<code>FORWARD = 360</code>. How many times does the robot move? About how "
              "many cm in all, to the nearest 5?"),
        "a": [
            "The first one: 3 times. <code>range(3)</code> runs the line inside it 3 times.",
            "The second one: about %d cm. Each move is about %d cm, and %d + %d + %d = %d. "
            "To the nearest 5, that is %d cm." % (THREE, ONE, ONE, ONE, ONE, THREE_BY_HAND, THREE),
        ],
    },

    "brief": {
        "minutes": 25,
        "title": "Around the crate",
        "intro": [
            "A crate has been left in the middle of the warehouse floor. Your robot is the "
            "cart that checks it: it drives all the way around the crate and comes back to "
            "where it started. If the cart touches the crate, the check has failed.",
            "The square is bigger now. Each side is about %d cm." % SIDE,
        ],
        "figure": square_figure(SIDE, crate=True, caption="The mission from above. Each side "
                                "is about %d cm and the crate sits in the middle." % SIDE),
        "values": [
            ("Start", "At the first corner, facing along side 1."),
            ("Wheel markers", "A small piece of tape on the floor beside each wheel, put down "
                              "before the first run."),
            ("Crate", "A box or cup no more than %d cm across, in the middle of the square." % CRATE_CM),
            ("Side", "<code>FORWARD = 720</code>, about %d cm." % SIDE),
            ("Speed", "<code>velocity=250</code> on every move line."),
            ("Target", "The robot does not touch the crate, and each wheel ends within %d cm "
                       "of its wheel marker." % SQUARE_ZONE_CM),
        ],
        "code": MISSION,
        "code_note": ("Start from this program. It is the program from chunk 3 with line 5 "
                      "changed. Put your team's number on line 6 before the first run."),
        "steps": [
            "Put the crate in the middle. Put the robot at the first corner and put down the "
            "two wheel markers.",
            "Fill in the Expected column for run 1, then run the program.",
            "Measure how far each wheel is from its marker. Fill in the rest of the row.",
            "Decide on one change. Write it in the next row, fill in Expected, then run.",
        ],
        "sheet_head": ["Run", "The one thing changed", "Expected", "Measured: cm from the "
                       "markers", "Touched the crate?", "Inside the target?"],
        "sheet_rows": [["1", "Nothing yet"], ["2", None], ["3", None], ["4", None]],
        "expect": [("pair", "A", "E")] + [("move", 720, 0, 250), MOVE_T] * 4,
    },

    "exits": {
        "floor": ("Your team has its own number for <code>QUARTER_TURN</code>, found by "
                  "testing on the turn cross, with every run written down."),
        "middle": ("The square from chunk 3 closes: the robot ends near the first corner, "
                   "facing the way it started, and the program uses the <code>for</code> line."),
        "stretch": ("Around the crate: no touch, and each wheel within %d cm of its marker, "
                    "in 3 runs out of 3." % SQUARE_ZONE_CM),
    },

    "preview": {
        "minutes": 3,
        "title": "Coming in session 4: the delivery run",
        "body": [
            "In session 4 your families come to watch. Your robot will make a delivery: it "
            "moves to a line, turns a quarter turn, and stops inside a drop zone. Nobody "
            "will tell you how far away the line is.",
            "You already have the quarter turn. In session 3 you get the part that finds "
            "the line.",
        ],
    },

    "ledger_code": "QUARTER_TURN = ____\nfor count in range(4):",
    "ledger": ("Session 2. Write your team's number in the blank. A name in capitals at the "
               "top holds a number you may change. The <code>for</code> line runs the lines "
               "inside it 4 times."),
    "stamp": ("To get today's stamp, tell your teacher your team's number for "
              "<code>QUARTER_TURN</code> and how you found it."),

    "teacher": {
        "before": [
            "Keep the robots built between sessions. If one has been taken apart, its team "
            "rebuilds it from the robot page before the robot check.",
            "Charge every hub.",
            "Lay out one turn cross for every two teams: two strips of black tape, each about "
            "40 cm long, crossing at a right angle. Check the angle with the corner of a "
            "sheet of paper.",
            "Clear a floor space about 1 metre square for each team's square.",
            "Have one crate for each team: a box or cup no more than %d cm across." % CRATE_CM,
            "Log three runs on the reference robot for each program on this page, and the "
            "reference robot's own number for a quarter turn.",
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, a name for a number", 10),
            ("0:25", "Chunk 2, find your quarter turn", 15),
            ("0:40", "Chunk 3, the square two ways", 12),
            ("0:52", "Hinge question", 3),
            ("0:55", "Mission", 25),
            ("1:20", "Session 4 preview", 3),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("The test in chunk 2 is the heart of the session and may run past its 15 "
                   "minutes. That is time well spent. Stopping at the floor exit is a finish."),
        "misconceptions": [
            ("A team tries 90 for <code>QUARTER_TURN</code> because a quarter turn is 90.",
             "Let them run it and watch. Then ask what the 90 counted. The program counts "
             "degrees of motor turn. The 90 they have in mind is degrees of the robot's turn."),
            ("A team changes <code>QUARTER_TURN</code> by a big jump every run and keeps "
             "overshooting.",
             "Ask for the two numbers they have tried that were too small and too big. The "
             "next try goes between them."),
            ("The lines inside the <code>for</code> line are not lined up with each other.",
             "Point at the grey bars in the program on the page. Both lines inside sit behind "
             "the same two bars. Count the spaces together: eight."),
            ("The square does not close even with a good quarter turn.",
             "That is expected after four turns. Check that the robot starts in the same "
             "place each run, then let the team adjust the number by 1 or 2 at a time."),
            ("A team wants to change <code>FORWARD</code> and <code>QUARTER_TURN</code> "
             "together.",
             "One row, one change. Ask which of the two they think matters for the miss "
             "they measured."),
        ],
        "standards": ["3-5-ETS1-3", "NY-4.MD.5.b", "NY-4.MD.2"],
        "routing": ("If time is short, skip the crate and let the chunk 3 square be the "
                    "mission. Do not cut the test in chunk 2: sessions 3 and 4 use its number. "
                    "Keep the three minutes for the session 4 preview."),
        "deliberate": ("The 180 for <code>QUARTER_TURN</code> is a first try, not the answer. "
                       "Every team replaces it with its own number."),
    },
}
