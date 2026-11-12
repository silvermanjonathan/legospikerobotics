"""Standards registry: every code the site prints.

Each entry was retrieved through the Learning Commons Knowledge Graph (CASE Network)
on RESOLVED_ON and is printed with its CASE identifier. Statements are the retrieved
wording. A 3-5 science code has one identifier per grade; the course is for grades 4
and 5, so both are printed.

No CSTA or New York Computer Science and Digital Fluency code appears: the graph
returned no New York computer science codes on 12 November 2026 (style guide,
section 12).
"""

RESOLVED_ON = "12 November 2026"
CONNECTOR = "Learning Commons Knowledge Graph (CASE Network)"

STANDARDS = {
    "3-5-ETS1-3": {
        "framework": "New York State P-12 Science Learning Standards",
        "grades": "4 and 5",
        "statement": ("Plan and carry out fair tests in which variables are controlled and "
                      "failure points are considered to identify aspects of a model or "
                      "prototype that can be improved."),
        "uuids": [("Grade 4", "f9f9243b-9eff-43a3-9c15-5036ca8df270"),
                  ("Grade 5", "3f6f1ba6-3b02-42b3-9525-08fe3f98f552")],
        "why": "The mission changes one number per run and records every run.",
        "deviation": "",
    },
    "NY-4.MD.5.a": {
        "framework": "New York Next Generation Mathematics Learning Standards",
        "grades": "4",
        "statement": ("Recognize an angle is measured with reference to a circle with its "
                      "center at the common endpoint of the rays, by considering the fraction "
                      "of the circular arc between the points where the two rays intersect the "
                      "circle. An angle that turns through 1/360 of a circle is called a "
                      "“one-degree angle,” and can be used to measure angles."),
        "uuids": [("Grade 4", "70d72574-d7cc-11e8-824f-0242ac160002")],
        "why": "360 degrees of motor turn is one full turn of the wheel.",
        "deviation": ("The retrieved wording sets the fraction 1/360 in mathematical "
                      "notation. This page writes it on one line."),
    },
    "NY-4.MD.2": {
        "framework": "New York Next Generation Mathematics Learning Standards",
        "grades": "4",
        "statement": ("Use the four operations to solve word problems involving distances, "
                      "intervals of time, liquid volumes, masses of objects, and money."),
        "uuids": [("Grade 4", "70d71641-d7cc-11e8-824f-0242ac160002")],
        "why": "Full turns of the wheel are turned into centimetres before each run.",
        "deviation": "",
    },
}
