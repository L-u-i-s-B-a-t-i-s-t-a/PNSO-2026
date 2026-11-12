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

## Offsets table: `KCS_offsets.csv`

Half-breadths cut from the IGES surfaces, full scale, in metres.

- One row per station: the first column `x_m` is the station position from the AP, positive forward. There are 201 stations, from x = −6.0 m (transom) to x = 238.0 m (bulb nose). They are spaced 0.5 m at the ends (x below 25 m and above 205 m) and 2.5 m in the middle body.
- One column per waterline: `z=0.0` to `z=23.5`, every 0.1 m above the baseline.
- Each value is the half-breadth y in metres; 0 means no hull at that point, below or above the section or beyond its ends.

Check: integrated to T = 10.8 m, the table gives a displacement volume of 52,226 m³ (published 52,030 m³, +0.4 %), C_B 0.653 (0.6505), LCB −1.50 % Lpp (−1.48 %, aft of midship), C_M 0.985 and a waterline length of 232.5 m.

## Terms of use

The workshop page states no licence or terms of use. Use it for coursework, and cite it as:

KRISO Container Ship (KCS) hull geometry, Tokyo 2015 Workshop on CFD in Ship Hydrodynamics, National Maritime Research Institute (NMRI), Japan. https://t2015.nmri.go.jp/kcs_gc.html
