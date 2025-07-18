from Simulation_Config import *
import random
import math

# Define scenarios and their time windows
# These time points correspond to the original logic in your provided functions
SCENARIO_NORMAL_DRIVING = "normal_driving"
SCENARIO_FATIGUE_LIKE_DRIVING = "fatigue_like_driving"
SCENARIO_POST_FATIGUE_DRIVING = "post_fatigue_driving" # Or 'recovery' or 'different_style'

# Define the time boundaries for each scenario
# These are the direct translations from your original if/elif/else blocks
SCENARIO_BOUNDARIES = [
    (0, 50, SCENARIO_NORMAL_DRIVING),
    (50, 120, SCENARIO_FATIGUE_LIKE_DRIVING),
    (120, float('inf'), SCENARIO_POST_FATIGUE_DRIVING) # From 120s onwards
]

def _get_current_scenario(current_sim_time):
    """
    Determines the current driving scenario based on simulation time.
    This logic is now centralized here.
    """
    for start_time, end_time, scenario_name in SCENARIO_BOUNDARIES:
        if start_time <= current_sim_time < end_time:
            return scenario_name
    return SCENARIO_NORMAL_DRIVING # Fallback, should not be reached with float('inf')


def generate_simulated_vsa_lon_g(current_sim_time):
    """
    Generates a simulated VSA_LON_G value based on the current simulation time's scenario.
    Range for VSA_LON_G: [-24.5|24.452148949] m/s^2.
    Simulates longitudinal acceleration/deceleration.
    """
    scenario = _get_current_scenario(current_sim_time)
    
    if scenario == SCENARIO_NORMAL_DRIVING:
        # Normal, alert driving (consistent acceleration/deceleration)
        sim_value = random.uniform(-0.5, 0.5) # m/s^2
    elif scenario == SCENARIO_FATIGUE_LIKE_DRIVING:
        # Fatigue-like driving (more inconsistent, jerky acceleration/deceleration)
        sim_value = random.uniform(-1.0, 1.0) # m/s^2
    else: # SCENARIO_POST_FATIGUE_DRIVING
        # Returning to more normal
        sim_value = random.uniform(-0.7, 0.7) # m/s^2

    # Clamp to reasonable driving range, not full DBC range
    return max(-2.0, min(sim_value, 2.0))


def generate_simulated_str_angle(current_sim_time):
    """
    Generates a simulated STR_ANGLE value based on the current simulation time's scenario.
    The STR_ANGLE range is [-3276.8|3276.7] degrees.
    Simulated values will be within a typical driving range (e.g., +/- 45 degrees from center).
    """
    scenario = _get_current_scenario(current_sim_time)

    if scenario == SCENARIO_NORMAL_DRIVING:
        # Starts somewhat stable (normal, alert driving - small corrections)
        sim_angle = random.uniform(-2.0, 2.0)
    elif scenario == SCENARIO_FATIGUE_LIKE_DRIVING:
        # Introduce more variability (fatigue-like steering - larger, more frequent corrections)
        sim_angle = random.uniform(-10.0, 10.0)
    else: # SCENARIO_POST_FATIGUE_DRIVING
        # Return to more normal, but still some variability (recovery or different driving style)
        sim_angle = random.uniform(-5.0, 5.0)

    # Ensure simulated angle is within a reasonable sub-range for lane-keeping
    return max(-45.0, min(sim_angle, 45.0))


def generate_simulated_vsa_lat_g(current_sim_time):
    """
    Generates a simulated VSA_LAT_G value based on the current simulation time's scenario.
    Range for VSA_LAT_G: [-24.5|24.452148949] m/s^2.
    Simulates lateral acceleration (side-to-side movement).
    """
    scenario = _get_current_scenario(current_sim_time)

    if scenario == SCENARIO_NORMAL_DRIVING:
        # Normal, alert driving (smooth lane keeping)
        sim_value = random.uniform(-0.3, 0.3) # m/s^2
    elif scenario == SCENARIO_FATIGUE_LIKE_DRIVING:
        # Fatigue-like driving (more side-to-side movement, weaving)
        sim_value = random.uniform(-1.5, 1.5) # m/s^2
    else: # SCENARIO_POST_FATIGUE_DRIVING
        # Returning to more normal
        sim_value = random.uniform(-0.8, 0.8) # m/s^2
    
    # Clamp to reasonable driving range
    return max(-1.5, min(sim_value, 1.5))


def generate_simulated_vsa_yaw_1(current_sim_time):
    """
    Generates a simulated VSA_YAW_1 value based on the current simulation time's scenario.
    Range for VSA_YAW_1: [-125|124.75585938] deg/s.
    Simulates yaw rate (vehicle's rotation around its vertical axis).
    """
    scenario = _get_current_scenario(current_sim_time)

    if scenario == SCENARIO_NORMAL_DRIVING:
        # Normal, alert driving (smooth turns, minimal yaw on straight)
        sim_value = random.uniform(-0.5, 0.5) # deg/s
    elif scenario == SCENARIO_FATIGUE_LIKE_DRIVING:
        # Fatigue-like driving (more erratic rotation, weaving)
        sim_value = random.uniform(-2.0, 2.0) # deg/s
    else: # SCENARIO_POST_FATIGUE_DRIVING
        # Returning to more normal
        sim_value = random.uniform(-1.0, 1.0) # deg/s
    
    # Clamp to reasonable driving range
    return max(-5.0, min(sim_value, 5.0))


def generate_simulated_wheel_speeds(current_sim_time):
    """
    Generates simulated wheel speeds based on the current simulation time's scenario.
    Range for VSA_ABS_*_WHEEL_SPEED_255: [0|255] km/h.
    """
    scenario = _get_current_scenario(current_sim_time)
    
    base_speed = 90.0 # km/h, simulating highway speed

    fl, fr, rl, rr = base_speed, base_speed, base_speed, base_speed # Start with all equal

    if scenario == SCENARIO_NORMAL_DRIVING:
        # Small variations for normal driving
        fl += random.uniform(-1.0, 1.0)
        fr += random.uniform(-1.0, 1.0)
        rl += random.uniform(-1.0, 1.0)
        rr += random.uniform(-1.0, 1.0)
    elif scenario == SCENARIO_FATIGUE_LIKE_DRIVING:
        # Speeds might vary slightly, but we'll focus on the other signals for fatigue
        fl += random.uniform(-5.0, 5.0)
        fr += random.uniform(-5.0, 5.0)
        rl += random.uniform(-5.0, 5.0)
        rr += random.uniform(-5.0, 5.0)
    else: # SCENARIO_POST_FATIGUE_DRIVING
        # Return to more normal, but still some variability
        fl += random.uniform(-1.5, 1.5)
        fr += random.uniform(-1.5, 1.5)
        rl += random.uniform(-1.5, 1.5)
        rr += random.uniform(-1.5, 1.5)

    # Ensure speeds are non-negative and within reasonable bounds
    fl = max(0.0, min(fl, 200.0))
    fr = max(0.0, min(fr, 200.0))
    rl = max(0.0, min(rl, 200.0))
    rr = max(0.0, min(rr, 200.0))

    return fl, fr, rl, rr


def generate_simulated_vsa_maeps_myu_value(current_sim_time):
    """
    Generates a simulated VSA_MAEPS_MYU_VALUE (estimated road friction coefficient).
    Range: [-1.28|1.2799609375]. Typical values are 0.0 to 1.0+.
    Simulates varying road conditions.
    """
    if current_sim_time < 60:
        # Normal dry road conditions
        return random.uniform(0.7, 0.9)
    elif current_sim_time < 110:
        # Simulate a patch of low friction (e.g., wet road, black ice)
        return random.uniform(0.2, 0.4)
    else:
        # Return to somewhat normal or slightly reduced friction
        return random.uniform(0.5, 0.7)
    
# --- Main functions for Braking System Health Monitoring ---

def generate_simulated_meter_sw_status_brake_fluid(current_sim_time):
    """
    SG_ METER_SW_STATUS_BRAKE_FLUID: 0=Normal, 1=Low
    Simulates low brake fluid after a certain time.
    """
    if current_sim_time > 70 and current_sim_time < 150:
        return 1 # Simulate low brake fluid
    return 0 # Normal

def generate_simulated_eng_sw_status_brake_no(current_sim_time):
    """
    SG_ ENG_SW_STATUS_BRAKE_NO: 0=Brake NOT pressed, 1=Brake pressed
    Simulates driver pressing and releasing the brake pedal.
    """
    # Simulate short brake presses
    if (current_sim_time % 10 >= 2 and current_sim_time % 10 < 4) or \
       (current_sim_time % 10 >= 7 and current_sim_time % 10 < 8):
        return 1 # Brake pressed
    return 0 # Brake not pressed

def generate_simulated_vsa_master_cylinder_pressure(current_sim_time, brake_pedal_pressed):
    """
    SG_ VSA_MASTER_CYLINDER_PRESSURE: kPa
    Simulates master cylinder pressure based on pedal input and introduces faults.
    """
    if current_sim_time > 100 and current_sim_time < 130:
        # Simulate a pressure sensor fault (stuck at low value)
        return random.uniform(50, 150) # Very low pressure despite pedal
    
    if brake_pedal_pressed:
        # Normal braking pressure
        return random.uniform(5000, 15000) # kPa
    else:
        # No braking pressure, but allow for some residual/noise
        return random.uniform(0, 50) # kPa

def generate_simulated_vsa_warn_status_brake(current_sim_time):
    """
    SG_ VSA_WARN_STATUS_BRAKE: 0=Normal, 1=Warning
    Simulates general brake system warning.
    """
    if current_sim_time > 70 and current_sim_time < 170: # Active during fluid low, MC fault, etc.
        return 1
    return 0



def generate_simulated_vsa_warn_status_abs(current_sim_time):
    """
    SG_ VSA_WARN_STATUS_ABS: 0=Normal, 1=Warning
    Simulates ABS (Anti-lock Brake System) warning.
    """
    if current_sim_time > 100 and current_sim_time < 170: # Active during MC fault, etc.
        return 1
    return 0


def generate_simulated_vsa_warn_status_puncture(current_sim_time):
    """
    SG_ VSA_WARN_STATUS_PUNCTURE: 0=Normal, 1=Puncture Warning
    Simulates a tire puncture warning.
    """
    if current_sim_time > 80 and current_sim_time < 100:
        return 1 # Simulate a puncture
    return 0
