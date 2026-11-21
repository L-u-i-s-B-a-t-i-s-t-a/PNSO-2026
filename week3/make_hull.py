"""make_hull.py : a hull from a parent, ready to use.

Ship and Ocean Systems Design 2026.  The "MAKE THE HULL" box of the hold-capacity algorithm, as one file.

WHAT IT DOES
    You give six numbers: the block coefficient C_B, the position of the centre of buoyancy LCB, and the
    main dimensions L, B, T, D.  You get back a complete hull: a table of half-breadths, its hydrostatics
    (volume, coefficients, KB, BM, KM, waterplane, bulb) and a function that tells you the half-breadth at
    any point.  Two steps, both from Papanikolaou (2026) section 4.3:
        1. LACKENBY.  The KRISO Container Ship (KCS) is the parent.  Its stations are shifted forward and aft
           (the fore and aft halves separately) until the new hull has the C_B and the LCB you asked for.
           The two shift factors c_F and c_A are found by a Newton iteration.  Eqs. 4.10 to 4.19.
        2. STRETCH.  The result is scaled in length, breadth and draught to your L, B, T.  Above the
           waterline the side is stretched so that it ends at your depth D.
    The hull is only as good as the parent: it is a KCS-like hull with your coefficients and dimensions.

HOW TO USE
        from make_hull import make_hull, hull_y, summary, export_offsets

        hull = make_hull(CB=0.690, LCB=-1.0, L=200.0, B=30.0, T=10.5, D=16.0)
        summary(hull)
        print(hull["h"]["V"], hull["h"]["KB"])          # volume [m3], KB [m]
        print(hull_y(hull, x=100.0, z=2.0))             # half-breadth at midship, 2 m above the keel [m]
        export_offsets(hull, "my_hull.csv")             # offsets table for your own CAD or lines plan

    Run it as a script for a worked example and a self-test:   python make_hull.py

INPUTS (all lengths in metres)
        CB    block coefficient of the hull to the waterline T         (guideline range 0.64 to 0.71)
        LCB   centre of buoyancy in per cent of L from midship, + forward (the KCS has about -0.7)
        L     length between perpendiculars, x = 0 at the AP, x = L at the FP
        B     breadth
        T     design draught
        D     depth to the main deck at side (must be larger than T)

OUTPUT: a dictionary
        hull["x"], hull["y"], hull["z"]   stations [m], half-breadths [m] (stations x waterlines), waterline heights [m]
        hull["h"]                         hydrostatics: V, CB, CM, CP, CWP, LCB, LWL, ABT, hB, KB, BM, KM, A (section areas)
        hull["cF"], hull["cA"]            the Lackenby shift factors (0 = no shift)
        hull["warnings"]                  a list of texts: inputs outside the guideline range, or a target not reached
        hull["f"]                         callable f(points) with points of shape (n, 2) = (x, z): half-breadth, 0 outside

ERRORS
        ValueError with a plain message if the hull cannot be made (T >= D, a negative number, C_B so far from the
        parent that the iteration fails).  In the hold-capacity program this is the "hull cannot be made: dropped" path.

NEEDS: numpy, and the file KCS_offsets.csv in the same folder (or in the folder you run from).  If the file is not
found, it is downloaded once from the course site.
"""
import os
import numpy as np

__all__ = ["make_hull", "hull_y", "summary", "export_offsets", "hydrostatics", "check_range", "PARENT"]

# ----------------------------------------------------------------------------------------------------------------------
# The parent hull: KCS (KRISO Container Ship), Tokyo 2015 CFD workshop, full scale
# ----------------------------------------------------------------------------------------------------------------------
CSV_NAME = "KCS_offsets.csv"
CSV_URL = "https://raw.githubusercontent.com/L-u-i-s-B-a-t-i-s-t-a/PNSO-2026/main/sources/kcs_hull/KCS_offsets.csv"
L0, B0, T0 = 230.0, 32.2, 10.8      # KCS: Lpp, B, T
D0 = 17.2                           # side height of the KCS offsets at midship (top of the surfaces)
RANGE = dict(CB=(0.64, 0.71), LB=(5.5, 7.5), BT=(2.5, 3.5))   # guideline range of this method (course)

_trapz = getattr(np, "trapezoid", None) or np.trapz              # numpy 2 renamed trapz


def _read_parent():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, CSV_NAME), CSV_NAME):
        if os.path.exists(p):
            return np.genfromtxt(p, delimiter=",", skip_header=1)
    try:
        import urllib.request
        data = urllib.request.urlopen(CSV_URL, timeout=20).read().decode()
        with open(os.path.join(here, CSV_NAME), "w") as f:     # keep a local copy
            f.write(data)
        return np.genfromtxt(os.path.join(here, CSV_NAME), delimiter=",", skip_header=1)
    except Exception as e:
        raise FileNotFoundError(f"{CSV_NAME} not found next to make_hull.py, and it could not be downloaded ({e}). "
                                f"Put the file in the same folder as this script.")


_raw = _read_parent()
X0 = _raw[:, 0]                                     # station positions [m]
Y0 = _raw[:, 1:]                                    # half-breadths [m], shape (stations, waterlines)
Z0 = np.round(np.arange(Y0.shape[1]) * 0.1, 1)      # waterline heights [m]
XM = L0 / 2                                         # midship [m]


# ----------------------------------------------------------------------------------------------------------------------
# Hydrostatics of any hull given as offsets
# ----------------------------------------------------------------------------------------------------------------------
def hydrostatics(x, y, z, L, B, T):
    """x stations [m], y half-breadths (stations, waterlines) [m], z waterlines [m]; L = Lpp, x = 0 at the AP.
    Returns V [m3], CB, CM, CP, CWP, LCB [% L, + forward of midship], LWL, ABT (bulb area at the FP), hB, KB, BM, KM, A."""
    m = z <= T + 1e-9
    A = 2 * _trapz(y[:, m], z[m], axis=1)                    # section areas [m2]
    V = _trapz(A, x)                                         # displaced volume [m3]
    xB = _trapz(A * x, x) / V                                # centre of buoyancy from the AP [m]
    AM = np.interp(L / 2, x, A)                              # midship section area [m2]
    jT = np.argmin(abs(z - T))
    AWP = 2 * _trapz(y[:, jT], x)                            # waterplane area [m2]
    wet = x[y[:, jT] > 0]
    iF = np.argmin(abs(x - L))                               # bulb section at the FP
    ABT = A[iF]
    hB = _trapz(2 * y[iF, m] * z[m], z[m]) / ABT if ABT > 0 else 0.0
    Mz = 2 * _trapz(y[:, m] * z[m], z[m], axis=1)            # vertical moment of each section [m3]
    KB = _trapz(Mz, x) / V                                   # centre of buoyancy above the baseline [m]
    IT = 2 / 3 * _trapz(y[:, jT] ** 3, x)                    # transverse inertia of the waterplane [m4]
    BM = IT / V
    return dict(V=V, CB=V / (L * B * T), CM=AM / (B * T), CP=V / (AM * L), CWP=AWP / (L * B),
                LCB=(xB - L / 2) / L * 100, LWL=wet.max() - wet.min(), ABT=ABT, hB=hB,
                KB=KB, BM=BM, KM=KB + BM, A=A)


PARENT = hydrostatics(X0, Y0, Z0, L0, B0, T0)       # the KCS itself, from the offsets (published C_B 0.6505, V 52,030 m3)


# ----------------------------------------------------------------------------------------------------------------------
# Step 1: Lackenby
# ----------------------------------------------------------------------------------------------------------------------
def _lackenby(cF, cA, nx=1221):
    """Shift the KCS stations by dxi = c (1 - xi) in each half (xi = 0 at midship, 1 at the end) and return a new
    offsets grid on regular stations.  c > 0 makes that half fuller, c < 0 finer."""
    xi = np.where(X0 >= XM, (X0 - XM) / (L0 - XM), (XM - X0) / XM)
    c = np.where(X0 >= XM, cF, cA)
    xc = np.clip(xi, 0, 1)
    new = np.where(c >= 0, xc + c * (1 - xc), (xc + c) / (1 + c))   # c < 0: stations move in, those inside midship drop
    new = np.where(xi > 1, xi, new)                                  # beyond the AP and FP: no shift
    xn = np.where(X0 >= XM, XM + new * (L0 - XM), XM - new * XM)
    keep = ~(((X0 < XM) & (xn > XM)) | ((X0 >= XM) & (xn < XM)))
    x = np.linspace(X0.min(), X0.max(), nx)
    y = np.zeros((nx, len(Z0)))
    for j in range(len(Z0)):
        o = np.argsort(xn[keep])
        y[:, j] = np.interp(x, xn[keep][o], Y0[keep, j][o])
        ym = np.interp(XM, X0, Y0[:, j])                             # midship section fills the new parallel body
        y[(x >= XM - max(cA, 0) * XM) & (x <= XM + max(cF, 0) * (L0 - XM)), j] = ym
    return x, y


def _solve_lackenby(CB_target, LCB_target):
    """Find cF, cA that give the target C_B and LCB (% L, + forward) on the parent (Newton, two unknowns)."""
    p = np.zeros(2)
    h = None
    for _ in range(15):
        h = hydrostatics(*_lackenby(*p), Z0, L0, B0, T0)
        r = np.array([h["CB"] - CB_target, h["LCB"] - LCB_target])
        if abs(r[0]) < 2e-4 and abs(r[1]) < 0.02:
            return p, h
        J = np.zeros((2, 2)); e = 2e-3
        for k in range(2):
            q = p.copy(); q[k] += e
            hk = hydrostatics(*_lackenby(*q), Z0, L0, B0, T0)
            J[:, k] = [(hk["CB"] - h["CB"]) / e, (hk["LCB"] - h["LCB"]) / e]
        p = p - np.linalg.solve(J, r)
    return p, h


# ----------------------------------------------------------------------------------------------------------------------
# Step 2: stretch
# ----------------------------------------------------------------------------------------------------------------------
def _stretch(x, y, L, B, T, D):
    """Scale a hull given on the KCS grid to L, B, T and depth D: x by L/L0, y by B/B0, z by T/T0 below the
    waterline, and above it the side is stretched linearly so that it ends at D."""
    sx, sy, sz = L / L0, B / B0, T / T0
    z = np.where(Z0 <= T0, Z0 * sz, T + (Z0 - T0) * (D - T) / (D0 - T0))
    return x * sx, y * sy, z


# ----------------------------------------------------------------------------------------------------------------------
# Half-breadth at any point (bilinear, 0 outside the hull)
# ----------------------------------------------------------------------------------------------------------------------
class _Interp:
    def __init__(self, x, z, y):
        self.x, self.z, self.y = x, z, y

    def __call__(self, pts):
        pts = np.atleast_2d(np.asarray(pts, float)); xq, zq = pts[:, 0], pts[:, 1]
        x, z, y = self.x, self.z, self.y
        out = np.zeros(len(xq))
        ok = (xq >= x[0]) & (xq <= x[-1]) & (zq >= z[0]) & (zq <= z[-1])
        i = np.clip(np.searchsorted(x, xq[ok]) - 1, 0, len(x) - 2); j = np.clip(np.searchsorted(z, zq[ok]) - 1, 0, len(z) - 2)
        tx = (xq[ok] - x[i]) / (x[i + 1] - x[i]); tz = (zq[ok] - z[j]) / (z[j + 1] - z[j])
        out[ok] = ((1 - tx) * (1 - tz) * y[i, j] + tx * (1 - tz) * y[i + 1, j] + (1 - tx) * tz * y[i, j + 1] + tx * tz * y[i + 1, j + 1])
        return out


def hull_y(hull, x, z):
    """Half-breadth [m] at x from the AP and z above the baseline [m]; scalars or arrays."""
    x, z = np.broadcast_arrays(np.asarray(x, float), np.asarray(z, float))
    return hull["f"](np.stack([x.ravel(), z.ravel()], axis=-1)).reshape(x.shape)


# ----------------------------------------------------------------------------------------------------------------------
# The function
# ----------------------------------------------------------------------------------------------------------------------
def check_range(CB, L, B, T):
    """Warnings when an input is outside the guideline range of the method (not an error)."""
    msgs = []
    for name, val in [("CB", CB), ("LB", L / B), ("BT", B / T)]:
        lo, hi = RANGE[name]
        if not lo <= val <= hi:
            msgs.append(f"{name.replace('LB', 'L/B').replace('BT', 'B/T')} = {val:.3f} is outside {lo}-{hi}")
    return msgs


def make_hull(CB, LCB, L, B, T, D, warn=True):
    """A hull from the KCS: Lackenby to C_B and LCB (% L, + forward), then the stretch to L, B, T, D [m].
    See the top of this file.  Returns a dictionary (x, y, z, h, cF, cA, warnings, f ...)."""
    for name, v in (("L", L), ("B", B), ("T", T), ("D", D), ("CB", CB)):
        if not np.isfinite(v) or v <= 0:
            raise ValueError(f"{name} must be a positive number, got {v}")
    if T >= D:
        raise ValueError(f"the draught T = {T:.2f} m is at or above the depth D = {D:.2f} m: the hull cannot be made "
                         f"(the waterlines of the side would not be in increasing order). Make D larger or T smaller.")
    if abs(CB - PARENT["CB"]) < 1e-4 and abs(LCB - PARENT["LCB"]) < 0.02:
        cF, cA, x, y = 0.0, 0.0, X0, Y0                       # the parent itself, no Lackenby
    else:
        (cF, cA), _ = _solve_lackenby(CB, LCB)
        x, y = _lackenby(cF, cA)
    x, y, z = _stretch(x, y, L, B, T, D)
    h = hydrostatics(x, y, z, L, B, T)
    hull = dict(x=x, y=y, z=z, L=L, B=B, T=T, D=D, cF=cF, cA=cA, h=h, warnings=check_range(CB, L, B, T))
    if abs(h["CB"] - CB) > 1e-3 or abs(h["LCB"] - LCB) > 0.05:
        hull["warnings"].append(f"target not reached: C_B {h['CB']:.4f}, LCB {h['LCB']:+.2f} %")
    if warn:
        for w_ in hull["warnings"]:
            print("WARNING:", w_)
    hull["f"] = _Interp(x, z, y)
    return hull


def summary(hull):
    """Print the main numbers of a hull."""
    h = hull["h"]
    print(f"L {hull['L']:.1f} m, B {hull['B']:.2f} m, T {hull['T']:.2f} m, D {hull['D']:.2f} m;  c_F {hull['cF']:+.3f}, c_A {hull['cA']:+.3f}")
    print(f"V {h['V']:,.0f} m3, C_B {h['CB']:.4f}, C_P {h['CP']:.4f}, C_M {h['CM']:.4f}, C_WP {h['CWP']:.4f}, LCB {h['LCB']:+.2f} %, LWL {h['LWL']:.1f} m")
    print(f"KB {h['KB']:.2f} m, BM {h['BM']:.2f} m, KM {h['KM']:.2f} m")


def export_offsets(hull, filename):
    """Write the offsets of the hull: one row per station (x_m), one column per waterline (z=...)."""
    with open(filename, "w") as f:
        f.write("x_m," + ",".join(f"z={v:.3f}" for v in hull["z"]) + "\n")
        for i, xv in enumerate(hull["x"]):
            f.write(f"{xv:.3f}," + ",".join(f"{v:.4f}" for v in hull["y"][i]) + "\n")
    print(f"saved {filename}: {len(hull['x'])} stations x {len(hull['z'])} waterlines")


# ----------------------------------------------------------------------------------------------------------------------
# Worked example and self-test:  python make_hull.py
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("The parent, KCS, from the offsets:  C_B %.4f, V %.0f m3, LCB %+.2f %%   (published: C_B 0.6505, V 52,030 m3; the offsets are a cut of the IGES surface, about 0.4 %% apart)" % (PARENT["CB"], PARENT["V"], PARENT["LCB"]))
    print("\nA variant: C_B 0.69, LCB -1.0 %, L 200 m, B 30 m, T 10.5 m, D 16 m")
    hull = make_hull(CB=0.690, LCB=-1.0, L=200.0, B=30.0, T=10.5, D=16.0)
    summary(hull)
    print("half-breadth at midship, 2 m above the baseline: %.3f m" % hull_y(hull, 100.0, 2.0))
    assert abs(hull["h"]["CB"] - 0.690) < 1e-3 and abs(hull["h"]["LCB"] + 1.0) < 0.05, "the targets were not reached"
    print("\nWhat happens outside the guideline range (a warning, not an error):")
    make_hull(CB=0.60, LCB=-1.0, L=200.0, B=30.0, T=10.5, D=16.0)
    print("\nWhat happens when the hull cannot be made (an error you can catch):")
    try:
        make_hull(CB=0.69, LCB=-1.0, L=200.0, B=30.0, T=17.0, D=16.0)
    except ValueError as e:
        print("ValueError:", e)
    print("\nSelf-test passed.")
