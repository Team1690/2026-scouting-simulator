from __future__ import annotations
import random
import math
from robot_model import RobotModel
from matrics import MagazineSizeMatric
from utils import calculate_error
from robot_configs import all_robots

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

    scout = MagazineSizeMatric() # the simulated scouter

    robots_data = [] # a robot spesific data

    for robot in all_robots:
        if robot.name not in robots_to_simulate: # check if we want to run this robot
            continue

        total_shots = 0
        total_hits = 0
        total_scouted_shots = 0

        number_of_volleys = random.randint(1, 6) # random number of vollies to simulate
        for i in range(number_of_volleys):
            # print(f"\nSimulation run {i + 1} / {number_of_volleys}")

            magazine_percentage = random.uniform(0.1, 1.0) # random fill between 10% and 100% for the magazine
            # print(f"Starting simulation (Fuel Level: {magazine_percentage * 100:.1f}%)")

            # print(f"\nSimulation for: {robot.name}")

            # print(f"Model settings: Magazine Size: {robot.magazine_size}, Accuracy: {robot.accuracy}")
            # print("\n")

            current_fuel = round(magazine_percentage * robot.magazine_size)
            total_shots += current_fuel # add the fuel to the total shots
            # print(f"Fuel amount in magazine: {current_fuel}")

            points, misses = robot.get_points_for_magazine(magazine_percentage)
            total_hits += points # add the points to the total hits

            time_to_empty = robot.time_to_deplete(0.05, magazine_percentage)
            # print(f"Time to deplete: {time_to_empty:.2f}s")

            obs_time, obs_bucket = scout.recorded_observation_by_scouter(time_to_empty, magazine_percentage)
            # print(f"Scout result: Bucket {obs_bucket}%, [Observer recorded time (perfect): {obs_time:.2f}s]")

            # print("\nStats:")

            scouter_shots = obs_bucket / 100 * robot.magazine_size
            error = calculate_error(scouter_shots, current_fuel)
            # print(f"Shots error: {error:.2f}% (real: {current_fuel:.1f}, scouted: {scouter_shots:.1f})")

            scouter_shots = abs(obs_bucket / 100 * robot.magazine_size)
            total_scouted_shots += scouter_shots # add the shots to the total scouted shots
            shots_vs_hits_error = calculate_error(scouter_shots, points)
            # print(f"Hits error (scouted shots vs actual hits): {shots_vs_hits_error:.2f}% (real hits: {points}, scouted shots: {scouter_shots})")

            if current_fuel > 0:
                real_accuracy = (points / current_fuel) * 100
                # print(f"\nReal accuracy: {real_accuracy:.2f}% (Placed: {robot.accuracy * 100:.1f}%)")

            # print(f"Total shots: {current_fuel} ({points} hits, {misses} misses)")

        print("\n")
        print(f"=" * 20)
        print(f"SUMMERY RESULTS:")
        print(f"Robot: {robot.name}")
        print(f"=" * 20)

        print(f"\nNumber of volleys: {number_of_volleys}")

        print(f"\nTotal shots: {total_shots}")
        print(f"Total hits: {total_hits}")
        print(f"Total scouted shots: {total_scouted_shots}")

        print(f"\nStats:")

        total_accuracy = 100 * (total_hits / total_shots)
        print(f"Total accuracy: {total_accuracy:.2f}%")

        total_shots_error = calculate_error(total_scouted_shots, total_shots)
        print(f"Total shots error: {total_shots_error:.2f}%")

        total_hits_vs_shots_error = calculate_error(total_scouted_shots, total_hits)
        print(f"Total hits error (scouted shots vs actual hits): {total_hits_vs_shots_error:.2f}%")

        # save the data for the current robot
        robot_stats = {
            "name": robot.name,
            "magazine_size": robot.magazine_size,
            "placed_accuracy": robot.accuracy * 100,
            "accuracy": total_accuracy,
            "shots_error": total_shots_error,
            "hits_error": total_hits_vs_shots_error,
            "total_shots": total_shots,
            "total_hits": total_hits,
            "total_scouted_shots": total_scouted_shots,
            "volleys": number_of_volleys
        }
        robots_data.append(robot_stats) # add the robot stats to the end of the list

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
