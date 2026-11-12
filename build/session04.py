"""Session 4: the delivery run, and the demo for families.

No new Python. The session puts together session 2's quarter turn and session 3's
move until the line, and ends with each team showing its robot to families.

Chunk 2 ships a program with two lines in the wrong order, on purpose.
"""

from robot import delivery_figure, field_figure, DROP_CM, FAR_MIN, FAR_MAX
from wheel import whole_cm

HEAD = '''from hub import port
import color_sensor
import motor_pair
import runloop

LINE_SENSOR = port.B
DARK = 50
FORWARD = 360
QUARTER_TURN = 180


async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Move until the far line.
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=250)
    await runloop.until(lambda: color_sensor.reflection(LINE_SENSOR) < DARK)
    motor_pair.stop(motor_pair.PAIR_1)

    # Turn a quarter turn to the right, then move into the drop zone.
'''
TURN = "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, QUARTER_TURN, 100, velocity=250)"
FWD = "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, FORWARD, 0, velocity=250)"
END = '''


runloop.run(main())'''

C1 = HEAD + TURN + "\n" + FWD + END
C2 = HEAD + FWD + "\n" + TURN + END          # lines 22 and 23 swapped, on purpose
START = HEAD.replace("    # Turn a quarter turn to the right, then move into the drop zone.\n",
                     "    # Your lines go here.") + END

LEG = whole_cm(360)                       # about 28 cm
FLOOR_THEN_LINE = [80, 80, 80, 80, 10]
STARTED, STOPPED = ("start", 0, 250), ("stop",)
MOVE_T, MOVE_F = ("move", 180, 100, 250), ("move", 360, 0, 250)

SETUP = ("Setup: the robot is behind the start line with its front edge on the line, "
         "facing the far line. It starts here on every run.")

SESSION04 = {
    "num": 4,
    "slug": "session04_delivery_run_and_demo",
    "title": "The delivery run, and demo day",
    "subtitle": ("Everything from sessions 1 to 3 goes into one program. Then your team "
                 "shows its robot to your families."),
    "new": [],
    "new_text": "No new Python. Everything today is already on your ledger card.",
    "reuse": ("Moving until the line from session 3, the quarter turn and the names in "
              "capitals from session 2, and <code>await</code> from session 1."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. Nothing is loose and nothing is missing.",
            "Every cable is pushed all the way into its port.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session04</code>.",
            "Your ledger card is on the table. You need three things from it: your sensor's "
            "port letter, your number for <code>DARK</code>, and your number for "
            "<code>QUARTER_TURN</code>.",
        ],
        "after": ("The program in chunk 1 is today's test run, once your own three values "
                  "are in it."),
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from session 3?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("What does the colour sensor measure?",
             ["Reflected light: how much of its own light comes back from the floor, as a "
              "number from 0 to 100."]),
            ("Three lines move the robot until the line. What does each of the three do?",
             ["The first starts the wheels. The second waits until the reflected light is "
              "less than <code>DARK</code>. The third stops the wheels."]),
            ("Why does <code>DARK</code> have to be between your floor reading and your "
             "tape reading?",
             ["Then the test is false over the floor, so the hub keeps waiting, and true "
              "over the tape, so the hub goes on to the stop line."]),
            ("Your teacher moves the far line. Why does the robot still stop at it?",
             ["The program waits for a reading from the sensor. It does not count a "
              "distance."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "Read the whole program before it runs",
            "teach": [
                "This program has two parts. Lines 17 to 19 move the robot until the far "
                "line. Lines 22 and 23 turn it and move it forward.",
                "Lines 6 to 9 hold every number the program depends on. Put your own values "
                "on lines 6, 7, and 9 before you run it.",
            ],
            "code": C1,
            "where": ("Type the whole program. Take your time on line 18 and check it against "
                      "your ledger card."),
            "figure": delivery_figure(LEG, caption="The delivery run from above. The far line "
                                      "is drawn at 55 cm here. Your teacher puts it somewhere "
                                      "from %d to %d cm." % (FAR_MIN, FAR_MAX)),
            "setup": SETUP,
            "predict": ("In what order does the robot do things? Which line decides where the "
                        "robot first stops?"),
            "hints": ["Read the two notes, on lines 16 and 21. They say what each part does."],
            "reveal": [
                "The first one: it moves forward until the far line and stops. Then it turns "
                "a quarter turn to its right. Then it moves forward about %d cm." % LEG,
                "The second one: line 18. It waits until the reflected light is less than "
                "<code>DARK</code>. No number of degrees of motor turn decides that first "
                "stop.",
            ],
            "computed": "start the wheels, wait for the line, stop\nquarter turn to the right\nforward 1 full turn of the wheel, about %d cm" % LEG,
            "measure": ("Watch where your robot ends. Is it inside the drop zone? Do not "
                        "change anything yet."),
            "unit": "ends inside the drop zone, yes or no",
            "script": FLOOR_THEN_LINE,
            "expect": [("pair", "A", "E"), STARTED, STOPPED, MOVE_T, MOVE_F],
        },
        {
            "key": "chunk2",
            "title": "Find the fault",
            "teach": [
                "Another team typed the same program, and their robot ends in the wrong "
                "place. Their numbers are all right. Two of their lines are in the wrong "
                "order.",
            ],
            "code": C2,
            "where": "Do not type this one. Read it and compare it with your own program.",
            "show": "Decide first, then check here",
            "figure": delivery_figure(LEG, caption="The delivery run from above, as it should "
                                      "go."),
            "setup": SETUP,
            "predict": ("Which two lines are in the wrong order? What does this robot do after "
                        "it stops at the far line?"),
            "hints": ["Compare lines 22 and 23 with the same lines in chunk 1.",
                      "The hub runs line 22 before line 23. What does line 22 do here?"],
            "reveal": [
                "The first one: lines 22 and 23. The forward line is above the turn line.",
                "The second one: it moves forward about %d cm first, straight past the far "
                "line. Then it turns a quarter turn to its right and stops there. It ends "
                "past the far line, outside the drop zone." % LEG,
                "The fix is to swap the two lines back. The order of the lines is the order "
                "of the moves.",
            ],
            "computed": "start the wheels, wait for the line, stop\nforward about %d cm, past the far line\nquarter turn to the right, last" % LEG,
            "measure": ("You do not need to run this one. If you do, put your lines back in "
                        "the right order afterward."),
            "unit": "ends inside the drop zone, yes or no",
            "script": FLOOR_THEN_LINE,
            "expect": [("pair", "A", "E"), STARTED, STOPPED, MOVE_F, MOVE_T],
        },
    ],
    "checks": [("mission start", START, [("pair", "A", "E"), STARTED, STOPPED], FLOOR_THEN_LINE)],
    "arith": [("one full turn, whole cm", LEG, "about %d cm" % LEG, 360)],

    "hinge": {
        "code": TURN + "\n" + FWD,
        "context": C1,
        "q": ("These are lines 22 and 23. A team wants the robot to end in the same drop "
              "zone, but backing into it. Their plan: turn a quarter turn to the left, then "
              "move backward. What two changes do they make, one on each line?"),
        "a": [
            "On line 22, the steering changes from 100 to -100, so the robot turns to its "
            "left.",
            "On line 23, <code>FORWARD</code> gets a minus sign in front of it, so the robot "
            "moves backward.",
        ],
    },

    "brief": {
        "minutes": 30,
        "title": "The delivery run",
        "intro": [
            "Your robot is the cart that makes the last delivery of the day. It leaves the "
            "start line, finds the far line, turns, and parks in the drop zone. The far "
            "line is somewhere new on every run, and during the demo a visitor chooses "
            "where it goes.",
            "First, plan. There are at least two ways to end in the drop zone: turn right "
            "and move forward, or turn left and move backward. Write both plans down, pick "
            "the one your team thinks will pass more often, and say why.",
        ],
        "figure": delivery_figure(LEG, caption="The delivery run from above. The drop zone is "
                                  "a square of tape, %d cm on each side." % DROP_CM),
        "values": [
            ("Done means", "The robot stops at the far line, wherever it is, and both wheels "
                           "end inside the drop zone, in 3 runs out of 3."),
            ("Far line", "Somewhere from %d to %d cm from the start line." % (FAR_MIN, FAR_MAX)),
            ("Drop zone", "A square of tape, %d cm on each side, to the right of the far "
                          "line." % DROP_CM),
            ("You may use", "Only the Python on your ledger card, with <code>velocity=250</code>."),
            ("You may not", "Touch the robot after the program starts, or change the program "
                            "between the 3 runs."),
            ("Time", "30 minutes, then the demo."),
        ],
        "code": START,
        "code_note": ("Start from this program. Lines 1 to 19 are done, once your own values "
                      "are on lines 6, 7, and 9. Your own lines go under line 21."),
        "plan_head": ["Plan", "The moves, in order", "Why it might pass", "Why it might fail"],
        "plan_rows": [["A", None, None, None], ["B", None, None, None]],
        "steps": [
            "Fill in both rows of the plan sheet. Circle the plan you choose.",
            "Type your lines under line 21.",
            "Fill in the Expected column, then run. One change per run.",
            "When a run passes, ask a builder from another team to move the far line, and "
            "run again without changing the program.",
        ],
        "sheet_head": ["Run", "The one thing changed", "Expected", "Measured: where the "
                       "wheels ended", "Both wheels in the drop zone?"],
        "sheet_rows": [["1", "Nothing yet"], ["2", None], ["3", None], ["4", None], ["5", None]],
        "script": FLOOR_THEN_LINE,
        "expect": [("pair", "A", "E"), STARTED, STOPPED],
    },

    "exits": {
        "floor": ("The robot stops at the far line and turns a quarter turn toward the drop "
                  "zone, and your plan sheet has two plans with one chosen."),
        "middle": ("Both wheels end inside the drop zone with the far line at 55 cm."),
        "stretch": ("Both wheels end inside the drop zone in 3 runs out of 3, with the far "
                    "line in a different place each run."),
    },

    "demo": {
        "minutes": 20,
        "title": "Demo for families",
        "body": [
            "Each team has about four minutes. Decide who says what before your turn.",
        ],
        "steps": [
            "One builder says what the mission is, in one or two sentences.",
            "A visitor puts the far line somewhere between the two marks. The team runs "
            "the program. Do this up to 3 times.",
            "Each builder says which part of the robot they built in session 1.",
            "Each builder points at one line of the program and says what it does.",
            "If a run fails, say what you would change first, and which one thing you "
            "would change.",
        ],
    },

    "ledger_code": "LINE_SENSOR = port.____\nDARK = ____\nQUARTER_TURN = ____",
    "ledger_context": C1,
    "ledger": ("Session 4. Write the three values your team used today. Then write one "
               "sentence: what would you change first if you had one more session?"),
    "stamp": ("Today's stamp is for the demo: you said what one line of your team's program "
              "does."),

    "teacher": {
        "before": [
            "Keep the robots built and charge every hub.",
            "Run the chunk 1 program on the reference robot with the far line at 55 cm. Lay "
            "each lane's drop zone, a %d cm square of tape, centred on where the reference "
            "robot's wheels end." % DROP_CM,
            "Mark %d cm and %d cm beside each lane, so a visitor can put the far line "
            "anywhere between the marks." % (FAR_MIN, FAR_MAX),
            "Decide the order of teams for the demo and where families stand.",
            "Log three runs on the reference robot for the chunk 1 program, with the far "
            "line at 40, 55, and 70 cm.",
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, read the whole program", 8),
            ("0:23", "Chunk 2, find the fault", 7),
            ("0:30", "Hinge question", 3),
            ("0:33", "Mission", 30),
            ("1:03", "Demo for families", 20),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("Families arrive for the demo at 1:03. A team at the floor exit still "
                   "demos: its robot stops at the far line a visitor chose, and each builder "
                   "explains a line. That is a finish."),
        "misconceptions": [
            ("A team's robot ends short of the drop zone or past it.",
             "Ask which number sets the last move. It is <code>FORWARD</code> on line 8. One "
             "change, then run."),
            ("A team's robot turns too far or not far enough.",
             "Ask where the number came from. If it is not the number on their ledger card "
             "from session 2, start there."),
            ("A team rewrites lines 17 to 19 from memory and the robot does not stop.",
             "Send them to the ledger card and compare line 18 one character at a time."),
            ("A team fixes a miss by moving the robot's start.",
             "The start is fixed: behind the start line, front edge on the line. The "
             "program changes, not the setup."),
            ("In the demo a run fails and the team freezes.",
             "Ask the one question on the page: what would you change first? Naming the one "
             "change is a good answer in front of families."),
        ],
        "standards": ["3-5-ETS1-1", "3-5-ETS1-2", "3-5-ETS1-3"],
        "routing": ("If the mission runs long, the demo still starts at 1:03. Cut chunk 2 to "
                    "a spoken question if the room started late. Never cut the plan sheet: "
                    "comparing two plans is what the session is mapped to."),
        "deliberate": ("Chunk 2's program has lines 22 and 23 in the wrong order on purpose. "
                       "The 50, the 180, and <code>port.B</code> are first tries that each "
                       "team replaces with its own values."),
    },
}
