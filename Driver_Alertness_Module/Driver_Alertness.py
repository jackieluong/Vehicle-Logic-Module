# driver_alertness_scoring.py

from .alertness_thresholds import ( # Import thresholds from the new file
    STR_ANGLE_STD_THRESHOLDS,
    VSA_LON_G_STD_THRESHOLDS,
    VSA_LAT_G_STD_THRESHOLDS,
    VSA_YAW_1_STD_THRESHOLDS
)

class DriverAlertnessScore:
    """
    Manages the driver alertness score based on various input metrics.
    This class will be expanded to include Yaw Rate and other metrics later.
    """

    def __init__(self):
        self._current_alertness_score = 0
        self._str_angle_std_contribution = 0
        self._vsa_lon_g_std_contribution = 0
        self._vsa_lat_g_std_contribution = 0
        self._vsa_yaw_1_std_contribution = 0

    def update_str_angle_std_contribution(self, str_angle_std_60s):
        """
        Updates the score contribution based on STR_ANGLE_STD_60s.
        Higher STD leads to a higher contribution (more points towards fatigue).
        """
        if str_angle_std_60s <= STR_ANGLE_STD_THRESHOLDS["NORMAL_MAX"]:
            self._str_angle_std_contribution = 0
        elif str_angle_std_60s <= STR_ANGLE_STD_THRESHOLDS["MODERATE_FATIGUE_START"]:
            self._str_angle_std_contribution = 1
        elif str_angle_std_60s <= STR_ANGLE_STD_THRESHOLDS["SEVERE_FATIGUE_START"]:
            self._str_angle_std_contribution = 2
        else: # str_angle_std_60s > SEVERE_FATIGUE_START
            self._str_angle_std_contribution = 3

    def update_vsa_contribution(self, lon_g_std_60s, lat_g_std_60s, yaw_1_std_60s):
        """
        Updates the score contributions based on VSA longitudinal, lateral, and yaw standard deviations.
        """
        # Longitudinal G STD contribution
        if lon_g_std_60s <= VSA_LON_G_STD_THRESHOLDS["NORMAL_MAX"]:
            self._vsa_lon_g_std_contribution = 0
        elif lon_g_std_60s <= VSA_LON_G_STD_THRESHOLDS["MODERATE_START"]:
            self._vsa_lon_g_std_contribution = 1
        elif lon_g_std_60s <= VSA_LON_G_STD_THRESHOLDS["SEVERE_START"]:
            self._vsa_lon_g_std_contribution = 2
        else:
            self._vsa_lon_g_std_contribution = 3

        # Lateral G STD contribution
        if lat_g_std_60s <= VSA_LAT_G_STD_THRESHOLDS["NORMAL_MAX"]:
            self._vsa_lat_g_std_contribution = 0
        elif lat_g_std_60s <= VSA_LAT_G_STD_THRESHOLDS["MODERATE_START"]:
            self._vsa_lat_g_std_contribution = 1
        elif lat_g_std_60s <= VSA_LAT_G_STD_THRESHOLDS["SEVERE_START"]:
            self._vsa_lat_g_std_contribution = 2
        else:
            self._vsa_lat_g_std_contribution = 3

        # Yaw Rate STD contribution
        if yaw_1_std_60s <= VSA_YAW_1_STD_THRESHOLDS["NORMAL_MAX"]:
            self._vsa_yaw_1_std_contribution = 0
        elif yaw_1_std_60s <= VSA_YAW_1_STD_THRESHOLDS["MODERATE_START"]:
            self._vsa_yaw_1_std_contribution = 1
        elif yaw_1_std_60s <= VSA_YAW_1_STD_THRESHOLDS["SEVERE_START"]:
            self._vsa_yaw_1_std_contribution = 2
        else:
            self._vsa_yaw_1_std_contribution = 3

        # Aggregate all contributions to the total score
        self._current_alertness_score = (
            self._str_angle_std_contribution +
            self._vsa_lon_g_std_contribution +
            self._vsa_lat_g_std_contribution +
            self._vsa_yaw_1_std_contribution
        )

    def get_current_score(self):
        """Returns the current aggregated alertness score."""
        return self._current_alertness_score

    def get_alert_level(self):
        """
        Determines the alert level based on the current score.
        These are the "Critical Thresholds" you mentioned.
        """
        score = self._current_alertness_score
        # These thresholds are for the *total* aggregated score
        if score >= 30: # Example: High combined impact from multiple features
            return 3 # Critical Alert
        elif score >= 15: # Example: Moderate combined impact
            return 2 # Moderate Alert
        elif score >= 3: # Example: Mild combined impact
            return 1 # Mild Alert
        else:
            return 0 # Normal

    def reset_score(self):
        """Resets the alertness score and contributions."""
        self._current_alertness_score = 0
        self._str_angle_std_contribution = 0
        self._vsa_lon_g_std_contribution = 0
        self._vsa_lat_g_std_contribution = 0
        self._vsa_yaw_1_std_contribution = 0

# --- Alert Level Definitions (for interpretation) ---
ALERT_LEVEL_DESCRIPTIONS = {
    0: "Normal Driving",
    1: "Mild Fatigue/Distraction (Advisory - Consider a break)",
    2: "Moderate Fatigue/Distraction (Warning - Advise driver to pull over immediately!)",
    3: "Severe Fatigue/Distraction (Critical Alert - System intervention required!)"
}

