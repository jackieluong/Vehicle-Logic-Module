


from .Threeholds import *
class HealthMonitor:
    """
    Monitors the health of the vehicle's braking system using rule-based algorithms,
    focusing on the strictly defined signals.
    """
    def __init__(self):
        pass

    def check_braking_health(self, current_sim_time,
                              meter_sw_status_brake_fluid,
                              eng_sw_status_brake_no,
                              vsa_master_cylinder_pressure,
                              vsa_warn_status_brake,
                              vsa_warn_status_abs,
                              vsa_warn_status_puncture):
        """
        Applies rule-based algorithms to determine braking system health and alert level.

        Args (all current values for the time step):
            meter_sw_status_brake_fluid (int): SG_ METER_SW_STATUS_BRAKE_FLUID
            eng_sw_status_brake_no (int): SG_ ENG_SW_STATUS_BRAKE_NO
            vsa_master_cylinder_pressure (float): SG_ VSA_MASTER_CYLINDER_PRESSURE
            vsa_warn_status_brake (int): SG_ VSA_WARN_STATUS_BRAKE
            vsa_warn_status_abs (int): SG_ VSA_WARN_STATUS_ABS
            vsa_warn_status_puncture (int): SG_ VSA_WARN_STATUS_PUNCTURE

        Returns:
            tuple: (alert_level, alert_description)
        """
        current_alert_level = ALERT_LEVEL_NONE
        triggered_details = []

        # --- Rule 1: Brake Fluid Level Monitoring (HIGH Impact) ---
        if meter_sw_status_brake_fluid == LOW_BRAKE_FLUID_STATUS_FAULT:
            current_alert_level = ALERT_LEVEL_HIGH # Critical: Direct safety hazard
            triggered_details.append(BRAKING_HEALTH_DETAIL_DESCRIPTIONS["LOW_BRAKE_FLUID"])

        # --- Rule 2: Master Cylinder Pressure Plausibility Monitoring (HIGH Impact) ---
        # Since vsa_fail_mc_pressure_sensor is not used, we rely solely on plausibility.
        if eng_sw_status_brake_no == 1: # Brake pedal is pressed
            if vsa_master_cylinder_pressure < MIN_MASTER_CYLINDER_PRESSURE_ACTIVE_BRAKE_KPA:
                if current_alert_level == ALERT_LEVEL_NONE: current_alert_level = ALERT_LEVEL_MODERATE # Moderate: Potential hydraulic issue
                triggered_details.append(
                    BRAKING_HEALTH_DETAIL_DESCRIPTIONS["MC_PRESSURE_IMPLAUSIBLE_LOW"].format(
                        mc_pressure=vsa_master_cylinder_pressure
                    )
                )
        else: # Brake pedal is NOT pressed
            if vsa_master_cylinder_pressure > MAX_MASTER_CYLINDER_PRESSURE_NO_BRAKE_KPA:
                if current_alert_level == ALERT_LEVEL_NONE: current_alert_level = ALERT_LEVEL_MODERATE # Moderate: Possible stuck brake or sensor issue
                triggered_details.append(
                    BRAKING_HEALTH_DETAIL_DESCRIPTIONS["MC_PRESSURE_IMPLAUSIBLE_HIGH"].format(
                        mc_pressure=vsa_master_cylinder_pressure
                    )
                )

        # --- Rule 3: Overall Braking System Warning Statuses (HIGH Impact) ---
        # These are direct indicators from the vehicle's own safety systems
        if vsa_warn_status_brake == WARN_STATUS_ACTIVE:
            if current_alert_level == ALERT_LEVEL_NONE: current_alert_level = ALERT_LEVEL_HIGH # Critical: General brake system fault
            triggered_details.append(BRAKING_HEALTH_DETAIL_DESCRIPTIONS["BRAKE_WARNING_LIGHT"])
        
        if vsa_warn_status_abs == WARN_STATUS_ACTIVE:
            if current_alert_level == ALERT_LEVEL_NONE: current_alert_level = ALERT_LEVEL_HIGH # Critical: ABS system fault
            triggered_details.append(BRAKING_HEALTH_DETAIL_DESCRIPTIONS["ABS_WARNING_LIGHT"])
        
    
        # --- Rule 4: Tire Puncture Warning (MODERATE/HIGH Impact) ---
        # A puncture directly impacts braking effectiveness and vehicle control.
        if vsa_warn_status_puncture == PUNCTURE_WARN_ACTIVE:
            # If no higher alert, set to MODERATE. If already MODERATE or HIGH, just add detail.
            if current_alert_level == ALERT_LEVEL_NONE: current_alert_level = ALERT_LEVEL_MODERATE
            triggered_details.append(BRAKING_HEALTH_DETAIL_DESCRIPTIONS["TIRE_PUNCTURE_WARNING"])

        # Construct the final alert description
        final_alert_description = BRAKING_HEALTH_ALERT_BASE_DESCRIPTIONS[current_alert_level]
        if triggered_details:
            final_alert_description += " Details: " + "; ".join(triggered_details)

        return current_alert_level, final_alert_description

