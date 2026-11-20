"""Hold Capacity · Stage 2: count the containers in the real hull form (Demo 8).

T. Santos, L. Batista · Ship and Ocean Systems Design 2026

Run it after the cells of the Demo 8 notebook that define make_hull and hull_y
(or paste it in a new cell at the end of that notebook), with the main dimensions
of Stage 1. For every bay and every tier it asks the hull for its half-breadth and
counts how many rows of containers fit across. Python 3, numpy.

Limits of the Stage 1 estimate: k_U spreads the losses evenly along the ship, but they sit at the bow and
stern bays; it comes from an assumed block coefficient C_B that the hull gives only later; and it cannot see which rows and
tiers are cut. This program counts them bay by bay.
Disclaimer: this example is a generalization that illustrates the process. It does not address a ship with
the superstructure positioned forward, nor the space for LNG equipment and tanks. Both change the arrangement
(bridge and sight line, length, hold and deck space), so the equations might have to be adapted.

Not modelled separately (omitted for clarity): the transverse bulkheads between holds, the ends of the
hatch coamings, the tank top, girders, cell guides and the contents of the engine room. Their space is
inside the 6.55 m per 20 ft bay and inside the allowances L_AP, L_ER and L_FP.
"""
from math import floor, ceil

# ---- INPUTS: the Stage 1 result and the hull form --------------------------------
L, B, D, T = 128.4, 22.05, 11.33, 7.87   # from Stage 1 (T = T0 of the statistics)
n_R, n_T, n_B = 7, 4, 14                 # rows, tiers, bays of the chosen grid
N_H, N_D, n_TD = 268, 328, 3             # hold target, deck target, deck tiers
CB, LCB = 0.68, -1.0                     # hull form: block coefficient, LCB in % L
L_AP_ER = 21.6                           # from Stage 1: L_AP + L_ER, the aft block with no cargo (m)

# ---- the same data as Stage 1 (metres) -----------------------------------------------
w_DH, h_DB = 2.1, 0.8                    # FROM A REFERENCE SHIP: double hull, double bottom
n_l = 2                                  # FROM A REFERENCE SHIP: deck bays over the engine room
g_BC, g_BF = 0.15, 0.08                  # FROM TABLES: beam gaps (Table 2.9.2, lower values)
b_c, h_c, gap, bay = 2.438, 2.896, 0.013, 6.55   # STANDARD DATA: high-cube container, tier gap, bay length

hull = make_hull(CB, LCB, L, B, T, D)    # <- the hull-generating function of Demo 8

def rows_in_hold(xs, z_bottom, z_top):
    """Rows that fit across a hold: the narrowest section along its length rules (the cell guides are continuous)."""
    y = min(min(hull_y(hull, x, z_bottom), hull_y(hull, x, z_top)) for x in xs)   # narrowest of all stations and both heights
    room = 2 * (y - w_DH) - 2 * g_BC                                # between the double hulls
    return max(0, floor((room + g_BF) / (b_c + g_BF) + 0.01))   # 0.01: tolerance for rounded offsets

# ---- hold: every hold (two bays), every tier ----------------------------------------
hold = 0
for k in range(0, n_B, 2):                         # a hold is two bays: they share the cell guides
    x_aft = L_AP_ER + bay * k + 0.3                # a little inside the hold ends
    x_fwd = L_AP_ER + bay * (k + 2) - 0.3
    xs = [x_aft + (x_fwd - x_aft) * q / 4 for q in range(5)]   # five stations along the hold
    for t in range(n_T):
        z0 = h_DB + t * (h_c + gap)                # bottom of this tier
        z1 = min(z0 + h_c, D)                      # top of this tier
        r = min(rows_in_hold(xs, z0, z1), n_R)
        r = max(0, n_R - 2 * ceil((n_R - r) / 2))  # rows leave in symmetric pairs (7 -> 5 -> 3): the cell guides are fixed
        hold += 2 * r                              # both bays of the hold get the same rows

# ---- deck: rows across the deck edge, 2.464 m pitch, tiers from Stage 1 ----------------
def rows_on_deck(x):
    return floor((2 * (hull_y(hull, x, D) + 0.15) + (2.464 - b_c)) / 2.464 + 0.01)

z_BR = 0.22 * L + 0.28 * D ** 1.56 - 0.02 * L ** 0.806 * D ** 1.1     # bridge deck height (Stage 1, step 7)
z_eye, x_eye, x_sea = z_BR + 1.8, 10.8, L + min(2 * L, 500)
# SIMPLIFIED: the sight line is one straight line, on the centerline only, at the draught T,
# with the eye at a fixed place. It is for you to develop in the iterative loop (see Stage 1, step 7).

def tiers_visible(x_fwd):
    """Deck tiers a bay can carry under the sight line (SOLAS), as in Stage 1."""
    z_line = T + (z_eye - T) * (x_sea - x_fwd) / (x_sea - x_eye)
    return max(0, floor((z_line - (D + 1.6 + 0.6)) / (h_c + gap)))

deck = 0
for k in range(n_B + n_l):                         # the bays over the engine room count too
    x0 = L_AP_ER + bay * (k - n_l)
    r = min(rows_on_deck(x0 + 0.3), rows_on_deck(x0 + bay - 0.3))
    tiers = n_TD if k < n_l else min(n_TD, tiers_visible(x0 + bay))
    deck += r * tiers

k_U_real = hold / (n_B * n_R * n_T)
print(f"hold: {hold} TEU in the real hull (target {N_H}), real k_U = {k_U_real:.2f} (Stage 1 used 0.74)")
print(f"deck: {deck} TEU (target {N_D})")
print(f"total {hold + deck} TEU against {N_H + N_D} asked")
