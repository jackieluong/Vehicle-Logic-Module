# simulation_runner.py

import collections
import time
import numpy as np # For STD calculatio

from .Driver_Alertness import DriverAlertnessScore, ALERT_LEVEL_DESCRIPTIONS
from Read_Signal import generate_simulated_str_angle, generate_simulated_vsa_lon_g, generate_simulated_vsa_lat_g, generate_simulated_vsa_yaw_1
from Simulation_Config import WINDOW_DURATION_S, CAN_SAMPLE_INTERVAL_S, SIMULATION_DURATION_S


# --- Rolling Window Data Storage ---
# Store (value, timestamp) tuples for each signal
str_angle_window_60s = collections.deque()
vsa_lon_g_window_60s = collections.deque()
vsa_lat_g_window_60s = collections.deque()
vsa_yaw_1_window_60s = collections.deque()

# --- Functions for Feature Calculation and Window Management ---
def manage_rolling_window(deque_obj, value, current_timestamp, window_duration):
    """Adds new data and prunes old data from a deque."""
    deque_obj.append((value, current_timestamp))
    while deque_obj and (current_timestamp - deque_obj[0][1] > window_duration):
        deque_obj.popleft()

def calculate_std(deque_obj):
    """Calculates sample standard deviation from deque values."""
    values = [item[0] for item in deque_obj]
    if len(values) < 2: # Ensure there are at least 2 data points for ddof=1
        return 0.0 # Return 0.0 if not enough data
    return np.std(values, ddof=1)

# --- Encapsulated Simulation Logic ---
def run_simulation():
    """
    Runs the driver alertness detection simulation.
    This function can be called from a main script.
    """
    print(f"--- Simulating Rolling Window for {WINDOW_DURATION_S}s ---")
    print(f"CAN data arriving every {CAN_SAMPLE_INTERVAL_S}s.")

    # Initialize the alertness score manager
    alertness_scorer = DriverAlertnessScore()
    
    start_real_time = time.time()
    next_can_event_time = start_real_time + CAN_SAMPLE_INTERVAL_S # When the first CAN data should be processed

    while True:
        current_real_time = time.time()
        current_sim_time = current_real_time - start_real_time

        # Check if the total simulation duration has passed
        if current_sim_time >= SIMULATION_DURATION_S:
            break # End the simulation
        # Simulate receiving new CAN signals every CAN_SAMPLE_INTERVAL_S
        if current_real_time >= next_can_event_time:
            # Call individual simulation functions for each signal
            simulated_str_angle = generate_simulated_str_angle(current_sim_time)
            simulated_vsa_lon_g = generate_simulated_vsa_lon_g(current_sim_time)
            simulated_vsa_lat_g = generate_simulated_vsa_lat_g(current_sim_time)
            simulated_vsa_yaw_1 = generate_simulated_vsa_yaw_1(current_sim_time)

            # Manage rolling windows for all relevant signals
            manage_rolling_window(str_angle_window_60s, simulated_str_angle, current_sim_time, WINDOW_DURATION_S)
            manage_rolling_window(vsa_lon_g_window_60s, simulated_vsa_lon_g, current_sim_time, WINDOW_DURATION_S)
            manage_rolling_window(vsa_lat_g_window_60s, simulated_vsa_lat_g, current_sim_time, WINDOW_DURATION_S)
            manage_rolling_window(vsa_yaw_1_window_60s, simulated_vsa_yaw_1, current_sim_time, WINDOW_DURATION_S)

            # Calculate STDs for the current windows
            current_str_angle_std_60s = calculate_std(str_angle_window_60s)
            current_lon_g_std_60s = calculate_std(vsa_lon_g_window_60s)
            current_lat_g_std_60s = calculate_std(vsa_lat_g_window_60s)
            current_yaw_1_std_60s = calculate_std(vsa_yaw_1_window_60s)
            
            # Determine number of data points (should be same for all 60s windows)
            num_data_points = len(str_angle_window_60s)

            # Update the alertness score based on all relevant STD features
            alertness_scorer.update_str_angle_std_contribution(current_str_angle_std_60s)
            alertness_scorer.update_vsa_contribution(
                current_lon_g_std_60s,
                current_lat_g_std_60s,
                current_yaw_1_std_60s
            )
            current_alertness_score = alertness_scorer.get_current_score()
            current_alert_level = alertness_scorer.get_alert_level()

            print(f"Time: {current_sim_time:0.1f}s | "
                  f"STR_ANGLE: {simulated_str_angle:5.1f} | "
                  f"LON_G: {simulated_vsa_lon_g:5.1f} | "
                  f"LAT_G: {simulated_vsa_lat_g:5.1f} | "
                  f"YAW_1: {simulated_vsa_yaw_1:5.1f} | "
                  f"Window Size: {num_data_points:2d} pts")
            print(f"  STD_60s: STR_ANGLE={current_str_angle_std_60s:5.2f}, "
                  f"LON_G={current_lon_g_std_60s:5.2f}, "
                  f"LAT_G={current_lat_g_std_60s:5.2f}, "
                  f"YAW_1={current_yaw_1_std_60s:5.2f}")
            print(f"  Alert Score: {current_alertness_score} | "
                  f"Alert Level: {current_alert_level} ({ALERT_LEVEL_DESCRIPTIONS[current_alert_level]})\n")

            next_can_event_time += CAN_SAMPLE_INTERVAL_S

        # Advance simulation time
        time.sleep(CAN_SAMPLE_INTERVAL_S)
        # In a real system, you might `time.sleep(CAN_SAMPLE_INTERVAL_S)` to match real-time
    
    
    time.sleep(5)
    print("\n--- Simulation Ended ---")

