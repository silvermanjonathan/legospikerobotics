"""Session 8 (part 2): your own functions, your own mission, and the second demo.

This session opens the frame that session 1 handed over: async def main() is a
function, and students now write functions of their own beside it. The word lambda
stays unopened.

Each team writes its own mission card: what the robot does, what done means, and
what may not be changed.
"""

from robot import track_figure, delivery_figure, TRACK_CM
from wheel import whole_cm

TOP = '''from hub import motion_sensor, port%s
import %smotor_pair
import runloop

%sQUARTER = 900
'''

TURN_DEF = '''

async def quarter_turn():
    motion_sensor.reset_yaw(0)
    await runloop.sleep_ms(100)
    motor_pair.move(motor_pair.PAIR_1, 100, velocity=100)
    await runloop.until(lambda: abs(motion_sensor.tilt_angles()[0]) > QUARTER)
    motor_pair.stop(motor_pair.PAIR_1)
'''

FOLLOW_DEF = '''

async def follow_to_bar():
    while color_sensor.reflection(STOP_SENSOR) > DARK:
        if color_sensor.reflection(LINE_SENSOR) < DARK:
            motor_pair.move(motor_pair.PAIR_1, 30, velocity=150)
        else:
            motor_pair.move(motor_pair.PAIR_1, -30, velocity=150)
    motor_pair.stop(motor_pair.PAIR_1)
'''

MAIN = '''

async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

'''
END = '''


runloop.run(main())'''

C1 = (TOP % ("", "", "") + TURN_DEF + MAIN
      + "    await quarter_turn()\n    await quarter_turn()" + END)

NAMES = "LINE_SENSOR = port.B\nSTOP_SENSOR = port.F\nDARK = 50\nFORWARD = 360\n"
PLAN = ("    await follow_to_bar()\n    await quarter_turn()\n"
        "    await motor_pair.move_for_degrees(motor_pair.PAIR_1, FORWARD, 0, velocity=250)\n"
        "    await sound.beep(880, 500, 100)")
C2 = TOP % (", sound", "color_sensor\nimport ", NAMES) + FOLLOW_DEF + TURN_DEF + MAIN + PLAN + END
START = (TOP % (", sound", "color_sensor\nimport ", NAMES) + FOLLOW_DEF + TURN_DEF + MAIN
         + "    # Your plan goes here, one step on each line." + END)
HINGE = "    await quarter_turn()\n    await follow_to_bar()"

LEG = whole_cm(360)
WIGGLE = {"F": [80, 80, 80, 80, 10], "B": [10, 80, 10, 80]}
TURN = [("reset",), ("wait", 100), ("start", 100, 100), ("stop",)]
FOLLOW = [("start", 30, 150), ("start", -30, 150)] * 2 + [("stop",)]

SESSION08 = {
    "num": 8,
    "part": 2,
    "slug": "session08_your_own_functions_and_mission",
    "title": "Your own functions, your own mission",
    "subtitle": ("A group of lines gets a name. Then your team writes its own mission, "
                 "programs it, and shows it."),
    "new": ["async def name():", "await name()"],
    "new_text": ("<code>async def quarter_turn():</code> gives a group of lines a name. "
                 "<code>await quarter_turn()</code> runs that group of lines. A named group "
                 "of lines is called a function."),
    "reuse": ("The measured turn from session 6, the line follower from session 7, and the "
              "beep from session 5. They go inside functions today."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. Nothing is loose and nothing is missing.",
            "Every cable is pushed all the way into its port.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session08</code>.",
            "Your ledger card is on the table. You need your two port letters, your "
            "<code>DARK</code>, your <code>QUARTER</code>, and your steering and speed.",
        ],
        "after": ("The program in chunk 1 is today's test run, once your own "
                  "<code>QUARTER</code> is in it."),
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from session 7?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("An <code>if</code> line has an <code>else</code> line under it. How many of "
             "the two groups of lines run each time?",
             ["Exactly one. The lines inside <code>if</code> run when the test is true, and "
              "the lines inside <code>else</code> run when it is false."]),
            ("What does a <code>while</code> line do, and what ends it?",
             ["It runs the lines inside it again and again while its test is true. It ends "
              "when the test becomes false."]),
            ("In the line follower, what ended the <code>while</code> line?",
             ["The stop sensor reached the stop bar and read less than <code>DARK</code>."]),
            ("Every program since session 1 has had the line "
             "<code>async def main():</code> in it. What do you think that line does?",
             ["Talk about it now. Chunk 1 answers it."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "Give a group of lines a name",
            "teach": [
                "Lines 8 to 13 are the measured turn from session 6. Line 8 gives those "
                "lines a name: <code>quarter_turn</code>. A named group of lines is called "
                "a <b>function</b>. Writing it does not run it.",
                "Line 20 runs it: <code>await quarter_turn()</code>. The hub goes up to "
                "line 8, runs lines 9 to 13, then comes back and goes on to line 21.",
                "Now look at line 16. It has the same shape as line 8. "
                "<code>main</code> is a function too, and you have been writing it since "
                "session 1. The last line of the program, "
                "<code>runloop.run(main())</code>, is the line that runs it.",
            ],
            "code": C1,
            "where": ("Put your own number on line 5. Line 8 starts at the left edge, like "
                      "line 16, with two empty lines above it. The brackets after the name "
                      "are needed on lines 8, 20, and 21."),
            "figure": track_figure(caption="Today's field from above. Chunk 1 uses only the "
                                   "floor: put the robot anywhere with room to turn."),
            "setup": ("Setup: the robot sits on the floor with room to turn, facing along the "
                      "line. It starts here on every run."),
            "predict": ("How many quarter turns does the robot make? Which way does it face "
                        "when the program ends, compared with the start?"),
            "hints": ["Count the lines inside <code>main</code> that say "
                      "<code>await quarter_turn()</code>.",
                      "Two quarter turns to the right, one after the other, make what?"],
            "reveal": [
                "The first one: 2. Lines 20 and 21 each run the function once.",
                "The second one: the opposite way. Two quarter turns make a half turn, so "
                "the robot faces back the way it came, or close to it.",
            ],
            "computed": "quarter turn to the right\nquarter turn to the right\n2 quarter turns = a half turn: the robot faces the opposite way",
            "measure": ("Add a third <code>await quarter_turn()</code> line. Say which way the "
                        "robot will face before you run it."),
            "unit": "direction faced at the end",
            "expect": [("pair", "A", "E")] + TURN + TURN,
        },
        {
            "key": "chunk2",
            "title": "A program that reads like a plan",
            "teach": [
                "This program has two functions of its own: <code>follow_to_bar</code> is "
                "the line follower from session 7, and <code>quarter_turn</code> is the "
                "measured turn.",
                "With the hard parts named, <code>main</code> is short. Lines 34 to 37 are "
                "the plan, one step on each line. You can read what the robot will do "
                "without reading how it does it.",
            ],
            "code": C2,
            "where": ("Type <code>follow_to_bar</code> above <code>quarter_turn</code>. Put "
                      "your own values on lines 6 to 10, and your own steering and speed on "
                      "lines 16 and 18."),
            "figure": track_figure(caption="The line and its stop bar from above. The line is "
                                   "%d cm long." % TRACK_CM),
            "setup": ("Setup: the robot is at the start of the line, facing along it, with the "
                      "line sensor over the tape. It starts here on every run."),
            "predict": ("Read only lines 34 to 37. In what order does the robot do things, "
                        "and what is the last thing that happens?"),
            "hints": ["Each of the four lines is one step. Read their names."],
            "reveal": [
                "It follows the line to the stop bar. Then it turns a quarter turn to its "
                "right. Then it moves forward about %d cm. The last thing is a high beep "
                "from the hub." % LEG,
                "You could answer that from four lines, because the names say what the "
                "lines do.",
            ],
            "computed": "follow the line to the stop bar\nquarter turn to the right\nforward 1 full turn of the wheel, about %d cm\nbeep, pitch 880" % LEG,
            "measure": "Run it and check each step against the plan as it happens.",
            "unit": "steps done in order, yes or no",
            "script": WIGGLE,
            "expect": ([("pair", "A", "E")] + FOLLOW + TURN + [("move", 360, 0, 250),
                                                              ("beep", 880, 500)]),
        },
    ],
    "checks": [("mission start", START, [("pair", "A", "E")], None)],
    "arith": [("one full turn, whole cm", LEG, "about %d cm" % LEG, 360)],

    "hinge": {
        "code": HINGE,
        "context": C2,
        "q": ("A team swaps two lines of the plan, so <code>main</code> has these two lines "
              "first. The robot starts at the start of the line, as before. What does it "
              "do first, and is it likely to reach the stop bar?"),
        "a": [
            "It turns a quarter turn to its right first, away from the line.",
            "It is not likely to reach the stop bar. After the turn, the line sensor is no "
            "longer over the line the follower needs. The order of the lines in "
            "<code>main</code> is the order of the steps.",
        ],
    },

    "brief": {
        "minutes": 25,
        "title": "Write your own mission",
        "intro": [
            "Until now the warehouse gave the orders. Today your team runs the warehouse. "
            "Decide what your cart should do, write it down as a mission card, and then "
            "program it. Another team will read your card and check your robot against it.",
            "A good mission card says what the robot does, what done means, and what may "
            "not be changed. Write the card before you type.",
        ],
        "figure": delivery_figure(LEG, caption="One field you may use: the delivery run from "
                                  "session 4. You may also use the shelf lines, the line with "
                                  "its stop bar, or the square."),
        "values": [
            ("Your mission must use", "At least two functions of your own, each run with "
                                      "<code>await</code>, and one sound or one number on "
                                      "the light matrix."),
            ("It may use", "Any field from sessions 1 to 7, and any Python on your ledger card."),
            ("Done means", "Your team writes this. It must be something another team can "
                           "check by looking or measuring."),
            ("Time", "25 minutes, then the demo."),
        ],
        "plan_title": "Your mission card",
        "plan_intro": "Fill in the first three rows before you type anything.",
        "plan_head": ["Mission card", "Your team's words"],
        "plan_rows": [["What the robot does, in order", None],
                      ["Done means", None],
                      ["You may not", None],
                      ["Checked by (another team)", None]],
        "code": START,
        "code_note": ("Start from this program. Both functions are ready, once your own "
                      "values are in. Write your plan under line 34, and add a function of "
                      "your own if your mission needs one."),
        "steps": [
            "Fill in the mission card.",
            "Write the plan in <code>main</code>, one step on each line.",
            "Fill in Expected, then run. One change per run.",
            "Swap cards with another team. Run your mission for them and let them fill in "
            "the last row of your card.",
        ],
        "sheet_head": ["Run", "The one thing changed", "Expected", "Measured",
                       "Done, by your own card?"],
        "sheet_rows": [["1", "Nothing yet"], ["2", None], ["3", None], ["4", None], ["5", None]],
        "expect": [("pair", "A", "E")],
    },

    "exits": {
        "floor": ("The chunk 2 program runs with your team's own values, and your mission "
                  "card is filled in."),
        "middle": ("Your robot does your own mission once, and <code>main</code> reads as a "
                   "plan with one step on each line."),
        "stretch": ("Another team has checked your robot against your card and written "
                    "that it passes, in 3 runs out of 3."),
    },

    "demo": {
        "minutes": 20,
        "title": "Demo for families",
        "body": [
            "Each team has about four minutes. Decide who says what before your turn.",
        ],
        "steps": [
            "One builder reads the team's mission card aloud.",
            "The team runs the mission, up to 3 times.",
            "One builder shows <code>main</code> on the screen and reads the plan, one line "
            "at a time.",
            "Each builder names one function and says what it does.",
            "If a run fails, say which step of the plan it failed at and what you would "
            "change first.",
        ],
    },

    "ledger_code": "async def quarter_turn():\n    ...\n\nawait quarter_turn()",
    "ledger_context": C1,
    "ledger": ("Session 8. The first line gives a group of lines a name. The last line runs "
               "them. Write the names of your team's functions, and one sentence about "
               "your own mission."),
    "stamp": ("Today's stamp is for the demo: you named one function and said what it does."),

    "teacher": {
        "before": [
            "Charge every hub. Each team needs its ledger card with its own values.",
            "Lay out one of each field: the lane with a drop zone, the shelf lines, the line "
            "with its stop bar, and space for a square. Teams choose.",
            "Print one blank mission card for each team, or have them use the page.",
            "Decide the order of teams for the demo and where families stand.",
            "Log three runs of the chunk 1 and chunk 2 programs on the reference robot.",
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, give lines a name", 10),
            ("0:25", "Chunk 2, a program that reads like a plan", 10),
            ("0:35", "Hinge question", 3),
            ("0:38", "Mission", 25),
            ("1:03", "Demo for families", 20),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("Chunk 2's program is long to type. If devices still hold the session 6 "
                   "and 7 projects, let teams copy from them. A team at the floor exit "
                   "demos the chunk 2 program and reads its plan aloud. That is a finish."),
        "misconceptions": [
            ("A team writes <code>quarter_turn</code> without the brackets, or without "
             "<code>await</code>.",
             "The robot skips the turn. Compare the line with line 20 of chunk 1, one "
             "character at a time."),
            ("A function is typed inside <code>main</code>, or <code>main</code> inside a "
             "function.",
             "Each <code>async def</code> line starts at the left edge with two empty "
             "lines above it. Point at the grey bars on the page."),
            ("A team's mission card says \"the robot does it well\".",
             "Ask how another team would check that with a ruler or by looking. Done means "
             "something that can be seen or measured."),
            ("A team plans a mission that needs something new.",
             "The card says: any Python on your ledger card. Ask which of their functions "
             "could do the nearest thing."),
            ("In the demo a run fails.",
             "Ask which step of the plan it failed at. Reading <code>main</code> to find "
             "the step is the skill the session teaches."),
        ],
        "standards": ["3-5-ETS1-1", "3-5-ETS1-2", "3-5-ETS1-3"],
        "routing": ("If the mission runs long, the demo still starts at 1:03. Never cut the "
                    "mission card: writing what done means is what the session is mapped "
                    "to."),
        "deliberate": ("Session 1 handed over <code>async def main():</code> and "
                       "<code>runloop.run(main())</code> without explaining them. Chunk 1 "
                       "of this session explains them. The word <code>lambda</code> stays "
                       "unexplained."),
    },
}
