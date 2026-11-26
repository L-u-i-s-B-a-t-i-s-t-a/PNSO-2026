# Voyage model of Baseline A (the Azores Express): a very basic version, to read, run and change.
# One round voyage a week: Lisbon -> Ponta Delgada -> Praia da Vitoria -> Lisbon.
# Plain steps: no functions, no classes, only numbers, formulas, short loops and print.
#
#   C_RT = OC_d x 7 days + VC + CHC     the cost of one round voyage (a weekly line: the ship's time is the week)
#   VC   = FC + PD + TP + CD + ETS      fuel, port and light dues, tugs and pilotage, canal dues, carbon
#   Tv   = Tn + Tp                      round voyage time: at sea + in port
#
# HOW TO PLUG IT IN: change only sections A to D. Section A takes the results of the programs you already have.
#   value in A        where it comes from                                    the variable there
#   TEU_CAP           Hold_Capacity_Stage2_Basic.py (containers counted)     hold + deck
#   L, B, D           Hold_Capacity_Stage3_Displacement_Basic.py             L, B, D   (L = L_AP + L_ER + L_FP + 6.55 n_B)
#   T, C_B            Stage 3, the values printed after CLOSED               T, C_B
#   LWT, DWT          Stage 3, or Weight_and_CoG_Basic.py                    LWT, DWT
#   V, P_V            Stage 3 (Admiralty), Admiralty_Basic.py or             V, and P_V = the BRAKE power at V, kW
#                     Holtrop_Mennen_Basic.py (PE in W: P_V = PE / 1000 / (eta_D x eta_S) x (1 + sea margin))
#   N_EXP             the slope of log P against log V (video "Logs and slope"); 3 if you have no curve
# WAY 1, simplest: run those programs, read the printed values, type them into section A.
# WAY 2, one notebook: run make_hull.py, Stage 2 and Stage 3 in cells first; then paste this file with
#   section A replaced by these three lines (L, B, D, T, C_B, LWT, DWT and V are already set by Stage 3):
#       TEU_CAP = hold + deck
#       P_V = Delta ** (2 / 3) * V ** 3 / C_N
#       N_EXP = 3.0
#   With the 596 TEU feeder of the Manual (681 TEU counted by Stage 2) the CHECKS print FAIL: too small for this cargo.
#   That is the model working. Change section C to your own route and cargo, or enlarge the ship.
# The asserts stop the program if the values from the different programs do not agree with each other.
# Units: nm, kn, h, t, kW, g/kWh, USD (EUR converted). ASSUMED and ESTIMATE mark values to check.

import math

# ---- A. FROM YOUR OTHER PROGRAMS (here: Baseline A from the Appendix A fits of Weight_and_CoG_Basic.py) ----
TEU_CAP = 1300          # TEU the ship carries, hold + deck
L, B, D = 156.9, 24.91, 13.34     # m
T, C_B = 9.42, 0.653    # m, and block coefficient at T
LWT, DWT = 6365.0, 17333.0        # t, light ship and deadweight
V = 18.5                # kn, the speed at which P_V is known
P_V = 9605.0            # kW, brake power at V, sea margin included (ASSUMED: 85 % of an 11,300 kW engine)
N_EXP = 3.0             # power law P = P_V x (speed / V)^N_EXP: 3 is the cube law

# ---- B. FROM THE BRIEF ----------------------------------------------------------------------
SPEED = 18.5            # kn, the speed you sail (the brief: 18-19 kn)
WEEK = 168.0            # h, one round voyage a week
FUEL = "LNG"            # "LNG" (gas mode) or "OIL" (VLSFO): the ship is dual-fuel
PORTS = ["Lisbon", "Ponta Delgada", "Praia da Vitoria"]

# ---- C. THE OPERATION (ASSUMED: check and change) ------------------------------------------
DIST = [780.0, 92.0, 837.0]       # nm, leg after each port (Lisbon->Ponta Delgada, ->Praia da Vitoria, ->Lisbon)
LOAD = [1000, 460, 260]           # TEU loaded at each port
DISCH = [680, 650, 390]           # TEU discharged at each port
CRANES = [3, 2, 2]                # quay cranes at each port (the ship is gearless)
CRANE_RATE = 25.0                 # moves per hour per crane
TEU_PER_BOX = 1.6                 # mix of 20 ft and 40 ft boxes
T_FIXED = 4.0                     # h per call: pilot, mooring, services, papers
SEA_MARGIN = 1.03                 # 3 % more time at sea for weather
BUFFER = 6.0                      # h kept spare in the week for delays
T_PER_TEU = 12.0                  # t of cargo per loaded TEU
STORES = 300.0                    # t of water, stores, crew and constants
SFOC = 147.0 if FUEL == "LNG" else 170.0    # g/kWh: LNG in gas mode (ASSUMED) or VLSFO
PILOT = 1.0 if FUEL == "LNG" else 0.0       # g/kWh of gas oil as pilot fuel in gas mode (ASSUMED)
AUX = 2.5                         # t of gas oil a day in the generators
TANK_T = 17.0                     # t of LNG in one 40 ft tank container
DAYS_OFF = 10                     # days a year out of service

# ---- D. PRICES AND TARIFFS, NOVEMBER 2026 (date yours) --------------------------------------
FX = 1.0989                       # USD per EUR
OC_DAY = 9031.0                   # USD per working day: OC + PM of a 2026 feeder owner, 8,785 a day over 355 working days
PRICE = 1630.0 if FUEL == "LNG" else 706.0  # USD/t, LNG or VLSFO, Rotterdam
P_MGO = 1191.0                    # USD/t, gas oil
CF = 2.750 if FUEL == "LNG" else 3.151      # t CO2 per t of fuel
CF_MGO = 3.206
EUA = 90.5                        # EUR per t CO2
ETS_SHARE = 0.0                   # mainland <-> Azores: no allowances to surrender until 2030 (emissions still reported)
PD_CALL = [6000, 5500, 5500]      # EUR per call: port and light dues, mooring, agency (ESTIMATE)
TP_CALL = [9000, 6000, 6000]      # EUR per call: pilotage and towage (ESTIMATE)
CHC_BOX = 200.0                   # EUR per box moved (liner terms: the owner pays)

# ---- CHECKS ON THE INPUTS: the program stops if a value cannot be right ---------------------
n = len(PORTS)
assert len(DIST) == n and len(LOAD) == n and len(DISCH) == n and len(CRANES) == n, "one value per port in every list of section C"
assert sum(LOAD) == sum(DISCH), "every TEU loaded must be discharged in the round voyage"
assert FUEL in ("LNG", "OIL"), "FUEL is LNG or OIL"
assert 0 < T < D and 0.5 < C_B < 0.85, "hull values out of range"
DISPL = 1.025 * C_B * L * B * T
assert abs(LWT + DWT - DISPL) / DISPL < 0.05, "LWT + DWT is not the displacement 1.025 C_B L B T: the hull and the weights disagree"

# ---- 1. CARGO: TEU on board on the leg after each port, boxes moved at each call -------------
on_board = []
teu = 0
for i in range(n):
    teu = teu - DISCH[i] + LOAD[i] if i > 0 else LOAD[0]     # the ship leaves Lisbon with what Lisbon loads
    on_board.append(teu)
assert on_board[-1] == DISCH[0], "the cargo does not close: what arrives in Lisbon must be what Lisbon discharges"
boxes = []
for i in range(n):
    boxes.append((LOAD[i] + DISCH[i]) / TEU_PER_BOX)

# ---- 2. TIME: Tv = Tn + Tp ------------------------------------------------------------------
Tn = SEA_MARGIN * sum(DIST) / SPEED                          # h at sea
t_port = []
for i in range(n):
    t_port.append(T_FIXED + boxes[i] / (CRANES[i] * CRANE_RATE))   # h in port at each call
Tp = sum(t_port)
Tv = Tn + Tp

# ---- 3. THE SPEED THE WEEK NEEDS (the design objective: minimum power) ----------------------
V_MIN = SEA_MARGIN * sum(DIST) / (WEEK - Tp - BUFFER)        # kn
P = P_V * (SPEED / V) ** N_EXP                               # kW at the speed you sail
P_MIN = P_V * (V_MIN / V) ** N_EXP                           # kW at the minimum speed

# ---- 4. FUEL: Qf [t] = SFOC [g/kWh] x P [kW] x t [h] / 1,000,000 ----------------------------
Q_main = SFOC * P * Tn / 1e6                                 # t of LNG or VLSFO
Q_gasoil = PILOT * P * Tn / 1e6 + AUX * Tv / 24              # t of gas oil: pilot fuel + generators
FC = Q_main * PRICE + Q_gasoil * P_MGO                       # USD
CO2 = Q_main * CF + Q_gasoil * CF_MGO                        # t
tanks = math.ceil(1.3 * Q_main / TANK_T) if FUEL == "LNG" else 0   # LNG for 1.3 voyages in tank containers (2 TEU each)

# ---- 5. PORTS, CANALS AND CARBON: PD, TP, CD, ETS -------------------------------------------
PD = sum(PD_CALL) * FX
TP = sum(TP_CALL) * FX
CD = 0.0                                                     # no canal on this route
ETS = CO2 * EUA * FX * ETS_SHARE

# ---- 6. CARGO HANDLING AND THE ROUND VOYAGE -------------------------------------------------
CHC = sum(boxes) * CHC_BOX * FX
VC = FC + PD + TP + CD + ETS
C_RT = OC_DAY * WEEK / 24 + VC + CHC
Z = (365 - DAYS_OFF) / (WEEK / 24)                           # round voyages a year

# ---- PRINT ----------------------------------------------------------------------------------
print("BASELINE A: " + " -> ".join(PORTS + [PORTS[0]]) + ", once a week")
print(f"  {sum(DIST):,.0f} nm; most on board {max(on_board)} TEU of {TEU_CAP}; {sum(boxes):,.0f} boxes moved")
print(f"  time   Tn {Tn:.1f} h + Tp {Tp:.1f} h = Tv {Tv:.1f} h; spare in the week {WEEK - Tv:.1f} h")
print(f"  speed  sailing {SPEED:.1f} kn needs {P:,.0f} kW; the week needs only {V_MIN:.1f} kn -> {P_MIN:,.0f} kW")
print(f"  fuel   {Q_main:.1f} t of {FUEL} + {Q_gasoil:.1f} t gas oil; FC {FC:,.0f} USD; CO2 {CO2:.0f} t" + (f"; {tanks} LNG tank containers" if tanks else ""))
print(f"  costs  FC {FC:,.0f} + PD {PD:,.0f} + TP {TP:,.0f} + CD {CD:,.0f} + ETS {ETS:,.0f} = VC {VC:,.0f} USD")
print(f"  C_RT = OC {OC_DAY * WEEK / 24:,.0f} + VC {VC:,.0f} + CHC {CHC:,.0f} = {C_RT:,.0f} USD, {C_RT / sum(LOAD):,.0f} USD per TEU carried")
print()
print("CHECKS")
print("  " + ("OK  " if Tv + BUFFER <= WEEK else "FAIL") + "  the round voyage fits in the week")
print("  " + ("OK  " if max(on_board) + 2 * tanks <= TEU_CAP else "FAIL") + "  the cargo fits in the slots left by the LNG tanks")
print("  " + ("OK  " if max(on_board) * T_PER_TEU + Q_main * 1.3 + Q_gasoil + STORES <= DWT else "FAIL") + "  cargo + fuel + stores fit in the deadweight")
print()
print("FOR THE FINANCIAL MODEL (Lecture 4.2), a year")
print(f"  Z {Z:.1f} round voyages, {sum(LOAD) * Z:,.0f} TEU carried")
print(f"  OC + PM {OC_DAY * WEEK / 24 * Z:,.0f}   VC {VC * Z:,.0f}   CHC {CHC * Z:,.0f} USD;   CO2 {CO2 * Z:,.0f} t")
