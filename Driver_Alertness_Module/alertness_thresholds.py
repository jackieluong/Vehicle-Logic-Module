# alertness_thresholds.py

# Define thresholds for STR_ANGLE_STD_60s contribution to alertness score
# These are conceptual and need extensive real-world tuning.
# Lower STD means more stable steering, higher means more variable.
# The points added are inverse to alertness (higher points = more fatigue/distraction).
STR_ANGLE_STD_THRESHOLDS = {
    "NORMAL_MAX": 2.5,  # STD up to this is considered normal, 0 points
    "MILD_FATIGUE_START": 2.5, # STD above this adds 1 point
    "MODERATE_FATIGUE_START": 4.0, # STD above this adds 2 points
    "SEVERE_FATIGUE_START": 6.0  # STD above this adds 3 points
}

# Define thresholds for VSA_LON_G_STD_60s contribution (Longitudinal Inconsistency)
VSA_LON_G_STD_THRESHOLDS = {
    "NORMAL_MAX": 0.04, # m/s^2 STD
    "MILD_START": 0.04, # adds 1 point
    "MODERATE_START": 0.08, # adds 2 points
    "SEVERE_START": 0.12 # adds 3 points
}

# Define thresholds for VSA_LAT_G_STD_60s contribution (Lateral Inconsistency / Weaving)
VSA_LAT_G_STD_THRESHOLDS = {
    "NORMAL_MAX": 0.03, # m/s^2 STD
    "MILD_START": 0.03, # adds 1 point
    "MODERATE_START": 0.06, # adds 2 points
    "SEVERE_START": 0.09 # adds 3 points
}

# Define thresholds for VSA_YAW_1_STD_60s contribution (Rotational Inconsistency / Weaving)
VSA_YAW_1_STD_THRESHOLDS = {
    "NORMAL_MAX": 0.10, # deg/s STD
    "MILD_START": 0.10, # adds 1 point
    "MODERATE_START": 0.20, # adds 2 points
    "SEVERE_START": 0.30 # adds 3 points
}
 