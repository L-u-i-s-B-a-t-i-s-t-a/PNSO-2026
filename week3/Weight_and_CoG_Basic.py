# Light-ship weight and centre of gravity: a very basic version, to read, run and change.
# Two methods on one ship (Baseline A, the Azores Express), written as plain steps:
# no functions, no classes, only numbers, formulas and print.
#   Method 1: the textbook (Papanikolaou 2026, section 2.15 and Appendix A)
#   Method 2: the paper (Szelangiewicz and Zelazny 2025, Appl. Sci. 15, 7886)
# Units: metres, tonnes, kW, knots.
# The engine power, the generator power and the crew are ASSUMED (the brief does not give them).

import math

# ---- INPUTS: Baseline A ----------------------------------------------------
TEU = 1300          # containers, TEU
CARGO = 13000.0     # cargo deadweight, t
V = 18.5            # speed, knots
MCR = 11300.0       # main engine power, kW   (ASSUMED, scaled from the paper's ship A)
RPM = 105.0         # main engine speed, rpm  (ASSUMED)
NE = 2000.0         # power of the generating sets, kW (ASSUMED)
J = 20              # crew (ASSUMED)
DH_L = 24.0         # deckhouse length, m (ASSUMED)
DH_H = 17.5         # deckhouse height, m (ASSUMED)

# ---- 0. main dimensions from the Appendix A fits (as in the lectures) ------
DWT = CARGO / 0.75                                   # Fig. A.49
L = 3.54132 * DWT ** 0.388442                        # Fig. A.31
B = 1.55219 * DWT ** 0.284381                        # Fig. A.32
D = 0.299394 * DWT ** 0.38902                        # Fig. A.33 (depth)
T = -17.1581 + 2.72338 * math.log(DWT)               # Fig. A.34
Fn = V * 0.5144 / math.sqrt(9.81 * L)                # Froude number
CB = 1.06 - 1.68 * Fn                                # Horn, Table 2.15
LBH = L * B * D
print(f"Baseline A: DWT {DWT:.0f} t, L {L:.1f}, B {B:.2f}, D {D:.2f}, T {T:.2f} m, CB {CB:.3f}")
print()

# ============================================================================
# METHOD 1: THE TEXTBOOK
# ============================================================================

# ---- 1. steel, two routes --------------------------------------------------
# Watson: equipment numeral EN, then W = K * EN^1.36 * (1 + 0.5 * (CB' - 0.70))
EN = L * (B + T) + 0.85 * L * (D - T) + 0.75 * DH_L * DH_H
CB_PRIME = CB + (1 - CB) * (0.8 * D - T) / (3 * T)   # block coefficient at 0.8 D
K = 0.036                                            # container ships
W_ST_WATSON = K * EN ** 1.36 * (1 + 0.5 * (CB_PRIME - 0.70))
# Chapman: uses only L, B and D
W_ST_CHAPMAN = 0.0209 * L ** 1.759 * B ** 0.712 * D ** 0.374

# ---- 2. outfit and machinery -----------------------------------------------
W_OT = 0.36 * L * B                                  # K_OT = 0.36 t/m2, container ships
W_M = 12 * (MCR / RPM) ** 0.84 + 0.69 * MCR ** 0.70  # Watson machinery, MCR in kW

# ---- 3. light ship = (steel + outfit + machinery) * (1 + reserve) ----------
RESERVE = 0.02
WLS_WATSON = (W_ST_WATSON + W_OT + W_M) * (1 + RESERVE)
WLS_CHAPMAN = (W_ST_CHAPMAN + W_OT + W_M) * (1 + RESERVE)

# ---- 4. the appendix regression, for comparison (Fig. A.36) ----------------
WLS_A36 = 0.973087 * DWT ** 0.91242

print("TEXTBOOK, light ship")
print(f"  steel   Watson {W_ST_WATSON:7.0f} t    Chapman {W_ST_CHAPMAN:7.0f} t")
print(f"  outfit  {W_OT:7.0f} t     machinery {W_M:7.0f} t")
print(f"  light ship  Watson {WLS_WATSON:6.0f} t  ({(WLS_WATSON - WLS_A36) / WLS_A36 * 100:+.1f} % vs A.36)")
print(f"  light ship  Chapman {WLS_CHAPMAN:5.0f} t  ({(WLS_CHAPMAN - WLS_A36) / WLS_A36 * 100:+.1f} % vs A.36)")
print(f"  Appendix A.36 regression {WLS_A36:.0f} t")
print()

# ---- 5. vertical centre of gravity KG, by groups ---------------------------
# DS = depth raised for the superstructure volume (the deckhouse spread over L * B)
DS = D + (DH_L * DH_H * B) / (L * B)
KG_ST = 0.59 * DS       # steel, mid-band of Table 2.19 (55 to 63 % of DS)
KG_OT = 0.955 * DS      # outfit (86 to 105 %)
KG_M = 0.41 * DS        # machinery (29 to 53 %)
# with Watson steel
GROUPS_W = W_ST_WATSON + W_OT + W_M
KG_W = (W_ST_WATSON * KG_ST + W_OT * KG_OT + W_M * KG_M) / GROUPS_W
KG_W = (GROUPS_W * KG_W + RESERVE * GROUPS_W * 1.2 * KG_W) / (GROUPS_W * (1 + RESERVE))   # reserve at 1.2 KG
# with Chapman steel
GROUPS_C = W_ST_CHAPMAN + W_OT + W_M
KG_C = (W_ST_CHAPMAN * KG_ST + W_OT * KG_OT + W_M * KG_M) / GROUPS_C
KG_C = (GROUPS_C * KG_C + RESERVE * GROUPS_C * 1.2 * KG_C) / (GROUPS_C * (1 + RESERVE))   # reserve at 1.2 KG
print("TEXTBOOK, centre of gravity")
print(f"  DS = {DS:.2f} m    KG  Watson {KG_W:.2f} m    Chapman {KG_C:.2f} m")
print("  (the textbook route gives no longitudinal centre of gravity)")
print()

# ============================================================================
# METHOD 2: THE PAPER
# ============================================================================

# ---- 6. direct regressions for the light ship (R2 in brackets) -------------
WLS_42 = 0.106819 * DWT + 0.0585666 * LBH + 78.816 * V     # eq. (42)  (0.9886) needs DWT, LBH, V
WLS_26 = 4.0726 * TEU + 1150.9                             # eq. (26)  (0.8874) needs TEU
WLS_25 = 3.321 * DWT ** 0.7711                             # eq. (25)  (0.9110) needs DWT
WLS_27 = 0.1022 * LBH + 1216.9                             # eq. (27)  (0.9197) needs L*B*H

# ---- 7. eight weight classes, M = C * P (eqs 34 to 41) ---------------------
LB = L * B
C1 = 0.0913757 * DWT ** 0.1 - 0.00304364 * math.log(TEU) ** 2
C2 = -1.17147e7 * DWT ** -2 + 259.94 * TEU ** -0.9 - 3.60709e9 * LB ** -3
C3 = -0.241143 * math.log(DWT) ** 2 + 0.891088 * TEU ** -0.1 * LBH ** 0.4
C4 = 761505 * V ** -6 - 1.22616e6 * MCR ** -2 + 0.000588802 * V ** 5 * MCR ** -1.1
C5 = 0.00671665 * TEU ** (1 / 8) - 0.0000422513 * DWT ** 0.55
C6 = 1.30598e9 * J ** -8 + 0.000355803 * J ** 2.6 * NE ** -0.5
C7 = -33711.5 * LBH ** -1.8 + 0.229357 * DWT ** -0.6
C8 = 0.0614659 * LBH ** -0.5 - 1.89401e15 * TEU ** -7 + 0.0000307182 * LBH ** 4 * TEU ** -6
M1 = C1 * LBH      # hull, superstructure
M2 = C2 * LB       # deck equipment
M3 = C3 * J        # accommodation
M4 = C4 * MCR      # machinery
M5 = C5 * LBH      # piping systems
M6 = C6 * NE       # electric equipment
M7 = C7 * LBH      # special equipment
M8 = C8 * LBH      # inventories
WLS_CLASSES = M1 + M2 + M3 + M4 + M5 + M6 + M7 + M8

print("PAPER, light ship")
print(f"  eq. (42) {WLS_42:6.0f} t  ({(WLS_42 - WLS_A36) / WLS_A36 * 100:+.1f} % vs A.36)   <- the one to carry")
print(f"  eq. (26) {WLS_26:6.0f} t  ({(WLS_26 - WLS_A36) / WLS_A36 * 100:+.1f} %)")
print(f"  eq. (25) {WLS_25:6.0f} t  ({(WLS_25 - WLS_A36) / WLS_A36 * 100:+.1f} %)")
print(f"  eq. (27) {WLS_27:6.0f} t  ({(WLS_27 - WLS_A36) / WLS_A36 * 100:+.1f} %)")
print(f"  eight classes {WLS_CLASSES:.0f} t  ({(WLS_CLASSES - WLS_A36) / WLS_A36 * 100:+.1f} %)   needs MCR, NE and J")
print(f"    M1 {M1:.0f}  M2 {M2:.0f}  M3 {M3:.0f}  M4 {M4:.0f}  M5 {M5:.0f}  M6 {M6:.0f}  M7 {M7:.0f}  M8 {M8:.0f}")
print()

# ---- 8. centre of gravity: z is measured from the keel, x from the aft perpendicular
Z_44 = 4.18089 + 0.0000242958 * LBH + 0.253695 * V                              # eq. (44)
X_43 = 0.197216 * L ** 1.15 - 0.0000244495 * MCR ** 1.3 + 0.0000866675 * DWT ** 1.1   # eq. (43), needs MCR
X_30 = 1.3668 * LBH ** 0.3567                                                    # eq. (30)
print("PAPER, centre of gravity")
print(f"  vertical   z (44) = {Z_44:.2f} m")
print(f"  longitudinal  x (43) = {X_43:.1f} m   x (30) = {X_30:.1f} m   (from the aft perpendicular)")
print()

# ---- 9. how to read it -----------------------------------------------------
# Quote a band, not a single number. With no measured light ship for Baseline A this
# is agreement between estimates, not proof. Check every input against the range of
# the regressions (the paper's Table 3) before you trust a result: TEU 420 to 3,100,
# DWT 6,300 to 45,000 t, L 113.7 to 210.2 m, B 15.5 to 32.25 m, D 9.0 to 18.7 m,
# V 13.0 to 22.3 kn. Change the inputs at the top and run again.
