# I. Sensor & Motion Signals

# --- VSA_091: VSA Sensor Data ---
VSA_LON_G = 0.25  # Longitudinal acceleration in g (forward/backward)
VSA_LAT_G = -0.12  # Lateral acceleration in g (left/right)
VSA_YAW_1 = 1.5  # Yaw rate in deg/s (vehicle's rotation around vertical axis)

# --- STR_156: Steering Angle Sensor ---
STR_ANGLE = -15.0  # Steering wheel angle in degrees [-3276.8|3276.7] (negative = left, positive = right)

# --- ENG_130: Engine Control / Pedal Position ---
ENG_SMART_ACCELE_PEDAL_POSITION = 42.0  # Accelerator pedal position as a percentage (0–100%)

# --- ENG_17C: Engine Control / Brake Status / Speed ---
ENG_SW_STATUS_BRAKE_NO = 0  # Brake switch status (0 = pressed, 1 = not pressed)
ENG_ENG_SPEED = 2200  # Engine RPM, can be used to estimate vehicle speed

# --- VSA_255: ABS Wheel Speeds ---
VSA_ABS_FL_WHEEL_SPEED_255 = 52.3  # Front Left wheel speed in km/h
VSA_ABS_FR_WHEEL_SPEED_255 = 53.1  # Front Right wheel speed in km/h
VSA_ABS_RL_WHEEL_SPEED_255 = 50.8  # Rear Left wheel speed in km/h
VSA_ABS_RR_WHEEL_SPEED_255 = 51.2  # Rear Right wheel speed in km/h

# II. Contextual / Status Signals

# --- METER_164: Meter / Indicators ---
METER_SW_STATUS_PARK_BRAKE = 0  # Parking brake switch (0 = off/released, 1 = on/engaged)
METER_SW_STATUS_BRAKE_FLUID = 0  # Brake fluid level warning (0 = normal, 1 = low fluid)
METER_SW_STATUS_VSA_OFF = 0  # VSA OFF switch (0 = VSA active, 1 = driver turned off VSA)

# --- Example of estimated vehicle speed (average of 4 wheel speeds) ---
VEHICLE_SPEED = (VSA_ABS_FL_WHEEL_SPEED_255 + VSA_ABS_FR_WHEEL_SPEED_255 +
                 VSA_ABS_RL_WHEEL_SPEED_255 + VSA_ABS_RR_WHEEL_SPEED_255) / 4
# VEHICLE_SPEED: Approximate vehicle speed in km/h calculated from wheel speeds

# Print all values for debug/demo purposes
print("Yaw Rate:", VSA_YAW_1, "deg/s")
print("Lateral G:", VSA_LAT_G, "g")
print("Longitudinal G:", VSA_LON_G, "g")
print("Steering Angle:", STR_ANGLE, "deg")
print("Accel Pedal Pos:", ENG_SMART_ACCELE_PEDAL_POSITION, "%")
print("Brake Pressed:", ENG_SW_STATUS_BRAKE_NO == 0)
print("Engine RPM:", ENG_ENG_SPEED)
print("Vehicle Speed:", round(VEHICLE_SPEED, 2), "km/h")
