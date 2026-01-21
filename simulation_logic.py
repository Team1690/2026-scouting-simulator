from __future__ import annotations
import random
from utils import calculate_error
from robot_model import RobotModel
from metrics import MagazineSizeMetric

def scout_robot_match(robot: RobotModel, metric: MagazineSizeMetric) -> dict:
    total_shots = 0
    total_hits = 0
    total_scouted_shots = 0
    total_time_to_empty = 0
    stats_per_volley = []

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
        total_time_to_empty += time_to_empty
        # print(f"Time to deplete: {time_to_empty:.2f}s")

        obs_time, obs_bucket = metric.recorded_observation_by_scouter(time_to_empty, magazine_percentage)
        # print(f"Scout result: Bucket {obs_bucket}%, [Observer recorded time (perfect): {obs_time:.2f}s]")

        stats_per_volley.append({
            "points": points,
            "misses": misses,
            "time_to_empty": time_to_empty,
        })

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

    # same amount of deta as before just readable and understandable
    print(f"- Robot: {robot.name} (Volleys: {number_of_volleys})")
    print(f"Totals: Shots: {total_shots} | Hits: {total_hits} | Scouted: {total_scouted_shots:.1f}")

    if total_shots > 0:
        total_accuracy = 100 * (total_hits / total_shots)
    else:
        total_accuracy = 0

    total_shots_error = calculate_error(total_scouted_shots, total_shots)
    total_hits_vs_shots_error = calculate_error(total_scouted_shots, total_hits)

    # same amount of deta as before just readable and understandable
    print(f"Performance: Accuracy: {total_accuracy:.2f}% | Shot Error: {total_shots_error:.2f}% | Hit Error: {total_hits_vs_shots_error:.2f}%\n")

    # save the data for the current robot
    robot_stats = {
        "name": robot.name,
        "magazine_size": robot.magazine_size,
        "max_fire_rate": robot.max_fire_rate,
        "placed_accuracy": robot.accuracy * 100,
        "accuracy": total_accuracy,
        "shots_error": total_shots_error,
        "hits_error": total_hits_vs_shots_error,
        "total_shots": total_shots,
        "total_hits": total_hits,
        "total_scouted_shots": total_scouted_shots,
        "volleys": number_of_volleys,
        "total_fire_time": total_time_to_empty,
        "stats_per_volley": stats_per_volley,
    }

    return robot_stats
