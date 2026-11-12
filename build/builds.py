"""Word Block snippets for two more LEGO builds: the Game Master and the Grabbers.

These are SPIKE App Word Blocks, not Python, by Jonathan's direction on 12 November
2026. The snippets are written for this course. They are not copies of LEGO's
programs. Each one uses a single stack and only the blocks listed on the constraints
page for this page.

What came from LEGO, and where:
  - Ports. LEGO's own block programs for these models use port A for the motor and
    port B for the colour sensor on the Game Master, and port A for the motor and
    port E for the force sensor on the Grabbers' hand controller.
  - The Game Master's moves. LEGO's program runs motor A counterclockwise for 2.1
    seconds before it reads, and turns it 95 degrees of motor turn clockwise between
    one brick and the next. The snippets use the same two numbers.
  - The Grabbers' directions. LEGO's program turns motor A counterclockwise while the
    force sensor is pressed and clockwise when it is released. The snippets take
    counterclockwise as close and clockwise as open. That reading is checked on the
    built model, as the teacher panel says.
  - Block words and sound names (Bite, Win, Oops), as LEGO's programs show them.

LEGO's own lesson for the Game Master uses lists and broadcast messages. This course
uses neither, so these snippets reach the same result, the place of the red brick,
with a counter.
"""

from blocks import hat, blk, cblock, num, txt, dd, port, cw, ccw, boolean, var

_ASSET = "https://assets.education.lego.com/v3/assets/blt293eea581807678a/"

START = hat("events", "when program starts")


# ---------------------------------------------------------------- Game Master

def _red():
    return boolean("sensors", port("B"), "is color", dd("red"), "?")


READY = blk("motors", port("A"), "run", ccw(), "for", num("2.1"), dd("seconds"))
NEXT_BRICK = blk("motors", port("A"), "run", cw(), "for", num("95"), dd("degrees"))
PAUSE = blk("control", "wait", num("1"), "seconds")

G1 = [START, READY, blk("sound", "play sound", dd("Bite"), "until done")]
G2 = [START,
      cblock("control", ("if", _red(), "then"),
             [blk("sound", "play sound", dd("Win"), "until done")],
             [blk("sound", "play sound", dd("Oops"), "until done")])]
G3 = [START, READY,
      cblock("control", ("repeat", num("5")),
             [cblock("control", ("if", _red(), "then"),
                     [blk("sound", "play beep", num("72"), "for", num("0.2"), "seconds")]),
              NEXT_BRICK, PAUSE])]
G4 = [START,
      blk("variables", "set", dd("spot"), "to", num("0")),
      READY,
      cblock("control", ("repeat", num("5")),
             [blk("variables", "change", dd("spot"), "by", num("1")),
              cblock("control", ("if", _red(), "then"),
                     [blk("light", "write", var("spot"))]),
              NEXT_BRICK, PAUSE])]
G5 = [START,
      blk("variables", "set", dd("red bricks"), "to", num("0")),
      READY,
      cblock("control", ("repeat", num("5")),
             [cblock("control", ("if", _red(), "then"),
                     [blk("variables", "change", dd("red bricks"), "by", num("1"))]),
              NEXT_BRICK, PAUSE]),
      blk("light", "write", var("red bricks"))]


# ---------------------------------------------------------------- Grabbers

def _force(state):
    return boolean("sensors", port("E"), "is", dd(state), "?")


OPEN = blk("motors", port("A"), "run", cw(), "for", num("0.5"), dd("seconds"))
CLOSE_ON = blk("motors", port("A"), "start motor", ccw())
WAIT_PRESS = blk("control", "wait until", _force("pressed"))
WAIT_LET_GO = blk("control", "wait until", _force("released"))

R1 = [START, blk("motors", port("A"), "run", ccw(), "for", num("0.5"), dd("seconds")),
      blk("control", "wait", num("1"), "seconds"), OPEN]
R2 = [START, WAIT_PRESS, CLOSE_ON, WAIT_LET_GO, OPEN]
R3 = [START, cblock("control", ("repeat", num("5")), [WAIT_PRESS, CLOSE_ON, WAIT_LET_GO, OPEN])]
R4 = [START,
      blk("variables", "set", dd("grabs"), "to", num("0")),
      cblock("control", ("repeat", num("5")),
             [WAIT_PRESS, CLOSE_ON,
              blk("variables", "change", dd("grabs"), "by", num("1")),
              blk("light", "write", var("grabs")),
              WAIT_LET_GO, OPEN])]
R5 = [START, blk("motors", port("A"), "set speed to", num("30"), "%"),
      WAIT_PRESS, CLOSE_ON, WAIT_LET_GO, OPEN]


# ---------------------------------------------------------------- the page

BUILDS = [
    {
        "id": "game-master",
        "title": "The Game Master",
        "intro": [
            "The Game Master is a machine for a memory game. You push a candy stick into "
            "it: a row of five LEGO bricks in different colours. Motor A moves the candy "
            "stick along, one brick at a time, and the colour sensor in port B measures "
            "the colour of the brick above it.",
            "Every snippet here starts by moving the candy stick to its start. Then it "
            "turns motor A by 95 degrees of motor turn to move the stick on by one brick. "
            "LEGO's own program for this model uses the same two moves.",
        ],
        "books": [(1, "Body", _ASSET + "bltd0746117b01a34aa/5f8802c3e1d537018da30e20/brain-game-bi-pdf-book1of2.pdf?locale=en-us"),
                  (2, "Head", _ASSET + "bltb85fa1938f86d44d/5f880280c3d3c30be7c15202/brain-game-bi-pdf-book2of2.pdf?locale=en-us")],
        "team": "Two builders: one builds the body, one builds the head, then join them.",
        "ports": [("A", "Motor", "Moves the candy stick"),
                  ("B", "Colour sensor", "Measures the colour of one brick of the candy stick")],
        "lesson": "https://education.lego.com/en-us/lessons/prime-life-hacks/brain-game/",
        "snippets": [
            {"key": "g1", "title": "Get the candy stick ready", "stack": G1,
             "teach": "This is the start of every Game Master program on this page.",
             "setup": "Setup: a candy stick is pushed into the Game Master.",
             "q": "Which happens first, the motor or the sound? Does the sound start while the motor is still turning?",
             "a": ["The motor turns first, then the sound plays.",
                   "No. A <b>run for</b> block finishes before the block under it starts, so "
                   "the sound waits until the motor has turned for 2.1 seconds."]},
            {"key": "g2", "title": "Is this brick red?", "stack": G2,
             "teach": ("The six-sided block asks a question that is true or false. The if "
                       "block runs the blocks in its top part when the answer is true, and "
                       "the blocks in its else part when the answer is false. It never runs both."),
             "setup": "Setup: hold one brick over the colour sensor, then run the program. Try a red brick, then a blue one.",
             "q": "Which sound plays for the red brick? Which sound plays for the blue brick?",
             "a": ["Red brick: Win. The answer to the question is true, so the top part runs.",
                   "Blue brick: Oops. The answer is false, so the else part runs."]},
            {"key": "g3", "title": "Read all five bricks", "stack": G3,
             "teach": ("The repeat block runs the blocks inside it 5 times: one time for "
                       "each brick. Each time, it checks the brick, then moves the candy "
                       "stick on by one brick, then waits 1 second."),
             "setup": "Setup: a candy stick with red bricks in places 2 and 4. Place 1 is the first brick the colour sensor measures.",
             "q": "How many beeps do you hear? How many times does motor A turn by 95 degrees of motor turn?",
             "a": ["2 beeps, one for each red brick. The beep plays only when the answer to the question is true.",
                   "5 times. The motor block is inside the repeat block but not inside the if "
                   "block, so it runs every time round, red or not."]},
            {"key": "g4", "title": "Which place is the red brick in?", "stack": G4,
             "teach": ("A <b>variable</b> is a name that holds a number. This program counts "
                       "the places in a variable called spot. It starts at 0 and goes up by "
                       "1 for each brick. When the brick is red, the light matrix shows spot."),
             "setup": "Setup: a candy stick with one red brick, in place 3.",
             "q": "What number does the light matrix show?",
             "a": ["3. spot goes up by 1 before each brick is checked, so it is 1 for the "
                   "first brick, 2 for the second, and 3 for the third. The third brick is "
                   "red, so the light matrix shows 3."]},
            {"key": "g5", "title": "Count the red bricks", "stack": G5,
             "teach": ("This time the variable counts red bricks, not places. It goes up "
                       "only inside the if block. The write block is outside the repeat "
                       "block, so it runs once, at the end."),
             "setup": "Setup: a candy stick with red bricks in places 1, 2, and 5.",
             "q": "What number does the light matrix show, and when does it show it?",
             "a": ["3, and only after all five bricks have been read. The write block is "
                   "under the repeat block, not inside it."]},
        ],
        "game": [
            "Play it as a game. Player 1 builds a candy stick with one red brick and hides "
            "it from player 2.",
            "Player 2 guesses the place of the red brick, from 1 to 5, and writes the guess "
            "down. Then run the program from snippet 4. A right guess wins a point. Swap and "
            "play again.",
        ],
        "sheet_title": "Expected and shown",
        "sheet_head": ["Candy stick", "Colours, first brick to fifth", "Snippet",
                       "Expected on the light matrix", "Shown"],
        "sheet_rows": [["1", None, "4"], ["2", None, "4"], ["3", None, "5"], ["4", None, "5"]],
    },
    {
        "id": "grabbers",
        "title": "The Grabbers",
        "intro": [
            "The Grabbers are a hand controller and two different claws. You hold the "
            "controller and squeeze its force sensor, in port E. Motor A closes and opens "
            "the claw. Each claw is built for different things: one has a bendy claw and "
            "one has a split claw.",
            "In these snippets, motor A turning counterclockwise closes the claw and "
            "clockwise opens it. LEGO's own program for this model turns it the same way.",
        ],
        "books": [(1, "Hand controller", _ASSET + "blt56a81c75560c9a81/5f8802cbf71916144453a493/supercleaup-bi-pdf-book1of3.pdf?locale=en-us"),
                  (2, "Grabber 1, the bendy claw", _ASSET + "bltb5e585f94cb4e72b/5f8802e5a302dc0d859a734d/supercleaup-bi-pdf-book2of3.pdf?locale=en-us"),
                  (3, "Grabber 2, the split claw", _ASSET + "bltb8840f08a6d0362b/5f8802dc2792080f7721405c/supercleaup-bi-pdf-book3of3.pdf?locale=en-us")],
        "team": "Two builders: one builds Grabber 1, one builds Grabber 2 and the hand controller.",
        "ports": [("A", "Motor", "Closes and opens the claw"),
                  ("E", "Force sensor", "The part of the controller you squeeze")],
        "lesson": "https://education.lego.com/en-us/lessons/prime-invention-squad/super-cleanup/",
        "snippets": [
            {"key": "r1", "title": "Close, then open", "stack": R1,
             "teach": "This program does not use the force sensor. It is a test that the claw works.",
             "setup": "Setup: the claw is open and holds nothing.",
             "q": "Does the claw close first or open first? How long is it shut before it opens?",
             "a": ["It closes first. The first motor block turns counterclockwise.",
                   "About 1 second. The wait block sits between the two motor blocks."]},
            {"key": "r2", "title": "Squeeze to grab", "stack": R2,
             "teach": ("The wait until block waits until its question is true. The start "
                       "motor block starts the motor and does not stop it. The claw keeps "
                       "closing, and then holds, until another motor block runs."),
             "setup": "Setup: run the program, then squeeze the force sensor and hold it.",
             "q": "What does the claw do while you keep squeezing? What happens when you let go?",
             "a": ["It closes and keeps pushing closed, so it holds what it grabbed.",
                   "It opens. Letting go makes the second wait until block's question true, "
                   "and the last block turns the motor clockwise for 0.5 seconds."]},
            {"key": "r3", "title": "Grab five times", "stack": R3,
             "teach": "The repeat block runs the four blocks inside it 5 times: five grabs.",
             "setup": "Setup: run the program, then squeeze and let go six times.",
             "q": "What happens on the sixth squeeze?",
             "a": ["Nothing. The repeat block ran 5 times and the program ended. Run it again for five more grabs."]},
            {"key": "r4", "title": "Count the grabs", "stack": R4,
             "teach": ("The variable grabs holds the number of grabs so far. The light "
                       "matrix shows it after every squeeze."),
             "setup": "Setup: run the program, then squeeze and let go three times.",
             "q": "What number is on the light matrix after the third squeeze? What number does it show first?",
             "a": ["3 after the third squeeze.",
                   "1 first. grabs starts at 0, but it goes up by 1 before the write block "
                   "runs, so the first number shown is 1."]},
            {"key": "r5", "title": "A slower grab", "stack": R5,
             "teach": ("The set speed block changes how fast motor A turns in every motor "
                       "block under it. This program is snippet 2 with that one block added."),
             "setup": "Setup: run it next to snippet 2 on another team's grabber, and squeeze both at once.",
             "q": "Which claw closes faster? Does the slow claw open as wide as the fast one?",
             "a": ["The claw running snippet 2 closes faster.",
                   "No. Both open for 0.5 seconds, and the slow motor turns less far in the "
                   "same time, so the slow claw opens less wide. Try a longer time in the "
                   "last block, one change per run."]},
        ],
        "game": [
            "Run a fair test of the two claws, as LEGO's lesson does. Use snippet 2 on both, "
            "the same objects, and the same person squeezing. Change only the claw.",
            "Try things of different sizes that weigh about the same, then things of about "
            "the same size that weigh different amounts.",
        ],
        "sheet_title": "Fair test: which claw grabs it?",
        "sheet_head": ["Object", "Expected: Grabber 1", "Grabber 1 held it?",
                       "Expected: Grabber 2", "Grabber 2 held it?"],
        "sheet_rows": [["A LEGO brick"], ["A crumpled ball of paper"], ["An empty plastic bottle"],
                       ["A stack of LEGO wheels"], ["An apple"]],
    },
]

BLOCKS_USED = [
    ("Events", "when program starts"),
    ("Motors", "run for, in seconds or in degrees of motor turn; start motor; set speed to %"),
    ("Control", "wait, wait until, repeat, if then, if then else"),
    ("Sensors", "is color ?, is pressed or released ?"),
    ("Sound", "play sound until done, play beep"),
    ("Light", "write"),
    ("Variables", "set to, change by, and the variable itself"),
]
