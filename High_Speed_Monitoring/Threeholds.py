# simulation_config.py

# --- Simulation Parameters ---
CAN_SAMPLE_INTERVAL_S = 1.0  # Simulate CAN data arriving every 1 second
SIMULATION_DURATION_S = 180  # Total simulation duration in seconds (3 minutes)
WINDOW_DURATION_S = 10     # Rolling window duration for calculating STDs (e.g., 10 seconds)
SHORT_WINDOW_DURATION_S = 2 # Shorter window for rapid oscillation detection

# --- Thresholds for Vehicle Stability Monitoring (Illustrative - need tuning!) ---
HIGH_SPEED_THRESHOLD_KMH = 80  # km/h - System activates above this speed
MIN_STEERING_FOR_TURN_DEG = 5  # degrees - Minimum steering input considered intentional
HIGH_YAW_THRESHOLD_DEGS = 15   # deg/s - Yaw rate indicating rapid rotation/instability
HIGH_LAT_G_THRESHOLD_MS2 = 0.8 # m/s^2 - Lateral G indicating significant side slip/instability
WHEEL_SLIP_THRESHOLD_KMH = 10  # km/h - Difference between wheel speeds indicating slip
SMALL_STEERING_WINDOW_DEG = 3  # degrees - Steering angle considered "straight ahead" or minimal input
SUSTAINED_DURATION_SEC = 0.5   # seconds - For how long a condition must persist (not directly used for instantaneous rules, but conceptually important)

# New threshold for friction coefficient
LOW_FRICTION_THRESHOLD_MYU = 0.3 # Estimated friction coefficient below which grip is considered critically low

# --- Alert Levels (String Constants) ---
ALERT_LEVEL_NONE = "NONE"
ALERT_LEVEL_LOW = "LOW"
ALERT_LEVEL_MODERATE = "MODERATE"
ALERT_LEVEL_HIGH = "HIGH"

# --- Base Alert Descriptions for Vehicle Stability Monitoring ---
VEHICLE_STABILITY_ALERT_BASE_DESCRIPTIONS = {
    ALERT_LEVEL_NONE: "Vehicle stable.",
    ALERT_LEVEL_LOW: "Minor instability detected, monitoring.",
    ALERT_LEVEL_MODERATE: "Significant instability, potential loss of control.",
    ALERT_LEVEL_HIGH: "Critical instability, immediate driver action required!"
}

# --- Detailed Descriptions for Specific Rule Triggers (Format Strings) ---
VEHICLE_STABILITY_DETAIL_DESCRIPTIONS = {
    "HIGH_YAW_LOW_STEERING": "High Yaw ({abs_yaw_1:.1f} deg/s) with Low Steering ({abs_str_angle:.1f} deg).",
    "ASYMMETRIC_WHEEL_SPEEDS": "Asymmetric Wheel Speeds ({max_axle_speed_diff:.1f} km/h difference).",
    "HIGH_LAT_G_LOW_STEERING": "High Lateral G ({abs_lat_g:.1f} m/s^2) with Minimal Steering.",
    "LOW_ROAD_FRICTION": "Low Road Friction ({myu_value:.2f})." # New detail description
}

# --- Combined Alert Descriptions (for simulation_runner output) ---
ALERT_LEVEL_DESCRIPTIONS = {
    ALERT_LEVEL_NONE: "Vehicle stable.",
    ALERT_LEVEL_LOW: "Minor instability detected, monitoring.",
    ALERT_LEVEL_MODERATE: "Significant instability, potential loss of control.",
    ALERT_LEVEL_HIGH: "Critical instability, immediate driver action required!"
}
