"""Hold Capacity · Stage 3: from the capacity to the displacement (close the ship by draught).

T. Santos, L. Batista · Ship and Ocean Systems Design 2026

Stage 1 gave n_B, L, B and D. Now the ship must float at the weight it really has, and two numbers are still open: the
draught T and the block coefficient C_B. The hull carries 1.030 x C_B x L x B x T tonnes. The ship weighs light ship +
deadweight, and the light ship depends on T and C_B. So we guess, compute, correct and repeat until T moves less than 1 cm.

The loop starts from C_B = 0.68 and T = B / 2.9. They are only a start: the first pass replaces them.
At the end the script compares the closed C_B and T with the ones the hull of Stage 2 was made with. If they MOVED, make
the hull again at the new values (Stage 2), count again, and bring the new number of bays back here.

Same ship as Stage 1 and Stage 2: the 596 TEU feeder of the Manual. Check: T 7.23 m, C_B 0.615, power 6,150 kW,
light ship 4,065 t, displacement 12,958 t. For your own ship change n_B, B, D (from Stage 1), V and DWT (from your brief).
Plain steps, Python 3, no extra packages.
"""
from math import sqrt

# ==== INPUTS =================================================================

# ---- A. FROM STAGE 1 AND STAGE 2 (the capacity is settled) --------------------
n_B = 14                          # bays (Stage 1: 14; the real hull of Stage 2 may change it)
L_AP, L_ER, L_FP = 4.0, 17.6, 15.1   # aft peak, engine room, fore peak (m), as in Stage 1
L = L_AP + L_ER + L_FP + 6.55 * n_B  # m: 128.4 for 14 bays. Another number of bays is another length.
B, D = 22.046, 11.326             # m: from the rows and tiers (Stage 1)
T0 = 7.872                        # m: first draught of the statistics (Stage 1, step 2). Used for the first hull only.
C_B_hull, T_hull = 0.68, T0       # the C_B and T the real hull of Stage 2 was made with (round 1: the assumed ones)

# ---- B. FROM THE BRIEF ---------------------------------------------------------
V = 16.5                          # service speed, knots
DWT = 8893.0                      # deadweight, t (fixed by the brief of the Manual)

# ---- C. FROM THE REFERENCE SHIP AND THE MANUAL (sections 6.1 to 6.6) --------------
C_N = 403.0                       # Admiralty constant of the reference ship (Manual 6.1)
w_DH, h_CO = 2.1, 1.6             # double hull, hatch coaming (m)
g_LB, g_LF, l_c = 0.115, 0.180, 6.058          # guide clearances and 20 ft container length (m)
C_ST, C_1 = 0.093, 0.25           # Schneekluth steel constant; C_BD constant (Manual 6.3)
K_OT, R_frac = 0.36, 0.02         # outfit, t per m2; reserve margin (Manual 6.5)
C_DH = [57, 55, 52, 53, 40]       # deckhouse weights, kp per m3, layers I-IV and wheelhouse (Manual 6.3)
dh_l, dh_layers = 12.0, 5         # deckhouse length (m) and number of layers
rpm, mach_exp = 500.0, 1.0        # engine speed; exponent of the machinery weight as printed in the Manual (eq. 28)

# ---- D. THE ASSUMED STARTING VALUES -------------------------------------------
C_B = 0.68                        # first block coefficient (Manual, Step 2): replaced in the first pass
T = B / 2.9                       # first draught, only to start the loop

# ==== STEPS 5 AND 6: THE DRAUGHT LOOP ======================================
n_HO = n_B // 2                                   # holds (two bays each)
l_hold = 2 * g_LB + 2 * l_c + g_LF                # length of one hold, eq. (6)
bridge = 0.22 * L + 0.28 * D ** 1.56 - 0.02 * L ** 0.806 * D ** 1.1     # eq. (15): bridge height above the base line
h_dh = bridge - D                                 # height of the deckhouse
h_layer = h_dh / dh_layers

print(f"START: L {L:.1f} m, B {B:.3f} m, D {D:.3f} m, deadweight {DWT:.0f} t")
print(f"       assumed C_B {C_B:.2f} and first draught T {T:.2f} m (B / 2.9)")
print()

MAX_PASSES = 50                                  # a loop must have a limit: never an endless loop
for i in range(MAX_PASSES):
    # 1. What the hull displaces at the present C_B and T
    hull = 1.030 * C_B * L * B * T

    # 2. The power for that displacement (Admiralty, eq. 21)
    P = hull ** (2 / 3) * V ** 3 / C_N

    # 3. The light ship at the present T and C_B and that power
    C_BD = C_B + C_1 * (D - T) / T * (1 - C_B)                       # block coefficient up to the deck
    vol_U = L * B * D * C_BD + n_HO * l_hold * (B - 2 * w_DH) * h_CO # volume under the deck, with the coamings
    w_steel = (vol_U * C_ST * (1 + 2e-6 * (L - 120) ** 2) * (1 + 0.057 * (L / D - 12)) * sqrt(30 / (D + 14))
               * (1 + 0.1 * (B / D - 2.1) ** 2) * (1 + 0.2 * (T / D - 0.85)) * (0.92 + (1 - C_BD) ** 2))   # eq. (23)
    k1 = 1 + 0.02 * (h_layer - 2.6)
    k3 = min(1.0, max(0.95, 0.95 + 0.05 * (L - 100) / 20))
    w_deckhouse = sum(C_DH[:dh_layers]) / 1000 * dh_l * B * h_layer * k1 * k3                               # eq. (25)
    w_outfit = K_OT * L * B                                                                                 # outfit
    w_machinery = 12 * (P / rpm) ** mach_exp + 0.69 * P ** 0.70                                             # eq. (28)
    groups = w_steel + w_deckhouse + w_outfit + w_machinery
    LWT = groups * (1 + R_frac)                                                                             # light ship with reserve

    # 4. The weight the ship really has, and the shortfall of the hull
    weight = LWT + DWT
    shortfall = weight - hull                     # negative: the hull is bigger than the weight, so it floats too deep

    # 5. New C_B and T for that weight, TOGETHER (Katsoulis, eq. 19). Another small loop:
    T_try = B / 2.9
    for j in range(50):
        C_B_new = 0.8217 * L ** 0.42 * B ** -0.3072 * T_try ** 0.1721 * V ** -0.6135    # C_B from the draught
        T_new = weight / (1.030 * C_B_new * L * B)                                      # draught from C_B and the weight
        if abs(T_new - T_try) < 0.01:
            break
        T_try = T_new

    print(f"pass {i + 1}: T {T:.2f} m, light ship + deadweight {weight:.0f} t, hull {hull:.0f} t, "
          f"shortfall {shortfall:+.0f} t -> T {T_new:.2f} m, C_B {C_B_new:.3f}")

    # 6. Compare the new draught with the one this pass started from
    moved = abs(T_new - T)
    C_B, T = C_B_new, T_new                       # C_B and T from the SAME pass go to the next one
    if moved < 0.01:
        break
else:
    print(f"NOT CONVERGED: {MAX_PASSES} passes and T still moves ({moved * 100:.1f} cm per pass). Do not use these numbers.")

# ==== THE CLOSED DESIGN =====================================================
Delta = 1.030 * C_B * L * B * T
print()
print(f"CLOSED: T {T:.3f} m, C_B {C_B:.4f}, displacement {Delta:.0f} t, power {Delta ** (2 / 3) * V ** 3 / C_N:.0f} kW, "
      f"light ship {LWT:.0f} t (steel {w_steel:.0f}, deckhouse {w_deckhouse:.0f}, outfit {w_outfit:.0f}, "
      f"machinery {w_machinery:.0f}, reserve {LWT - groups:.0f})")

# ==== BACK TO THE HULL: DO THE ASSUMED VALUES STILL HOLD? =====================
# The real hull of Stage 2 was made with C_B_hull and T_hull (inputs above). If the closed values moved, the hull is made again.
print()
print(f"Hull of Stage 2 was made at C_B {C_B_hull:.3f}, T {T_hull:.2f} m; the ship closed at C_B {C_B:.3f}, T {T:.2f} m.")
if abs(C_B - C_B_hull) > 0.003 or abs(T - T_hull) > 0.05:
    print("MOVED (C_B by more than 0.003 or T by more than 0.05 m): make the hull again at the new C_B and T,")
    print("count the containers again, correct the bays if the count changed, and close the weights again (a new round).")
else:
    print("NOT MOVED: the hull of Stage 2 is the hull of the closed ship.")
