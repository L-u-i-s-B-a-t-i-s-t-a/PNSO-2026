// groups.js: the Ship Design Project data shared by the Groups section (index.html) and the group pages (group.html).
// To publish a file: put it in the folder shown and set released: true. Nothing else changes.

// PROJECT_REFS: links, documents and information for all groups (Groups tab, "Links and information from the instructor").
// file: a site path (groups/common/...) or a web link (https://...); leave it out for an information-only item.
// released: true to show the link; general: true also lists it in the Bibliography.
var PROJECT_REFS = [
  // { d: "2026-11-12", t: "Title", file: "groups/common/File.pdf" or "https://...", note: "one line on what it is for", general: true, released: true }
  // { d: "2026-11-12", t: "Information for all groups", note: "the text" }
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G1/Project_Scope_Sheet_G1.pdf",
        "released": true
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G1/Statement_of_Work_G1.pdf",
        "released": true
      },
      {
        "t": "Owner's requirements, Baseline B",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=5",
        "released": false
      }
    ],
    "notes": [],
    "name": "Fernão de Oliveira"
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G2/Project_Scope_Sheet_G2.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G2/Statement_of_Work_G2.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G3/Project_Scope_Sheet_G3.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G3/Statement_of_Work_G3.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
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
      "SP11 Dimensional Analysis"
    ],
    "inputs": [
      {
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G4/Project_Scope_Sheet_G4.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G4/Statement_of_Work_G4.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G5/Project_Scope_Sheet_G5.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G5/Statement_of_Work_G5.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G6/Project_Scope_Sheet_G6.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G6/Statement_of_Work_G6.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G7/Project_Scope_Sheet_G7.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G7/Statement_of_Work_G7.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
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
        "t": "Project Scope Sheet",
        "x": "your deliverables, specializations and dates",
        "file": "groups/G8/Project_Scope_Sheet_G8.pdf",
        "released": false
      },
      {
        "t": "Statement of Work, your specializations",
        "x": "what each of your two specializations must contain",
        "file": "groups/G8/Statement_of_Work_G8.pdf",
        "released": false
      },
      {
        "t": "Owner's requirements, Baseline A",
        "x": "the brief of your ship, deck 0.2",
        "file": "week1/0.2_Ship_Design_Project.pdf#page=4",
        "released": false
      }
    ],
    "notes": []
  }
};
