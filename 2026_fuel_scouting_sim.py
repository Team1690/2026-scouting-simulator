from __future__ import annotations
from scouter_model import ScouterModel
from match_maker import make_matches
import random
from robot_model import *
from metrics import *
from simulation_logic import *
from robot_configs import *
from utils import *
from scouter_model import *

def main():
    NUMBER_OF_RUNS = 10

    total_avg_magazine_error = 0
    total_avg_fire_rate_error = 0
    total_avg_volley_error = 0
    total_avg_opr_error = 0
    total_avg_weight_based_max_fire_rate_error = 0
    total_avg_weight_based_error = 0
    total_avg_weight_based_first_volley_error = 0
    total_avg_magazine_shots_error = 0
    total_avg_volley_shots_error = 0

    for i in range(NUMBER_OF_RUNS):
        print(f"\n\nRUN {i + 1} / {NUMBER_OF_RUNS} \n\n")
        avg_magazine_error, avg_fire_rate_error, avg_volley_error, avg_opr_error, avg_weight_based_max_fire_rate_error, avg_weight_based_error, avg_weight_based_first_volley_error, avg_magazine_shots_error, avg_volley_shots_error = run_simulation()

        total_avg_magazine_error += avg_magazine_error
        total_avg_fire_rate_error += avg_fire_rate_error
        total_avg_volley_error += avg_volley_error
        total_avg_opr_error += avg_opr_error
        total_avg_weight_based_max_fire_rate_error += avg_weight_based_max_fire_rate_error
        total_avg_weight_based_error += avg_weight_based_error
        total_avg_weight_based_first_volley_error += avg_weight_based_first_volley_error
        total_avg_magazine_shots_error += avg_magazine_shots_error
        total_avg_volley_shots_error += avg_volley_shots_error

    print(f"Total avg magazine error: {total_avg_magazine_error / NUMBER_OF_RUNS}")
    print(f"Total avg fire rate error: {total_avg_fire_rate_error / NUMBER_OF_RUNS}")
    print(f"Total avg volley error: {total_avg_volley_error / NUMBER_OF_RUNS}")
    print(f"Total avg opr error: {total_avg_opr_error / NUMBER_OF_RUNS}")
    print("-" * 40)
    print(f"Total avg magazine shots error: {total_avg_magazine_shots_error / NUMBER_OF_RUNS}")
    print(f"Total avg volley shots error: {total_avg_volley_shots_error / NUMBER_OF_RUNS}")
    print("-" * 40)
    print(f"Total avg weight based max fire rate error: {total_avg_weight_based_max_fire_rate_error / NUMBER_OF_RUNS}")
    print(f"Total avg weight based error: {total_avg_weight_based_error / NUMBER_OF_RUNS}")
    print(f"Total avg weight based (first volley) error: {total_avg_weight_based_first_volley_error / NUMBER_OF_RUNS}")


def run_simulation():
    MATCHES_PER_ROBOT = 10
    ITERATIONS = 5000

    all_robots = get_all_robots()

    schedule, schedule_score = make_matches(all_robots, MATCHES_PER_ROBOT, ITERATIONS)

    match_results = []

    scout = ScouterModel(-1.0, 1.0, 0.1)
    fire_rate_metric = IterativeAverageFireRateMetric(all_robots)
    fixed_window_metric = MatchAvgRateFixedWindowMetric()
    volley_avg_rate_fixed_window_metric = VolleyAvgRateFixedWindowMetric(all_robots)
    opr = OPR(all_robots)
    weight_based_max_fire_rate_metric = WeightBasedMaxFireRateMetric(all_robots)
    weight_based_metric = WeightBasedMetric(all_robots)
    weight_based_first_volley_metric = WeightBasedFirstVolleyMetric(all_robots)

    notification_step = 1  # just to save console space where we can
    for i, match in enumerate(schedule): # enumerate takes a list and returns pairs of (index, value)
        # if (i + 1) % notification_step == 0:
        #     print("\n" + "=" * 80)
        #     print(f" MATCH: {i + 1} | Red: {match.red_alliance} vs Blue: {match.blue_alliance}")
        #     print("=" * 80)

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
        # if (i + 1) % notification_step == 0: # check if the match number is a multiple of the notification step
        #     print("\n[RED TEAM]")
        for robot in match.red_alliance:
            stats = scout_robot_match(robot, scout)
            current_match_data["red_team_robots"].append(stats)
            current_match_data["red_team_hits"] += stats["total_hits"]
            current_match_data["red_team_shots"] += stats["total_shots"]

            stats["AvgRateFixedWindow"] = fixed_window_metric.calculate_AvgRateFixedWindow(robot.name, stats["total_hits"], stats["total_fire_time"])
            stats["VolleyAvgRate"] = volley_avg_rate_fixed_window_metric.calculate_volley_avg_rate_fixed_window(stats)

        robot_scores = fire_rate_metric.calculate_score_by_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"], 10)
        weight_based_max_fire_rate_metric.calculate_weight_based_max_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        weight_based_metric.calculate_weight_based_metric(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        weight_based_first_volley_metric.calculate_weight_based_first_volley_metric(current_match_data["red_team_robots"], current_match_data["red_team_hits"])

        if (i + 1) % notification_step == 0:
            # print(f"Total red team shots: {current_match_data['red_team_shots']}")
            # print(f"Total red team hits: {current_match_data['red_team_hits']}")
            # print("\n")

            # for robot_name in robot_scores:
                # print(f"Scouted hits based on fire rate: {robot_scores[robot_name]:.2f} for {robot_name}")
                # for current_match_robot_data in current_match_data["red_team_robots"]:
                #     if current_match_robot_data["name"] == robot_name:
                #         # print(f"Shots error rate based on fire rate: {calculate_error(robot_scores[robot_name], current_match_robot_data['total_shots']):.2f}%")
                #         # print(f"Hits error rate based on fire rate: {calculate_error(robot_scores[robot_name], current_match_robot_data['total_hits']):.2f}%")

            total_score = sum(robot_scores.values())
            # print(f"\nTotal scouted hits based on fire rate: {total_score:.2f}")
            # print(f"Shots error rate based on fire rate: {calculate_error(total_score, current_match_data['red_team_shots']):.2f}%")
            # print(f"Hits error rate based on fire rate: {calculate_error(total_score, current_match_data['red_team_hits']):.2f}%")

            # print("\n")
            # match_total_fixed_window_scouted = 0
            # for robot in current_match_data["red_team_robots"]:
            #     print(f"Window avg rate scouted hits: {robot['AvgRateFixedWindow']:.2f} for {robot['name']}")
            #     match_total_fixed_window_scouted += robot['AvgRateFixedWindow']
            # print(f"\nTotal window avg rate scouted hits: {match_total_fixed_window_scouted:.2f}")

            # print("\n")
            match_total_volley_avg_window_scouted = 0
            for robot in current_match_data["red_team_robots"]:
                # print(f"{robot['name']} Volley avg rate scouted hits: {volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score']:.2f}")

                shots_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_shots'])
                hits_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_hits'])
                # print(f"{robot['name']} Shots volley error rate: {shots_volley_error_rate:.2f}%")
                # print(f"{robot['name']} Hits volley error rate: {hits_volley_error_rate:.2f}%")

                match_total_volley_avg_window_scouted += volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score']
            # print(f"\nTotal volley avg rate scouted hits: {match_total_volley_avg_window_scouted:.2f}")
            # print(f"Total shots volley error rate: {calculate_error(match_total_volley_avg_window_scouted, current_match_data['red_team_shots']):.2f}%")
            # print(f"Total hits volley error rate: {calculate_error(match_total_volley_avg_window_scouted, current_match_data['red_team_hits']):.2f}%")

            for robot in current_match_data["red_team_robots"]:
                volley_avg_rate_fixed_window_metric.reset_robot_volleys(robot['name'])


        # Blue Team
        # if (i + 1) % notification_step == 0: # same as above
            # print("\n[BLUE TEAM]")
        for robot in match.blue_alliance:
            stats = scout_robot_match(robot, scout)
            current_match_data["blue_team_robots"].append(stats)
            current_match_data["blue_team_shots"] += stats["total_shots"]
            current_match_data["blue_team_hits"] += stats["total_hits"]

            stats["AvgRateFixedWindow"] = fixed_window_metric.calculate_AvgRateFixedWindow(robot.name, stats["total_hits"], stats["total_fire_time"])
            stats["VolleyAvgRate"] = volley_avg_rate_fixed_window_metric.calculate_volley_avg_rate_fixed_window(stats)

        robot_scores = fire_rate_metric.calculate_score_by_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"], 10)
        weight_based_max_fire_rate_metric.calculate_weight_based_max_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        weight_based_metric.calculate_weight_based_metric(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        weight_based_first_volley_metric.calculate_weight_based_first_volley_metric(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])

        opr.add_match(match.red_alliance, current_match_data["red_team_hits"], match.blue_alliance, current_match_data["blue_team_hits"])
        opr.calculate_opr()

        match_results.append(current_match_data)

        if (i + 1) % notification_step == 0:
            # print(f"Total blue team shots: {current_match_data['blue_team_shots']}")
            # print(f"Total blue team hits: {current_match_data['blue_team_hits']}")
            # print("\n")

            # for robot_name in robot_scores:
                # print(f"Scouted hits based on fire rate: {robot_scores[robot_name]:.2f} for {robot_name}")
                # for current_match_robot_data in current_match_data["blue_team_robots"]:
                #     if current_match_robot_data["name"] == robot_name:
                        # print(f"Shots error rate based on fire rate: {calculate_error(robot_scores[robot_name], current_match_robot_data['total_shots']):.2f}%")
                        # print(f"Hits error rate based on fire rate: {calculate_error(robot_scores[robot_name], current_match_robot_data['total_hits']):.2f}%")

            total_score = sum(robot_scores.values())
            # print(f"\nTotal scouted hits based on fire rate: {total_score:.2f}")
            # print(f"Shots error rate based on fire rate: {calculate_error(total_score, current_match_data['blue_team_shots']):.2f}%")
            # print(f"Hits error rate based on fire rate: {calculate_error(total_score, current_match_data['blue_team_hits']):.2f}%")

            # print("\n")
            # match_total_fixed_window_scouted = 0
            # for robot in current_match_data["blue_team_robots"]:
            #     print(f"Window avg rate: {robot['AvgRateFixedWindow']:.2f} for {robot['name']}")
            #     match_total_fixed_window_scouted += robot['AvgRateFixedWindow']
            # print(f"\nTotal window avg rate: {match_total_fixed_window_scouted:.2f}")

            # print("\n")
            match_total_volley_avg_window_scouted = 0
            for robot in current_match_data["blue_team_robots"]:
                # print(f"{robot['name']} Volley avg rate scouted hits: {(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score']):.2f}")

                shots_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_shots'])
                # print(f"{robot['name']} Shots Volley error rate: {shots_volley_error_rate:.2f}%")
                hits_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_hits'])
                # print(f"{robot['name']} Hits Volley error rate: {hits_volley_error_rate:.2f}%")


                match_total_volley_avg_window_scouted += volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score']
            # print(f"\nTotal volley avg rate scouted hits: {match_total_volley_avg_window_scouted:.2f}")
            # print(f"Total shots Volley error rate: {calculate_error(match_total_volley_avg_window_scouted, current_match_data['blue_team_shots']):.2f}%")
            # print(f"Total hits Volley error rate: {calculate_error(match_total_volley_avg_window_scouted, current_match_data['blue_team_hits']):.2f}%")

            for robot in current_match_data["blue_team_robots"]:
                volley_avg_rate_fixed_window_metric.reset_robot_volleys(robot['name'])

    # print("\n")
    # print(f"Schedule Score: {schedule_score}")
    # print("Simulation completed!")
    # print(f"Total matches simulated: {len(match_results)}")

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
                    "total_AvgRateFixedWindow": 0,
                    "total_VolleyAvgRate": 0,
                }

            # Add the data from this match to the total
            final_robot_stats[name]["total_shots_fired"] += robot_data["total_shots"]
            final_robot_stats[name]["total_shots_hit"] += robot_data["total_hits"]
            final_robot_stats[name]["total_shots_scouted"] += robot_data["total_scouted_shots"]
            final_robot_stats[name]["matches_played"] += 1
            final_robot_stats[name]["volleys_fired"] += robot_data["volleys"]
            final_robot_stats[name]["total_fire_time"] += robot_data["total_fire_time"]
            final_robot_stats[name]["total_AvgRateFixedWindow"] += robot_data["AvgRateFixedWindow"]
            final_robot_stats[name]["total_VolleyAvgRate"] += robot_data["VolleyAvgRate"]

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
                    "total_AvgRateFixedWindow": 0,
                    "total_VolleyAvgRate": 0,
                }

            final_robot_stats[name]["total_shots_fired"] += robot_data["total_shots"]
            final_robot_stats[name]["total_shots_hit"] += robot_data["total_hits"]
            final_robot_stats[name]["total_shots_scouted"] += robot_data["total_scouted_shots"]
            final_robot_stats[name]["matches_played"] += 1
            final_robot_stats[name]["volleys_fired"] += robot_data["volleys"]
            final_robot_stats[name]["total_fire_time"] += robot_data["total_fire_time"]
            final_robot_stats[name]["total_AvgRateFixedWindow"] += robot_data["AvgRateFixedWindow"]
            final_robot_stats[name]["total_VolleyAvgRate"] += robot_data["VolleyAvgRate"]

    # print("\n")
    # print("=" * 40)
    # print("FINAL RESULTS FOR EACH ROBOT")
    # print("=" * 40)
    # print("\n")

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

        # print(f"Robot Name: {name}")
        # print(f" Matches: {data['matches_played']} | Volleys: {data['volleys_fired']}")
        # print(f" Shots: {shots}, Hits: {hits} | Scouted: {scouted:.1f}")
        # print(f" Real Accuracy: {real_acc:.2f}% (Placed: {data['placed_accuracy']:.1f}%)")
        # print(f" Shot Error: {shot_error:.2f}% | Hit Error: {hit_error:.2f}%")
        # print(f"\n")
        # print(f" Robot avg fire rate: {robot_avg_fire_rate:.2f}")
        # print(f" Shots: {shots}, Hits: {hits} | Scouted: {fire_rate_scouted:.2f}")
        # print(f" Fire rate error: {fire_rate_error:.2f}%")
        # print(f"\n")
        # print(f" Volley avg error rate: {calculate_error(data['total_VolleyAvgRate'], hits):.2f}%")
        # print("\n")
        # print(f" OPR: {opr.get_opr()[name]:.2f}")
        # print(f" Real avg hits per match: {hits / data['matches_played']:.2f}")
        # print(f" OPR error rate: {calculate_error(opr.get_opr()[name], hits / data['matches_played']):.2f}%")
        # print(f"\n")
        # print(f" Fixed window scouted hits: {data['total_AvgRateFixedWindow']:.2f}")
        # print(f" Fixed window error rate: {calculate_error(data['total_AvgRateFixedWindow'], hits):.2f}%")
        # print(f" Fixed window avg rate: {fixed_window_metric.get_rates()[name]:.2f}")

        # print("-" * 30)

    # print("\n")
    # print("-" * 40)
    # print("TOTAL ERROR RATES ACROSS ALL MATCHES AND ROBOTS")
    # print("-" * 40)

    total_magazine_error = 0
    total_fire_rate_error = 0
    total_volley_error = 0
    total_opr_error = 0
    total_weight_based_max_fire_rate_error = 0
    total_weight_based_error = 0
    total_weight_based_first_volley_error = 0
    total_magazine_shots_error = 0
    total_volley_shots_error = 0

    robot_count = len(robot_names_list)

    for robot_name in robot_names_list:
        robot_stats = final_robot_stats[robot_name]

        actual_hits = robot_stats["total_shots_hit"]
        actual_shots = robot_stats["total_shots_fired"]
        scouted_shots = robot_stats["total_shots_scouted"]

        magazine_error = calculate_error(scouted_shots, actual_hits)
        total_magazine_error += magazine_error

        magazine_shots_error = calculate_error(scouted_shots, actual_shots)
        total_magazine_shots_error += magazine_shots_error

        robot_avg_fire_rate = fire_rate_metric.get_averages()[robot_name][1]
        fire_rate_scouted_hits = robot_avg_fire_rate * robot_stats['total_fire_time']

        fire_rate_error = calculate_error(fire_rate_scouted_hits, actual_hits)
        total_fire_rate_error += fire_rate_error

        volley_avg_rate_total = robot_stats['total_VolleyAvgRate']

        volley_error = calculate_error(volley_avg_rate_total, actual_hits)
        total_volley_error += volley_error

        volley_shots_error = calculate_error(volley_avg_rate_total, actual_shots)
        total_volley_shots_error += volley_shots_error

        opr_value = opr.get_opr()[robot_name]

        matches_played = robot_stats['matches_played']
        real_hits_per_match = actual_hits / matches_played

        opr_error = calculate_error(opr_value, real_hits_per_match)
        total_opr_error += opr_error

        weight_based_max_fire_rate_error = calculate_error(weight_based_max_fire_rate_metric.get_final_scores()[robot_name], actual_hits)
        total_weight_based_max_fire_rate_error += weight_based_max_fire_rate_error

        weight_based_error = calculate_error(weight_based_metric.get_final_scores()[robot_name], actual_hits)
        total_weight_based_error += weight_based_error

        weight_based_first_volley_error = calculate_error(weight_based_first_volley_metric.get_final_scores()[robot_name], actual_hits)
        total_weight_based_first_volley_error += weight_based_first_volley_error

    avg_opr_error = total_opr_error / robot_count
    print(f"Average OPR Error: {avg_opr_error:.2f}%")

    avg_fire_rate_error = total_fire_rate_error / robot_count
    print(f"Average Fire Rate Error: {avg_fire_rate_error:.2f}%")

    print("-" * 40)

    avg_magazine_error = total_magazine_error / robot_count
    print(f"Magazine Size Hits Error: {avg_magazine_error:.2f}%")

    avg_magazine_shots_error = total_magazine_shots_error / robot_count
    print(f"Magazine Size Shots Error: {avg_magazine_shots_error:.2f}%")

    avg_volley_error = total_volley_error / robot_count
    print(f"First Volley Hits Error: {avg_volley_error:.2f}%")

    avg_volley_shots_error = total_volley_shots_error / robot_count
    print(f"First Volley Shots Error: {avg_volley_shots_error:.2f}%")

    print("-" * 40)

    avg_weight_based_max_fire_rate_error = total_weight_based_max_fire_rate_error / robot_count
    print(f"Weight Based + Max Fire Rate (Magazine) error rate: {avg_weight_based_max_fire_rate_error:.2f}%")

    avg_weight_based_error = total_weight_based_error / robot_count
    print(f"Weight Based (Magazine) error rate: {avg_weight_based_error:.2f}%")

    avg_weight_based_first_volley_error = total_weight_based_first_volley_error / robot_count
    print(f"Weight Based (First Volley) error rate: {avg_weight_based_first_volley_error:.2f}%")

    print("\n") # like alw terminal next to a line is annoying me

    return avg_magazine_error, avg_fire_rate_error, avg_volley_error, avg_opr_error, avg_weight_based_max_fire_rate_error, avg_weight_based_error, avg_weight_based_first_volley_error, avg_magazine_shots_error, avg_volley_shots_error


if __name__ == "__main__":
    main()
