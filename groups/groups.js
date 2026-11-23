// groups.js: the Ship Design Project data shared by the Groups section (index.html) and the group pages (group.html).
// To publish a file: put it in the folder shown and set released: true. Nothing else changes.

// PROJECT_REFS: links, documents and information for all groups (Groups tab, "Links and information from the instructor").
// file: a site path (groups/common/...) or a web link (https://...); leave it out for an information-only item.
// released: true to show the link; general: true also lists it in the Bibliography.
var PROJECT_REFS = [
  { d: "2026-11-12", t: "Planning (advised)", note: "A work plan is not a deliverable, but plan inside your group: a rough approach and a split of the tasks, so that the work, the presentation and the knowledge of the whole project are shared evenly by every member. You are welcome to share the plan and discuss it with the instructor." },
  { d: "2026-11-12", t: "0.3 Report Template", file: "groups/common/0.3_Report_Template.pdf", note: "the template of your project report", released: false }
];

// SP_RESOURCES: tools and resources for all groups, shown in the Groups section (Tools and resources) only; hidden: true keeps an entry off the site; stamp: "..." writes a stamp across its items, which stay clickable.
var SP_RESOURCES = [
  { id: "lackenby", t: "From a Parent Hull to a New Design: the Lackenby Shift and the Stretch",
    x: "For all groups, ahead of D8, and in particular for SP05 Parametric Hull: how a parent hull is reshaped to a new CP and LCB and then scaled to the design's L, B, T and D. It prepares Demo 8, next to this box, and Lecture 6.2 (Papanikolaou §4.3).",
    items: [
      { k: "1 · Watch", t: "Animation · Lackenby shift and stretch on the KCS", file: "resources/hull_form/Lackenby_Animation.html", note: "17 steps, about 3 minutes; play, pause or go step by step", released: true },
      { k: "2 · Calculate", t: "Workbook · Lackenby shift and stretch by hand (Excel)", file: "resources/hull_form/Lackenby_Hand_Calculation.xlsx", note: "21 stations and Simpson's rule, the shift formulas, Newton's method row by row, the stretch", released: true }
    ] },
  { id: "hull", stamp: "Under development", t: "Hull Form from a Parent (Demo 8)",
    x: "For all groups, Baseline A or B, optional: generate your hull from the KCS parent by the Lackenby section shift and a stretch of L, B, T and D, for D8 (hydrostatics check, container count on your own lines, 3D hull). Read first, then run the notebook with the guide at hand.",
    items: [
      { k: "1 · Read", t: "Reading · Hull Form Variation from a Parent", file: "resources/hull_form/Reading_Hull_Form_Variation_from_a_Parent.pdf", note: "the method, with two worked examples", released: true },
      { k: "2 · Guide", t: "User Guide · Demo 8 Hull Generator", file: "resources/hull_form/User_Guide_Demo8_Hull_Generator.pdf", note: "how to use the notebook: quick start, functions, use in your design model, STEP file", released: true },
      { k: "3 · Run", t: "Demo 8 · Hull Form Variation from a Parent (notebook)", file: "https://colab.research.google.com/github/L-u-i-s-B-a-t-i-s-t-a/PNSO-2026/blob/main/notebooks/Demo8_Hull_Form_Variation_Lackenby.ipynb", note: "opens in Google Colab", released: true }
    ] },
  { id: "propulsion", t: "Propulsion: the Logarithm, the Power Law and the Resistance Curve",
    x: "For all groups, in particular for SP02 Propulsion Matching, before Lecture 3.3 Main Machinery and Propeller: how the slope n of a log-log plot turns the resistance curve into a power law, using the Holtrop–Mennen example ship. Extended reading, not for evaluation.",
    items: [
      { k: "1 · Watch", t: "Video · Logarithms and the slope n (7 min, the log series)", file: "week3/Logs_and_Slope_narrated.mp4", note: "logarithm rules, log-log axes, what k and n do", released: false },
      { k: "2 · Watch", t: "Animation · Propulsion, Steps 1 to 3", file: "week3/Propulsion_Steps_1-3_Animation.html", note: "from the square curve to the resistance power law; play, pause or go step by step", released: false },
      { k: "3 · Watch", t: "Video · Propulsion, Steps 1 to 3, narrated (6 min)", file: "week3/Propulsion_Steps_1-3_narrated.mp4", note: "the animation with voice", released: false },
      { k: "4 · Play", t: "Narrated animation · Propulsion, Steps 1 to 3 (interactive, 6 min)", file: "week3/Propulsion_Steps_1-3_Narrated.html", note: "the voice drives the animation; pause, jump, captions and sound on or off. On a phone, swipe the chart sideways", released: true }
    ] },
  { id: "python", t: "Python for AI: a beginner course (optional)",
    x: "For anyone who wants to strengthen their Python before the notebooks and the calculations of the project. It starts from zero; take what you need, in any order.",
    items: [
      { k: "Course", t: "Python for AI Beginner Course (Datalumina)", file: "https://python.datalumina.com/", note: "the course site, to follow at your own pace", released: true },
      { k: "Video", t: "Python for AI, Full Beginner Course (Dave Ebbelaar, YouTube)", file: "https://www.youtube.com/watch?v=ygXn5nV5qFc", note: "over 5 hours with chapters: set-up (Python, VS Code, Jupyter, environments), the basics, functions, APIs, pandas, matplotlib, Git and GitHub", released: true }
    ] }
];

// GROUPS: members (student numbers), Baseline, specializations, the three instructor inputs and the instructor's notes.
// notes: newest first, { d: "YYYY-MM-DD", t: "title", x: "text", file: "groups/G1/....pdf" (optional), general: true (also add the file to PROJECT_REFS) }
var GROUPS = {
  "G1": {
    "ids": [
      "106238",
      "107304",
      "106645"
    ],
    "baseline": "B",
    "sps": [
      "SP01 Longitudinal Strength",
      "SP02 Propulsion Matching"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G1/0.5_Project_Scope_Sheet_G1.pdf?v=20261113-0915",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G1/0.4_Datasheet_Template_G1.pdf",
        "released": false
      },
      {
        "t": "Hold capacity program for the Azores Feeder, Stages 1, 2 and 3 in one file",
        "x": "the Baseline B version of the hold-capacity program: main dimensions, container count in the real hull, closing by draught, with two separate sizings for you to work out (electric: the battery; fuel: gensets and MGO for the transit to the mainland). Needs make_hull.py and the KCS offsets (Tools and resources, Hull Form from a Parent). Read the CHECK and TRY lines at the top",
        "file": "groups/G1/Hold_Capacity_B_Stages_1_2_3.py",
        "released": true
      },
      {
        "t": "Azores Feeder, high-level arrangement: profile and top view",
        "x": "an example of a first arrangement for 130 TEU, drawn on the 86 m ship of the program above. The hull holds 42 TEU below deck and 88 stand on deck. Two cranes (about 45 t each, assumed) reach every container, the battery containers stand aft and the gensets are forward. It is a starting point built on assumed values, not a solution: the stability does not close as drawn, and the program shows why",
        "file": "groups/G1/Baseline_B_Arrangement_Profile_and_Top_View.png?v=20261122-1930",
        "released": true
      },
      {
        "t": "Animation of the hold-capacity program, from the inputs to the displacement equation",
        "x": "a step-by-step walk through the program above, with the real lines of code beside the numbers of the default run: the two sizings, Stage 1, the count in the hull, the draught loop until the weight equals the displacement, the GM check and the rounds. It has a narrated voice (press Play); open it in a browser. The values are those of the program with its assumed inputs",
        "file": "groups/G1/Baseline_B_Program_Animation.html?v=20261122-2120",
        "released": true
      },
      {
        "t": "Stage 3 draught loop of the program above, narrated (10 min)",
        "x": "the same level of detail as the Baseline A video: one pass in detail, a loop that does not converge, a loop that converges (two passes, with the batteries settled), a bad start, and MOVED with the roll back to the hull, all over the real lines of Stage 3 with the loop indices i (passes) and j (repeats). At the end, what is different from Baseline A because this ship is more a one-off than a type: the computed deadweight, the electric plant and the two sizings, the cranes, the calibrated C_N, the battery condition in the stop test, the GM check and the light condition. Press Play; open it in a browser",
        "file": "groups/G1/Baseline_B_Stage3_Draught_Loop_Animation.html?v=20261123-0120",
        "released": true,
        "fresh": true
      }
    ],
    "notes": []
  },
  "G2": {
    "ids": [
      "120960",
      "120562",
      "120565"
    ],
    "baseline": "A",
    "sps": [
      "SP10 Emissions",
      "SP12 Alternative Fuel"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G2/0.5_Project_Scope_Sheet_G2.pdf?v=20261113-0915",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G2/0.4_Datasheet_Template_G2.pdf",
        "released": false
      }
    ],
    "notes": []
  },
  "G3": {
    "ids": [
      "116025",
      "116366",
      "116084"
    ],
    "baseline": "A",
    "sps": [
      "SP01 Longitudinal Strength",
      "SP07 Stability"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G3/0.5_Project_Scope_Sheet_G3.pdf?v=20261113-0915",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G3/0.4_Datasheet_Template_G3.pdf",
        "released": false
      }
    ],
    "notes": []
  },
  "G4": {
    "ids": [
      "96720",
      "105343",
      "121344"
    ],
    "baseline": "A",
    "sps": [
      "SP05 Parametric Hull",
      "SP11 Neural Network Surrogate Model"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G4/0.5_Project_Scope_Sheet_G4.pdf?v=20261113-1025",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G4/0.4_Datasheet_Template_G4.pdf",
        "released": false
      }
    ],
    "notes": []
  },
  "G5": {
    "ids": [
      "117328",
      "116303",
      "107276"
    ],
    "baseline": "A",
    "sps": [
      "SP01 Longitudinal Strength",
      "SP07 Stability"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G5/0.5_Project_Scope_Sheet_G5.pdf?v=20261113-0915",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G5/0.4_Datasheet_Template_G5.pdf",
        "released": false
      }
    ],
    "notes": []
  },
  "G6": {
    "ids": [
      "106053",
      "107234",
      "116330"
    ],
    "baseline": "A",
    "sps": [
      "SP02 Propulsion Matching",
      "SP03 Electrical Load Balance"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G6/0.5_Project_Scope_Sheet_G6.pdf?v=20261113-0835",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G6/0.4_Datasheet_Template_G6.pdf",
        "released": false
      }
    ],
    "notes": []
  },
  "G7": {
    "ids": [
      "116316",
      "106140",
      "76941"
    ],
    "baseline": "A",
    "sps": [
      "SP05 Parametric Hull",
      "SP07 Stability"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G7/0.5_Project_Scope_Sheet_G7.pdf?v=20261113-0015",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G7/0.4_Datasheet_Template_G7.pdf",
        "released": false
      }
    ],
    "notes": []
  },
  "G8": {
    "ids": [
      "121529",
      "121534",
      "97439"
    ],
    "baseline": "A",
    "sps": [
      "SP02 Propulsion Matching",
      "SP07 Stability"
    ],
    "inputs": [
      {
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G8/0.5_Project_Scope_Sheet_G8.pdf?v=20261112-2130",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G8/0.4_Datasheet_Template_G8.pdf",
        "released": false
      }
    ],
    "notes": []
  }
};
