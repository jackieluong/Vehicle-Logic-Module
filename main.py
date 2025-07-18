# main.py

from Driver_Alertness_Module import Alertness_Runner
from High_Speed_Monitoring import Simulation_Runner

if __name__ == "__main__":
    print("Starting the Driver Alertness Detection Application...")
    # Alertness_Runner.run_simulation()
    
    Simulation_Runner.run_simulation()
    print("Application finished.")
