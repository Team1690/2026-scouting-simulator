from __future__ import annotations
import random
from robot_model import *
from metrics import *
from simulation_logic import *
from robot_configs import *

def main():
    robots_to_simulate = ["Quick fire", "Log", "Inconsistent shooting with jam - Askof's function", "Consistent spray fire", "Burst then jam fire", "Stutter wave fire"]

    # Assigning robots to teams
    blue_team = []
    red_team = []

    random.shuffle(all_robots) # cheep way to make the teams random

    for i in range(len(all_robots)): # //todo: make it max at 3 robots per team
        if i % 2 == 0:
            blue_team.append(all_robots[i])
        else:
            red_team.append(all_robots[i])

    print("Blue Team:")
    for robot in blue_team:
        print(f"- {robot.name}")

    print("\nRed Team:")
    for robot in red_team:
        print(f"- {robot.name}")

    scout = MagazineSizeMetric() # the simulated scouter

    robots_data = [] # a robot spesific data

    for robot in all_robots:
        if robot.name not in robots_to_simulate: # check if we want to run this robot
            continue

        robot_stats = scout_robot_match(robot, scout)
        robots_data.append(robot_stats)

    print(f"\nTeams")
    print(f"Blue team: {blue_team}")
    print(f"Red team: {red_team}")

    print("\n" * 2)
    print("=" * 40)
    print("FINAL COMPARISON OF ALL THE ROBOTS")
    print("=" * 40)

    for data in robots_data:
        print(f"\nRobot Name: {data['name']}")
        print(f"magazine size: {data['magazine_size']}")
        print(f"Simulation runs: {data['volleys']}")
        print(f"- Overall accuracy: {data['accuracy']:.2f}% (placed: {data['placed_accuracy']:.1f}%)")
        print(f"- Average shots error: {data['shots_error']:.2f}% (real: {data['total_shots']}, scouted: {data['total_scouted_shots']:.1f})")
        print(f"- Average hits error: {data['hits_error']:.2f}% (real: {data['total_hits']}, scouted: {data['total_scouted_shots']:.1f})")

    print("\n" * 2)
    print("=" * 16)
    print("TEAM STATISTICS")
    print("=" * 16)

    # blue team stats
    blue_total_shots = 0
    blue_total_hits = 0
    blue_total_scouted = 0

    for robot in blue_team: # add the stats to the team stats
        for data in robots_data:
            if data["name"] == robot.name:
                blue_total_shots += data["total_shots"]
                blue_total_hits += data["total_hits"]
                blue_total_scouted += data["total_scouted_shots"]

    print("\nBlue Team Stats:")
    print(f"Robots in team: {[r.name for r in blue_team]}")
    print(f"Total Shots: {blue_total_shots}")
    print(f"Total Hits: {blue_total_hits}")
    print(f"Total Scouted Shots: {blue_total_scouted:.2f}")

    # red team stats
    red_total_shots = 0
    red_total_hits = 0
    red_total_scouted = 0

    for robot in red_team: # add the stats to the team stats
        for data in robots_data:
            if data["name"] == robot.name:
                red_total_shots += data["total_shots"]
                red_total_hits += data["total_hits"]
                red_total_scouted += data["total_scouted_shots"]

    print("\nRed Team Results:")
    print(f"Members: {[r.name for r in red_team]}")
    print(f"Total Shots: {red_total_shots}")
    print(f"Total Hits: {red_total_hits}")
    print(f"Total Scouted Shots: {red_total_scouted:.2f}")
    print(f"\n") # annoyed me that the terminal line was next to it


if __name__ == "__main__":
    main()
