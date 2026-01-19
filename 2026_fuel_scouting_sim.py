from __future__ import annotations
from match_maker import make_matches
import random
from robot_model import *
from metrics import *
from simulation_logic import *
from robot_configs import *
from utils import *

def main():
    MATCHES_PER_ROBOT = 10
    ITERATIONS = 10000

    schedule, schedule_score = make_matches(all_robots, MATCHES_PER_ROBOT, ITERATIONS)

    match_results = []

    scout = MagazineSizeMetric() # The scout creates the data
    fire_rate_metric = IterativeAverageFireRateMetric(all_robots)
    opr = OPR(all_robots)

    notification_step = 1  # just to save console space where we can
    for i, match in enumerate(schedule): # enumerate takes a list and returns pairs of (index, value)
        if (i + 1) % notification_step == 0:
            print("\n" + "=" * 80)
            print(f" MATCH: {i + 1} | Red: {match.red_alliance} vs Blue: {match.blue_alliance}")
            print("=" * 80)

        current_match_data = {
            "match_number": i + 1,
            "red_team_robots": [],
            "blue_team_robots": [],
            "red_team_hits": 0,
            "red_team_shots": 0,
            "blue_team_hits": 0,
            "blue_team_shots": 0
        }

        # Red Team
        if (i + 1) % notification_step == 0: # check if the match number is a multiple of the notification step
            print("\n[RED TEAM]")
        for robot in match.red_alliance:
            stats = scout_robot_match(robot, scout)
            current_match_data["red_team_robots"].append(stats)
            current_match_data["red_team_hits"] += stats["total_hits"]
            current_match_data["red_team_shots"] += stats["total_shots"]

        robot_scores = fire_rate_metric.calculate_score_by_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"], 10)

        if (i + 1) % notification_step == 0:
            print(f"Total red team hits: {current_match_data['red_team_hits']}")
            print(f"Total red team shots: {current_match_data['red_team_shots']}")
            print("\n")

            for robot_name in robot_scores:
                print(f"Scouted hits based on fire rate: {robot_scores[robot_name]:.2f} for {robot_name}")

            total_score = sum(robot_scores.values())
            print(f"\nTotal scouted hits based on fire rate: {total_score:.2f}")

        # Blue Team
        if (i + 1) % notification_step == 0: # same as above
            print("\n[BLUE TEAM]")
        for robot in match.blue_alliance:
            stats = scout_robot_match(robot, scout)
            current_match_data["blue_team_robots"].append(stats)
            current_match_data["blue_team_hits"] += stats["total_hits"]
            current_match_data["blue_team_shots"] += stats["total_shots"]

        robot_scores = fire_rate_metric.calculate_score_by_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"], 10)

        opr.add_match(match.red_alliance, current_match_data["red_team_hits"], match.blue_alliance, current_match_data["blue_team_hits"])
        opr.calculate_opr()

        match_results.append(current_match_data)

        if (i + 1) % notification_step == 0:
            print(f"Total blue team hits: {current_match_data['blue_team_hits']}")
            print(f"Total blue team shots: {current_match_data['blue_team_shots']}")
            print("\n")

            for robot_name in robot_scores:
                print(f"Scouted hits based on fire rate: {robot_scores[robot_name]:.2f} for {robot_name}")

            total_score = sum(robot_scores.values())
            print(f"\nTotal scouted hits based on fire rate: {total_score:.2f}")

    print("\n")
    print(f"Schedule Score: {schedule_score}")
    print("Simulation completed!")
    print(f"Total matches simulated: {len(match_results)}")

    final_robot_stats = {} # empty dictionary to store totals

    for match_info in match_results:
        for robot_data in match_info["red_team_robots"]: # for every robot in the red team
            name = robot_data["name"]

            if name not in final_robot_stats: # if we haven't seen this robot before
                final_robot_stats[name] = {
                    "total_shots_fired": 0,
                    "total_shots_hit": 0,
                    "total_shots_scouted": 0,
                    "matches_played": 0,
                    "volleys_fired": 0,
                    "placed_accuracy": robot_data["placed_accuracy"],
                    "total_fire_time": 0,
                }

            # Add the data from this match to the total
            final_robot_stats[name]["total_shots_fired"] += robot_data["total_shots"]
            final_robot_stats[name]["total_shots_hit"] += robot_data["total_hits"]
            final_robot_stats[name]["total_shots_scouted"] += robot_data["total_scouted_shots"]
            final_robot_stats[name]["matches_played"] += 1
            final_robot_stats[name]["volleys_fired"] += robot_data["volleys"]
            final_robot_stats[name]["total_fire_time"] += robot_data["total_fire_time"]

        # Do the blue team (same exact thing)
        for robot_data in match_info["blue_team_robots"]:
            name = robot_data["name"]

            if name not in final_robot_stats:
                final_robot_stats[name] = {
                    "total_shots_fired": 0,
                    "total_shots_hit": 0,
                    "total_shots_scouted": 0,
                    "matches_played": 0,
                    "volleys_fired": 0,
                    "placed_accuracy": robot_data["placed_accuracy"],
                    "total_fire_time": 0,
                }

            final_robot_stats[name]["total_shots_fired"] += robot_data["total_shots"]
            final_robot_stats[name]["total_shots_hit"] += robot_data["total_hits"]
            final_robot_stats[name]["total_shots_scouted"] += robot_data["total_scouted_shots"]
            final_robot_stats[name]["matches_played"] += 1
            final_robot_stats[name]["volleys_fired"] += robot_data["volleys"]
            final_robot_stats[name]["total_fire_time"] += robot_data["total_fire_time"]

    print("\n")
    print("=" * 40)
    print("FINAL RESULTS FOR EACH ROBOT")
    print("=" * 40)
    print("\n")

    robot_names_list = list(final_robot_stats.keys()) # get the list of names
    robot_names_list.sort() # sort them (look better)

    for name in robot_names_list:
        data = final_robot_stats[name]

        robot_avg_fire_rate = fire_rate_metric.get_averages()[name][1]

        shots = data["total_shots_fired"]
        hits = data["total_shots_hit"]
        scouted = data["total_shots_scouted"]

        # calculate accuracy and prevent division by zero
        if shots > 0:
            real_acc = (hits / shots) * 100
        else:
            real_acc = 0

        shot_error = calculate_error(scouted, shots)
        hit_error = calculate_error(scouted, hits)
        fire_rate_scouted = robot_avg_fire_rate * data['total_fire_time']
        fire_rate_error = calculate_error(fire_rate_scouted, hits)

        print(f"Robot Name: {name}")
        print(f" Matches: {data['matches_played']} | Volleys: {data['volleys_fired']}")
        print(f" Shots: {shots}, Hits: {hits} | Scouted: {scouted:.1f}")
        print(f" Real Accuracy: {real_acc:.2f}% (Placed: {data['placed_accuracy']:.1f}%)")
        print(f" Shot Error: {shot_error:.2f}% | Hit Error: {hit_error:.2f}%")
        print(f"\n")
        print(f" Robot avg fire rate: {robot_avg_fire_rate:.2f}")
        print(f" Shots: {shots}, Hits: {hits} | Scouted: {fire_rate_scouted:.2f}")
        print(f" Fire rate error: {fire_rate_error:.2f}%")
        print(f" OPR: {opr.get_opr()[name]:.2f}")
        print(f" Real avg hits per match: {hits / data['matches_played']:.2f}")
        print(f" OPR error rate: {calculate_error(opr.get_opr()[name], hits / data['matches_played']):.2f}%")
        print("-" * 30)


if __name__ == "__main__":
    main()
