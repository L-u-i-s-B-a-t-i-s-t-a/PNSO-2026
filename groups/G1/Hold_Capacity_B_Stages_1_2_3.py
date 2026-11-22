"""Hold Capacity, Baseline B (Azores Feeder): Stages 1, 2 and 3 in one program.

Ship and Ocean Systems Design 2026. Baseline B version of the three Baseline A programs
(Hold_Capacity_Stage1_Basic, _Stage2_Basic, _Stage3_Displacement_Basic; T. Santos, L. Batista). Same method, same
step names, same rolled-back loop; here it runs top to bottom in ONE file, so the numbers pass from stage to stage by
themselves.

  SIZING 1 ELECTRIC: the battery for the longest leg (containers, energy, installed motor power)   <- a task of its own
  SIZING 2 FUEL: gensets and MGO for the transit to the mainland at 6-7 kn                            <- a task of its own
  STAGE 1  main dimensions from the number of containers (rows, tiers, bays, L, B, D), plus the battery bays
  STAGE 2  count the containers in the real hull (Demo 8): bay by bay, tier by tier
  STAGE 3  close the ship by draught: displacement = light ship + deadweight, then check the hull and the GM
  ROUNDS   if the closed C_B and T are not the ones the hull was made with (MOVED), the hull is made again

HOW THE TWO SIZINGS ENTER THE SHIP (this is what the students must work out, one group member each)
  SIZING 1 gives  DEADWEIGHT: the battery containers (N_BAT x m_BAT)          LIGHT SHIP: motors, converters, shafts
  SIZING 2 gives  DEADWEIGHT: the MGO for the transit                          LIGHT SHIP: gensets (and the tank volume)
  Both depend on the power, the power depends on the displacement, the displacement depends on both: they sit INSIDE
  the draught loop of Stage 3 and are recomputed in every pass (the design spiral). Both are functions below.

RUN IT
  Python 3 and numpy. Needs make_hull and hull_y of Demo 8: put make_hull.py (and KCS_offsets.csv) in the same folder,
  or paste this program in a new cell at the end of the Demo 8 notebook. Change the INPUTS and run.

WHAT IS DIFFERENT FROM BASELINE A (the disclaimer of Baseline A lists these as not covered)
  * The superstructure is FORWARD. The cargo is aft of the bridge, so there is no sight-line rule for the deck tiers.
    What limits the deck tiers is the stability (Stage 3, step 7).
  * No engine room full of engines. The motor room is aft and the swappable battery containers stand on the deck above
    it (battery bays). Their length sets the aft block of the ship.
  * Batteries are deadweight (N_BAT x container mass), cranes are light ship, the plant is electric.
  * The ship is small (130 TEU). The statistics of the manual were made for larger ships: they are printed as a
    comparison only. Rows and tiers are chosen. Each hold is one bay (short holds, a simplification).
CHECK (the defaults, as released): Stage 1 gives 9 bays, L 86.0, B 13.99, D 7.20 m. Round 1 (hull at C_B 0.650, T 4.00 m)
counts 42 containers in the hold and 88 on deck (130) and 16 battery slots. Stage 3 closes at T 3.80 m, C_B 0.650, 3,060 t,
855 kW brake (1,093 kW installed), light ship 1,332 t, deadweight 1,728 t. SIZING 1: 14 battery containers (39 MWh nominal,
27.1 MWh usable for the longest leg). SIZING 2: 2 x 200 kW gensets, 260 kW electric at 7 kn, 7.9 t of MGO for 800 nm.
Round 1 prints MOVED, round 2 counts the same and prints NOT MOVED. The GM check says -0.09 m: the ship as sized does NOT
float upright with 88 containers on deck. That is the result, not a bug.
LIGHT CONDITION (step 8): no cargo, 1,760 t, T 2.45 m, GM +1.6 m (KM rises when the draught falls, so the GM is NOT the
problem), roll period 9 s. The propeller (2.5 m) wants T >= 3.0 m: about 500 t of water ballast low in the ship.
TRY (change one input, run again, compare):
  * w_DH = 2.4  -> B 15.1 m, 10 bays, about 3,290 t, GM about +1.3 m (the beam buys the stability; B/T leaves the Demo 8 range)
  * n_TD = 1    -> the deck cannot carry 130, the ship grows to 14 bays and about 119 m, GM +1.7 m
  * LEG_MAX_NM = 554 and hotel_call = 7.25 (Tiago's rule: one loop plus the transit between swaps) -> 47 containers, 4,656 t
  * s_H, rows, tiers, h_DB, m_BAT, E_BAT, t_per_TEU, k_EM, C_N: which of them moves the GM most?
Every number marked ASSUMED is an assumption of the lecturer, not a source. Say which values you changed.
Not modelled: bulkheads between holds, coaming ends, tank top, girders, cell guides, free surface, wind, the
weather criterion. Their space is inside the 6.55 m of a bay and inside the allowances.
"""
from math import exp, log, floor, ceil, sqrt
import contextlib, io
import numpy as np
trap = getattr(np, 'trapezoid', None) or np.trapz     # numpy 1 and 2
try:
    make_hull, hull_y                      # already defined (Demo 8 notebook)?
except NameError:
    from make_hull import make_hull, hull_y

# ==================================================================================================
# INPUTS: everything the program is given, and where each number comes from
# ==================================================================================================

# ---- A. THE BRIEF and the designer's choices ----------------------------------------------
N_TEU = 130            # containers (TEU): 1,300 t at 10 t per TEU (brief of Tiago Santos)
t_per_TEU = 10.0       # t per container, loaded
s_H = 0.36             # share carried in the hold (choice). A small hull fills its hold badly, so the deck takes more
n_R, n_T = 4, 2        # rows across and tiers in the hold (choice). 4 across gives B about 14 m, inside the Demo 8 range
n_TD = 2               # deck tiers (choice; step 7 checks that they carry the deck containers, Stage 3 checks the GM)
N_BAT = 14             # FIRST guess of the battery containers: only to size the first battery bays. SIZING 1 replaces it
BATT_ROWS, BATT_TIERS = 4, 2   # battery bay: containers across and tiers (ASSUMED)
V = 12.0               # service speed (kn): the upper end of the brief (11-12 kn)
LCB = 0.0              # LCB of the hull, per cent of L from midship (+ forward)

# ---- B. THE ENDS OF THE SHIP (m), from the arrangement ---------------------------------------
L_AP_m, L_MR_min, L_CD_m, L_ACC_m, L_FP_m = 2.0, 10.0, 2.0, 8.0, 2.0
#   aft peak | motor room, minimum (the battery bays may need more) | cofferdam | deckhouse | fore peak with the thruster

# ---- C. REFERENCE VALUES (ASSUMED for an 85 m ship; replace them with your reference ships) --------------
w_DH, h_DB, h_CO, c_HC = 1.85, 1.5, 0.0, 0.49   # wing tank (also the anti-heeling tank), double bottom, coaming, cover margin
t_cover = 0.6          # hatch cover
C_B_assumed = 0.65     # first block coefficient (Katsoulis gives 0.65 for this ship at 12 kn)
T_start = 4.0          # first draught (m), only to start: the loop replaces it
deck_extra_rows = 1    # the deck is one row wider than the hold

# ---- D. TABLES AND STANDARDS (Manual table 2.9.2; standard 20 ft container) -------------------------
g_BC, g_BF = 0.15, 0.08
b_c, h_c, gap, bay = 2.438, 2.591, 0.013, 6.55   # width, height (8 ft 6 in; high cube 2.896), tier gap, bay length

# ---- E. WEIGHTS AND POWER (Manual 6.1 to 6.6; electric plant ASSUMED) -------------------------------
C_N = 426.0            # Admiralty constant, CALIBRATED on the Demo 8 hull at 12 kn (855 kW brake at 3,060 t). It is
                       # NOT independent: replace by your own Holtrop-Mennen (see the option at the end)
C_ST, C_1 = 0.093, 0.25            # Schneekluth steel constant; C_BD constant
K_OT, R_frac = 0.36, 0.02          # outfit (t per m2 of L x B); reserve margin
C_DH = [57, 55, 52, 53, 40]        # deckhouse kp per m3, layers I-IV and wheelhouse
dh_l, dh_layers = 6.0, 5           # deckhouse length (m) and layers (4 decks and the wheelhouse)
k_EM = 0.045           # motors, converters, shafts and propellers, t per installed kW (ASSUMED)
k_GEN = 0.015          # gensets, t per kW of rating (ASSUMED)
w_cranes = 120.0       # two cranes, 2 x 60 t (ASSUMED)
w_stores = 70.0        # crew, provisions, fresh water, lube; the MGO is sized in SIZING 2 (ASSUMED)
KG_stores, KG_crane_above_deck, KG_light_frac = 3.0, 5.0, 0.58   # ASSUMED, for the GM check
prop_D, prop_immersion = 2.5, 1.2   # propeller diameter (m, ASSUMED 0.65 T) and the draught wanted as a multiple of it (ASSUMED)
KG_ballast = 1.0       # m, water ballast in the double bottom (ASSUMED)
GM_min = 0.5           # m, the margin wanted at this level of detail (the real criteria are the IMO ones: not included)
MAX_ROUNDS = 10


# ==================================================================================================
# SIZING 1 (a task of its own): ELECTRIC. The battery for the longest leg between two swaps.
# ==================================================================================================
E_BAT = 2.8            # MWh per 20 ft battery container, nominal (given by the lecturer)
m_BAT = 25.0           # t per battery container (ASSUMED: not confirmed by the supplier)
DoD, ageing = 0.80, 0.90   # depth of discharge and ageing: the container gives E_BAT x 0.80 x 0.90 = 2.0 MWh
LEG_MAX_NM = 214       # longest leg between swaps: Flores - Praia da Vitoria (great circle + 10 %, ASSUMED route)
weather = 1.35         # energy factor for the sizing case (sea 35 % heavier than planned)
hotel_call = 1.45      # MWh for one port call (hotel, crane, thrusters) (ASSUMED)
eta_chain = 0.85       # battery to propeller: inverter, motor, shaft (ASSUMED)
P_hotel_sea = 0.06     # MW of hotel load at sea (ASSUMED)
sea_margin, eng_load = 1.15, 0.90   # installed power = brake power x 1.15 / 0.90

def size_electric(P_brake):
    """EXERCISE 1. From the brake power at V (kW) to the battery and the motors.
    Returns: containers N_BAT, usable MWh the package must hold, installed motor power (kW).
    Policy used: swap at every island call, so the package only has to cover the LONGEST leg. Tiago's rule is
    different: one loop plus the transit between swaps (set LEG_MAX_NM to that distance and hotel_call to its calls)."""
    P_el = P_brake / eta_chain / 1000 + P_hotel_sea        # MW from the battery at V
    e_nm = P_el / V                                         # MWh per nautical mile
    E_leg = LEG_MAX_NM * e_nm * weather + hotel_call        # usable MWh for the longest leg and one call
    n = ceil(E_leg / (E_BAT * DoD * ageing) - 1e-9)
    return n, E_leg, P_brake * sea_margin / eng_load

# ==================================================================================================
# SIZING 2 (a task of its own): FUEL. Gensets and MGO for the transit to the mainland at 6-7 kn.
# ==================================================================================================
V_TR = 7.0             # transit speed (kn): brief says 6-7 kn, through the PTI
TRANSIT_NM = 800       # distance to the mainland and back to the islands (ASSUMED: not in the brief)
n_gen = 2              # gensets: one can fail
GEN_SIZES = [100, 150, 200, 250, 320, 400, 500]   # standard ratings (kW electric)
gen_max_load = 0.85    # the gensets run at no more than 85 % of the rating
SFOC = 0.230           # t of MGO per MWh electric (230 g/kWh, ASSUMED)
fuel_margin, rho_MGO = 1.15, 0.85   # margin on the fuel (ASSUMED); MGO density t/m3

def size_fuel(Delta):
    """EXERCISE 2. From the displacement (t) to the gensets and the fuel of the mainland transit.
    Returns: genset rating (kW), number, electric power at V_TR (kW), fuel (t), tank volume (m3).
    The ship moves at V_TR by the shafts: the power follows the Admiralty law (speed cubed), the energy is
    taken from the gensets (not from the battery). Think about: the return leg, bunkering at the mainland,
    emergency reserve, which of the two gensets can fail."""
    P_tr = Delta ** (2 / 3) * V_TR ** 3 / C_N               # brake kW at the transit speed
    P_el = P_tr / eta_chain + P_hotel_sea * 1000            # electric kW from the gensets
    need = P_el * 1.15 / (n_gen * gen_max_load)             # 15 % margin; every genset shares the load
    P_gen = next(g for g in GEN_SIZES if g >= need)
    fuel = P_el / 1000 * (TRANSIT_NM / V_TR) * SFOC * fuel_margin
    return P_gen, n_gen, P_el, fuel, fuel / rho_MGO * 1.05

# ==================================================================================================
# STAGE 1: MAIN DIMENSIONS FROM THE NUMBER OF CONTAINERS
# ==================================================================================================
k_U = 0.5 * C_B_assumed + 0.4                        # eq. (8): hold utilisation
N_H = round(s_H * N_TEU)                             # 1 split
N_D = N_TEU - N_H

L0 = 113.5 + 0.082 * N_H - 3607.5 / N_H              # 2 the statistics (comparison only for this small ship)
B0 = exp(0.674 - 2.7e-4 * N_H + 0.44 * log(N_H))
D0 = exp(0.249 - 5.36e-6 * N_H + 0.375 * log(N_H))

n_B = ceil(N_H / (n_R * n_T * k_U) - 1e-9)           # 3-4 rows and tiers are chosen; bays: the smallest number that holds N_H
n_BB = ceil(N_BAT / (BATT_ROWS * BATT_TIERS))        # 8 battery bays (they set the aft block)

def L_AP():  return L_AP_m
def L_MR():  return max(L_MR_min, n_BB * bay)        # the battery bays stand on the deck above the motor room
def L_CD():  return L_CD_m
def L_ACC(): return L_ACC_m
def L_FP():  return L_FP_m
def L_AFT(): return L_AP() + L_MR() + L_CD()         # x of the first cargo bay
def length(nb): return L_AFT() + bay * nb + L_ACC() + L_FP()

L = length(n_B)                                      # 5 the dimensions
B = 2 * w_DH + 2 * g_BC + n_R * b_c + g_BF * (n_R - 1)
D = n_T * (h_c + gap) + h_DB + c_HC - h_CO
per_tier = n_B * (n_R + deck_extra_rows)             # 7 deck containers in one tier
ratios = {"L/B": (L / B, 5.5, 7.5), "B/T": (B / T_start, 2.5, 3.5)}   # 6 range of the Demo 8 hull

print("=" * 100)
print("STAGE 1")
print(f"hold {N_H} + deck {N_D} = {N_TEU} TEU.  Statistics (large ships, comparison only): B0 {B0:.1f}, D0 {D0:.1f} m.")
print(f"chosen: rows {n_R}, tiers {n_T}; bays {n_B};  L {L:.1f}  B {B:.2f}  D {D:.2f} m  (aft block {L_AFT():.1f} m)")
for k, (v, lo, hi) in ratios.items():
    print(f"  {k} {v:5.2f}  [{lo}-{hi}]  {'ok' if lo <= v <= hi else 'OUT'}")
print(f"deck: {per_tier} per tier x {n_TD} tiers = {per_tier * n_TD} for {N_D}  {'ok' if per_tier * n_TD >= N_D else 'TOO FEW'}")
print(f"battery: {N_BAT} x {m_BAT:.0f} t, {E_BAT * N_BAT:.0f} MWh nominal, {n_BB} bays of {BATT_ROWS} x {BATT_TIERS} = {n_BB * BATT_ROWS * BATT_TIERS} slots")

# ==================================================================================================
# ROUNDS: hull -> count (Stage 2) -> close by draught (Stage 3) -> compare the hull with the closed ship
# ==================================================================================================
C_B_hull, T_hull = C_B_assumed, T_start              # the first hull is made with the assumed values
for rnd in range(1, MAX_ROUNDS + 1):

    # ============================== STAGE 2: COUNT IN THE REAL HULL ==============================
    L = length(n_B)                                  # L follows the number of bays
    with contextlib.redirect_stdout(io.StringIO()):  # make_hull prints a summary: not needed here
        hull = make_hull(C_B_hull, LCB, L, B, T_hull, D)

    def rows_in_hold(xs, z_bottom, z_top):
        """Rows that fit across one hold: the narrowest section of the bay rules (cell guides are straight)."""
        y = min(min(hull_y(hull, x, z_bottom), hull_y(hull, x, z_top)) for x in xs)
        room = 2 * (y - w_DH) - 2 * g_BC
        return max(0, floor((room + g_BF) / (b_c + g_BF) + 0.01))

    def rows_on_deck(x):
        return floor((2 * (hull_y(hull, x, D) + 0.15) + (2.464 - b_c)) / 2.464 + 0.01)

    hold_t = [0] * n_T                               # containers in each hold tier
    for k in range(n_B):                             # one bay = one hold
        xa, xb = L_AFT() + bay * k + 0.3, L_AFT() + bay * (k + 1) - 0.3
        xs = [xa + (xb - xa) * q / 4 for q in range(5)]
        for t in range(n_T):
            z0 = h_DB + t * (h_c + gap)
            r = min(rows_in_hold(xs, z0, min(z0 + h_c, D)), n_R)
            r = max(0, n_R - 2 * ceil((n_R - r) / 2))    # rows leave in symmetric pairs (4 -> 2 -> 0)
            hold_t[t] += r
    hold = sum(hold_t)

    deck = 0
    for k in range(n_B):
        x0 = L_AFT() + bay * k
        r = min(rows_on_deck(x0 + 0.3), rows_on_deck(x0 + bay - 0.3), n_R + deck_extra_rows)
        deck += r * n_TD
    batt = 0                                         # battery slots in the real deck width, aft
    for k in range(n_BB):
        x0 = L_AP() + bay * k
        batt += min(rows_on_deck(x0 + 0.3), rows_on_deck(x0 + bay - 0.3), BATT_ROWS) * BATT_TIERS

    print("=" * 100)
    print(f"ROUND {rnd}  hull made at C_B {C_B_hull:.4f}, T {T_hull:.3f} m, L {L:.1f} m ({n_B} bays)")
    print(f"STAGE 2  hold {hold} (tiers {hold_t}, k_U real {hold / (n_B * n_R * n_T):.2f}, Stage 1 used {k_U:.2f}),"
          f" deck {deck}, total {hold + deck} for {N_TEU};  battery slots {batt} for {N_BAT}")
    if batt < N_BAT:
        print("  TOO FEW battery slots in the width of the stern: add a battery bay or a tier (BATT_TIERS) and run again")
        break
    if hold + deck < N_TEU:
        n_B += 1
        print(f"  NOT ENOUGH containers: one bay more ({n_B}) and the hull is made again")
        continue
    cap_hold = min(N_TEU, hold)                      # cargo goes to the hold first (the best case for the KG)
    cap_deck = N_TEU - cap_hold

    # ============================== STAGE 3: CLOSE THE SHIP BY DRAUGHT ==============================
    C_B, T = C_B_assumed, T_start
    N_BAT_pass, fuel, P_gen = N_BAT, 8.0, 200      # first values of the two sizings, replaced in every pass
    bridge = 0.22 * L + 0.28 * D ** 1.56 - 0.02 * L ** 0.806 * D ** 1.1     # Manual eq. (15)
    h_layer = (bridge - D) / dh_layers
    N_BAT_prev = -1
    for i in range(50):
        hull_t = 1.030 * C_B * L * B * T                                    # 1 what the hull displaces
        P = hull_t ** (2 / 3) * V ** 3 / C_N                                # 2 brake power (Admiralty)
        C_BD = C_B + C_1 * (D - T) / T * (1 - C_B)                          # 3 light ship
        vol_U = L * B * D * C_BD
        w_steel = (vol_U * C_ST * (1 + 2e-6 * (L - 120) ** 2) * (1 + 0.057 * (L / D - 12)) * sqrt(30 / (D + 14))
                   * (1 + 0.1 * (B / D - 2.1) ** 2) * (1 + 0.2 * (T / D - 0.85)) * (0.92 + (1 - C_BD) ** 2))
        k1 = 1 + 0.02 * (h_layer - 2.6)
        k3 = min(1.0, max(0.95, 0.95 + 0.05 * (L - 100) / 20))
        w_dh = sum(C_DH[:dh_layers]) / 1000 * dh_l * B * h_layer * k1 * k3
        w_outfit = K_OT * L * B
        N_BAT_pass, E_leg, P_inst = size_electric(P)                        # SIZING 1: battery (deadweight), motors (light ship)
        P_gen, n_g, P_el_tr, fuel, V_tank = size_fuel(hull_t)               # SIZING 2: gensets (light ship), MGO (deadweight)
        w_mach = k_EM * P_inst + k_GEN * n_g * P_gen
        groups = w_steel + w_dh + w_outfit + w_mach + w_cranes
        LWT = groups * (1 + R_frac)
        DWT = N_TEU * t_per_TEU + w_stores + N_BAT_pass * m_BAT + fuel      # cargo, stores, batteries, MGO
        weight = LWT + DWT                                                  # 4 the weight and the shortfall
        T_try = B / 2.9                                                     # 5 C_B and T together (Katsoulis, eq. 19)
        for j in range(50):
            C_B_new = 0.8217 * L ** 0.42 * B ** -0.3072 * T_try ** 0.1721 * V ** -0.6135
            T_new = weight / (1.030 * C_B_new * L * B)
            if abs(T_new - T_try) < 0.01:
                break
            T_try = T_new
        moved_T = abs(T_new - T)                                            # 6 compare with the start of this pass
        shortfall = weight - hull_t
        C_B, T = C_B_new, T_new
        if moved_T < 0.01 and N_BAT_pass == N_BAT_prev:
            break
        N_BAT_prev = N_BAT_pass
    else:
        print("STAGE 3  NOT CONVERGED: do not use these numbers")
    Delta = 1.030 * C_B * L * B * T
    print(f"STAGE 3  closed in {i + 1} passes: T {T:.3f} m, C_B {C_B:.4f}, displacement {Delta:.0f} t, brake power {P:.0f} kW "
          f"(installed {P_inst:.0f}), freeboard {D - T:.2f} m")
    print(f"         light ship {LWT:.0f} t (steel {w_steel:.0f}, deckhouse {w_dh:.0f}, outfit {w_outfit:.0f}, "
          f"plant {w_mach:.0f} (motors {k_EM * P_inst:.0f}, gensets {k_GEN * n_g * P_gen:.0f}), cranes {w_cranes:.0f}, reserve {LWT - groups:.0f});"
          f" deadweight {DWT:.0f} t (cargo {N_TEU * t_per_TEU:.0f}, batteries {N_BAT_pass * m_BAT:.0f}, stores {w_stores:.0f}, MGO {fuel:.1f})")
    print(f"         SIZING 1 electric: {N_BAT_pass} containers = {N_BAT_pass * E_BAT:.0f} MWh nominal, the longest leg needs {E_leg:.1f} MWh usable, motors {P_inst:.0f} kW installed")
    print(f"         SIZING 2 fuel: {n_g} x {P_gen} kW gensets, {P_el_tr:.0f} kW electric at {V_TR:.0f} kn, MGO {fuel:.1f} t for {TRANSIT_NM} nm, tank {V_tank:.1f} m3")
    N_BAT = N_BAT_pass

    # ---- step 7 (NEW): first GM check with the hull of this round ----------------------------------
    with contextlib.redirect_stdout(io.StringIO()):
        hull_c = make_hull(C_B, LCB, L, B, T, D)              # the hull at the CLOSED C_B and T
    KM = hull_c["h"]["KM"]
    items = [(LWT - w_cranes * (1 + R_frac) - w_dh * (1 + R_frac), KG_light_frac * D), (w_dh * (1 + R_frac), D + (bridge - D) / 2),
             (w_cranes, D + KG_crane_above_deck), (w_stores + fuel, KG_stores)]
    left = N_BAT
    for t in range(BATT_TIERS):
        n_t = min(left, n_BB * BATT_ROWS); left -= n_t
        items.append((n_t * m_BAT, D + t_cover + (t + 0.5) * (h_c + gap)))
    items_nc = list(items)                                    # everything except the cargo (for step 8)
    left = cap_hold                                           # cargo: hold tiers first (counts of Stage 2), then the deck
    for t in range(n_T):
        n_t = min(left, hold_t[t]); left -= n_t
        items.append((n_t * t_per_TEU, h_DB + (t + 0.5) * (h_c + gap)))
    left = cap_deck
    for t in range(n_TD):
        n_t = min(left, per_tier); left -= n_t
        items.append((n_t * t_per_TEU, D + t_cover + (t + 0.5) * (h_c + gap)))
    W = sum(m for m, _ in items); KG = sum(m * z for m, z in items) / W
    GM = KM - KG
    print(f"         GM check ({cap_hold} in the hold, {cap_deck} on deck, best stowage): KM {KM:.2f}, KG {KG:.2f}, "
          f"GM {GM:.2f} m  {'ok' if GM >= GM_min else 'BELOW ' + str(GM_min) + ' m: more hold, fewer deck tiers, or more beam'}"
          f"  (items sum {W:.0f} t)")


    # ---- step 8 (NEW): the light condition, no cargo, batteries aboard ---------------------------------
    def hydro_at(h, wl):
        """Displacement (t) and KM (m) of the hull at a lower waterline wl: the offsets integrated up to wl."""
        xs_, zs_ = np.linspace(0, L, 61), np.linspace(0, wl, 21)
        Y = np.array([[float(hull_y(h, x, z)) for z in zs_] for x in xs_])
        A = trap(2 * Y, zs_, axis=1)
        V_ = trap(A, xs_)
        KB_ = trap(trap(2 * Y * zs_, zs_, axis=1), xs_) / V_
        return 1.025 * V_, KB_ + trap((2 * Y[:, -1]) ** 3 / 12, xs_) / V_
    W0 = sum(m for m, _ in items_nc); KG0 = sum(m * z for m, z in items_nc) / W0
    T_l = next(t_ for t_ in np.arange(1.0, T, 0.05) if hydro_at(hull_c, t_)[0] >= W0)
    KM_l = hydro_at(hull_c, T_l)[1]
    T_min = prop_immersion * prop_D                           # the draught the propeller wants (trim ignored)
    W_min, KM_min = hydro_at(hull_c, T_min)
    ballast = max(0.0, W_min - W0)
    KG_min = (W0 * KG0 + ballast * KG_ballast) / (W0 + ballast)
    print(f"STEP 8   light condition (no cargo, {W0:.0f} t): T {T_l:.2f} m, GM {KM_l - KG0:+.2f} m, roll period {2 * 3.1416 * 0.4 * B / sqrt(9.81 * (KM_l - KG0)):.1f} s;"
          f" the propeller wants T >= {T_min:.2f} m: ballast {ballast:.0f} t of water low in the ship -> GM {KM_min - KG_min:+.2f} m")
    print(f"         NOT included: trim, wind heel (deck batteries, high freeboard), the crane lift (heel of a 25 t container at 14 m: "
          f"{np.degrees(np.arctan(25 * 14 / ((W0 + ballast) * max(0.05, KM_min - KG_min)))):.1f} deg), free surface, ballast water rules")

    # ---- the check: is the hull still the hull of the closed ship? -----------------------------------
    if ceil(N_BAT / (BATT_ROWS * BATT_TIERS)) != n_BB:
        n_BB = ceil(N_BAT / (BATT_ROWS * BATT_TIERS))
        print(f"BATTERY BAYS CHANGED: {n_BB} bays for {N_BAT} containers. The aft block moves: run the round again.")
        C_B_hull, T_hull = C_B, T
        continue
    if abs(C_B - C_B_hull) > 0.003 or abs(T - T_hull) > 0.05:
        print(f"MOVED: C_B {C_B_hull:.4f} -> {C_B:.4f}, T {T_hull:.3f} -> {T:.3f} m. Make the hull again at the closed values.")
        C_B_hull, T_hull = C_B, T
    else:
        print("NOT MOVED: the hull of Stage 2 is the hull of the closed ship. Done.")
        break
else:
    print("MAX_ROUNDS reached without NOT MOVED: do not use these numbers.")

# ----------------------------------------------------------------------
# OPTION: Holtrop-Mennen instead of Admiralty (not used above). Replace the line  P = ...  in Stage 3 by:
#   CM = 1 - 0.062 * (V * 0.514444 / sqrt(9.81 * L)) ** 0.792
#   r = holtrop_mennen(V, L, B, T, C_B * L * B * T, lcb=LCB, CM=CM, ABT=0.06 * B * T * CM, hB=0.5 * T, AT=0.0,
#                      SAPP=0.015 * L * (2 * T + B) * 0.55, Dp=0.65 * T, AE_A0=0.6)     # single screw script
#   P = r["PE"] / (r["etaH"] * r["etaR"] * 0.60 * 0.98)      # 0.60 open-water efficiency ASSUMED, shaft 0.98
# The script is for ONE screw and the ship has TWO: say which appendages and efficiencies you assumed.
# ----------------------------------------------------------------------
