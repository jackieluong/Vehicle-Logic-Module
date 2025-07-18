
from .Threeholds import *
class VehicleStabilityMonitor:
    """
    Monitors vehicle stability based on steering angle, yaw rate, lateral acceleration,
    and wheel speeds using rule-based algorithms.
    """
    def __init__(self):
        # Thresholds are imported from simulation_config.py
        pass

    def check_stability(self, vehicle_speed, abs_str_angle, abs_yaw_1, abs_lat_g, max_axle_speed_diff, myu_value):
        """
        Applies rule-based algorithms to determine vehicle stability and alert level.

        Args:
            vehicle_speed (float): Average vehicle speed in km/h.
            abs_str_angle (float): Absolute steering wheel angle in degrees.
            abs_yaw_1 (float): Absolute yaw rate in deg/s.
            abs_lat_g (float): Absolute lateral acceleration in m/s^2.
            max_axle_speed_diff (float): Maximum difference between wheel speeds on an axle (km/h).
            myu_value (float): Estimated road friction coefficient.

        Returns:
            tuple: (alert_level, alert_description)
        """
        current_alert_level = ALERT_LEVEL_NONE
        triggered_details = [] # Collect specific reasons for the alert

        # System only activates under high-speed conditions
        if vehicle_speed < HIGH_SPEED_THRESHOLD_KMH:
            return ALERT_LEVEL_NONE, VEHICLE_STABILITY_ALERT_BASE_DESCRIPTIONS[ALERT_LEVEL_NONE] # Too slow for highway stability monitoring

           # --- Rule E1: Critically Low Road Friction (New Rule) ---
        # This rule provides an early warning of low grip, even before full instability.
        if myu_value < LOW_FRICTION_THRESHOLD_MYU:
            current_alert_level = ALERT_LEVEL_LOW # Initial alert for low friction
            triggered_details.append(
                VEHICLE_STABILITY_DETAIL_DESCRIPTIONS["LOW_ROAD_FRICTION"].format(
                    myu_value=myu_value
                )
            )
            
        # --- Rule A1: High Yaw, Low Steering (Uncommanded Yaw / Oversteer / Spin) ---
        # This rule detects when the vehicle is rotating significantly (high yaw)
        # but the driver's steering input is minimal, suggesting an unintended spin.
        if (abs_yaw_1 > HIGH_YAW_THRESHOLD_DEGS and
            abs_str_angle < MIN_STEERING_FOR_TURN_DEG): # Add a check for some lateral movement
            
            current_alert_level = ALERT_LEVEL_HIGH
            triggered_details.append(
                VEHICLE_STABILITY_DETAIL_DESCRIPTIONS["HIGH_YAW_LOW_STEERING"].format(
                    abs_yaw_1=abs_yaw_1, abs_str_angle=abs_str_angle
                )
            )

        # --- Rule C1: Asymmetric Wheel Speeds (Skidding/Hydroplaning) ---
        # This rule detects significant differences in wheel speeds across an axle,
        # indicating a loss of traction (skidding, hydroplaning).
        if max_axle_speed_diff > WHEEL_SLIP_THRESHOLD_KMH:
            if current_alert_level == ALERT_LEVEL_NONE:
                current_alert_level = ALERT_LEVEL_MODERATE
            elif current_alert_level == ALERT_LEVEL_LOW:
                current_alert_level = ALERT_LEVEL_MODERATE # Elevate if already low
            
            triggered_details.append(
                VEHICLE_STABILITY_DETAIL_DESCRIPTIONS["ASYMMETRIC_WHEEL_SPEEDS"].format(
                    max_axle_speed_diff=max_axle_speed_diff
                )
            )

        # --- Additional Rule (Example: High Lateral G with Low Steering - Sliding) ---
        # This rule detects when the vehicle is experiencing significant side forces
        # but the driver is not actively steering much, indicating a lateral slide.
        if (abs_lat_g > HIGH_LAT_G_THRESHOLD_MS2 and
            abs_str_angle < SMALL_STEERING_WINDOW_DEG and
            abs_yaw_1 < HIGH_YAW_THRESHOLD_DEGS * 0.5): # Not a full spin yet
            
            if current_alert_level == ALERT_LEVEL_NONE:
                current_alert_level = ALERT_LEVEL_MODERATE
            elif current_alert_level == ALERT_LEVEL_LOW:
                current_alert_level = ALERT_LEVEL_MODERATE # Elevate if already low
            
            triggered_details.append(
                VEHICLE_STABILITY_DETAIL_DESCRIPTIONS["HIGH_LAT_G_LOW_STEERING"].format(
                    abs_lat_g=abs_lat_g
                )
            )

        # Construct the final alert description
        current_alert_description = VEHICLE_STABILITY_ALERT_BASE_DESCRIPTIONS[current_alert_level]
        if triggered_details:
            current_alert_description += " Details: " + "; ".join(triggered_details)

        return current_alert_level, current_alert_description

