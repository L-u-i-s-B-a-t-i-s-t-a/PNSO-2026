# Holtrop-Mennen (1982): a very basic version, to read, run and change.
# One ship, one speed, calm water. Single screw. Units: m, kN, kW, knots.
# Not included: sea margin, design margin, service margin, air and wind drag.
# Change the constants in the first block and run the file.

from math import sqrt, exp, log10, cos

# ---- INPUTS: the ship of the paper's worked example -----------------------
L = 205.0        # length on the waterline, m
B = 32.0         # beam, m
T = 10.0         # draught, m
VOL = 37500.0    # displaced volume, m3
LCB = -0.75      # centre of buoyancy, % of L from midship (+ forward)
CM = 0.98        # midship section coefficient
CWP = 0.75       # waterplane coefficient
ABT = 20.0       # bulb section area at the stem, m2 (0 = no bulb)
HB = 4.0         # height of the bulb centre above the keel, m
AT = 16.0        # immersed transom area at rest, m2 (0 = no transom)
SAPP = 50.0      # wetted area of the appendages, m2
K2 = 1.5         # appendage form factor (1 + k2)
CSTERN = 10.0    # afterbody shape (10 = U-shaped sections)
DP = 8.0         # propeller diameter, m
AE = 0.7393      # propeller blade area ratio AE/A0
V_KN = 25.0      # speed, knots

# ---- CONSTANTS -------------------------------------------------------------
RHO = 1025.0     # sea water density, kg/m3
G = 9.81         # gravity, m/s2
NU = 1.1883e-6   # kinematic viscosity, m2/s (sea water, 15 C)

# ---- 1. speed and form numbers ---------------------------------------------
V = V_KN * 0.514444                 # speed, m/s
FN = V / sqrt(G * L)                # Froude number
CB = VOL / (L * B * T)              # block coefficient
CP = CB / CM                        # prismatic coefficient
Q = 0.5 * RHO * V * V               # dynamic pressure, N/m2

# ---- 2. wetted surface and friction ----------------------------------------
S = L * (2 * T + B) * sqrt(CM) * (0.453 + 0.4425 * CB - 0.2862 * CM
    - 0.003467 * B / T + 0.3696 * CWP) + 2.38 * ABT / CB
RN = V * L / NU                                  # Reynolds number
CF = 0.075 / (log10(RN) - 2) ** 2                # ITTC-1957 friction line
RF = Q * S * CF                                  # hull friction, N

# ---- 3. form factor (1 + k1) ------------------------------------------------
LR = L * (1 - CP + 0.06 * CP * LCB / (4 * CP - 1))    # length of run
C12 = (T / L) ** 0.2228446                            # valid for T/L > 0.05 ...
if T / L <= 0.05:
    C12 = 48.20 * (T / L - 0.02) ** 2.078 + 0.479948  # ... and 0.02 < T/L <= 0.05
C13 = 1 + 0.003 * CSTERN
K1 = C13 * (0.93 + C12 * (B / LR) ** 0.92497 * (0.95 - CP) ** -0.521448
            * (1 - CP + 0.0225 * LCB) ** 0.6906)

# ---- 4. appendages ----------------------------------------------------------
RAPP = Q * SAPP * K2 * CF

# ---- 5. wave resistance -----------------------------------------------------
C7 = B / L                                       # valid for 0.11 < B/L < 0.25
IE = 1 + 89 * exp(-(L / B) ** 0.80856 * (1 - CWP) ** 0.30484
     * (1 - CP - 0.0225 * LCB) ** 0.6367 * (LR / B) ** 0.34574
     * (100 * VOL / L ** 3) ** 0.16302)          # half angle of entrance, degrees
C1 = 2223105 * C7 ** 3.78613 * (T / B) ** 1.07961 * (90 - IE) ** -1.37565
C3 = 0.56 * ABT ** 1.5 / (B * T * (0.31 * sqrt(ABT) + T - HB))   # bulb
C2 = exp(-1.89 * sqrt(C3))                                       # bulb effect
C5 = 1 - 0.8 * AT / (B * T * CM)                                 # transom effect
LAM = 1.446 * CP - 0.03 * L / B                                  # for L/B < 12
C16 = 8.07981 * CP - 13.8673 * CP ** 2 + 6.984388 * CP ** 3      # for CP < 0.8
M1 = 0.0140407 * L / T - 1.75254 * VOL ** (1 / 3) / L - 4.79323 * B / L - C16
C15 = -1.69385                                                   # for L^3/VOL < 512
if L ** 3 / VOL >= 512:
    C15 = -1.69385 + (L / VOL ** (1 / 3) - 8) / 2.36             # for L^3/VOL < 1727
M2 = C15 * CP ** 2 * exp(-0.1 / FN ** 2)
RW = C1 * C2 * C5 * VOL * RHO * G * exp(M1 * FN ** -0.9 + M2 * cos(LAM / FN ** 2))

# ---- 6. bulb and transom pressure resistance --------------------------------
PB = 0.56 * sqrt(ABT) / (T - 1.5 * HB)
FNI = V / sqrt(G * (T - HB - 0.25 * sqrt(ABT)) + 0.15 * V * V)
RB = 0.11 * exp(-3 * PB ** -2) * FNI ** 3 * ABT ** 1.5 * RHO * G / (1 + FNI ** 2)
FNT = V / sqrt(2 * G * AT / (B + B * CWP))
RTR = Q * AT * 0.2 * (1 - 0.2 * FNT)
if FNT >= 5:
    RTR = 0.0

# ---- 7. correlation allowance ------------------------------------------------
C4 = 0.04                                         # T/L is above 0.04 here
if T / L < 0.04:
    C4 = T / L
CA = 0.006 * (L + 100) ** -0.16 - 0.00205 + 0.003 * sqrt(L / 7.5) * CB ** 4 * C2 * (0.04 - C4)
RA = Q * S * CA

# ---- 8. total resistance and effective power ----------------------------------
RT = RF * K1 + RAPP + RW + RB + RTR + RA          # N
PE = RT * V                                       # W

# ---- 9. results ---------------------------------------------------------------
print("Speed", V_KN, "kn   Froude number", round(FN, 3))
print("Wetted surface S      ", round(S, 1), "m2")
print("Friction RF (1 + k1)  ", round(RF * K1 / 1000, 1), "kN")
print("Appendages RAPP       ", round(RAPP / 1000, 1), "kN")
print("Waves RW              ", round(RW / 1000, 1), "kN")
print("Bulb RB               ", round(RB / 1000, 2), "kN")
print("Transom RTR           ", round(RTR / 1000, 2), "kN")
print("Correlation RA        ", round(RA / 1000, 1), "kN")
print("Total RT              ", round(RT / 1000, 1), "kN")
print("Effective power PE    ", round(PE / 1000), "kW")
# Expected for the paper's ship at 25 kn: RT about 1792 kN, PE about 23047 kW.
