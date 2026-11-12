"""Session 6 (part 2): the motion sensor, and turns that measure themselves.

The hub's motion sensor counts the robot's turn in tenths of a degree. The turn ends
when the sensor's count passes QUARTER, not after a number of degrees of motor turn.

Two things are stated plainly on the page because published tests of the SPIKE App 3
support them: the count needs a moment after reset_yaw before it reads 0, and the
robot ends a little past the angle it waited for. How far past is measured, not
printed.
"""

from robot import cross_figure, square_figure
from wheel import nearest5, cm

READ = '''from hub import motion_sensor
import runloop


async def main():
    motion_sensor.reset_yaw(0)
    await runloop.sleep_ms(5000)
    print(motion_sensor.tilt_angles()[0])


runloop.run(main())'''

HEAD = '''from hub import motion_sensor, port
import motor_pair
import runloop

%s

async def main():
    # The left drive motor is in port A. The right drive motor is in port E.
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

'''
END = '''


runloop.run(main())'''
WAIT = "await runloop.until(lambda: abs(motion_sensor.tilt_angles()[0]) > QUARTER)"


def turn(velocity, pad="    "):
    return (pad + "motion_sensor.reset_yaw(0)\n" + pad + "await runloop.sleep_ms(100)\n"
            + pad + "motor_pair.move(motor_pair.PAIR_1, 100, velocity=%d)\n" % velocity
            + pad + WAIT + "\n" + pad + "motor_pair.stop(motor_pair.PAIR_1)")


NOTE = "    # Set the count to 0. Turn right until the count passes QUARTER. Stop.\n"
C2 = HEAD % "QUARTER = 900\n" + NOTE + turn(250) + END
C3 = HEAD % "QUARTER = 900\n" + NOTE + turn(100) + END
MISSION = (HEAD % "FORWARD = 720\nQUARTER = 900\n"
           + "    for count in range(4):\n"
           + "        await motor_pair.move_for_degrees(motor_pair.PAIR_1, FORWARD, 0, velocity=250)\n"
           + turn(100, pad="        ") + END)

SIDE = nearest5(cm(720))
TURN_250 = [("reset",), ("wait", 100), ("start", 100, 250), ("stop",)]
TURN_100 = [("reset",), ("wait", 100), ("start", 100, 100), ("stop",)]

SETUP = ("Setup: the robot sits over the middle of the turn cross and faces along "
         "strip 1. It starts here on every run.")

SESSION06 = {
    "num": 6,
    "part": 2,
    "slug": "session06_turns_that_measure_themselves",
    "title": "Turns that measure themselves",
    "subtitle": ("The hub has a sensor that counts how far the robot has turned. The turn "
                 "ends when the count is big enough."),
    "new": ["motion_sensor.reset_yaw", "motion_sensor.tilt_angles()[0]", "abs",
            "runloop.sleep_ms"],
    "new_text": ("<code>motion_sensor.tilt_angles()[0]</code> gives the robot's turn as a "
                 "number. <code>motion_sensor.reset_yaw(0)</code> sets that number back to "
                 "0. <code>abs</code> takes away a minus sign. "
                 "<code>runloop.sleep_ms</code> waits for a set time."),
    "reuse": ("Start the wheels, wait, stop the wheels, from session 3. The turn cross and "
              "the square from session 2."),

    "check": {
        "minutes": 5,
        "items": [
            "The robot matches the robot page. Nothing is loose and nothing is missing.",
            "Every cable is pushed all the way into its port.",
            "The hub is charged, switched on, and connected to the SPIKE App.",
            "A new Python project is open and named, like <code>Jonathan_session06</code>.",
            "The robot is standing still on the table when you press run. The motion sensor "
            "needs the hub to be still at the start.",
        ],
        "after": "The program in chunk 1 is today's test run. It uses no motors.",
    },

    "opener": {
        "minutes": 10,
        "title": "What do you remember from session 5?",
        "body": ("Talk each question through with your team before you open its answer. "
                 "Your ledger card can help."),
        "questions": [
            ("Crossing a line took two waits. What was each one waiting for?",
             ["The first waited for the tape: a reading less than <code>DARK</code>. The "
              "second waited for the floor after the tape: a reading greater than "
              "<code>DARK</code>."]),
            ("In <code>for count in range(3):</code>, what numbers does <code>count</code> "
             "hold?",
             ["0, then 1, then 2. Python starts counting at 0."]),
            ("In session 2 your team found its own number for a quarter turn. What did that "
             "number count?",
             ["Degrees of motor turn. It was found by testing, and it was different from "
              "the 90 degrees of the robot's turn in a quarter turn."]),
            ("What do the three lines \"start the wheels, wait, stop the wheels\" let the "
             "robot do that a number of degrees of motor turn cannot?",
             ["Stop when a sensor's reading changes, wherever that happens."]),
        ],
    },

    "chunks": [
        {
            "key": "chunk1",
            "title": "The hub counts its own turn",
            "teach": [
                "Inside the hub is a <b>motion sensor</b>. It measures how far the hub has "
                "turned since the count was last set to 0. It counts in tenths of a degree "
                "of the robot's turn, so a quarter turn, which is 90 degrees of the robot's "
                "turn, counts as about 900.",
                "Line 6 sets the count to 0. Line 7 waits 5000 thousandths of a second, "
                "which is 5 seconds. Line 8 prints the count. The <code>[0]</code> picks "
                "the first of three numbers the sensor gives. Type it exactly.",
            ],
            "code": READ,
            "where": ("During the 5 seconds, one builder turns the robot by hand, flat on the "
                      "table, a quarter turn to its right."),
            "figure": cross_figure(caption="The turn cross from above. Turn the robot by hand "
                                   "from strip 1 to strip 2."),
            "setup": ("Setup: the robot sits still over the middle of the turn cross, facing "
                      "along strip 1. Press run, then turn it by hand to face along strip 2."),
            "predict": ("Which is the printed number closest to: 9, 90, or 900? It may have a "
                        "minus sign in front."),
            "hints": ["The sensor counts in tenths. How many tenths are in 90 whole ones?"],
            "reveal": [
                "900, or close to it. The robot turned about 90 degrees of the robot's turn, "
                "and the sensor counts each one as 10.",
                "Turning one way gives a minus sign and turning the other way does not. Run "
                "it twice, once turning right and once turning left, and write both numbers "
                "in the sheet.",
            ],
            "computed": "a quarter turn is 90 degrees of the robot's turn\nthe sensor counts in tenths: 90 x 10 = 900",
            "measure": "Your numbers will not be exactly 900, because a hand is not exact.",
            "unit": "count for a quarter turn by hand, right then left",
            "sheet": {
                "title": "Your two counts",
                "intro": "Write what the console prints, with its minus sign if it has one.",
                "head": ["Turned by hand", "Printed count"],
                "rows": [["A quarter turn to the robot's right", None],
                         ["A quarter turn to the robot's left", None]],
            },
            "expect": [("reset",), ("wait", 5000)],
            "prints": ["-100"],
        },
        {
            "key": "chunk2",
            "title": "Turn until the count says a quarter turn",
            "teach": [
                "This is start, wait, stop again, with a new test. Line 13 sets the count "
                "to 0, and line 14 waits a tenth of a second for the sensor to settle. "
                "Line 15 starts a turn to the right on the spot.",
                "Line 16 waits until the count is greater than <code>QUARTER</code>. "
                "<code>abs</code> takes away a minus sign, so the test works whichever way "
                "the sensor counts. Line 17 stops the wheels.",
            ],
            "code": C2,
            "where": "Type the whole program. Take your time with the brackets on line 16.",
            "parts_title": "The parts of line 16",
            "parts": [
                ("motion_sensor.tilt_angles()[0]", "The count: the robot's turn, in tenths of a degree of the robot's turn."),
                ("abs( )", "Takes away a minus sign, so -900 and 900 both count as 900."),
                ("> QUARTER", "The test: the count is greater than QUARTER."),
            ],
            "figure": cross_figure(caption="The turn cross from above."),
            "setup": SETUP,
            "predict": ("What ends this turn: a number of degrees of motor turn, or a reading "
                        "from a sensor? Does the robot end facing exactly along strip 2, a "
                        "little short of it, or a little past it?"),
            "hints": ["Read line 16. Then think about the wheels at the moment the test "
                      "becomes true: are they still turning?"],
            "reveal": [
                "The first one: a reading from a sensor. No line in this program counts "
                "degrees of motor turn.",
                "The second one: a little past. The wheels are still turning at the moment "
                "the count passes 900, and they take a moment to stop.",
            ],
            "computed": "set the count to 0, wait, start turning right\nwait until the count passes 900\nstop: the wheels take a moment, so the robot ends a little past",
            "measure": ("Run it three times from the same start. Does it end in the same place "
                        "each time? That matters more than how far past it is."),
            "unit": "past strip 2: a little or a lot",
            "expect": [("pair", "A", "E")] + TURN_250,
        },
        {
            "key": "chunk3",
            "title": "A slower turn, and your own QUARTER",
            "teach": [
                "Two things bring the robot closer to strip 2. One is to turn more slowly. "
                "The other is to ask for a little less than 900, so that going past it "
                "lands in the right place.",
                "This program changes only the speed of the turn, on line 15, from 250 to "
                "100. One change per run.",
            ],
            "code": C3,
            "where": "Change only line 15.",
            "figure": cross_figure(caption="The turn cross from above."),
            "setup": SETUP,
            "predict": ("Which turn ends further past strip 2: the turn at "
                        "<code>velocity=250</code> or the turn at <code>velocity=100</code>?"),
            "hints": ["Which wheels take longer to stop, fast ones or slow ones?"],
            "reveal": [
                "The turn at 250. Faster wheels take longer to stop, so the robot turns "
                "further in that time.",
                "Now keep the speed at 100 and change <code>QUARTER</code> on line 5, one "
                "change per run, until the robot ends along strip 2. Use the sheet below.",
            ],
            "computed": "velocity=250: ends further past strip 2\nvelocity=100: ends closer to strip 2",
            "measure": ("Write your team's number for <code>QUARTER</code> on your ledger "
                        "card."),
            "unit": "past strip 2: a little or a lot",
            "sheet": {
                "title": "Expected and measured: your QUARTER",
                "intro": "Fill in the Expected column before each run. One change per run.",
                "head": ["Run", "QUARTER on line 5", "Expected: short of strip 2, along it, "
                         "or past it", "Measured: what the robot did", "Along strip 2?"],
                "rows": [["1", "900"], ["2", None], ["3", None], ["4", None], ["5", None]],
            },
            "expect": [("pair", "A", "E")] + TURN_100,
        },
    ],
    "checks": [],

    "hinge": {
        "code": "    " + WAIT,
        "context": C2,
        "q": ("A team wants a half turn, which is 180 degrees of the robot's turn. Before any "
              "testing, what first try should they give <code>QUARTER</code>? And is the "
              "name still a good one?"),
        "a": [
            "1800. The sensor counts in tenths, so 180 counts as 1800.",
            "The name is no longer good. A number for a half turn should be called "
            "something like <code>HALF</code>. Names say what they do.",
        ],
    },

    "brief": {
        "minutes": 31,
        "title": "Two ways to turn: which is better?",
        "intro": [
            "The warehouse wants its cart to drive a square route around a crate, like in "
            "session 2, and it wants to know which way of turning to trust. Your team has "
            "two: the counted turn from session 2, which uses your number of degrees of "
            "motor turn, and the measured turn from today, which uses the motion sensor.",
            "You will run the same square both ways and let the wheel markers decide.",
        ],
        "figure": square_figure(SIDE, crate=True, caption="The square from above. Each side is "
                                "about %d cm." % SIDE),
        "values": [
            ("Start", "At the first corner, facing along side 1, with a wheel marker beside "
                      "each wheel."),
            ("Plan A", "The session 2 square program, with your team's "
                       "<code>QUARTER_TURN</code> from your ledger card."),
            ("Plan B", "The program below, with your team's <code>QUARTER</code> from today."),
            ("Fair test", "Three runs of each plan, from the same start, on the same floor."),
            ("Done means", "Six rows filled in, and one sentence saying which plan your team "
                           "would choose and why."),
        ],
        "plan_head": ["Plan", "How the turn ends", "Our guess: closer or further from the "
                      "markers?", "Why we think so"],
        "plan_rows": [["A, counted", None, None, None], ["B, measured", None, None, None]],
        "code": MISSION,
        "code_note": ("This is plan B. Lines 14 to 19 are inside the <code>for</code> line: "
                      "one side, then one measured turn. Put your own number on line 6."),
        "steps": [
            "Fill in the plan sheet with your guesses before any run.",
            "Run plan B three times. After each run, measure how far each wheel is from its "
            "marker and write down the bigger of the two.",
            "Run plan A three times and do the same.",
            "Compare the six numbers. Which plan lands closer? Which plan lands in the same "
            "place each time?",
        ],
        "sheet_head": ["Run", "Plan", "Expected", "Measured: cm from the markers",
                       "Touched the crate?"],
        "sheet_rows": [["1", "B"], ["2", "B"], ["3", "B"], ["4", "A"], ["5", "A"], ["6", "A"]],
        "expect": [("pair", "A", "E")] + ([("move", 720, 0, 250)] + TURN_100) * 4,
    },

    "exits": {
        "floor": ("Your team has its own <code>QUARTER</code>, found by testing on the turn "
                  "cross, and the measured turn ends along strip 2."),
        "middle": ("Three runs of plan B are measured and written down, and the square does "
                   "not touch the crate."),
        "stretch": ("All six runs are measured, and your team has written which plan it "
                    "would choose and what the numbers say about it."),
    },

    "ledger_code": ("motion_sensor.reset_yaw(0)\nawait runloop.sleep_ms(100)\n"
                    "motor_pair.move(motor_pair.PAIR_1, 100, velocity=100)\n" + WAIT
                    + "\nmotor_pair.stop(motor_pair.PAIR_1)"),
    "ledger_context": C3,
    "ledger": ("Session 6. A measured turn: set the count to 0, start turning, wait until "
               "the count passes QUARTER, stop. Write your team's QUARTER beside it. The "
               "sensor counts in tenths."),
    "stamp": ("To get today's stamp, tell your teacher why the robot ends a little past the "
              "angle it waited for."),

    "teacher": {
        "before": [
            "Charge every hub. The robots must be the same build as in session 2, or plan "
            "A's number no longer fits.",
            "Lay out the turn crosses and the square spaces from session 2, with one crate "
            "for each team.",
            "Each team needs its session 2 square program. If it is not on the device, the "
            "team types it again from the session 2 page with its own number.",
            "Log three runs of each program on the reference robot, and the reference "
            "robot's own <code>QUARTER</code>.",
        ],
        "timing": [
            ("0:00", "Robot check", 5),
            ("0:05", "Opener", 10),
            ("0:15", "Chunk 1, the hub counts its own turn", 10),
            ("0:25", "Chunk 2, turn until the count", 10),
            ("0:35", "Chunk 3, a slower turn and your own QUARTER", 13),
            ("0:48", "Hinge question", 4),
            ("0:52", "Mission", 31),
            ("1:23", "Pack away", 5),
            ("1:28", "Ledger stamp", 2),
        ],
        "pacing": ("The mission is a comparison, and either answer is a good one if the "
                   "numbers back it. Do not tell teams which plan should win. Stopping at "
                   "the floor exit is a finish."),
        "misconceptions": [
            ("The robot spins and does not stop.",
             "Check line 16 against the page: the <code>[0]</code>, the <code>abs</code>, "
             "and <code>&gt;</code>. Then check that line 13 is there."),
            ("The turn ends at once, before the robot has turned.",
             "Line 14 may be missing. The count needs a moment after line 13 before it "
             "reads 0."),
            ("A student says the sensor is broken because the robot went past.",
             "Ask what the wheels were doing at the moment the count passed 900. Then run "
             "chunk 3: the same sensor, slower wheels."),
            ("The printed count in chunk 1 is small, even after a good hand turn.",
             "The robot was lifted or tilted while it was turned. Slide it flat on the "
             "table."),
            ("A team decides plan B must be better because it uses a sensor.",
             "Ask for the six numbers. The plan sheet has their guess; the run sheet has "
             "the answer, and they may differ."),
        ],
        "standards": ["3-5-ETS1-2", "3-5-ETS1-3", "NY-4.MD.5.b"],
        "routing": ("If time is short, run plan B three times and plan A once. Keep the "
                    "written sentence: comparing two solutions is what the session is "
                    "mapped to."),
        "deliberate": ("The 900 for <code>QUARTER</code> is a first try that lands past "
                       "strip 2 on purpose. Each team replaces it with its own number."),
    },
}
