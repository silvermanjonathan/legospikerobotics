"""Every LEGO piece the course's three builds use, with its name and its drawing.

The three builds are the Advanced Driving Base (the class robot), the Game Master,
and the Grabbers.

Where each fact comes from, 13 November 2026:

  - Which pieces a build uses. Read from LEGO's own building books, every page of
    all ten: five for the Advanced Driving Base, two for the Game Master, three for
    the Grabbers. The books show the pieces for each step in a grey box. Pieces that
    look alike at that size (the black peg and the black axle peg, the grey long peg
    with a stop) were read again at twice the size.
  - LEGO's name, design number, and element number. LEGO's own parts lists for the
    SPIKE Prime set 45678 and the SPIKE Prime Expansion Set 45681, as Brickset
    publishes them (brickset.com/inventories/45678-1 and /45681-1). The names are
    copied as LEGO writes them, capitals, short forms, and misspellings included.
  - The second check. Each design number was looked up in the LDraw parts library,
    which names pieces on its own, and the two names had to describe the same piece.
    Every piece and colour read from a book also had to be on the parts list of a
    set that build needs. All of them were.
  - The names LEGO sells the hub, motors, and sensors under (Technic Large Hub
    45601 and so on). LEGO Education's own product pages.
  - The drawings. Made by build/ldraw_render.py from the LDraw parts library
    (library.ldraw.org, CC BY 4.0). They are not LEGO's pictures.

This page lists which pieces a build uses, not how many. LEGO's books give the count
at every step.

ADB, GM, GR are the three builds. CORE and EXP are the two sets.
"""

ADB, GM, GR = "adb", "gm", "gr"
BUILD_NAMES = {ADB: "Advanced Driving Base", GM: "Game Master", GR: "Grabbers"}
BUILD_SHORT = {ADB: "Driving Base", GM: "Game Master", GR: "Grabbers"}
# the ids builds.py gives its two builds, to the filter names on the pieces page
BUILD_ANCHOR = {"game-master": GM, "grabbers": GR}
CORE, EXP = "core", "exp"
SET_NAMES = {CORE: "SPIKE Prime set", EXP: "Expansion Set"}

SOURCE_CORE = "https://brickset.com/inventories/45678-1"
SOURCE_EXP = "https://brickset.com/inventories/45681-1"
SOURCE_LDRAW = "https://library.ldraw.org/"
CHECKED = "13 November 2026"

# LDraw colour codes
BLACK, BLUE, GREEN, RED, YELLOW, WHITE, TAN = 0, 1, 2, 4, 14, 15, 19
MAGENTA, BROWN, GREY, AZURE, SILVER, CLEAR = 26, 70, 71, 322, 179, 47

GROUPS = [
    ("electric", "Hub, motors, and sensors",
     "The hub runs the program. Each motor and each sensor has a cable that plugs into "
     "a port on the hub."),
    ("frames", "Frames and panels",
     "A frame is a rectangle of beams made as one piece. The two numbers count its "
     "holes: a frame 11 by 15 has 11 holes along its short side and 15 along its long "
     "side."),
    ("beams", "Beams",
     "A beam is a bar with a row of round holes. Its number is how many holes it has. "
     "LEGO's books print that number in a square next to a long beam."),
    ("blocks", "Blocks and joiners",
     "These pieces join other pieces at a corner, or hold something in place."),
    ("pegs", "Pegs",
     "A peg snaps into a round hole and holds two pieces together. An axle peg is a peg "
     "at one end and an axle at the other."),
    ("axles", "Axles and bushes",
     "An axle is a rod shaped like a plus sign. It fits a plus-shaped hole, so the "
     "piece on it turns when the axle turns. Its number is its length, counted in beam "
     "holes. LEGO's books print that number in a circle next to most axles."),
    ("wheels", "Wheels, gears, and the hose", ""),
    ("bricks", "Bricks, plates, and tiles",
     "These pieces have studs, the round bumps on top. Only the Game Master uses them, "
     "apart from the yellow brick, which the Advanced Driving Base uses too."),
]

# One row per piece. Fields:
#   id       the drawing's file name in parts/
#   group    one of GROUPS
#   name     the plain name on the card
#   colour   the colour in the builds, in words
#   lego     LEGO's own name, verbatim
#   design   LEGO's design number (the shape)
#   element  LEGO's element number or numbers (the shape in one colour)
#   sets     which sets have it
#   builds   which builds use it
#   tell     one sentence: what it does, or how to tell it from a piece like it
#   ldraw    the LDraw file the drawing and the second name check use
#   ldname   LDraw's own name for that file
PIECES = [
    # ------------------------------------------------------------ electric
    dict(id="hub", group="electric", name="Hub", colour="yellow and white",
         lego="HUB, NO. 8", design="105474", element="6464165", sets=[CORE],
         builds=[ADB, GM, GR],
         tell="The hub runs the program. It has six ports, A to F, and the battery "
              "slides into it. LEGO sells it as the Technic Large Hub, number 45601.",
         ldraw="45601c01", ldname="Electric Powered Up 6 Port Hub with Yellow Bottom"),
    dict(id="large_motor", group="electric", name="Large motor", colour="light blue and white",
         lego="MOTOR, NO. 11", design="99085", element="6384811", sets=[CORE, EXP],
         builds=[ADB],
         tell="The two large motors turn the two big wheels of the Advanced Driving Base. "
              "One comes in each set. LEGO sells it as the Technic Large Angular Motor, "
              "number 45602.",
         ldraw="54675", ldname="Electric Powered Up Large Angular Motor with Medium Azure Back"),
    dict(id="medium_motor", group="electric", name="Medium motor", colour="light blue and white",
         lego="MOTOR, NO. 12", design="79818", element="6359210", sets=[CORE],
         builds=[ADB, GM, GR],
         tell="Shorter than the large motor. LEGO sells it as the Technic Medium Angular "
              "Motor, number 45603.",
         ldraw="54696p01",
         ldname="Electric Powered Up Medium Angular Motor with Medium Azure Back and Hub"),
    dict(id="colour_sensor", group="electric", name="Colour sensor", colour="white and black",
         lego="SENSOR COLOUR, NO. 2", design="37308", element="6217705", sets=[CORE, EXP],
         builds=[ADB, GM],
         tell="It measures colour and reflected light through the round window in its "
              "face. One comes in each set. LEGO sells it as the Technic Color Sensor, "
              "number 45605.",
         ldraw="37308", ldname="Electric Powered Up Colour Sensor"),
    dict(id="force_sensor", group="electric", name="Force sensor", colour="white and black",
         lego="SENSOR FORCE, NO. 1", design="37312", element="6217712", sets=[CORE],
         builds=[GR],
         tell="It has a black button on the front. It measures how hard the button is "
              "pressed. LEGO sells it as the Technic Force Sensor, number 45606.",
         ldraw="37312", ldname="Electric Powered Up Force Sensor"),

    # ------------------------------------------------------------ frames
    dict(id="frame_11x15", group="frames", name="Frame, 11 by 15", colour="light blue",
         lego="FRAME 11X15", design="39790", element="6245375", sets=[CORE, EXP],
         builds=[ADB, GM], tell="The biggest frame.",
         ldraw="39790", ldname="Technic Beam 15 x 11 with Open Center 13 x 9"),
    dict(id="frame_7x11", group="frames", name="Frame, 7 by 11", colour="purple",
         lego="FRAME 7X11", design="39794", element="6252663", sets=[CORE, EXP],
         builds=[ADB], tell="",
         ldraw="39794", ldname="Technic Beam 11 x 7 with Open Center 9 x 5"),
    dict(id="frame_5x7", group="frames", name="Frame, 5 by 7", colour="black",
         lego="BEAM FRAME 5X7 Ø 4.85", design="64179", element="6016154", sets=[CORE, EXP],
         builds=[ADB], tell="",
         ldraw="64179", ldname="Technic Beam 7 x 5 with Open Center 5 x 3"),
    dict(id="frame_3x3", group="frames", name="Square frame, 3 by 3", colour="purple",
         lego="FRAME 3X3", design="39793", element="6252656", sets=[CORE, EXP],
         builds=[ADB, GR],
         tell="A small square block with holes on every side.",
         ldraw="39793", ldname="Technic Connector Block 3 x 3 with 9 Perpendicular Holes"),
    dict(id="panel_11x19", group="frames", name="Base panel, 11 by 19", colour="yellow",
         lego="PANEL 11X19", design="39369", element="6252630", sets=[CORE],
         builds=[GM], tell="A flat plate full of holes. The Game Master uses two.",
         ldraw="39369", ldname="Technic Beam 19 x 11 Baseplate"),
    dict(id="flat_panel_3x11", group="frames", name="Flat panel, 3 by 11", colour="black",
         lego="FLAT PANEL 3X11M", design="15458", element="6080356", sets=[CORE],
         builds=[GM], tell="",
         ldraw="15458", ldname="Technic Panel 3 x 11"),
    dict(id="curved_panel", group="frames", name="Curved panel, 3 by 11", colour="light blue",
         lego="BOWED PANEL 3X11X2 Ø4,85 (X19)", design="11954", element="6133928", sets=[CORE],
         builds=[GM], tell="",
         ldraw="11954", ldname="Technic Panel Smooth 11 x 2 x 3 with 10 Front Pin Holes"),

    # ------------------------------------------------------------ beams
    dict(id="beam_15", group="beams", name="Beam, 15 holes", colour="black",
         lego="TECHNIC 15M BEAM", design="64871", element="4542573", sets=[CORE, EXP],
         builds=[ADB, GM, GR], tell="",
         ldraw="32278", ldname="Technic Beam 15"),
    dict(id="beam_13", group="beams", name="Beam, 13 holes", colour="light blue",
         lego="TECHNIC 13M BEAM", design="41239", element="6261643", sets=[CORE, EXP],
         builds=[ADB, GM], tell="",
         ldraw="41239", ldname="Technic Beam 13"),
    dict(id="beam_9", group="beams", name="Beam, 9 holes", colour="black",
         lego="TECHNIC 9M BEAM", design="64289", element="4645732", sets=[CORE, EXP],
         builds=[ADB, GR], tell="",
         ldraw="40490", ldname="Technic Beam 9"),
    dict(id="beam_7", group="beams", name="Beam, 7 holes", colour="light blue",
         lego="TECHNIC 7M BEAM", design="32524", element="6261638", sets=[CORE, EXP],
         builds=[ADB, GR], tell="",
         ldraw="32524", ldname="Technic Beam 7"),
    dict(id="beam_5", group="beams", name="Beam, 5 holes", colour="purple",
         lego="TECHNIC 5M BEAM", design="32316", element="6261642", sets=[CORE, EXP],
         builds=[GR], tell="",
         ldraw="32316", ldname="Technic Beam 5"),
    dict(id="beam_3", group="beams", name="Beam, 3 holes", colour="yellow",
         lego="TECHNIC 3M BEAM", design="32523", element="4153707", sets=[CORE, EXP],
         builds=[ADB, GR], tell="",
         ldraw="32523", ldname="Technic Beam 3"),
    dict(id="corner_beam", group="beams", name="Corner beam, 3 by 5", colour="light blue",
         lego="TECHNIC ANG. BEAM 3X5 90 DEG.", design="32526", element="6173003",
         sets=[CORE, EXP], builds=[ADB, GR],
         tell="Shaped like the letter L, with a square corner.",
         ldraw="32526", ldname="Technic Beam 3 x 5 Bent 90"),
    dict(id="bent_beam", group="beams", name="Double bent beam, 3 by 7", colour="black",
         lego="DOUBLE ANGULAR BEAM 3X7 45°", design="41486", element="6271152",
         sets=[CORE, EXP], builds=[ADB, GR],
         tell="It bends twice. Each end has a plus-shaped hole.",
         ldraw="32009", ldname="Technic Beam 3 x 3.8 x 7 Liftarm Bent 45 Double"),
    dict(id="h_beam", group="beams", name="H beam, 3 by 5", colour="grey",
         lego="BEAM I -FRAME 3X5 90 DEGR. HOLE Ø4.85", design="14720", element="6055519",
         sets=[CORE, EXP], builds=[ADB, GR],
         tell="Shaped like the letter H. The holes in its two ends face one way and the "
              "holes in its middle bar face another.",
         ldraw="14720", ldname="Technic Beam 5 x 3 H-shaped"),
    dict(id="beam_2", group="beams", name="Beam, 2 holes", colour="light blue",
         lego="BEAM 1X2 W/CROSS AND HOLE", design="40147", element="6344813", sets=[CORE],
         builds=[ADB, GR],
         tell="One hole is round, for a peg. The other is plus-shaped, for an axle.",
         ldraw="60483", ldname="Technic Beam 2 Liftarm"),
    dict(id="ball_holder", group="beams", name="Ball holder", colour="light blue",
         lego="BEAM 3X5 W/ DIA. 19 WHEEL CUP", design="39370", element="6261590",
         sets=[CORE, EXP], builds=[ADB],
         tell="The ball snaps into its cup and rolls in any direction.",
         ldraw="39370", ldname="Technic Beam 5 x 3 H-shaped with Ball Socket"),
    dict(id="ball", group="beams", name="Ball", colour="white",
         lego="DIA. 19 WHEEL BALL", design="52629", element="6261647", sets=[CORE, EXP],
         builds=[ADB], tell="It goes in the ball holder.",
         ldraw="52629", ldname="Technic Ball 19mm for Ball Castor"),

    # ------------------------------------------------------------ blocks
    dict(id="peg_block", group="blocks", name="Peg block, 3 holes and 4 pegs", colour="grey",
         lego="BEAM 3 MODULE W/ 4 SNAP", design="65489", element="6282158", sets=[CORE, EXP],
         builds=[ADB, GM, GR],
         tell="A 3-hole beam with four pegs already on it, two at each end.",
         ldraw="48989", ldname="Technic Cross Block 1 x 3 (Pin/Pin/Pin) with 4 Pins"),
    dict(id="cross_block_3", group="blocks", name="Cross block, 3 long", colour="white",
         lego="DOUBLE CROSS BLOCK", design="42142", element="6276981", sets=[CORE, EXP],
         builds=[ADB, GR],
         tell="A plus-shaped hole at each end and a round hole through the middle, facing "
              "the other way.",
         ldraw="32184", ldname="Technic Cross Block 1 x 3 (Axle/Pin/Axle)"),
    dict(id="cross_block_2", group="blocks", name="Cross block, 2 long", colour="black",
         lego="CROSS BLOCK 90°", design="40146", element="6261371", sets=[EXP],
         builds=[ADB],
         tell="One plus-shaped hole and one round hole, facing different ways.",
         ldraw="6536", ldname="Technic Cross Block 1 x 2 (Axle/Pin)"),
    dict(id="cross_block_3x2", group="blocks", name="Cross block, 3 by 2", colour="grey",
         lego="CROSS BLOCK 3X2", design="42191", element="6331441", sets=[EXP],
         builds=[ADB],
         tell="Three round holes in a row, and one plus-shaped hole on top that faces the "
              "other way.",
         ldraw="63869", ldname="Technic Cross Block 3 x 2 (Axle/Triple Pin)"),
    dict(id="spacer", group="blocks", name="Round spacer, 1 long", colour="black",
         lego="BEAM 1X1", design="18654", element="6121485", sets=[EXP],
         builds=[ADB], tell="A short ring with one round hole. LEGO calls it a beam.",
         ldraw="18654", ldname="Technic Beam 1"),
    dict(id="tube", group="blocks", name="Tube, 2 long", colour="yellow",
         lego="TUBE, W/ DOUBLE 4.85 HOLE", design="29219", element="6173122", sets=[CORE, EXP],
         builds=[ADB], tell="A peg goes into each end.",
         ldraw="62462", ldname="Technic Pin Joiner Round with Slot",
         ldnote="LDraw files 29219 as the same piece as 62462."),
    dict(id="cable_clip", group="blocks", name="Cable clip", colour="blue, green, red, purple, yellow, or light blue",
         lego="WIRE CLIP, W/ CROSS HOLE", design="49283",
         element="6263071 blue, 6263072 green, 6263067 red, 6263193 purple, "
                 "6263069 yellow, 6263192 light blue",
         sets=[CORE, EXP], builds=[ADB, GR],
         tell="It holds a cable in place. The Advanced Driving Base uses one of each "
              "colour. The Grabbers use a yellow one.",
         ldraw="49283", ldname="Technic Cable Clip"),
    dict(id="rubber_joiner", group="blocks", name="Rubber joiner, 2 long", colour="black",
         lego="DAMPER 2M", design="45590", element="4198367", sets=[CORE],
         builds=[GR],
         tell="Made of rubber, with two plus-shaped holes side by side.",
         ldraw="45590", ldname="Technic Axle Joiner Double Flexible"),
    dict(id="elbow_6", group="blocks", name="Elbow connector, number 6", colour="yellow",
         lego="ANGLE ELEMENT, 90 DEGREES [6]", design="42155", element="6268925",
         sets=[CORE, EXP], builds=[GR],
         tell="A square corner for two axles. It has the number 6 on its side.",
         ldraw="32014", ldname="Technic Angle Connector #6 (90 degree)"),
    dict(id="peg_with_hole", group="blocks", name="Long peg with a hole in the middle",
         colour="grey",
         lego="DOUBLE BUSH 3M Ø4.9", design="44874", element="6321303", sets=[CORE],
         builds=[GM],
         tell="A peg at each end and a round hole through the middle.",
         ldraw="87082", ldname="Technic Pin Long with Pin Hole Type 1"),

    # ------------------------------------------------------------ pegs
    dict(id="peg_black", group="pegs", name="Peg", colour="black",
         lego="CONNECTOR PEG W. FRICTION", design="61332", element="6279875",
         sets=[CORE, EXP], builds=[ADB, GM, GR],
         tell="2 long. It grips the hole, so the pieces it joins do not swing. Every "
              "build uses it.",
         ldraw="2780", ldname="Technic Pin with Friction and Slots"),
    dict(id="peg_long_blue", group="pegs", name="Long peg", colour="blue",
         lego="CONNECTOR PEG W. FRICTION 3M", design="42924", element="6299413",
         sets=[CORE, EXP], builds=[ADB, GM, GR],
         tell="3 long, so it can join three pieces.",
         ldraw="6558", ldname="Technic Pin Long with Friction and Slot"),
    dict(id="peg_long_stop", group="pegs", name="Long peg with a stop", colour="grey or red",
         lego="2M FRIC. SNAP W/CROSS HOLE", design="65304",
         element="6321747 grey, 6347789 red", sets=[CORE, EXP],
         builds=[ADB, GM],
         tell="3 long, with a wide collar at one end that stops it going all the way "
              "through. The collar has a plus-shaped hole. The grey one comes in both "
              "sets. The red one comes in the Expansion Set, and only the Advanced Driving "
              "Base uses it.",
         ldraw="32054", ldname="Technic Pin Long with Stop Bush"),
    dict(id="axle_peg_red", group="pegs", name="Long axle peg", colour="red",
         lego="CON. BUSH 2M FR. + CROSS AXLE", design="11214", element="6209519", sets=[EXP],
         builds=[ADB],
         tell="3 long: a peg 2 long, then an axle 1 long.",
         ldraw="11214", ldname="Technic Axle Pin Long with Friction with 2L Pin"),
    dict(id="axle_peg_blue", group="pegs", name="Axle peg", colour="blue",
         lego="CONN.BUSH W.FRIC./CROSSALE", design="43093", element="4206482", sets=[EXP],
         builds=[ADB],
         tell="2 long: a peg 1 long, then an axle 1 long. Shorter than the blue long peg.",
         ldraw="43093", ldname="Technic Axle Pin with Friction"),
    dict(id="axle_peg_black", group="pegs", name="Axle peg with a long axle", colour="black",
         lego="Cross axle 2m w. snap w. fric.", design="18651", element="6089119", sets=[CORE],
         builds=[ADB, GM, GR],
         tell="3 long: a peg 1 long, then an axle 2 long. It is black like the peg, so "
              "look for the plus-shaped end.",
         ldraw="18651", ldname="Technic Axle Pin Long with Friction with 2L Axle"),
    dict(id="axle_peg_tan", group="pegs", name="Smooth axle peg", colour="tan",
         lego="CONNECTOR PEG/CROSS AXLE", design="6562", element="4666579", sets=[CORE],
         builds=[GM, GR],
         tell="2 long. Its peg end is smooth, so a piece on it turns freely.",
         ldraw="3749", ldname="Technic Axle Pin"),

    # ------------------------------------------------------------ axles
    dict(id="axle_2", group="axles", name="Axle, 2 long", colour="red",
         lego="2M CROSS AXLE W. GROOVE", design="32062", element="4142865", sets=[CORE, EXP],
         builds=[GR], tell="",
         ldraw="32062", ldname="Technic Axle 2 Notched"),
    dict(id="axle_3", group="axles", name="Axle, 3 long", colour="yellow",
         lego="CROSS AXLE 3M", design="4519", element="6130007", sets=[CORE, EXP],
         builds=[ADB, GM, GR], tell="",
         ldraw="4519", ldname="Technic Axle 3"),
    dict(id="axle_4", group="axles", name="Axle, 4 long", colour="black",
         lego="CROSS AXLE 4M", design="3705", element="370526", sets=[CORE, EXP],
         builds=[ADB, GR], tell="",
         ldraw="3705", ldname="Technic Axle 4"),
    dict(id="axle_5", group="axles", name="Axle, 5 long", colour="grey",
         lego="CROSS AXLE 5M", design="32073", element="4211639", sets=[CORE, EXP],
         builds=[ADB], tell="",
         ldraw="32073", ldname="Technic Axle 5"),
    dict(id="axle_5_stop", group="axles", name="Axle with a stop, 5 long", colour="brown",
         lego="CROSS AXLE 5M WITH END STOP", design="15462", element="6159763", sets=[EXP],
         builds=[ADB],
         tell="One end is round and wider, so the axle cannot slide all the way through.",
         ldraw="15462", ldname="Technic Axle 5 with Stop"),
    dict(id="bush", group="axles", name="Bush", colour="grey",
         lego="BUSH FOR CROSS AXLE", design="42798", element="6275844", sets=[CORE, EXP],
         builds=[ADB],
         tell="A ring that slides onto an axle and stops the axle sliding out.",
         ldraw="3713", ldname="Technic Bush with Two Flanges"),

    # ------------------------------------------------------------ wheels
    dict(id="gear_28", group="wheels", name="Gear, 28 teeth", colour="grey",
         lego="ANGLED GEAR WHEEL Z28", design="46372", element="6259270", sets=[CORE, EXP],
         builds=[ADB],
         tell="One goes on each of the two medium motors.",
         ldraw="46372", ldname="Technic Gear 28 Tooth Double Bevel"),
    dict(id="big_wheel", group="wheels", name="Big wheel", colour="black with a light blue tyre",
         lego="WHEEL DIA. 88X14.34, W/ CROSS HOLE", design="49295", element="6261593",
         sets=[EXP], builds=[ADB],
         tell="The drive wheel of the Advanced Driving Base, about 9 cm across. The tyre "
              "does not come off.",
         ldraw="49295p01", ldname="Wheel 14 x 80 with 4 Spokes with Integral Medium Azure Tyre"),
    dict(id="pulley_wheel", group="wheels", name="Pulley wheel", colour="black",
         lego="WEDGE-BELT WHEEL Ø24", design="49750", element="6323668", sets=[CORE],
         builds=[GM],
         tell="A wheel with a groove around its edge. The pulley tyre fits in the groove.",
         ldraw="4185a", ldname="Technic Wedge Belt Wheel - Not Reinforced"),
    dict(id="pulley_tyre", group="wheels", name="Pulley tyre", colour="black",
         lego="TYRE FOR WEDGE-BELT WHEEL", design="2815", element="6028041", sets=[CORE],
         builds=[GM], tell="A rubber ring. It goes on the pulley wheel.",
         ldraw="2815", ldname="Technic Wedge Belt Wheel Tyre"),
    dict(id="small_rim", group="wheels", name="Small wheel rim", colour="white",
         lego="RIM NARROW, DIA. 18X7, W/ CROSS", design="56903", element="6013484", sets=[CORE],
         builds=[GR], tell="The small tyre goes on it.",
         ldraw="56903", ldname="Wheel Rim 8 x 18 with Deep Centre Groove and Axle Hole"),
    dict(id="small_tyre", group="wheels", name="Small tyre", colour="black",
         lego="TYRE LOW NARROW Ø24x7MM", design="61254", element="4541455", sets=[CORE],
         builds=[GR], tell="A rubber tyre with bumps. It goes on the small wheel rim.",
         ldraw="61254", ldname="Tyre 7/ 45 x 17 Offset Tread with Middle Band"),
    dict(id="hose", group="wheels", name="Bendy hose", colour="silver",
         lego="FLEX HOSE 19M W/3. 18 STICK", design="14925", element="6044636", sets=[CORE],
         builds=[GR],
         tell="A ribbed tube that bends. Each end pushes into an elbow connector. The "
              "drawing shows it straight.",
         ldraw="43675", ldname="Technic Ribbed Hose 19L",
         ldnote="LDraw has no file numbered 14925. Its ribbed hose of the same length, "
                "19, is file 43675."),

    # ------------------------------------------------------------ bricks
    dict(id="brick_2x4", group="bricks", name="Brick, 2 by 4, with plus-shaped holes",
         colour="yellow, blue, red, purple, or green",
         lego="BRICK 2X4 W/ CROSS HOLE", design="39789",
         element="6244914 yellow, 6244916 blue, 6244918 red, 6252647 purple, 6244915 green",
         sets=[CORE, EXP], builds=[ADB, GM],
         tell="The Advanced Driving Base uses yellow ones. The Game Master uses two of "
              "each colour.",
         ldraw="39789", ldname="Brick 2 x 4 with 3 Axleholes Vertical"),
    dict(id="plate_2x8", group="bricks", name="Plate with holes, 2 by 8", colour="black",
         lego="PLATE 2X8 W. HOLES", design="3738", element="373826", sets=[CORE],
         builds=[GM], tell="",
         ldraw="3738", ldname="Technic Plate 2 x 8 with Holes"),
    dict(id="plate_2x16", group="bricks", name="Plate, 2 by 16", colour="purple",
         lego="PLATE 2X16", design="4282", element="6173062", sets=[CORE],
         builds=[GM], tell="",
         ldraw="4282", ldname="Plate 2 x 16"),
    dict(id="round_brick", group="bricks", name="Round brick, 2 by 2", colour="white",
         lego="BRICK Ø16 W. CROSS", design="6143", element="614301", sets=[CORE],
         builds=[GM], tell="It has a plus-shaped hole down the middle.",
         ldraw="6143", ldname="Brick 2 x 2 Round Reinforced"),
    dict(id="round_plate", group="bricks", name="Round plate, 2 by 2", colour="light blue",
         lego="PLATE 2X2 ROUND", design="4032", element="6109752", sets=[CORE],
         builds=[GM], tell="",
         ldraw="4032a", ldname="Plate 2 x 2 Round with Axlehole"),
    dict(id="dish", group="bricks", name="Clear dish, 6 by 6", colour="clear",
         lego="SATELLITE DISH 6X6", design="35327", element="6220743 or 6507944", sets=[CORE],
         builds=[GM], tell="You can see through it.",
         ldraw="44375b", ldname="Dish 6 x 6 Inverted with Solid Studs",
         ldnote="LDraw files 35327 as the same piece as 44375b."),
    dict(id="spiral_tile", group="bricks", name="Round tile with a spiral, 2 by 2",
         colour="white with a black spiral",
         lego="FLAT TILE 2X2, ROUND, NO. 1099", design="37006", element="6215018", sets=[CORE],
         builds=[GM], tell="A smooth round tile. It goes in the middle of a clear dish.",
         ldraw="14769p0e", ldname="Tile 2 x 2 Round with Black Spiral Pattern",
         ldnote="37006 is LEGO's number for this print. LDraw files the printed tile as "
                "14769p0e."),
]

# The battery is part of the hub in every book, so it has a line in the teacher's
# table but no card of its own.
SOURCE_PRODUCTS = ("https://education.lego.com/en-us/teacher-resources/lego-education-spike-prime/"
                   "support-technical-info/lego-education-spike-prime-support-technical-info-"
                   "product-info")
BATTERY = dict(name="Hub battery", lego="RECHARGEABLE BATTERY, NO. 2", design="107826",
               element="6482346", sets=[CORE], ldraw="45610",
               ldname="Electric Powered Up 6 Port Hub Rechargeable Battery")

# How each piece is drawn: LDraw file, LDraw colour, and any turn that shows it best.
_DRAW = {
    "hub": dict(files=[("45601c01.dat", WHITE)]),
    "large_motor": dict(files=[("54675.dat", WHITE)]),
    "medium_motor": dict(files=[("54696p01.dat", WHITE)]),
    "colour_sensor": dict(files=[("37308.dat", WHITE)]),
    "force_sensor": dict(files=[("37312.dat", WHITE)]),
    "frame_11x15": AZURE, "frame_7x11": MAGENTA, "frame_5x7": BLACK, "frame_3x3": MAGENTA,
    "panel_11x19": YELLOW, "flat_panel_3x11": BLACK, "curved_panel": AZURE,
    "beam_15": BLACK, "beam_13": AZURE, "beam_9": BLACK, "beam_7": AZURE, "beam_5": MAGENTA,
    "beam_3": YELLOW, "corner_beam": AZURE, "bent_beam": BLACK, "h_beam": GREY,
    "beam_2": AZURE, "ball_holder": AZURE, "ball": WHITE,
    "peg_block": GREY, "cross_block_3": WHITE, "cross_block_2": BLACK,
    "cross_block_3x2": GREY, "spacer": BLACK, "tube": YELLOW, "cable_clip": BLUE,
    "rubber_joiner": BLACK, "elbow_6": YELLOW, "peg_with_hole": GREY,
    "peg_black": BLACK, "peg_long_blue": BLUE, "peg_long_stop": GREY, "axle_peg_red": RED,
    "axle_peg_blue": BLUE, "axle_peg_black": BLACK, "axle_peg_tan": TAN,
    "axle_2": RED, "axle_3": YELLOW, "axle_4": BLACK, "axle_5": GREY, "axle_5_stop": BROWN,
    "bush": GREY, "gear_28": GREY, "big_wheel": dict(files=[("49295p01.dat", BLACK)]),
    "pulley_wheel": BLACK, "pulley_tyre": BLACK, "small_rim": WHITE, "small_tyre": BLACK,
    "hose": SILVER, "brick_2x4": YELLOW, "plate_2x8": BLACK, "plate_2x16": MAGENTA,
    "round_brick": WHITE, "round_plate": AZURE, "dish": CLEAR, "spiral_tile": WHITE,
}
# Turns that show a piece best, found by looking at each drawing.
_TURN = {
    # the hose is all ribs; its edge lines would fill it in black
    "hose": {"edges": False},
}


def _drawings():
    out = []
    for p in PIECES:
        spec = _DRAW[p["id"]]
        if isinstance(spec, dict):
            d = dict(spec)
            d["files"] = [(f, c, None, None) for f, c in spec["files"]]
        else:
            d = {"files": [(p["ldraw"] + ".dat", spec, None, None)]}
        d["img"] = p["id"]
        d.update(_TURN.get(p["id"], {}))
        out.append(d)
    return out


DRAWINGS = _drawings()


def check():
    """Stops the build if the list contradicts itself."""
    ids = [p["id"] for p in PIECES]
    assert len(ids) == len(set(ids)), "two pieces share an id"
    groups = {g[0] for g in GROUPS}
    for p in PIECES:
        assert p["group"] in groups, p["id"]
        assert p["builds"] and set(p["builds"]) <= {ADB, GM, GR}, p["id"]
        assert p["sets"] and set(p["sets"]) <= {CORE, EXP}, p["id"]
        assert p["design"].isdigit() and p["lego"] and p["ldname"], p["id"]
        # the Game Master and the Grabbers are built from the SPIKE Prime set alone
        if GM in p["builds"] or GR in p["builds"]:
            assert CORE in p["sets"], p["id"] + " is in a one-set build but not in that set"
    assert set(_DRAW) == set(ids), "a piece has no drawing, or a drawing has no piece"


check()
