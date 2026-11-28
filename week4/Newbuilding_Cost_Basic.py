# Newbuilding cost estimation: a very basic program, to read, run and change.
# Plain steps: no functions, no classes, only numbers, formulas, short loops and print. Run it top to bottom.
#
#   C_ship = C_1 + C_2 + ... + C_9        the direct cost: the sum of the nine groups
#   C_g    = sum of the items of group g  every item has its own formula; LABOUR is one item of each group
#   EXTERNAL ITEMS (lump sums or ratios) and FROM COST TO PRICE are added at the end.
#
# HOW TO USE IT
#   PART 1 holds ALL the inputs, divided by group. Change only PART 1: put the results of your own programs there
#   (dimensions, steel weight, power, capacity) and the equipment you selected. PART 2 and PART 3 need no change.
#   Every input says its unit and where it comes from:
#     [DESIGN]    from your own design programs (dimensions, weights, power, capacity)
#     [EQUIPMENT] from the equipment you selected (engine, pumps, anchors, boats...): catalogues, class rules, suppliers
#     [YARD]      from the shipyard or the market (labour rate, man-hours, steel price)
#     [ASSUMED]   a value of this program: replace it with your own and say where it comes from
# The example is a 1,300 TEU container feeder, 157 m, 11,300 kW two-stroke engine. Its values are an example, not data.
# Costs in euros. The cost formulas do not state the year of their prices: state the year of yours.
# Engine power in bhp (1 kW = 1.341 bhp). Same results as the animation "Newbuilding Cost Estimation".


# #####################################################################################################
# PART 1: THE INPUTS, BY GROUP
# #####################################################################################################

# ---- 0. GENERAL INPUTS (used by several groups) -----------------------------------------------------
FAMILY = "container"            # "container", "bulk" or "tanker": only group 2, deck and cargo, changes
LABOUR_COST = 30.0              # [YARD] EUR per hour per worker
L = 156.9                       # [DESIGN] ship length, m
B = 24.9                        # [DESIGN] beam, m
D = 13.34                       # [DESIGN] depth, m
SPEED = 18.5                    # [DESIGN] service speed, kn
GT = 14000                      # [DESIGN] gross tonnage
CREW = 18                       # [DESIGN] crew members
PASSENGERS = 0                  # [DESIGN] passengers
HOLD_VOLUME = 22000.0           # [DESIGN] cargo holds total volume, m3
CABIN_AREA = 350.0              # [DESIGN] total area of the cabins, m2
ER_LENGTH = 22.0                # [DESIGN] engine room length, m
ER_HEIGHT = 12.0                # [DESIGN] engine room height, m
P_BHP = 15150.0                 # [DESIGN] main engine power rating, bhp (11,300 kW x 1.341)
RPM = 100.0                     # [EQUIPMENT] main engine speed, rpm
STROKES = 2                     # [EQUIPMENT] 2-stroke or 4-stroke main engine

# ---- STEEL WEIGHT W (Watson 1998, Papanikolaou section 2.15, Table 2.24) ----------------------------
W_GIVEN = None                  # [DESIGN] your own steel weight in t (from your weight program); None = Watson
T = 9.42                        # [DESIGN] draught, m
C_B = 0.653                     # [DESIGN] block coefficient at T
K_STEEL = 0.036                 # [DESIGN] Table 2.24: container ships 0.036, bulk carriers 0.031, crude oil tankers 0.032
FC_L, FC_H = 12.0, 2.6          # [DESIGN] forecastle (superstructure) length and height, m
DH_L, DH_H = 16.0, 15.0         # [DESIGN] deckhouse length and height above the deck, m

# ---- 1. STEEL STRUCTURE -----------------------------------------------------------------------------
MH_PER_T = 40.0                 # [YARD] man-hours per tonne of steel
F1 = 0.15                       # [YARD] consumables (welding, gas) as a share of the steel labour cost
WASTE = 0.08                    # [YARD] steel lost in cutting, share of W
STEEL_PRICE = 750.0             # [YARD] EUR per tonne of steel plate and profiles
N_DELIVERIES = 30               # [YARD] voyages to bring the steel to the yard
COST_DELIVERY = 2000.0          # [YARD] EUR per voyage
S_UW, S_AW, S_IN = 5000.0, 3500.0, 30000.0   # [DESIGN] areas to paint: hull under water, above water, inside, m2
T_UW, T_AW, T_IN = 300.0, 250.0, 200.0       # [EQUIPMENT] coating thickness for each area, micron

# ---- 2. DECK AND CARGO HANDLING ----------------------------------------------------------------------
N_ANCHORS, ANCHOR_T = 2, 5.0    # [EQUIPMENT] number of anchors and mass of each, t (class rules: equipment number)
CHAIN_D, CHAIN_LEN = 64.0, 550.0   # [EQUIPMENT] chain diameter, mm, and length, m
CHAIN_GRADE = 2                 # [EQUIPMENT] 1 mild steel, 2 high strength, 3 extra high strength
N_CRANES, CRANE_T, CRANE_REACH = 0, 0.0, 0.0   # [EQUIPMENT] ship cranes: number, capacity t, reach m (0 = gearless)
N_HATCHES, HATCH_L, HATCH_B = 24, 12.7, 10.0   # [DESIGN] hatch covers: number, length m, width m
RUDDER_L, RUDDER_H = 5.0, 8.0   # [DESIGN] rudder chord and height, m
WINDLASS_CHAIN_D = 64.0         # [EQUIPMENT] chain diameter at the windlass, mm
CAPSTAN_T = 10.0                # [EQUIPMENT] capstan traction, t (from 5 t a mooring winch is priced instead)
WINCH_PULL_KN, WINCH_DRUMS = 150.0, 2   # [EQUIPMENT] mooring winch rated pull, kN, and number of drums
TEU_ON_DECK = 800               # [DESIGN] container ships only: TEU on deck (loose lashing gear)
CARGO_DENSITY, PUMP_HEAD, PUMP_EFF, N_CARGO_PUMPS = 0.85, 120.0, 0.75, 3   # [EQUIPMENT] tankers only: t/m3, m, -, number
PIPE_D, PIPE_THK, PIPE_LEN = 0.4, 12.0, 600.0                             # [EQUIPMENT] tankers only: cargo pipe m, mm, m
CARGO_LEN, LARGEST_TANK_A, MONITOR_A = 120.0, 400.0, 600.0                 # [DESIGN] tankers only: m, m2, m2
DECK_LABOUR_FIX = False         # False = the formula of the cost model (see the note in PART 2); True = suggested correction

# ---- 3. PROPULSION -----------------------------------------------------------------------------------
N_ENGINES = 1                   # [EQUIPMENT] main engines
N_CYL = 6                       # [EQUIPMENT] cylinders per engine
BORE = 500.0                    # [EQUIPMENT] cylinder bore, mm
GEAR_T = 0.0                    # [EQUIPMENT] reduction gear mass, t (0 = direct drive)
MCR_KW = 11300.0                # [EQUIPMENT] MCR, kW
SHAFT_LEN = 20.0                # [DESIGN] shaft line length, m
N_PROPELLERS = 1                # [DESIGN] propellers
PITCH = "fixed"                 # [EQUIPMENT] "fixed" or "controllable"
N_ER_FANS, ER_FAN_FLOW = 4, 40000.0   # [EQUIPMENT] engine room fans and the flow of each, m3/h

# ---- 4. AUXILIARY MACHINERY AND SYSTEMS --------------------------------------------------------------
STEAM_T_H = 1.5                 # [EQUIPMENT] steam production, t/h
N_COMPRESSORS, COMPRESSOR_FLOW = 2, 100.0   # [EQUIPMENT] starting air compressors and flow of each, m3/h
N_FUEL_PUMPS, FUEL_PUMP_FLOW = 2, 20.0      # [EQUIPMENT] fuel transfer pumps and capacity of each, m3/h
N_LO_PUR, N_DO_PUR, N_FO_PUR = 2, 1, 2      # [EQUIPMENT] purifiers: lube oil, diesel oil, fuel oil
LO_PUR_FLOW, DO_PUR_FLOW, FO_PUR_FLOW = 2.0, 1.5, 3.0   # [EQUIPMENT] flow of each purifier, m3/h
SELF_CLEANING = True            # [EQUIPMENT] self-cleaning purifiers
FO_VISCOSITY = 1500             # [EQUIPMENT] fuel oil viscosity, Redwood seconds at 100 F
BILGE_PUMP_FLOW, FIRE_PUMP_FLOW = 100.0, 120.0   # [EQUIPMENT] m3/h
PROTECTED_VOLUME = 3000.0       # [DESIGN] volume protected by the fixed firefighting system, m3
BALLAST_PUMP_FLOW = 600.0       # [EQUIPMENT] m3/h
N_BOW_THRUSTERS = 1             # [EQUIPMENT] bow thrusters
LATERAL_AREA = 1800.0           # [DESIGN] lateral (wind) area of the ship, m2
SCRUBBER = "none"               # [EQUIPMENT] "none", "open", "closed" or "hybrid" SOx scrubber

# ---- 5. ELECTRICAL POWER -----------------------------------------------------------------------------
N_DG, DG_CYL, DG_BORE, DG_KW, DG_RPM = 3, 6, 270.0, 900.0, 900.0   # [EQUIPMENT] diesel generators: number (0 = none), cylinders, bore mm, kW, rpm
N_TG, TG_KW = 0, 500.0          # [EQUIPMENT] turbo-generators: number, kW each
N_CLUTCH_G, CLUTCH_G_KW = 0, 500.0   # [EQUIPMENT] generators driven by the main engine through a clutch
N_SHAFT_G, SHAFT_G_KW = 0, 800.0     # [EQUIPMENT] shaft generators
P_INSTALLED_KW = 3000.0         # [DESIGN] electrical power installed, kW

# ---- 6. LIVING SPACES --------------------------------------------------------------------------------
COLD_STORE_M3 = 60.0            # [DESIGN] refrigerated provision stores, m3 (cabin area, crew and passengers: in 0.)

# ---- 7. SANITARY SYSTEM ------------------------------------------------------------------------------
N_FW_GEN, FW_GEN_T_DAY = 1, 25.0   # [EQUIPMENT] fresh water generators and output of each, t/day

# ---- 8. NAVIGATION AND COMMUNICATION -----------------------------------------------------------------
NAV_LEVEL = "medium"            # [EQUIPMENT] "low", "medium" or "high" package

# ---- 9. SAFETY EQUIPMENT -----------------------------------------------------------------------------
#                 number  people each      [EQUIPMENT] boats and liferafts
ROWBOATS =        (0,     0)
OPEN_BOATS =      (1,     6)               # e.g. the rescue boat
SEMI_CLOSED =     (0,     0)
CLOSED_BOATS =    (0,     0)
FIRE_RES_BOATS =  (1,     25)              # e.g. the free-fall lifeboat
LIFERAFTS =       (2,     25)

# ---- EXTERNAL ITEMS: lump sums or ratios (not covered by the nine groups) ----------------------------
# Each item: cost = size x rate; a share of it is labour. Every rate is [ASSUMED], an order of magnitude to start
# with: replace it with a supplier's quote or a reference and say where it comes from. Size 0 = not on the ship.
#                              size    unit of the size          rate    EUR per unit                             labour share
LNG_TANK_M3 =                 (0,     "m3 of LNG tank",         3500,   "EUR/m3, tank + fuel gas supply system", 0.15)
LNG_ENGINE_KW =               (0,     "kW dual-fuel engine",    60,     "EUR/kW extra over a diesel engine",     0.0)
BATTERY_KWH =                 (0,     "kWh installed",          600,    "EUR/kWh, battery system with racks",    0.10)
E_MOTOR_KW =                  (0,     "kW electric propulsion", 250,    "EUR/kW, motor + converter",             0.15)
AZIMUTH_KW =                  (0,     "kW azimuth thrusters",   400,    "EUR/kW",                                0.10)
SHORE_POWER =                 (0,     "lump sum",               1,      "EUR (enter the quote as the size)",     0.0)
CELL_GUIDES_TEU =             (0,     "TEU in the hold",        500,    "EUR/TEU",                               0.30)
OTHER_LUMP_SUMS = {             # [ASSUMED] any other item from a quote: name -> (cost in EUR, labour share)
    # "Reefer plugs and power": (150000, 0.3),
}

# ---- FROM COST TO PRICE: shares of the cost, all [ASSUMED] -------------------------------------------
DESIGN_ENGINEERING = 0.06       # [ASSUMED] design and engineering
CLASS_CERTIFICATION = 0.015     # [ASSUMED] class approval and certificates
YARD_OVERHEADS = 0.15           # [ASSUMED] yard overheads
CONTINGENCY = 0.05              # [ASSUMED] contingency
PROFIT = 0.08                   # [ASSUMED] yard profit

# #####################################################################################################
# PART 2: THE CALCULATION (no change needed)
# #####################################################################################################
people = PASSENGERS + CREW

# ---- steel weight W ----------------------------------------------------------------------------------
EN = L * (B + T) + 0.85 * L * (D - T) + 0.85 * FC_L * FC_H + 0.75 * DH_L * DH_H      # equipment numeral
C_B_08D = C_B + (1 - C_B) * (0.8 * D - T) / (3 * T)                                  # C_B at 0.8 D
W_WATSON = K_STEEL * EN ** 1.36 * (1 + 0.5 * (C_B_08D - 0.70))
W = W_GIVEN if W_GIVEN is not None else W_WATSON

# ---- 1. steel structure ------------------------------------------------------------------------------
steel_bought = W * (1 + WASTE)
s1_labour = W * MH_PER_T * LABOUR_COST                       # man-hours x rate
s1_consumables = F1 * s1_labour
s1_steel = steel_bought * STEEL_PRICE
s1_logistics = 240 * steel_bought + N_DELIVERIES * COST_DELIVERY   # 240 EUR/t is fixed in the cost model
s1_paint = 0.036 * S_UW * T_UW + 0.023 * S_AW * T_AW + 0.018 * S_IN * T_IN
s1_piping_coating = 1.4 * (0.1 * P_BHP + 0.3 * L)
s1_galvanising = 0.075 * s1_paint
s1_anodes = 2.5 * S_UW                                       # cathodic protection
G1_EQUIP = s1_consumables + s1_steel + s1_logistics + s1_paint + s1_piping_coating + s1_galvanising + s1_anodes
G1_LABOUR = s1_labour

# ---- 2. deck and cargo handling ----------------------------------------------------------------------
K_CHAIN = {1: 0.067, 2: 0.074, 3: 0.081}[CHAIN_GRADE]
s2_anchors = 4050 * N_ANCHORS * ANCHOR_T
s2_chains = K_CHAIN * CHAIN_LEN * CHAIN_D ** 2
s2_cranes = 4074 * CRANE_T ** 0.765 * CRANE_REACH ** 0.85 * N_CRANES
s2_ventilation = 21 * (10 * HOLD_VOLUME) ** 0.5
s2_hatches = 98.61 * HATCH_L * HATCH_B ** 1.77 * N_HATCHES
s2_rudder = 66 * RUDDER_H * RUDDER_L ** 2
M_rudder = 0.0045 * 0.12 * RUDDER_H * (RUDDER_H + RUDDER_L) * (SPEED + 0.007 * L ** 2)   # torque index
s2_steering = 6163 * M_rudder ** (2 / 3)
s2_windlass = 300 * WINDLASS_CHAIN_D ** 1.3
if CAPSTAN_T < 5:
    s2_mooring = 3748 * CAPSTAN_T ** 1.6
else:
    s2_mooring = 3500 * WINCH_PULL_KN ** 0.65 * WINCH_DRUMS
s2_family = 0.0
if FAMILY == "container":
    s2_family = 72 * TEU_ON_DECK                                      # loose lashing gear
if FAMILY == "tanker":
    Q = HOLD_VOLUME / 16                                              # cargo discharged in 16 h, m3/h
    P_shaft = CARGO_DENSITY * 9.81 * Q * PUMP_HEAD / (3600 * PUMP_EFF)
    R_foam = max(0.6 * B * CARGO_LEN, 6 * LARGEST_TANK_A, 3 * MONITOR_A, 1250)
    s2_family = (1086 * N_CARGO_PUMPS * P_shaft ** 0.82               # cargo pumps and drivers
                 + 197 * PIPE_D * PIPE_THK * PIPE_LEN * 1.4           # cargo piping
                 + 2300 * (1.25 * Q) ** 0.6                           # inert gas system
                 + 1.3 * (787 * CARGO_LEN + 1552 * (0.06 * R_foam) ** (1 / 3)))   # deck foam
G2_EQUIP = (s2_anchors + s2_chains + s2_cranes + s2_ventilation + s2_hatches + s2_rudder + s2_steering
            + s2_windlass + s2_mooring + s2_family)
deck_hours = (27 * (ANCHOR_T * N_ANCHORS) ** 0.4 + 290 * N_CRANES * CRANE_T ** (1 / 3)
              + 460 * (HATCH_L * HATCH_B) ** 0.3 + 33 * RUDDER_L ** (2 / 3))
# In the cost model 0.2 x (the equipment, in EUR) sits inside the bracket multiplied by the labour rate, so euros
# are counted as hours (about 14 M EUR here). DECK_LABOUR_FIX = True counts them as euros, outside the bracket.
if DECK_LABOUR_FIX:
    G2_LABOUR = LABOUR_COST * deck_hours + 0.2 * G2_EQUIP
else:
    G2_LABOUR = LABOUR_COST * (deck_hours + 0.2 * G2_EQUIP)

# ---- 3. propulsion -----------------------------------------------------------------------------------
if STROKES == 2:
    s3_engine = 4514 * N_CYL ** 0.75 * BORE ** 0.9 * N_ENGINES
else:
    s3_engine = 67 * N_CYL ** 0.85 * BORE ** 2.2 / RPM ** 0.75 * N_ENGINES
s3_coupling = 2748 * P_BHP / RPM
s3_gear = 40413 * GEAR_T ** 0.5
s3_shaft = 0.081 * (MCR_KW / RPM) ** (2 / 3) * SHAFT_LEN * 754
s3_axle = 12.14 * P_BHP ** 0.85
s3_brake = 20530
if PITCH == "fixed":
    s3_propeller = 400 * P_BHP ** 0.7 * N_PROPELLERS
    K1, K2 = 240, 0.004
else:
    s3_propeller = 582 * P_BHP ** 0.7 * N_PROPELLERS
    K1, K2 = 700, 0.44
s3_fans = 12.12 * N_ER_FANS * ER_FAN_FLOW ** 0.5
G3_EQUIP = s3_engine + s3_coupling + s3_gear + s3_shaft + s3_axle + s3_brake + s3_propeller + s3_fans
prop_hours = 10 * P_BHP ** (2 / 3) * N_ENGINES + K1 + K2 * P_BHP * N_PROPELLERS + 420 + 0.47 * L * (B + D)
G3_LABOUR = LABOUR_COST * prop_hours

# ---- 4. auxiliary machinery and systems --------------------------------------------------------------
if FO_VISCOSITY < 500:
    K3v = 1.65
elif FO_VISCOSITY < 1500:
    K3v = 2.2
elif FO_VISCOSITY < 3500:
    K3v = 2.85
else:
    K3v = 4.0
K4v = 1.25 if FO_VISCOSITY > 3500 else 1.0
K5 = 1.0 if SELF_CLEANING else 0.55
K1gt = 1 if GT < 150 else (2 if GT < 4000 else 3)      # pump classes by gross tonnage
K2gt = 0.0 if GT < 1000 else (2.5 if GT < 2000 else 4.0)
K3gt = 0 if GT < 1000 else 1
p_ratio = P_BHP / 2237
s4_cooling = 55000 * p_ratio ** 0.65 + 52500 * p_ratio ** 0.65 + 35000 * p_ratio ** 0.5   # circulating, refrigeration, lube
s4_steam = 11000 * STEAM_T_H ** 0.65
s4_starting = 126 * N_COMPRESSORS * COMPRESSOR_FLOW
s4_fuel_transfer = 71.13 * N_FUEL_PUMPS * FUEL_PUMP_FLOW + 3.4 * P_BHP
s4_purifiers = (16165 * N_LO_PUR * LO_PUR_FLOW * K5 + 7679 * N_DO_PUR * DO_PUR_FLOW * K5
                + 8406 * N_FO_PUR * FO_PUR_FLOW * K3v * K4v * K5)
s4_static_purifiers = 1617 + 0.2 * P_BHP
s4_bilge_separator = 252 * GT ** 0.5
s4_pumps = (970 * K1gt * BILGE_PUMP_FLOW ** (1 / 3) + 1552 * K1gt * FIRE_PUMP_FLOW ** (1 / 3)
            + 1552 * K2gt * FIRE_PUMP_FLOW + 1778 * K3gt * BILGE_PUMP_FLOW)
s4_firefighting = 13.58 * PROTECTED_VOLUME
s4_piping = 73 * ER_LENGTH * ER_HEIGHT * B + 787 * L + 13 * P_BHP + 3 * HOLD_VOLUME + 10 * CABIN_AREA
s4_ballast_treatment = 150000 + 100 * BALLAST_PUMP_FLOW
P_thruster = 3.572 * 0.065 * LATERAL_AREA                  # thruster power from the lateral area
s4_bow_thruster = 1086 * P_thruster ** 0.82 * N_BOW_THRUSTERS
s4_nox = 45 * P_BHP                                        # always charged in the cost model
s4_scrubber = {"none": 0, "open": 150, "closed": 360, "hybrid": 250}[SCRUBBER] * P_BHP
G4_EQUIP = (s4_cooling + s4_steam + s4_starting + s4_fuel_transfer + s4_purifiers + s4_static_purifiers
            + s4_bilge_separator + s4_pumps + s4_firefighting + s4_piping + s4_ballast_treatment
            + s4_bow_thruster + s4_nox + s4_scrubber)
aux_hours = (5.5 * L + 11 * P_BHP ** 0.35 + (230 if STROKES == 2 else 2250) + 0.18 * P_BHP
             + N_COMPRESSORS * (40 + 3.5 * COMPRESSOR_FLOW) + 0.27 * P_BHP
             + (300 + 0.056 * P_BHP) * N_LO_PUR * N_DO_PUR * N_FO_PUR)   # the three purifier counts multiply
G4_LABOUR = LABOUR_COST * aux_hours

# ---- 5. electrical power -----------------------------------------------------------------------------
s5_diesel_gen = 0.0
if N_DG > 0:
    s5_diesel_gen = N_DG * (407 * DG_BORE ** 2.2 * DG_CYL ** 0.8 / DG_RPM + 38797 * (DG_KW / DG_RPM) ** (2 / 3))
s5_turbo_gen = N_TG * 300000 * (TG_KW / 50) ** 0.7
x_clutch = (CLUTCH_G_KW / RPM) ** (2 / 3)
s5_clutch_gen = N_CLUTCH_G * (38797 * x_clutch + 21338 * x_clutch)
s5_shaft_gen = N_SHAFT_G * 38797 * (SHAFT_G_KW / RPM) ** (2 / 3)
s5_installation = 776 * P_INSTALLED_KW ** 0.77
G5_EQUIP = s5_diesel_gen + s5_turbo_gen + s5_clutch_gen + s5_shaft_gen + s5_installation
gen_kw = N_DG * DG_KW + N_TG * TG_KW + N_CLUTCH_G * CLUTCH_G_KW + N_SHAFT_G * SHAFT_G_KW
G5_LABOUR = LABOUR_COST * (4 * CABIN_AREA + 6 * gen_kw)

# ---- 6. living spaces --------------------------------------------------------------------------------
G6_EQUIP = (606 * CABIN_AREA                               # cabins
            + 485 * people + 2910 * COLD_STORE_M3 ** (2 / 3)  # galley and cold stores
            + 388 * CREW                                   # laundry
            + 97 * CABIN_AREA                              # air conditioning
            + 367 * people + 2 * CABIN_AREA                # mechanical ventilation
            + 4372 * people ** 0.48                        # doors and windows
            + 36 * L ** 1.6)                               # stairs
G6_LABOUR = LABOUR_COST * (18 * CABIN_AREA + 115 * CREW)

# ---- 7. sanitary system ------------------------------------------------------------------------------
G7_EQUIP = (2231 * N_FW_GEN * FW_GEN_T_DAY + 1067 * people ** 0.5    # fresh water generators, pressure sets
            + 4268 * people ** 0.4 + 18428 * people ** 0.2)          # sewage treatment, incinerator
G7_LABOUR = LABOUR_COST * (280 + 8 * N_FW_GEN * FW_GEN_T_DAY + 200 + 3.5 * people)

# ---- 8. navigation and communication -----------------------------------------------------------------
nav = {"low": 203561, "medium": 292291, "high": 381021}[NAV_LEVEL]
internal_comm = 800 * PASSENGERS ** 0.85 + {"low": 20000, "medium": 40000, "high": 60000}[NAV_LEVEL]
G8_EQUIP = nav + 0.08 * nav + internal_comm
G8_LABOUR = 0.12 * nav          # the cost model takes this labour as 12 % of the package, not from hours

# ---- 9. safety equipment -----------------------------------------------------------------------------
G9_EQUIP = (1616 * ROWBOATS[0] * ROWBOATS[1] ** (2 / 3) + 3232 * OPEN_BOATS[0] * OPEN_BOATS[1] ** (2 / 3)
            + 3636 * SEMI_CLOSED[0] * SEMI_CLOSED[1] ** (2 / 3) + 4849 * CLOSED_BOATS[0] * CLOSED_BOATS[1] ** (2 / 3)
            + 7274 * FIRE_RES_BOATS[0] * FIRE_RES_BOATS[1] ** (2 / 3) + 1778 * LIFERAFTS[0] * LIFERAFTS[1] ** (1 / 3))
n_boats = ROWBOATS[0] + OPEN_BOATS[0] + SEMI_CLOSED[0] + CLOSED_BOATS[0] + FIRE_RES_BOATS[0]
max_people = max(ROWBOATS[1], OPEN_BOATS[1], SEMI_CLOSED[1], CLOSED_BOATS[1], FIRE_RES_BOATS[1])
G9_EQUIP = G9_EQUIP + 6465 * n_boats * max_people ** (2 / 3) + 4041 + 30 * people   # davits, protective equipment
G9_LABOUR = LABOUR_COST * (300 + 1.5 * people)

# ---- external items: cost = size x rate --------------------------------------------------------------
EXTERNAL = {"LNG fuel system": LNG_TANK_M3, "Dual-fuel engine extra": LNG_ENGINE_KW, "Battery system": BATTERY_KWH,
            "Electric propulsion": E_MOTOR_KW, "Azimuth thrusters": AZIMUTH_KW, "Shore connection": SHORE_POWER,
            "Cell guides": CELL_GUIDES_TEU}
GX_EQUIP = 0.0
GX_LABOUR = 0.0
for name in EXTERNAL:
    size, unit, rate, rate_unit, labour_share = EXTERNAL[name]
    cost = size * rate
    GX_EQUIP = GX_EQUIP + cost * (1 - labour_share)
    GX_LABOUR = GX_LABOUR + cost * labour_share
for name in OTHER_LUMP_SUMS:
    cost, labour_share = OTHER_LUMP_SUMS[name]
    GX_EQUIP = GX_EQUIP + cost * (1 - labour_share)
    GX_LABOUR = GX_LABOUR + cost * labour_share

# #####################################################################################################
# PART 3: THE RESULTS (no change needed)
# #####################################################################################################
print(f"STEEL WEIGHT  EN = {EN:,.0f}, C_B(0.8D) = {C_B_08D:.3f}, Watson W = {W_WATSON:,.0f} t;  W used = {W:,.0f} t")
GROUPS = [("1 Steel structure", G1_EQUIP, G1_LABOUR), ("2 Deck and cargo handling", G2_EQUIP, G2_LABOUR),
          ("3 Propulsion", G3_EQUIP, G3_LABOUR), ("4 Auxiliary machinery", G4_EQUIP, G4_LABOUR),
          ("5 Electrical power", G5_EQUIP, G5_LABOUR), ("6 Living spaces", G6_EQUIP, G6_LABOUR),
          ("7 Sanitary system", G7_EQUIP, G7_LABOUR), ("8 Navigation", G8_EQUIP, G8_LABOUR),
          ("9 Safety equipment", G9_EQUIP, G9_LABOUR)]
print()
print(f"{'GROUP':30s} {'EQUIPMENT':>14s} {'LABOUR':>14s} {'MAN-HOURS':>11s} {'TOTAL':>14s}")
E_sum = 0.0
L_sum = 0.0
for name, e, lab in GROUPS:
    print(f"{name:30s} {e:14,.0f} {lab:14,.0f} {lab / LABOUR_COST:11,.0f} {e + lab:14,.0f}")
    E_sum = E_sum + e
    L_sum = L_sum + lab
DIRECT = E_sum + L_sum
print(f"{'A. DIRECT COST (nine groups)':30s} {E_sum:14,.0f} {L_sum:14,.0f} {L_sum / LABOUR_COST:11,.0f} {DIRECT:14,.0f}")
print(f"{'B. External items':30s} {GX_EQUIP:14,.0f} {GX_LABOUR:14,.0f} {GX_LABOUR / LABOUR_COST:11,.0f} {GX_EQUIP + GX_LABOUR:14,.0f}")
COST = DIRECT + GX_EQUIP + GX_LABOUR
print(f"{'A + B':30s} {'':14s} {'':14s} {'':11s} {COST:14,.0f}")
PRICE = COST * (1 + DESIGN_ENGINEERING + CLASS_CERTIFICATION + YARD_OVERHEADS + CONTINGENCY + PROFIT)
print(f"{'C. PRICE (illustrative)':30s} {'':14s} {'':14s} {'':11s} {PRICE:14,.0f}")
print(f"\nPer tonne of steel: direct cost {DIRECT / W:,.0f} EUR/t.  Labour is {L_sum / DIRECT:.0%} of the direct cost.")
