from __future__ import annotations
from match_maker import make_matches
import random
from robot_model import *
from metrics import *
from simulation_logic import *
from robot_configs import *

def main():
    MATCHES_PER_ROBOT = 10
    ITERATIONS = 10000

    schedule, schedule_score = make_matches(all_robots, MATCHES_PER_ROBOT, ITERATIONS)

    match_results = []

    scout = MagazineSizeMetric() # The scout creates the data

    notification_step = 1  # how often to print progress
    for i, match in enumerate(schedule): # enumerate takes a list and returns pairs of (index, value)
        if (i + 1) % notification_step == 0:
            print("\n" * 2)
            print("-" * 50)
            print(f"Match Number: {i + 1}, Blue Team: {match.blue_alliance}, Red Team: {match.red_alliance}")
            print("-" * 50)

        current_match_data = {
            "match_number": i + 1,
            "red_team_stats": [],
            "blue_team_stats": []
        }

        # Red Team
        for robot in match.red_alliance:
            stats = scout_robot_match(robot, scout)
            current_match_data["red_team_stats"].append(stats)

        # Blue Team
        for robot in match.blue_alliance:
            stats = scout_robot_match(robot, scout)
            current_match_data["blue_team_stats"].append(stats)

        match_results.append(current_match_data)

    print(f"Schedule Score: {schedule_score}")
    print("Simulation completed!")
    print(f"Total matches simulated: {len(match_results)}")

if __name__ == "__main__":
    main()
