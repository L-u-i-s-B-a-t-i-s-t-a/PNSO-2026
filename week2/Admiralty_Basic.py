# Admiralty coefficient: a very basic version, to read, run and change.
# One parent ship (known displacement, speed, power) and one new case.
# Units: tonnes, knots, kW. Valid only where C_T stays about the same
# (similar Froude number, no hump between the two speeds, similar hull form).

# ---- INPUTS: the parent ship -----------------------------------------------
DELTA0 = 13200.7   # parent displacement, t
V0 = 14.0          # parent speed, knots
P0 = 3500.0        # parent power, kW (same definition of power for both ships)

# ---- INPUTS: the new case --------------------------------------------------
DELTA1 = 13200.7 * 1.05   # new displacement, t (here: sister ship 5 % heavier)
V1 = 14.5                 # new speed, knots
P_AVAILABLE = 3500.0      # power available, kW, for the speed question

# ---- 1. the Admiralty coefficient of the parent ----------------------------
C = DELTA0 ** (2 / 3) * V0 ** 3 / P0          # C = Delta^(2/3) V^3 / P
print(f"Admiralty coefficient of the parent: C = {C:.1f}")

# ---- 2. power of the new case ----------------------------------------------
P1 = DELTA1 ** (2 / 3) * V1 ** 3 / C          # P = Delta^(2/3) V^3 / C
print(f"Power at {V1} kn with {DELTA1:.0f} t: {P1:.0f} kW")

# ---- 3. speed on the power available ---------------------------------------
V_NEW = (C * P_AVAILABLE / DELTA1 ** (2 / 3)) ** (1 / 3)   # V = (C P / Delta^(2/3))^(1/3)
print(f"Speed on {P_AVAILABLE:.0f} kW with {DELTA1:.0f} t: {V_NEW:.2f} kn")

# ---- 4. the two laws inside the formula ------------------------------------
print(f"Cube law: speed +10 % -> power x{1.10 ** 3:.2f} (+{(1.10 ** 3 - 1) * 100:.0f} %)")
print(f"Two-thirds law: displacement +10 % -> power x{1.10 ** (2 / 3):.3f} "
      f"(+{(1.10 ** (2 / 3) - 1) * 100:.1f} %) at the same speed")

# ---- 5. a check you must always make ---------------------------------------
# C is constant only if C_T is. Compare with a resistance method
# (Holtrop_Mennen_Basic.py) when the new speed is more than about 1 knot away,
# or when a hump lies between the two speeds. Example from the lectures:
# at 16 kn the formula gives 5,397 kW against 6,476 kW from Holtrop-Mennen:
# 17 % too low, because 16 kn lies on the hump.
