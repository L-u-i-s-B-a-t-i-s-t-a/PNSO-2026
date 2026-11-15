"""Holtrop-Mennen (1982) resistance and power estimate, single screw, calm water.

Ship and Ocean Systems Design 2026. Written to follow the steps of the
animation: every function is one box of the method. Units: m, kN, kW, knots.

Not included (see Lecture 3.3): sea margin, design margin, service margin,
air and wind drag. The result is calm water, clean hull, trial condition.

Run:  python Holtrop_Mennen_Code.py
"""
import math

RHO, G, KN, NU = 1025.0, 9.81, 0.514444, 1.1883e-6  # sea water, 15 C

# ---- the ship of the paper's worked example (hull and appendage data) -------
SHIP = dict(L=205.0, B=32.0, T=10.0, vol=37500.0, lcb=-0.75,  # lcb: % of L, + forward of L/2
            CM=0.98, CWP=0.75, ABT=20.0, hB=4.0, AT=16.0, SAPP=50.0,
            k2=1.5, Cstern=10.0, Dp=8.0, AE=0.7393)


def hull_coefficients(s):
    """Block, prismatic, Froude-independent form numbers."""
    CB = s["vol"] / (s["L"] * s["B"] * s["T"])
    CP = CB / s["CM"]
    return CB, CP


def wetted_surface(s, CB):
    L, B, T, CM, CWP = s["L"], s["B"], s["T"], s["CM"], s["CWP"]
    return (L * (2 * T + B) * math.sqrt(CM)
            * (0.453 + 0.4425 * CB - 0.2862 * CM - 0.003467 * B / T + 0.3696 * CWP)
            + 2.38 * s["ABT"] / CB)


def friction_coefficient(V, L):
    """ITTC-1957 line; V in m/s."""
    Rn = V * L / NU
    return 0.075 / (math.log10(Rn) - 2) ** 2


def form_factor_k1(s, CP):
    """1 + k1 is the form factor on the hull friction."""
    L, B, T, lcb = s["L"], s["B"], s["T"], s["lcb"]
    LR = L * (1 - CP + 0.06 * CP * lcb / (4 * CP - 1))     # length of run
    TL = T / L
    if TL > 0.05:
        c12 = TL ** 0.2228446
    elif TL > 0.02:
        c12 = 48.20 * (TL - 0.02) ** 2.078 + 0.479948
    else:
        c12 = 0.479948
    c13 = 1 + 0.003 * s["Cstern"]
    k1 = c13 * (0.93 + c12 * (B / LR) ** 0.92497 * (0.95 - CP) ** -0.521448
                * (1 - CP + 0.0225 * lcb) ** 0.6906)
    return k1, LR


def wave_resistance(s, V, CB, CP, LR):
    """RW = c1 c2 c5 * vol rho g * exp(m1 Fn^-0.9 + m2 cos(lam Fn^-2)); returns N and parts."""
    L, B, T, vol, lcb = s["L"], s["B"], s["T"], s["vol"], s["lcb"]
    ABT, hB, AT, CM, CWP = s["ABT"], s["hB"], s["AT"], s["CM"], s["CWP"]
    Fn = V / math.sqrt(G * L)
    BL = B / L
    # c7
    if BL < 0.11:
        c7 = 0.229577 * BL ** (1 / 3)
    elif BL < 0.25:
        c7 = BL
    else:
        c7 = 0.5 - 0.0625 / BL
    # half angle of entrance iE (degrees) from the formula (can also be given)
    iE = 1 + 89 * math.exp(-(L / B) ** 0.80856 * (1 - CWP) ** 0.30484
                           * (1 - CP - 0.0225 * lcb) ** 0.6367 * (LR / B) ** 0.34574
                           * (100 * vol / L ** 3) ** 0.16302)
    c1 = 2223105 * c7 ** 3.78613 * (T / B) ** 1.07961 * (90 - iE) ** -1.37565
    # bulb: c3 -> c2
    c3 = 0.56 * ABT ** 1.5 / (B * T * (0.31 * math.sqrt(ABT) + T - hB)) if ABT > 0 else 0.0
    c2 = math.exp(-1.89 * math.sqrt(c3))
    # transom: c5
    c5 = 1 - 0.8 * AT / (B * T * CM)
    # humps and hollows
    lam = 1.446 * CP - 0.03 * L / B if L / B < 12 else 1.446 * CP - 0.36
    c16 = (8.07981 * CP - 13.8673 * CP ** 2 + 6.984388 * CP ** 3) if CP < 0.8 \
        else 1.73014 - 0.7067 * CP
    m1 = 0.0140407 * L / T - 1.75254 * vol ** (1 / 3) / L - 4.79323 * B / L - c16
    L3V = L ** 3 / vol
    if L3V < 512:
        c15 = -1.69385
    elif L3V < 1727:
        c15 = -1.69385 + (L / vol ** (1 / 3) - 8) / 2.36
    else:
        c15 = 0.0
    m2 = c15 * CP ** 2 * math.exp(-0.1 / Fn ** 2)
    RW = (c1 * c2 * c5 * vol * RHO * G
          * math.exp(m1 * Fn ** -0.9 + m2 * math.cos(lam / Fn ** 2)))
    return RW, dict(Fn=Fn, iE=iE, c1=c1, c2=c2, c3=c3, c5=c5, lam=lam, m1=m1, m2=m2)


def bulb_resistance(s, V):
    ABT, hB, T = s["ABT"], s["hB"], s["T"]
    if ABT <= 0:
        return 0.0
    PB = 0.56 * math.sqrt(ABT) / (T - 1.5 * hB)
    Fni = V / math.sqrt(G * (T - hB - 0.25 * math.sqrt(ABT)) + 0.15 * V ** 2)
    return (0.11 * math.exp(-3 * PB ** -2) * Fni ** 3 * ABT ** 1.5 * RHO * G
            / (1 + Fni ** 2))


def transom_resistance(s, V, q):
    AT, B, CWP = s["AT"], s["B"], s["CWP"]
    if AT <= 0:
        return 0.0
    FnT = V / math.sqrt(2 * G * AT / (B + B * CWP))
    return q * AT * 0.2 * (1 - 0.2 * FnT) if FnT < 5 else 0.0


def correlation_allowance(s, CB, c2):
    L, T = s["L"], s["T"]
    c4 = T / L if T / L <= 0.04 else 0.04
    return (0.006 * (L + 100) ** -0.16 - 0.00205
            + 0.003 * math.sqrt(L / 7.5) * CB ** 4 * c2 * (0.04 - c4))


def wake_and_thrust(s, CB, CP, S, CF, k1, CA):
    """Wake fraction w, thrust deduction t, relative rotative efficiency (single screw)."""
    L, B, T, lcb, Dp, Cs = s["L"], s["B"], s["T"], s["lcb"], s["Dp"], s["Cstern"]
    SAPP, k2 = s["SAPP"], s["k2"]
    CV = (k1 + (k2 - k1) * SAPP / (S + SAPP)) * CF + CA
    CP1 = 1.45 * CP - 0.315 - 0.0225 * lcb
    BTA = B / T
    c8 = B * S / (L * Dp * T) if BTA < 5 else S * (7 * BTA - 25) / (L * Dp * (BTA - 3))
    c9 = c8 if c8 < 28 else 32 - 16 / (c8 - 24)
    c11 = T / Dp if T / Dp < 2 else 0.0833333 * (T / Dp) ** 3 + 1.33333
    w = (c9 * CV * L / T * (0.0661875 + 1.21756 * c11 * CV / (1 - CP1))
         + 0.24558 * math.sqrt(B / (L * (1 - CP1))) - 0.09726 / (0.95 - CP)
         + 0.11434 / (0.95 - CB) + 0.75 * Cs * CV + 0.002 * Cs)
    c10 = B / L if L / B > 5.2 else 0.25 - 0.003328402 / (B / L - 0.134615385)
    t = (0.001979 * L / (B - B * CP1) + 1.0585 * c10 - 0.00524
         - 0.1418 * Dp ** 2 / (B * T) + 0.0015 * Cs)
    etaR = 0.9922 - 0.05908 * s["AE"] + 0.07424 * (CP - 0.0225 * lcb)
    return w, t, etaR


def holtrop_mennen(s, V_kn, eta0=None):
    """All resistance components in kN, effective power PE in kW (and PS if eta0 given)."""
    V = V_kn * KN
    CB, CP = hull_coefficients(s)
    S = wetted_surface(s, CB)
    CF = friction_coefficient(V, s["L"])
    k1, LR = form_factor_k1(s, CP)
    q = 0.5 * RHO * V ** 2                                    # dynamic pressure, Pa
    RF = q * S * CF
    RAPP = q * s["SAPP"] * s["k2"] * CF
    RW, w_parts = wave_resistance(s, V, CB, CP, LR)
    RB = bulb_resistance(s, V)
    RTR = transom_resistance(s, V, q)
    CA = correlation_allowance(s, CB, w_parts["c2"])
    RA = q * S * CA
    RT = RF * k1 + RAPP + RW + RB + RTR + RA                  # N
    w, t, etaR = wake_and_thrust(s, CB, CP, S, CF, k1, CA)
    out = dict(V=V_kn, Fn=w_parts["Fn"], CB=CB, CP=CP, S=S, CF=CF, k1=k1,
               RF=RF / 1e3, RF_k1=RF * k1 / 1e3, RAPP=RAPP / 1e3, RW=RW / 1e3,
               RB=RB / 1e3, RTR=RTR / 1e3, RA=RA / 1e3, RT=RT / 1e3,
               PE=RT * V / 1e3, w=w, t=t, etaR=etaR, etaH=(1 - t) / (1 - w), **{
                   k: v for k, v in w_parts.items() if k != "Fn"})
    if eta0:
        out["PS"] = out["PE"] / (out["etaH"] * etaR * eta0)
    return out


def check_validity(s, Fn):
    """Ranges as commonly quoted; here for container ships / destroyers."""
    CB, CP = hull_coefficients(s)
    tests = {"Fn <= 0.45": Fn <= 0.45, "0.55 <= CP <= 0.67": 0.55 <= CP <= 0.67,
             "6.0 <= L/B <= 9.5": 6.0 <= s["L"] / s["B"] <= 9.5,
             "3.0 <= B/T <= 4.0": 3.0 <= s["B"] / s["T"] <= 4.0}
    return tests


if __name__ == "__main__":
    r = holtrop_mennen(SHIP, 25.0)
    print("Fn %.3f  CB %.3f  CP %.3f  S %.1f m2" % (r["Fn"], r["CB"], r["CP"], r["S"]))
    for k in ("RF_k1", "RAPP", "RW", "RB", "RTR", "RA", "RT"):
        print("%-6s %9.1f kN" % (k, r[k]))
    print("PE     %9.0f kW   w %.3f  t %.3f  etaR %.3f" % (r["PE"], r["w"], r["t"], r["etaR"]))
    print("validity:", check_validity(SHIP, r["Fn"]))
    # self-test against the course animation (and the paper's example, within ~0.6 %)
    assert abs(r["RT"] - 1792) < 10 and abs(r["PE"] - 23047) < 120, "check failed"
    print("self-test passed: RT = 1,792 kN, PE = 23,047 kW")
    print("speed sweep:")
    for v in range(15, 31, 5):
        x = holtrop_mennen(SHIP, v)
        print("  %2d kn  Fn %.3f  RT %7.1f kN  PE %8.0f kW" % (v, x["Fn"], x["RT"], x["PE"]))
