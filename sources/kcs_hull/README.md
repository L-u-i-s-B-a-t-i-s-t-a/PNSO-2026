# KCS hull geometry (KRISO Container Ship)

`KCS_hull_SVA.igs` is the bare hull of the KRISO Container Ship (KCS), as distributed by the Tokyo 2015 Workshop on CFD in Ship Hydrodynamics (NMRI), file `KCS_hull_SVA.zip`. The workshop memo notes that it is the same IGES data used in the Gothenburg 2010 CFD workshop (G2010) and SIMMAN 2014.

Official download page: https://t2015.nmri.go.jp/kcs_gc.html

## Main particulars (full scale, from the workshop page)

| Lpp | B | T | Displacement volume | Wetted surface (without rudder) | C_B | Service speed |
|---|---|---|---|---|---|---|
| 230.0 m | 32.2 m | 10.8 m | 52,030 m³ | 9,424 m² | 0.6505 | 24.0 kn (Fn 0.26) |

## What is in the file

- 55 NURBS surfaces (IGES entity 128), full scale, in metres.
- One side of the hull only (y ≥ 0); mirror it for the other side.
- x from the AP, positive forward (FP at x = 230 m); z up from the baseline.

## Terms of use

The workshop page states no licence or terms of use. Use it for coursework, and cite it as:

KRISO Container Ship (KCS) hull geometry, Tokyo 2015 Workshop on CFD in Ship Hydrodynamics, National Maritime Research Institute (NMRI), Japan. https://t2015.nmri.go.jp/kcs_gc.html
