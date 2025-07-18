# simulation_runner.py

import collections
import time
import numpy as np # For STD calculation

from .vehicle_stability_monitor import VehicleStabilityMonitor
# IMPORTING FROM YOUR PROVIDED Read_Signal.py
import Read_Signal # Changed to import the module directly

from .Threeholds import *
from Simulation_Config import *


# --- Rolling Window Data Storage ---
# Store (value, timestamp) tuples for each signal that needs history
str_angle_window = collections.deque()
vsa_lon_g_window = collections.deque()
vsa_lat_g_window = collections.deque()
vsa_yaw_1_window = collections.deque()
fl_speed_window = collections.deque()
fr_speed_window = collections.deque()
rl_speed_window = collections.deque()
rr_speed_window = collections.deque()
maeps_myu_value_window = collections.deque() # New window for MYU value


# --- Functions for Window Management ---
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
    Runs the vehicle stability detection simulation.
    This function simulates real-time data reception and processing,
    with processing occurring every CAN_SAMPLE_INTERVAL_S.
    """
    print(f"--- Simulating Vehicle Stability Monitoring for {SIMULATION_DURATION_S}s ---")
    print(f"CAN data simulated to arrive every {CAN_SAMPLE_INTERVAL_S}s.")
    print(f"Rolling window duration: {WINDOW_DURATION_S}s.")

    # Print the name of the module providing simulated signals
    print(f"Simulated signals generated from module: {Read_Signal.__name__}\n")

    # Initialize the stability monitor
    stability_monitor = VehicleStabilityMonitor()

    # We will use a simple counter for simulation time, as time.sleep paces the loop
    current_sim_time = 0.0

    while current_sim_time < SIMULATION_DURATION_S:
        # --- Generate simulated CAN signals using YOUR Read_Signal.py functions ---
        # All signals are generated for the current simulation timestamp
        simulated_str_angle = Read_Signal.generate_simulated_str_angle(current_sim_time)
        simulated_vsa_lon_g = Read_Signal.generate_simulated_vsa_lon_g(current_sim_time)
        simulated_vsa_lat_g = Read_Signal.generate_simulated_vsa_lat_g(current_sim_time)
        simulated_vsa_yaw_1 = Read_Signal.generate_simulated_vsa_yaw_1(current_sim_time)
        simulated_fl_speed, simulated_fr_speed, simulated_rl_speed, simulated_rr_speed = Read_Signal.generate_simulated_wheel_speeds(current_sim_time)
        simulated_maeps_myu_value = Read_Signal.generate_simulated_vsa_maeps_myu_value(current_sim_time) # New signal

        # --- Manage rolling windows for all relevant signals ---
        manage_rolling_window(str_angle_window, simulated_str_angle, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(vsa_lon_g_window, simulated_vsa_lon_g, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(vsa_lat_g_window, simulated_vsa_lat_g, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(vsa_yaw_1_window, simulated_vsa_yaw_1, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(fl_speed_window, simulated_fl_speed, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(fr_speed_window, simulated_fr_speed, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(rl_speed_window, simulated_rl_speed, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(rr_speed_window, simulated_rr_speed, current_sim_time, WINDOW_DURATION_S)
        manage_rolling_window(maeps_myu_value_window, simulated_maeps_myu_value, current_sim_time, WINDOW_DURATION_S) # New window

        # --- Calculate Derived Features for Rules ---
        # Average Vehicle Speed
        current_vehicle_speed = (simulated_fl_speed + simulated_fr_speed + simulated_rl_speed + simulated_rr_speed) / 4.0

        # Absolute values for comparison with thresholds
        abs_str_angle = abs(simulated_str_angle)
        abs_yaw_1 = abs(simulated_vsa_yaw_1)
        abs_lat_g = abs(simulated_vsa_lat_g)

        # Max Axle Speed Difference (for skidding/hydroplaning)
        front_axle_diff = abs(simulated_fl_speed - simulated_fr_speed)
        rear_axle_diff = abs(simulated_rl_speed - simulated_rr_speed)
        max_axle_speed_diff = max(front_axle_diff, rear_axle_diff)

        # --- Apply Stability Monitoring Rules ---
        current_alert_level, current_alert_description = stability_monitor.check_stability(
            current_vehicle_speed, abs_str_angle, abs_yaw_1, abs_lat_g, max_axle_speed_diff, simulated_maeps_myu_value
        )

        # --- Print Simulation Status ---
        print(f"Time: {current_sim_time:0.1f}s")
        print(f"  Speed: {current_vehicle_speed:5.1f} km/h | STR_ANGLE: {simulated_str_angle:5.1f} deg | "
              f"YAW_1: {simulated_vsa_yaw_1:5.1f} deg/s | LAT_G: {simulated_vsa_lat_g:5.1f} m/s^2")
        print(f"  Wheel Speeds (FL/FR/RL/RR): {simulated_fl_speed:5.1f}/{simulated_fr_speed:5.1f}/{simulated_rl_speed:5.1f}/{simulated_rr_speed:5.1f} km/h | "
              f"Max Axle Diff: {max_axle_speed_diff:5.1f} km/h")
        print(f"  MYU Value: {simulated_maeps_myu_value:.2f}") # Print MYU value
        print(f"  Alert Level: {current_alert_level} | Description: {current_alert_description}\n")

        # Advance simulation time for the next iteration
        current_sim_time += CAN_SAMPLE_INTERVAL_S
        
        # Pause for the specified interval to simulate real-time data arrival
        time.sleep(CAN_SAMPLE_INTERVAL_S)

    print("\n--- Simulation Ended ---")
