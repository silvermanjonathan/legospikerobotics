"""Session 1: build the Advanced Driving Base, then move it with Python.

Adapted from LEGO Education's lesson "Assembling an Advanced Driving Base" (linked in
the teacher panel). The LEGO lesson is for grades 6 to 8; this one is rewritten for
grades 4 and 5 in the house style. Python, by Jonathan's direction on 12 November
2026 (see the README's locked decisions).

Locked exception to the session anatomy: session 1 has no opener, because there is
no earlier session to retrieve from. That time goes to building the robot.

Every number on the page is computed in wheel.py or measured on the reference robot
and logged in runs.csv. render.py prints a measured range only when runs.csv holds at
least three runs for it.
"""

from robot import field_figure, turn_figure, BOOKS, FAR_CM, ZONE_CM
from wheel import whole_cm, nearest5, classroom_cm

# ---------------------------------------------------------------- the programs

TOP = '''from hub import port
import motor_pair
import runloop


async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
'''

END = '''


runloop.run(main())'''

FORWARD = '''
    # Move forward. The wheels turn 720 degrees of motor turn.
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 720, 0, velocity=250)'''

BACKWARD = '''

    # Move backward. The minus sign turns the wheels the other way.
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -720, 0, velocity=250)'''

TURN_LEFT = '''
    # Turn on the spot. The steering is -100.
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 360, -100, velocity=250)'''

TURN_TEST = '''

    # Turn on the spot. Change only the first number, one change per run.
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 100, velocity=250)'''

C1 = TOP + FORWARD + END
C2 = TOP + FORWARD + BACKWARD + END
C3 = TOP + TURN_LEFT + END
MISSION = TOP + FORWARD + TURN_TEST + END
HINGE = "await motor_pair.move_for_degrees(motor_pair.PAIR_1, -360, 0, velocity=250)"

# the distances the page prints, each from wheel.py
ONE_TURN = whole_cm(360)                 # about 28 cm
TWO_TURNS_BY_HAND = int(classroom_cm(720))   # 28 + 28 = 56
TWO_TURNS = nearest5(classroom_cm(720))  # 55, to the nearest 5
HINGE_CM = nearest5(classroom_cm(-360))  # 30, to the nearest 5
assert TWO_TURNS == FAR_CM, "the far line must sit where two full turns of the wheel end"

SETUP = ("Setup: the robot is behind the start line with its front edge on the line. It "
         "faces forward, across the field. It starts here on every run.")

SESSION01 = {
    "num": 1,
    "slug": "session01_advanced_driving_base",
    "title": "Build the Advanced Driving Base and move it with Python",
    "subtitle": ("A team of four builds one robot. Then a Python program moves it forward, "
                 "backward, and through a turn."),
    "new": ["motor_pair.pair", "motor_pair.move_for_degrees", "await",
            "a minus sign on the first number", "steering"],
    "new_text": ("<code>motor_pair.pair</code> tells the hub which two motors turn the wheels. "
                 "<code>motor_pair.move_for_degrees</code> turns the wheels. <code>await</code> "
                 "makes the hub finish one move before it starts the next. A minus sign on the "
                 "first number moves the robot backward. The second number is steering."),
    "reuse": "Nothing yet. This is the first session, so every idea on this page is new.",

    # ------------------------------------------------------------ the build
    "build": {
        "minutes": 45,
        "title": "Build the Advanced Driving Base",
        "intro": [
            "Today your team of four builds one robot. LEGO calls it the Advanced Driving "
            "Base. A <b>driving base</b> is a robot with two wheels, and each wheel is "
            "turned by its own motor.",
            "The robot is built in four parts. Each builder makes one part from one "
            "building book. Then the whole team joins the four parts with a fifth book.",
        ],
        "steps": [
            "Decide who builds which part. Each builder opens one book.",
            "Build your own part. Follow the steps in order. Check each step against its "
            "picture before you start the next step.",
            "When all four parts are done, open Book 5 as a team. Join the four parts. "
            "Plug in every cable the way Book 5 shows.",
            "Fill in the port map below from your own robot.",
        ],
        "words": ("The <b>hub</b> is the box with the buttons and the square of lights. It "
                  "holds the program and runs it. A <b>port</b> is one of the six sockets on "
                  "the hub. The ports are lettered A to F, and each cable plugs into one port. "
                  "A <b>motor</b> turns something. A <b>sensor</b> measures something."),
        "portmap_intro": ("Look at your own robot. For each port, write what is plugged into "
                          "it: a large motor, a medium motor, or a colour sensor. Then write "
                          "where that part sits on the robot. Left and right are always the "
                          "robot's left and right, as if you were sitting in the robot facing "
                          "forward. The part from Book 1 is the front."),
        "portmap_check": [
            "Two ports matter most today. Port A holds the large motor that turns the left "
            "wheel. Port E holds the large motor that turns the right wheel. Today's "
            "programs name those two ports.",
            "Your sheet should also list two medium motors and two colour sensors, in the "
            "ports Book 5 shows. Today's programs do not use them.",
            "If port A or port E holds something else on your robot, move the cables now.",
        ],
    },

    # ------------------------------------------------------------ robot check
    "check": {
        "minutes": 5,
        "items": [
            "Every cable is pushed all the way into its port.",
            "Port A holds the large motor that turns the left wheel. Port E holds the large "
            "motor that turns the right wheel.",
            "The hub is switched on and connected to the SPIKE App.",
            "A new Python project is open. Its name is the first name of the builder who is "
            "typing, an underscore, and the session: <code>Jonathan_session01</code>.",
        ],
        "after": ("The first program in chunk 1 is today's test run. If the robot does not "
                  "move in chunk 1, come back to this list and check each line of it again."),
    },

    # ------------------------------------------------------------ chunks
    "chunks": [
        {
            "key": "chunk1",
            "title": "Pair the motors, then move forward",
            "teach": [
                "A <b>program</b> is a list of lines. The hub runs the lines in order, from "
                "the top down. Lines 1 to 3 bring in the tools this program uses. Line 8 "
                "tells the hub which two motors turn the wheels: the left motor is in port A "
                "and the right motor is in port E. Line 11 turns the wheels.",
                "The first number on line 11 says how far the motors turn. It is counted in "
                "degrees of motor turn. 360 degrees of motor turn is one full turn of the "
                "wheel, and one full turn of this wheel moves the robot about %d cm." % ONE_TURN,
            ],
            "parts_title": "The parts of line 11",
            "parts": [
                ("motor_pair.PAIR_1", "The two drive motors that line 8 paired."),
                ("720", "How far the motors turn, in degrees of motor turn."),
                ("0", "The steering. 0 means straight."),
                ("velocity=250", "The speed. The motors turn 250 degrees of motor turn each second."),
            ],
            "code": C1,
            "where": ("Delete any lines the new project already has. Then type this program "
                      "exactly as it is here. Line 6 and line 14 are the frame that every hub "
                      "program sits in. Your own lines go between them, and each one starts "
                      "four spaces in from the left edge. Capital letters matter: "
                      "<code>PAIR_1</code>, <code>A</code>, and <code>E</code> are capitals. "
                      "A line that starts with <code>#</code> is a note for the reader. The "
                      "hub skips it."),
            "figure": field_figure(caption="The field from above for chunk 1. The robot is "
                                           "behind the start line, facing forward."),
            "setup": SETUP,
            "predict": ("Look at line 11. Which way does the robot move, forward or backward? "
                        "About how many cm does it move, to the nearest 5?"),
            "hints": ["720 is 360 + 360. How many full turns of the wheel is that?",
                      "One full turn of the wheel moves the robot about %d cm. Add that up "
                      "for each full turn." % ONE_TURN],
            "reveal": [
                "The first one: forward. The first number on line 11 is 720, with no minus "
                "sign.",
                "The second one: about %d cm. 720 degrees of motor turn is 2 full turns of "
                "the wheel, because 360 + 360 = 720. Each full turn moves the robot about "
                "%d cm, and %d + %d = %d. To the nearest 5, that is %d cm."
                % (TWO_TURNS, ONE_TURN, ONE_TURN, ONE_TURN, TWO_TURNS_BY_HAND, TWO_TURNS),
            ],
            "computed": "2 full turns of the wheel\n%d cm + %d cm = %d cm\nto the nearest 5: %d cm"
                        % (ONE_TURN, ONE_TURN, TWO_TURNS_BY_HAND, TWO_TURNS),
            "measure": ("Now measure your own run. Lay a ruler from the start line to the "
                        "robot's front edge and write the number down. Your number may differ "
                        "from %d by a little. If it differs by a lot, go back to the robot "
                        "check list." % TWO_TURNS),
            "unit": "cm",
            "expect": [("pair", "A", "E"), ("move", 720, 0, 250)],
        },
        {
            "key": "chunk2",
            "title": "A minus sign moves the robot backward",
            "teach": [
                "Each move line starts with <code>await</code>. <code>await</code> makes the "
                "hub finish that move before it starts the next line. So two move lines "
                "give two moves, one after the other.",
                "A minus sign in front of the first number turns the wheels the other way. "
                "The robot moves backward.",
            ],
            "code": C2,
            "start": C1,
            "steps": [
                {"label": "Line 14",
                 "q": ("Line 11 has moved the robot forward. Line 14 moves it backward by the "
                       "same number of degrees of motor turn. What is line 14?"),
                 "hints": ["Line 14 uses the same function as line 11.",
                           "Only the first number is different from line 11.",
                           {"text": "Here is line 14 with one part left blank.",
                            "code": "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, ____, 0, velocity=250)"}],
                 "line": "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -720, 0, velocity=250)",
                 "note": ("Type it under line 11, with one empty line between them. Line 13 "
                          "is a note for the reader. Line 14 starts four spaces in from the "
                          "left edge, in line with line 11.")},
            ],
            "figure": field_figure(far=True, caption="The field from above for chunk 2. The far "
                                   "line is %d cm from the start line." % FAR_CM),
            "setup": SETUP,
            "predict": ("Which move happens first, forward or backward? When the program ends, "
                        "where is the robot's front edge: on the start line, on the far line, "
                        "or past the far line?"),
            "hints": ["The hub runs the lines from the top down. Which move line is higher up?"],
            "reveal": [
                "The first one: forward. Line 11 is above line 14, and <code>await</code> on "
                "line 11 makes the hub finish the forward move before line 14 starts.",
                "The second one: on the start line, or close to it. The robot moves forward "
                "about %d cm to the far line. Then it moves backward about %d cm."
                % (TWO_TURNS, TWO_TURNS),
            ],
            "computed": "forward 2 full turns of the wheel: about %d cm\nbackward 2 full turns "
                        "of the wheel: about %d cm\nfront edge ends about 0 cm from the start line"
                        % (TWO_TURNS, TWO_TURNS),
            "measure": ("Measure how close your robot's front edge is to the start line when "
                        "the program ends. Write the number down."),
            "unit": "cm from the start line",
            "expect": [("pair", "A", "E"), ("move", 720, 0, 250), ("move", -720, 0, 250)],
        },
        {
            "key": "chunk3",
            "title": "Steering turns the robot",
            "teach": [
                "The second number in a move line is the <b>steering</b>. With steering 0, "
                "both wheels turn the same way and the robot moves straight.",
                "With steering 100, the left wheel turns forward and the right wheel turns "
                "backward. The robot stays on its spot and turns to its right. A minus sign "
                "on the steering swaps the two wheels.",
            ],
            "code": C3,
            "where": ("Keep lines 1 to 8. Replace the move lines with lines 10 and 11 here. "
                      "This program has one move."),
            "figure": turn_figure(caption="The robot from above. Left and right are the robot's "
                                  "own left and right."),
            "setup": SETUP,
            "predict": ("Look at line 11. Which wheel turns forward, the left wheel or the right "
                        "wheel? Which way does the robot turn, to its left or to its right?"),
            "hints": ["The steering on line 11 is -100. What does the minus sign do to the two "
                      "wheels?"],
            "reveal": [
                "The first one: the right wheel turns forward, and the left wheel turns "
                "backward. The minus sign on the steering swaps the two wheels.",
                "The second one: the robot turns to its left.",
                "How far round the robot turns depends on the first number. You will test "
                "that in the mission.",
            ],
            "computed": "steering -100\nright wheel forward, left wheel backward\nthe robot turns to its left, on the spot",
            "measure": ("Watch your own run from above. Check which wheel turns forward and "
                        "which way the front of the robot swings."),
            "unit": "which way the robot turns",
            "expect": [("pair", "A", "E"), ("move", 360, -100, 250)],
        },
    ],

    # ------------------------------------------------------------ hinge
    "hinge": {
        "code": HINGE,
        "q": ("This is the only move line in a program. Does the robot move forward, move "
              "backward, or turn? About how many cm does it move, to the nearest 5?"),
        "a": [
            "The first one: backward. The first number has a minus sign, and the steering is "
            "0, so the robot does not turn.",
            "The second one: about %d cm. 360 degrees of motor turn is one full turn of the "
            "wheel, which is about %d cm. To the nearest 5, that is %d cm."
            % (HINGE_CM, ONE_TURN, HINGE_CM),
        ],
    },

    # ------------------------------------------------------------ mission
    "brief": {
        "minutes": 10,
        "title": "Out, around, and home",
        "intro": [
            "Your robot is a delivery cart in a warehouse. It drives out to the far line, "
            "turns to face home, and drives back. A cart that stops out in the aisle is in "
            "the way of the next cart, so the wheels must end where they started.",
            "You already know how far to drive. You do not yet know what number makes the "
            "robot turn half way round, so that it faces home. You will find it by testing: "
            "change one number, run, and write down what the robot did.",
        ],
        "figure": field_figure(far=True, markers=True, caption="The field from above for the "
                               "mission. The far line is %d cm from the start line. A wheel "
                               "marker is a small piece of tape on the floor beside each wheel."
                               % FAR_CM),
        "values": [
            ("Start", "Behind the start line, front edge on the line, facing the far line."),
            ("Wheel markers", "Before the first run, put a small piece of tape on the floor "
                              "beside each wheel."),
            ("Far line", "%d cm from the start line." % FAR_CM),
            ("Speed", "<code>velocity=250</code> on every move line."),
            ("Target", "Both wheels end within %d cm of a wheel marker." % ZONE_CM),
        ],
        "code": MISSION,
        "code_note": ("Start from this program. Lines 1 to 11 are chunk 1. Line 14 is a turn "
                      "on the spot with steering 100, and its first number, 180, is a first "
                      "try."),
        "steps": [
            "Put the robot behind the start line and put down the two wheel markers.",
            "Fill in the Expected column for run 1. Then run the program. Does the robot "
            "face home after the turn? Fill in the rest of the row.",
            "Change only the first number on line 14. Fill in Expected, then run. Use one "
            "row for each run.",
            "Keep going until the robot faces home after the turn.",
            "Add one more move line under line 14 that moves the robot home. The robot now "
            "faces home, so decide whether the first number needs a minus sign.",
        ],
        "sheet_head": ["Run", "First number on line 14", "Expected: the robot turns less "
                       "than half way, half way, or more than half way",
                       "Measured: what the robot did", "Faces home?"],
        "sheet_rows": [["1", "180"], ["2", ""], ["3", ""], ["4", ""], ["5", ""]],
        "expect": [("pair", "A", "E"), ("move", 720, 0, 250), ("move", 180, 100, 250)],
    },

    "checks": [("hinge", TOP + "\n    " + HINGE + END, [("pair", "A", "E"), ("move", -360, 0, 250)], None)],
    "arith": [("one full turn, whole cm", ONE_TURN, "about %d cm" % ONE_TURN, 360),
              ("two full turns, nearest 5", TWO_TURNS, "that is %d cm" % TWO_TURNS, 720),
              ("hinge, nearest 5", HINGE_CM, "that is %d cm" % HINGE_CM, 360)],

    "exits": {
        "floor": ("The robot moves forward to the far line and backward to the start line "
                  "with the program from chunk 2. Each builder can say what each of the "
                  "numbers 720, 0, and 250 on line 11 does."),
        "middle": ("Your turn line makes the robot face home. Your sheet has one row for each "
                   "run, and only the first number on line 14 changes from row to row."),
        "stretch": ("Out, around, and home: both wheels end within %d cm of a wheel marker "
                    "in 3 runs out of 3." % ZONE_CM),
    },

    "ledger_code": "await motor_pair.move_for_degrees(motor_pair.PAIR_1, 720, 0, velocity=250)",
    "ledger": ("Session 1. This line moves the robot forward about %d cm. A minus sign on "
               "the 720 moves it backward. The 0 is the steering." % TWO_TURNS),
    "stamp": ("To get today's stamp, tell your teacher which part of the robot you built and "
              "what one number in your team's program does."),

    # ------------------------------------------------------------ teacher panel
    "teacher": {
        "before": [
            "Each team of four needs one SPIKE Prime set and one SPIKE Prime Expansion Set. "
            "LEGO states that this robot needs both.",
            "Charge every hub and connect each hub to its device once before class.",
            "Open the five building books on the devices, or print them. Keep your own "
            "unpublished copy of all five: LEGO keeps its SPIKE lessons online only until "
            "30 June 2031.",
            "Build the reference robot from the same five books and check its port map "
            "against the robot page.",
            "Lay out one test lane for every two teams: a start line and a far line of "
            "black tape, %d cm apart, measured from the middle of one tape to the middle of the other." % FAR_CM,
            "Run each program on this page three times on the reference robot and log the "
            "runs in <code>runs.csv</code>, then rebuild. The measured result boxes appear "
            "on this page only when the log holds three runs for them.",
        ],
        "timing": [
            ("0:00", "Teams of four, one building book each", 5),
            ("0:05", "Build the four parts", 30),
            ("0:35", "Join the parts with Book 5, cables, port map", 10),
            ("0:45", "Robot check", 5),
            ("0:50", "Chunk 1, pair the motors and move forward", 8),
            ("0:58", "Chunk 2, a minus sign moves the robot backward", 7),
            ("1:05", "Chunk 3, steering turns the robot", 7),
            ("1:12", "Hinge question", 3),
            ("1:15", "Mission", 10),
            ("1:25", "Pack away", 3),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("LEGO allows 30 minutes for this build with teams of four in grades 6 to "
                   "8, and 90 to 120 minutes for its whole lesson. Builders in grades 4 and 5 "
                   "may need longer than the 45 minutes planned here. Stopping at an exit is a "
                   "finish. Most rooms will not reach the stretch exit today."),
        "misconceptions": [
            ("One builder finishes a part early and starts building a neighbour's part.",
             "Give that builder Book 5 to read ahead, and ask them to find the cables and "
             "the parts the team will need for it."),
            ("In chunk 1 the robot moves backward.",
             "Check the port map. The cables of the two large motors are likely swapped: "
             "port A must hold the left wheel's motor and port E the right wheel's motor."),
            ("In chunk 1 the program stops and the robot does not move.",
             "Go through the robot check list with the team. Then read line 8 and line 11 "
             "aloud with them, one character at a time, against the page. Look for a "
             "lower-case letter where a capital belongs and for a missing "
             "<code>await</code>."),
            ("The robot curves when the steering is 0.",
             "Look for a cable that rubs a wheel and for a wheel that is not pushed fully "
             "onto its axle. Compare the robot with Book 5."),
            ("A student says the robot will turn half way round, because line 14 says 180.",
             "Ask what the 180 counts. It counts degrees of motor turn. How far the robot "
             "turns is a different number, and the sheet is how the team finds it."),
            ("A team changes the first number and the steering in the same run.",
             "Point at the sheet: one row, one change. Ask which of the two changes made "
             "the difference they saw."),
        ],
        "standards": ["3-5-ETS1-3", "NY-4.MD.5.a", "NY-4.MD.2"],
        "routing": ("If the robots are not built and checked by 0:50, run chunk 1 with the "
                    "teams that are ready and let the others watch it run. Chunk 1 is the "
                    "floor for such a day. Chunks 2 and 3 and the mission then open the next "
                    "session after its robot check. If only the mission is cut short, the "
                    "middle exit is the finish and the homeward line waits a week."),
        "deliberate": ("The 180 on line 14 of the mission program is a first try, not the "
                       "answer. It is there to be changed."),
    },
}
