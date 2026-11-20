"""Hold Capacity · Stage 1: main dimensions from the number of containers (no hull lines yet).

T. Santos, L. Batista · Ship and Ocean Systems Design 2026

Plain steps of the Design Manual (Alvarino, Azpiroz and Meizoso 1997, section 2.9.3):
  1 split the containers in hold and deck       2 first estimate of L, B, D, T from the hold containers
  3 whole rows and tiers in the hold            4 bays   5 L, B, D from the bays, rows and tiers
  6 ratio check                                 7 deck tiers under the sight line
Not modelled separately (omitted for clarity): the transverse bulkheads between holds, the ends of the
hatch coamings, the tank top, girders, cell guides and the contents of the engine room. Their space is
inside the 6.55 m per 20 ft bay and inside the allowances L_AP, L_ER and L_FP.
Python 3, no extra packages. Change N_TEU and s_H and run it.
Disclaimer: this example is a generalization that illustrates the process. It does not address a ship with
the superstructure positioned forward, nor the space for LNG equipment and tanks. Both change the arrangement
(bridge and sight line, length, hold and deck space), so the equations might have to be adapted.
"""
from math import exp, log, floor, ceil

# ==== INPUTS: everything the program is given, with where each number comes from =====

# ---- A. THE BRIEF and the designer's choices --------------------------------
N_TEU = 596          # total containers (TEU), from the owner's brief
s_H = 0.45           # share carried in the hold (a choice; the manual sweeps 0.30 to 0.50)
add_row, add_tier = 1, 1   # 0 or 1: one more row or tier than the whole number of step 3

# ---- B. FROM SIMILAR SHIPS: the lengths at the ends of the ship (not computed here) ----
# Give them in metres (USE_RATIOS = False) or as fractions of the length L (USE_RATIOS = True).
USE_RATIOS = False
L_AP_m, L_ER_m, L_FP_m = 4.0, 17.6, 15.1     # aft peak, engine room, fore peak (m)
r_AP, r_ER, r_FP = 0.035, 0.156, 0.134       # the same three as fractions of L
# Reference ship of the manual: L = 112.9 m, aft peak + engine room 21.6 m, fore peak 15.1 m.
# The manual gives only the sum L_AP + L_ER; the split above is illustrative, the sum is not.

# ---- C. FROM A REFERENCE SHIP (Design Manual I.3, I.5, III.1), metres ----------
w_DH, h_DB, h_CO, c_HC = 2.1, 0.8, 1.6, 0.49   # double hull, double bottom, coaming, margin under the hatch cover
t_cover = 0.6                                  # hatch cover (used for the deck, step 7)
n_l = 2                                        # deck bays over the engine room
x_eye, h_eye = 10.8, 1.8                       # officer's eye: distance from the stern, height above the bridge deck
C_B_assumed = 0.68                             # assumed block coefficient, only to get k_U

# ---- D. FROM TABLES AND STANDARDS ---------------------------------------------
g_BC, g_BF = 0.15, 0.08                        # beam gaps, Table 2.9.2 (lower values)
b_c, h_c = 2.438, 2.896                        # high-cube container: width, height
gap, bay = 0.013, 6.55                         # gap added to each tier; length of one bay

# ---- derived from the inputs above ---------------------------------------------
k_U = 0.5 * C_B_assumed + 0.4                  # eq. (8): hold utilisation = 0.74

# ---- 1. split ---------------------------------------------------------------
N_H = round(s_H * N_TEU)         # containers in the hold
N_D = N_TEU - N_H                # containers on deck

# ---- 2. first estimate from statistics (Panama fit, B <= 32.2 m) ---------------
L0 = 113.5 + 0.082 * N_H - 3607.5 / N_H
B0 = exp(0.674 - 2.7e-4 * N_H + 0.44 * log(N_H))
D0 = exp(0.249 - 5.36e-6 * N_H + 0.375 * log(N_H))
T0 = -6.05 + 2.49 * log(N_H)

# ---- 3. whole rows and tiers -------------------------------------------------
n_R = floor((B0 - 2 * w_DH) / 2.54) + add_row
n_T = floor((D0 + h_CO - h_DB - c_HC) / (h_c + gap)) + add_tier

# ---- 4. bays: the smallest even number that holds N_H -------------------------
n_B = ceil(N_H / (n_R * n_T * k_U) - 1e-9)
if n_B % 2 == 1:        # % is the remainder after dividing by 2: 1 means an odd number
    n_B = n_B + 1       # add one bay, because bays go in pairs

# ---- 5. the dimensions ---------------------------------------------------------
# One function for each allowance. Today each returns an input (a length, or a ratio times L).
# Exercise: replace the body by a calculation (for the engine room, from the installed power).
def L_AP(L):
    return r_AP * L if USE_RATIOS else L_AP_m
def L_ER(L):
    return r_ER * L if USE_RATIOS else L_ER_m
def L_FP(L):
    return r_FP * L if USE_RATIOS else L_FP_m

L = bay * n_B                                  # first guess: the bays alone
for _ in range(20):                            # L is on both sides when the allowances are ratios,
    L = bay * n_B + L_AP(L) + L_ER(L) + L_FP(L)    # so repeat the sum until it settles
B = 2 * w_DH + 2 * g_BC + n_R * b_c + g_BF * (n_R - 1)
D = n_T * (h_c + gap) + h_DB + c_HC - h_CO

# ---- 6. ratio check: the manual's table, Panama row chosen by N_H -------------------
if N_H < 1000:
    rng = {"L/B": (5.2, 6.5), "B/D": (1.7, 2.2), "B/T": (2.4, 3.2), "L/D": (10.5, 13.0), "T/D": (0.63, 0.79)}
elif N_H < 1500:
    rng = {"L/B": (5.7, 7.5), "B/D": (1.6, 1.9), "B/T": (2.4, 3.1), "L/D": (10.5, 12.7), "T/D": (0.57, 0.70)}
else:
    rng = {"L/B": (6.5, 8.5), "B/D": (1.5, 1.7), "B/T": (2.4, 2.9), "L/D": (11.0, 13.5), "T/D": (0.55, 0.65)}
value = {"L/B": L / B, "B/D": B / D, "B/T": B / T0, "L/D": L / D, "T/D": T0 / D}

# ---- 7. deck tiers under the sight line ----------------------------------------
# SIMPLIFIED: one straight line from the eye to the sea, on the centerline only, at the draught T0,
# with the eye at a fixed place over the engine room (x_eye, h_eye). Like L_AP, L_ER and L_FP,
# this is for you to develop in the iterative loop: the real position of the bridge, trim,
# the rows off the centerline, the shape of the bow.
z_BR = 0.22 * L + 0.28 * D ** 1.56 - 0.02 * L ** 0.806 * D ** 1.1   # bridge deck height
z_eye = z_BR + h_eye
x_sea = L + min(2 * L, 500)                      # where the line meets the sea
def tiers_visible(x_fwd):
    z_line = T0 + (z_eye - T0) * (x_sea - x_fwd) / (x_sea - x_eye)
    return max(0, floor((z_line - (D + h_CO + t_cover)) / (h_c + gap)))

per_tier = (n_B + n_l) * (n_R + 2)               # containers in one deck tier (n_l bays over the engine room)
for n_TD in range(1, 6):
    if per_tier * n_TD >= N_D:
        break

print(f"hold {N_H} + deck {N_D} = {N_TEU} TEU")
print(f"first estimate  L0 {L0:.1f}  B0 {B0:.2f}  D0 {D0:.2f}  T0 {T0:.2f} m")
print(f"rows {n_R}, tiers {n_T}, bays {n_B}  ->  L {L:.1f}  B {B:.2f}  D {D:.2f} m")
for name, (lo, hi) in rng.items():
    print(f"  {name} {value[name]:5.2f}  [{lo}-{hi}]  {'ok' if lo <= value[name] <= hi else 'OUT'}")
print(f"deck: {n_TD} tiers needed; the sight line allows {tiers_visible(L_AP(L) + L_ER(L) + bay * n_B)} at the foremost bay (bridge {z_BR:.1f} m)")
