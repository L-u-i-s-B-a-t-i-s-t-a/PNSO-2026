"""Container Ships · Design Manual: Sizing from Bays, Rows and Tiers
Appendix D · Writing the code: the code of the four harder steps.

T. Santos, L. Batista · Ship and Ocean Systems Design 2026

These are the functions printed in Appendix D of the manual, copied here so that
the indentation survives. They are not a complete program: they use the input
names of Step 0 and the constants of Steps 6 and 7 as global names, and they call
the functions of the Appendix D table that your group writes (split, bays, length,
beam, depth, cb_katsoulis, admiralty_power, lightship, close_weights, consumables,
deck_tiers_needed, load_cargo, deckhouse_weight, centre_of_gravity,
hold_utilization, ballast_capacity, ...). Python 3 with no extra packages.

Check your program on the worked example of III.1 before using it on your brief.
"""

import math

def tiers_visible(x_fwd, x_eye, z_eye, x_bow, T, distance, z_base, h_c):
    """Eqs. (13) and (14): tiers a deck bay can carry under the sight line.

    The sight line goes from the eye (x_eye, z_eye) to the sea surface at
    'distance' ahead of the bow (SOLAS V/22: 2 L_OA or 500 m, whichever is less).
    x is measured forward from the aft perpendicular, z up from the base line.
    x_fwd  : forward end of the bay, m
    T      : draught, m
    z_base : top of the hatch cover, where the first deck tier stands, m
    """
    x_sea = x_bow + distance
    z_line = T + (z_eye - T) * (x_sea - x_fwd) / (x_sea - x_eye)   # height of the line at x_fwd
    n = math.floor((z_line - z_base) / (h_c + gap))
    if n < 0:
        n = 0
    return n


def solve_cb_t(Delta, L_PP, B, V):
    """Eq. (19): find C_B and T together for a displacement Delta (t).

    Start from a draught, compute C_B with Katsoulis, then the draught that
    gives Delta = 1.030 C_B L_PP B T. Repeat until T changes by less than 1 cm.
    Returns C_B and T.
    """
    T = B / 2.9                                   # starting draught, any value works
    for i in range(50):
        C_B = cb_katsoulis(L_PP, B, T, V)
        T_new = Delta / (1.030 * C_B * L_PP * B)
        if abs(T_new - T) < 0.01:
            return C_B, T_new
        T = T_new
    print("The C_B and T loop did not converge")
    return None, None


def close_design(s_H, n_R, n_T, show):
    """Steps 5 and 6 for one candidate: the weight balance of eq. (30), closed by draught.

    As in Lecture 3.1: lightship + deadweight against the hull. Here C_B follows the
    draught (Katsoulis, eq. 19) and the lightship follows T, C_B and the power, so the
    balance is repeated until the draught changes by less than 1 cm. Then k_U is
    recomputed with the new C_B (step 5.4); if the number of bays changes, it starts
    again. With show=True it prints each pass.
    """
    N_H, N_D = split(N_TEU, s_H)
    C_B = 0.68                                                   # starting value (step 2)
    for outer in range(10):
        n_B = bays(N_H, n_R, n_T, hold_utilization(C_B))
        L = length(n_B, L_AP_ER, L_FP)
        B = beam(n_R, w_DH, g_BC, g_BF)
        D = depth(n_T, h_DB, h_CO, c_HC, c_DK, h_c)
        n_HO = n_B // 2
        l_hold = 2 * 0.115 + 2 * l_c + 0.180                     # eq. (6), g_LB = 0.115, g_LF = 0.180
        T = B / 2.9                                              # starting draught
        for i in range(50):
            hull = 1.030 * C_B * L * B * T                       # what the hull floats now
            P = admiralty_power(hull, V)                         # power for that displacement
            ls = lightship(L, B, D, T, C_B, P, n_HO, l_hold)     # lightship from its parts
            shortfall = ls["LWT"] + DWT - hull                   # > 0: the hull is too small
            Delta, C_B, T_new = close_weights(DWT, ls["LWT"], L, B, V)   # eq. (30): new C_B and T
            if show:
                print(f"    pass {i + 1}: T {T:.2f} m, LWT + DWT {ls['LWT'] + DWT:.0f} t,"
                      f" hull {hull:.0f} t, shortfall {shortfall:+.0f} t (reserve {ls['R']:.0f} t)"
                      f" -> T {T_new:.2f} m, C_B {C_B:.3f}")
            if abs(T_new - T) < 0.01:
                T = T_new
                break
            T = T_new
        if bays(N_H, n_R, n_T, hold_utilization(C_B)) == n_B:
            break
    Delta = 1.030 * C_B * L * B * T
    return {"s_H": s_H, "N_H": N_H, "N_D": N_D, "n_R": n_R, "n_T": n_T, "n_B": n_B,
            "L": L, "B": B, "D": D, "T": T, "C_B": C_B, "Delta": Delta,
            "P": admiralty_power(Delta, V), "ls": ls}


def stability(c, condition, ballast, n_teu):
    """Step 7 for one candidate c (from close_design): one loading condition,
    n_teu containers and a mass of water ballast in the double bottom, t.

    condition: "departure", "arrival" or "homogeneous" (section 7.4).
    Returns T, KG, KB, BM, the free-surface correction, GM and the roll period.
    """
    L, B, D, T, C_B = c["L"], c["B"], c["D"], c["T"], c["C_B"]
    cons = consumables(c["P"], V)
    tanks = cons["fuel"] + cons["lub"] + cons["water"]
    people = cons["food"] + cons["crew"]
    if condition == "arrival":
        tanks = 0.10 * tanks
        people = 0.10 * cons["food"] + cons["crew"]
    mass = m_homog if condition == "homogeneous" else m_design
    n_TD = deck_tiers_needed(c["N_D"], c["n_B"], n_l, c["n_R"])
    per_deck_tier = (c["n_B"] + n_l) * (c["n_R"] + 2)
    cargo_m, cargo_z = load_cargo(n_teu, mass, c["N_H"], c["n_T"], n_TD, per_deck_tier, D)
    W_DH, z_DH, h_layer = deckhouse_weight(L, B, D)
    masses = [c["ls"]["LWT"], tanks, people, ballast] + cargo_m
    heights = [c["ls"]["KG_L"], z_tanks, z_DH, z_tanks] + cargo_z
    KG, Delta_c = centre_of_gravity(masses, heights)
    # hydrostatics at the draught of this condition (wall-sided, as Demo 5)
    C_WP = (1 + 2 * C_B) / 3                                   # eq. (34), Papanikolaou Eq. 2.83
    T_c = T + (Delta_c - c["Delta"]) / (1.030 * C_WP * L * B)
    C_Bc = Delta_c / (1.030 * L * B * T_c)
    KB = T_c * (5 / 6 - C_Bc / (3 * C_WP))                    # eq. (33)
    C_IT = C_WP * (0.1272 + 0.8724 * C_WP)                     # eq. (34), Papanikolaou Eq. 2.95
    BM = C_IT * L * B**3 / 12 / (C_Bc * L * B * T_c)          # eq. (33)
    l_tank = 2 * 0.115 + 2 * l_c + 0.180                       # one hold long
    b_tank = (B - 2 * w_DH) / 2                                # half the inner bottom
    dGM_FS = rho_fuel * l_tank * b_tank**3 / 12 / Delta_c      # eq. (34), one slack tank (ASSUMED)
    GM = KB + BM - KG - dGM_FS                                 # eq. (33)
    C = 0.373 + 0.023 * B / T_c - 0.043 * L / 100              # eq. (35), L_WL taken as L_PP
    T_roll = 2 * C * B / math.sqrt(GM) if GM > 0 else None
    return {"T": T_c, "Delta": Delta_c, "n_teu": n_teu, "ballast": ballast, "KG": KG,
            "KB": KB, "BM": BM, "dGM_FS": dGM_FS, "GM": GM, "T_roll": T_roll}


def ballast_needed(c, condition, n_teu):
    """Section 7.4: the least double-bottom ballast (in steps of 10 t) that gives
    GM >= 0.15 m. Returns the stability result, or None if the double bottom
    cannot give that GM."""
    ballast = 0.0
    while ballast <= ballast_capacity(c, condition, n_teu):
        st = stability(c, condition, ballast, n_teu)
        if st["GM"] >= GM_min:
            return st
        ballast = ballast + 10
    return None
