# Brake Fluid
LOW_BRAKE_FLUID_STATUS_FAULT = 1 # Value indicating low brake fluid

# Master Cylinder Pressure
MIN_MASTER_CYLINDER_PRESSURE_ACTIVE_BRAKE_KPA = 1000 # kPa: Min expected pressure when pedal is pressed
MAX_MASTER_CYLINDER_PRESSURE_NO_BRAKE_KPA = 100     # kPa: Max expected pressure when pedal is NOT pressed

# Warning Lights / System Status
WARN_STATUS_ACTIVE = 1 # Value indicating a warning status is active (e.g., for BRAKE, ABS)

# Tire Puncture
PUNCTURE_WARN_ACTIVE = 1 # Value indicating a tire puncture warning is active

# --- Alert Levels (String Constants) ---
ALERT_LEVEL_NONE = "NONE"
ALERT_LEVEL_LOW = "LOW"
ALERT_LEVEL_MODERATE = "MODERATE"
ALERT_LEVEL_HIGH = "HIGH"

# --- Base Alert Descriptions ---
BRAKING_HEALTH_ALERT_BASE_DESCRIPTIONS = {
    ALERT_LEVEL_NONE: "Braking system normal.",
    ALERT_LEVEL_LOW: "Braking system advisory.",
    ALERT_LEVEL_MODERATE: "Braking system warning.",
    ALERT_LEVEL_HIGH: "Braking system critical fault!"
}

# --- Detailed Descriptions for Specific Braking Health Triggers (Strictly Defined Signals) ---
BRAKING_HEALTH_DETAIL_DESCRIPTIONS = {
    "LOW_BRAKE_FLUID": "Low Brake Fluid detected.",
    "MC_PRESSURE_IMPLAUSIBLE_LOW": "Master Cylinder Pressure too low ({mc_pressure:.1f} kPa) with pedal pressed.",
    "MC_PRESSURE_IMPLAUSIBLE_HIGH": "Master Cylinder Pressure too high ({mc_pressure:.1f} kPa) with pedal released.",
    "BRAKE_WARNING_LIGHT": "General Brake Warning Light active.",
    "ABS_WARNING_LIGHT": "ABS Warning Light active.",
    "TIRE_PUNCTURE_WARNING": "Tire Puncture Warning active."
}

# --- Alert Levels for simulation_runner output (for consistency) ---
ALERT_LEVEL_DESCRIPTIONS = {
    ALERT_LEVEL_NONE: "Normal Driving",
    ALERT_LEVEL_LOW: "Mild Advisory",
    ALERT_LEVEL_MODERATE: "Moderate Warning",
    ALERT_LEVEL_HIGH: "Critical Alert"
}
