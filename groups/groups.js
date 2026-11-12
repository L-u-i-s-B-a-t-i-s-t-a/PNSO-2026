// groups.js: the Ship Design Project data shared by the Groups section (index.html) and the group pages (group.html).
// To publish a file: put it in the folder shown and set released: true. Nothing else changes.

// PROJECT_REFS: links, documents and information for all groups (Groups tab, "Links and information from the instructor").
// file: a site path (groups/common/...) or a web link (https://...); leave it out for an information-only item.
// released: true to show the link; general: true also lists it in the Bibliography.
var PROJECT_REFS = [
  { d: "2026-11-12", t: "Planning (advised)", note: "A work plan is not a deliverable, but plan inside your group: a rough approach and a split of the tasks, so that the work, the presentation and the knowledge of the whole project are shared evenly by every member. You are welcome to share the plan and discuss it with the instructor." },
  { d: "2026-11-12", t: "0.3 Report Template", file: "groups/common/0.3_Report_Template.pdf", note: "the template of your project report", released: false }
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
        "file": "groups/G1/0.5_Project_Scope_Sheet_G1.pdf?v=20261112-2005",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G1/0.4_Datasheet_Template_G1.pdf",
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
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G2/0.5_Project_Scope_Sheet_G2.pdf?v=20261112-2100",
        "released": true
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G2/0.4_Datasheet_Template_G2.pdf",
        "released": false
      }
    ],
    "notes": [],
    "name": "Manuel Fernandes"
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
        "file": "groups/G3/0.5_Project_Scope_Sheet_G3.pdf",
        "released": false
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G3/0.4_Datasheet_Template_G3.pdf",
        "released": false
      }
    ],
    "notes": [],
    "name": "João Baptista Lavanha"
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
        "t": "0.5 Project Scope Sheet",
        "x": "your deliverables, studies and drawings, and specializations",
        "file": "groups/G4/0.5_Project_Scope_Sheet_G4.pdf",
        "released": false
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G4/0.4_Datasheet_Template_G4.pdf",
        "released": false
      }
    ],
    "notes": [],
    "name": "Bartolomeu Dias"
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
        "file": "groups/G5/0.5_Project_Scope_Sheet_G5.pdf",
        "released": false
      },
      {
        "t": "0.4 Datasheet Template",
        "x": "the one-page A4 datasheet of your ship, part of D10",
        "file": "groups/G5/0.4_Datasheet_Template_G5.pdf",
        "released": false
      }
    ],
    "notes": [],
    "name": "Infante Dom Henrique"
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
        "file": "groups/G6/0.5_Project_Scope_Sheet_G6.pdf",
        "released": false
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
        "file": "groups/G7/0.5_Project_Scope_Sheet_G7.pdf",
        "released": false
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
        "file": "groups/G8/0.5_Project_Scope_Sheet_G8.pdf",
        "released": false
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
