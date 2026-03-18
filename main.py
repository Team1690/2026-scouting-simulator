from __future__ import annotations
from scouter_model import ScouterModel
from match_maker import make_matches, Match
import random
from robot_model import *
from metrics import *
from simulation_logic import *
from robot_configs import *
from robot_configs import get_time_based_robots
from robot_configs_magazine_size import get_all_robots as get_magazine_robots
from utils import *
from scouter_model import *
from parameters import *

def enabled(metric_name):
    return metric_name in ENABLED_METRICS

def remap_schedule(schedule, from_robots, to_robots):
    robot_index = {id(robot): i for i, robot in enumerate(from_robots)}
    new_schedule = []
    for match in schedule:
        new_red = [to_robots[robot_index[id(r)]] for r in match.red_alliance]
        new_blue = [to_robots[robot_index[id(r)]] for r in match.blue_alliance]
        new_schedule.append(Match(new_red, new_blue))
    return new_schedule

def run_full_simulation_suite(all_robots, suite_label, schedules):
    totals = {}

    for i in range(NUMBER_OF_RUNS):
        print(f"\n\nRUN {i + 1} / {NUMBER_OF_RUNS} \n\n")
        schedule = random.choice(schedules)
        run_results = run_simulation(all_robots, schedule)

        for key, value in run_results.items():
            totals[key] = totals.get(key, 0) + value

    return {key: value / NUMBER_OF_RUNS for key, value in totals.items()}


def run_simulation(all_robots, schedule):
    match_results = []

    scout = ScouterModel(SCOUT_MIN_TIME_ERROR, SCOUT_MAX_TIME_ERROR, SCOUT_MAGAZINE_ERROR) # min_time_error, max_time_error, magazine_error

    # Only instantiate enabled metrics
    fire_rate_metric = IterativeAverageFireRateMetric(all_robots) if enabled("fire_rate") else None
    fixed_window_metric = MatchAvgRateFixedWindowMetric() if enabled("fixed_window") else None
    volley_avg_rate_fixed_window_metric = VolleyAvgRateFixedWindowMetric(all_robots) if enabled("volley_avg_rate") else None
    opr = OPR(all_robots) if enabled("opr") else None
    weight_based_max_fire_rate_metric = WeightBasedMaxFireRateMetric(all_robots) if enabled("weight_based_max_fire_rate") else None
    weight_based_metric = WeightBasedMetric(all_robots) if enabled("weight_based") else None
    weight_based_first_volley_metric = WeightBasedFirstVolleyMetric(all_robots) if enabled("weight_based_first_volley") else None
    first_volley_accuracy_weight_metric = FirstVolleyAccuracyWeightMetric(all_robots) if enabled("first_volley_accuracy_weight") else None
    first_volley_accuracy_weight_metric_tournament = FirstVolleyAccuracyWeightMetricTournament(all_robots) if enabled("first_volley_accuracy_weight_tournament") else None
    first_volley_bps_weighted_accuracy_metric = FirstVolleyBPSWeightedAccuracy(all_robots) if enabled("first_volley_bps_weighted_accuracy") else None
    first_volley_bps_weighted_accuracy_tournament_metric = FirstVolleyBPSWeightedAccuracyTournament(all_robots) if enabled("first_volley_bps_weighted_accuracy_tournament") else None
    fire_time_weight_metric = FireTimeWeightMetric(all_robots) if enabled("fire_time_weight") else None

    notification_step = NOTIFICATION_STEP  # just to save console space where we can
    for i, match in enumerate(schedule): # enumerate takes a list and returns pairs of (index, value)
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
        for robot in match.red_alliance:
            stats = scout_robot_match(robot, scout, MATCH_ACCURACY_VARIANCE)
            current_match_data["red_team_robots"].append(stats)
            current_match_data["red_team_hits"] += stats["total_hits"]
            current_match_data["red_team_shots"] += stats["total_shots"]

            if fixed_window_metric:
                stats["AvgRateFixedWindow"] = fixed_window_metric.calculate_AvgRateFixedWindow(robot.name, stats["total_hits"], stats["total_fire_time"])
            else:
                stats["AvgRateFixedWindow"] = 0
            if volley_avg_rate_fixed_window_metric:
                stats["VolleyAvgRate"] = volley_avg_rate_fixed_window_metric.calculate_volley_avg_rate_fixed_window(stats)
            else:
                stats["VolleyAvgRate"] = 0

        if fire_rate_metric:
            robot_scores = fire_rate_metric.calculate_score_by_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"], 10)
        if weight_based_max_fire_rate_metric:
            weight_based_max_fire_rate_metric.calculate_weight_based_max_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if weight_based_metric:
            weight_based_metric.calculate_weight_based_metric(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if weight_based_first_volley_metric:
            weight_based_first_volley_metric.calculate_weight_based_first_volley_metric(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if first_volley_accuracy_weight_metric:
            first_volley_accuracy_weight_metric.calculate_first_volley_accuracy_weight(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if first_volley_accuracy_weight_metric_tournament:
            first_volley_accuracy_weight_metric_tournament.calculate_first_volley_accuracy_weight_tournament(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if first_volley_bps_weighted_accuracy_metric:
            first_volley_bps_weighted_accuracy_metric.calculate_first_volley_bps_weighted_accuracy(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if first_volley_bps_weighted_accuracy_tournament_metric:
            first_volley_bps_weighted_accuracy_tournament_metric.calculate_first_volley_bps_weighted_accuracy_tournament(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        if fire_time_weight_metric:
            fire_time_weight_metric.calculate_fire_time_weight(current_match_data["red_team_robots"], current_match_data["red_team_hits"])

        if (i + 1) % notification_step == 0:
            if fire_rate_metric:
                total_score = sum(robot_scores.values())

            if volley_avg_rate_fixed_window_metric:
                match_total_volley_avg_window_scouted = 0
                for robot in current_match_data["red_team_robots"]:
                    shots_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_shots'])
                    hits_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_hits'])
                    match_total_volley_avg_window_scouted += volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score']

                for robot in current_match_data["red_team_robots"]:
                    volley_avg_rate_fixed_window_metric.reset_robot_volleys(robot['name'])


        # Blue Team
        for robot in match.blue_alliance:
            stats = scout_robot_match(robot, scout, MATCH_ACCURACY_VARIANCE)
            current_match_data["blue_team_robots"].append(stats)
            current_match_data["blue_team_shots"] += stats["total_shots"]
            current_match_data["blue_team_hits"] += stats["total_hits"]

            if fixed_window_metric:
                stats["AvgRateFixedWindow"] = fixed_window_metric.calculate_AvgRateFixedWindow(robot.name, stats["total_hits"], stats["total_fire_time"])
            else:
                stats["AvgRateFixedWindow"] = 0
            if volley_avg_rate_fixed_window_metric:
                stats["VolleyAvgRate"] = volley_avg_rate_fixed_window_metric.calculate_volley_avg_rate_fixed_window(stats)
            else:
                stats["VolleyAvgRate"] = 0

        if fire_rate_metric:
            robot_scores = fire_rate_metric.calculate_score_by_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"], 10)
        if weight_based_max_fire_rate_metric:
            weight_based_max_fire_rate_metric.calculate_weight_based_max_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if weight_based_metric:
            weight_based_metric.calculate_weight_based_metric(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if weight_based_first_volley_metric:
            weight_based_first_volley_metric.calculate_weight_based_first_volley_metric(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if first_volley_accuracy_weight_metric:
            first_volley_accuracy_weight_metric.calculate_first_volley_accuracy_weight(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if first_volley_accuracy_weight_metric_tournament:
            first_volley_accuracy_weight_metric_tournament.calculate_first_volley_accuracy_weight_tournament(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if first_volley_bps_weighted_accuracy_metric:
            first_volley_bps_weighted_accuracy_metric.calculate_first_volley_bps_weighted_accuracy(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if first_volley_bps_weighted_accuracy_tournament_metric:
            first_volley_bps_weighted_accuracy_tournament_metric.calculate_first_volley_bps_weighted_accuracy_tournament(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        if fire_time_weight_metric:
            fire_time_weight_metric.calculate_fire_time_weight(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])

        if opr:
            opr.add_match(match.red_alliance, current_match_data["red_team_hits"], match.blue_alliance, current_match_data["blue_team_hits"])
            opr.calculate_opr()

        match_results.append(current_match_data)

        if (i + 1) % notification_step == 0:
            if fire_rate_metric:
                total_score = sum(robot_scores.values())

            if volley_avg_rate_fixed_window_metric:
                match_total_volley_avg_window_scouted = 0
                for robot in current_match_data["blue_team_robots"]:
                    shots_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_shots'])
                    hits_volley_error_rate = calculate_error(volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score'], robot['total_hits'])
                    match_total_volley_avg_window_scouted += volley_avg_rate_fixed_window_metric.get_volley_scores()[robot['name']]['volleys_score']

                for robot in current_match_data["blue_team_robots"]:
                    volley_avg_rate_fixed_window_metric.reset_robot_volleys(robot['name'])

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

    robot_names_list = list(final_robot_stats.keys()) # get the list of names
    robot_names_list.sort() # sort them (look better)

    for name in robot_names_list:
        data = final_robot_stats[name]

        if fire_rate_metric:
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
        if fire_rate_metric:
            fire_rate_scouted = robot_avg_fire_rate * data['total_fire_time']
            fire_rate_error = calculate_error(fire_rate_scouted, hits)

    # Error calculation - only for enabled metrics
    errors = {}
    robot_count = len(robot_names_list)

    for robot_name in robot_names_list:
        robot_stats = final_robot_stats[robot_name]

        actual_hits = robot_stats["total_shots_hit"]
        actual_shots = robot_stats["total_shots_fired"]
        scouted_shots = robot_stats["total_shots_scouted"]

        # Magazine errors (always computed since they use raw scouting data)
        magazine_error = calculate_error(scouted_shots, actual_hits)
        errors["magazine_error"] = errors.get("magazine_error", 0) + magazine_error

        magazine_shots_error = calculate_error(scouted_shots, actual_shots)
        errors["magazine_shots_error"] = errors.get("magazine_shots_error", 0) + magazine_shots_error

        if fire_rate_metric:
            robot_avg_fire_rate = fire_rate_metric.get_averages()[robot_name][1]
            fire_rate_scouted_hits = robot_avg_fire_rate * robot_stats['total_fire_time']
            fire_rate_error = calculate_error(fire_rate_scouted_hits, actual_hits)
            errors["fire_rate_error"] = errors.get("fire_rate_error", 0) + fire_rate_error

        if volley_avg_rate_fixed_window_metric:
            volley_avg_rate_total = robot_stats['total_VolleyAvgRate']
            volley_error = calculate_error(volley_avg_rate_total, actual_hits)
            errors["volley_error"] = errors.get("volley_error", 0) + volley_error
            volley_shots_error = calculate_error(volley_avg_rate_total, actual_shots)
            errors["volley_shots_error"] = errors.get("volley_shots_error", 0) + volley_shots_error

        if opr:
            opr_value = opr.get_opr()[robot_name]
            matches_played = robot_stats['matches_played']
            real_hits_per_match = actual_hits / matches_played
            opr_error = calculate_error(opr_value, real_hits_per_match)
            errors["opr_error"] = errors.get("opr_error", 0) + opr_error

        if weight_based_max_fire_rate_metric:
            err = calculate_error(weight_based_max_fire_rate_metric.get_final_scores()[robot_name], actual_hits)
            errors["weight_based_max_fire_rate_error"] = errors.get("weight_based_max_fire_rate_error", 0) + err

        if weight_based_metric:
            err = calculate_error(weight_based_metric.get_final_scores()[robot_name], actual_hits)
            errors["weight_based_error"] = errors.get("weight_based_error", 0) + err

        if weight_based_first_volley_metric:
            err = calculate_error(weight_based_first_volley_metric.get_final_scores()[robot_name], actual_hits)
            errors["weight_based_first_volley_error"] = errors.get("weight_based_first_volley_error", 0) + err

        if first_volley_accuracy_weight_metric:
            err = calculate_error(first_volley_accuracy_weight_metric.get_final_scores()[robot_name], actual_hits)
            errors["first_volley_accuracy_weight_error"] = errors.get("first_volley_accuracy_weight_error", 0) + err

        if first_volley_accuracy_weight_metric_tournament:
            err = calculate_error(first_volley_accuracy_weight_metric_tournament.get_final_scores()[robot_name], actual_hits)
            errors["first_volley_accuracy_weight_tournament_error"] = errors.get("first_volley_accuracy_weight_tournament_error", 0) + err

        if first_volley_bps_weighted_accuracy_metric:
            err = calculate_error(first_volley_bps_weighted_accuracy_metric.get_final_scores()[robot_name], actual_hits)
            errors["first_volley_bps_weighted_accuracy_error"] = errors.get("first_volley_bps_weighted_accuracy_error", 0) + err

        if first_volley_bps_weighted_accuracy_tournament_metric:
            err = calculate_error(first_volley_bps_weighted_accuracy_tournament_metric.get_final_scores()[robot_name], actual_hits)
            errors["first_volley_bps_weighted_accuracy_tournament_error"] = errors.get("first_volley_bps_weighted_accuracy_tournament_error", 0) + err

        if fire_time_weight_metric:
            err = calculate_error(fire_time_weight_metric.get_final_scores()[robot_name], actual_hits)
            errors["fire_time_weight_error"] = errors.get("fire_time_weight_error", 0) + err

    # Average all errors by robot count
    avg_errors = {key: value / robot_count for key, value in errors.items()}

    # Print enabled metric results
    if "opr_error" in avg_errors:
        print(f"Average OPR Error: {avg_errors['opr_error']:.2f}%")
    if "fire_rate_error" in avg_errors:
        print(f"Average Fire Rate Error: {avg_errors['fire_rate_error']:.2f}%")

    print("-" * 40)

    print(f"Magazine Size Hits Error: {avg_errors.get('magazine_error', 0):.2f}%")
    print(f"Magazine Size Shots Error: {avg_errors.get('magazine_shots_error', 0):.2f}%")

    if "volley_error" in avg_errors:
        print(f"First Volley Hits Error: {avg_errors['volley_error']:.2f}%")
    if "volley_shots_error" in avg_errors:
        print(f"First Volley Shots Error: {avg_errors['volley_shots_error']:.2f}%")

    print("-" * 40)

    if "weight_based_max_fire_rate_error" in avg_errors:
        print(f"Weight Based + Max Fire Rate (Magazine) error rate: {avg_errors['weight_based_max_fire_rate_error']:.2f}%")
    if "weight_based_error" in avg_errors:
        print(f"Weight Based (Magazine) error rate: {avg_errors['weight_based_error']:.2f}%")
    if "weight_based_first_volley_error" in avg_errors:
        print(f"Weight Based (First Volley) error rate: {avg_errors['weight_based_first_volley_error']:.2f}%")
    if "first_volley_accuracy_weight_error" in avg_errors:
        print(f"First Volley Accuracy Weight error rate: {avg_errors['first_volley_accuracy_weight_error']:.2f}%")
    if "first_volley_accuracy_weight_tournament_error" in avg_errors:
        print(f"First Volley Accuracy Weight (Tournament) error rate: {avg_errors['first_volley_accuracy_weight_tournament_error']:.2f}%")
    if "first_volley_bps_weighted_accuracy_error" in avg_errors:
        print(f"First Volley BPS Weighted Accuracy error rate: {avg_errors['first_volley_bps_weighted_accuracy_error']:.2f}%")
    if "first_volley_bps_weighted_accuracy_tournament_error" in avg_errors:
        print(f"First Volley BPS Weighted Accuracy (Tournament) error rate: {avg_errors['first_volley_bps_weighted_accuracy_tournament_error']:.2f}%")
    if "fire_time_weight_error" in avg_errors:
        print(f"Fire Time Weight error rate: {avg_errors['fire_time_weight_error']:.2f}%")

    print("\n") # like alw terminal next to a line is annoying me

    return avg_errors


def print_suite_results(stats, suite_label):
    print(f"\n\n{'='*20} {suite_label} RESULTS {'='*20}\n\n")

    label_map = {
        "magazine_error": "Total avg magazine error",
        "fire_rate_error": "Total avg fire rate error",
        "volley_error": "Total avg volley error",
        "opr_error": "Total avg opr error",
        "magazine_shots_error": "Total avg magazine shots error",
        "volley_shots_error": "Total avg volley shots error",
        "weight_based_max_fire_rate_error": "Total avg weight based max fire rate error",
        "weight_based_error": "Total avg weight based error",
        "weight_based_first_volley_error": "Total avg weight based (first volley BPS) error",
        "first_volley_accuracy_weight_error": "Total avg first volley accuracy weight error",
        "first_volley_accuracy_weight_tournament_error": "Total avg first volley accuracy weight (tournament) error",
        "first_volley_bps_weighted_accuracy_error": "Total avg first volley BPS weighted accuracy error",
        "first_volley_bps_weighted_accuracy_tournament_error": "Total avg first volley BPS weighted accuracy (tournament) error",
        "fire_time_weight_error": "Total avg fire time weight error",
    }

    for key, label in label_map.items():
        if key in stats:
            print(f"{label}: {stats[key]}")


def main():
    print(f"Enabled metrics: {', '.join(sorted(ENABLED_METRICS))}")
    print()

    time_based_robots = get_time_based_robots()
    magazine_robots = get_magazine_robots()

    print(f"Pre-generating {NUMBER_OF_SCHEDULES} schedules...")
    schedules = []
    for s in range(NUMBER_OF_SCHEDULES):
        schedule, score = make_matches(time_based_robots, MATCHES_PER_ROBOT, ITERATIONS)
        schedules.append(schedule)
        print(f"  Schedule {s + 1}/{NUMBER_OF_SCHEDULES} generated (score: {score})")

    magazine_schedules = [remap_schedule(s, time_based_robots, magazine_robots) for s in schedules]

    time_based_stats = run_full_simulation_suite(time_based_robots, "TIME BASED ROBOT CONFIGS", schedules)
    magazine_stats = run_full_simulation_suite(magazine_robots, "MAGAZINE SIZE BASED ROBOT CONFIGS", magazine_schedules)

    print_suite_results(time_based_stats, "TIME BASED ROBOT CONFIGS")
    print_suite_results(magazine_stats, "MAGAZINE SIZE BASED ROBOT CONFIGS")

    print("\n" + "=" * 25)
    print("SIMULATION CONFIGURATION")
    print("=" * 25)
    print(f"Min Time Error: {SCOUT_MIN_TIME_ERROR} | Max Time Error: {SCOUT_MAX_TIME_ERROR}")
    print(f"Magazine Error: {SCOUT_MAGAZINE_ERROR * 100}%")
    print(f"Match Accuracy Variance: {MATCH_ACCURACY_VARIANCE * 100}%")
    print("-" * 40)
    print(f"Robot Config Accuracy: {MIN_ACCURACY * 100}% - {MAX_ACCURACY * 100}%")
    print(f"Robot Config Magazine Size: {MIN_MAGAZINE_SIZE} - {MAX_MAGAZINE_SIZE}")
    print("-" * 40)
    print(f"Number of runs: {NUMBER_OF_RUNS}")
    print(f"Matches per robot: {MATCHES_PER_ROBOT}")
    print(f"Iterations: {ITERATIONS}")
    print("-" * 40)
    print(f"Simulation time step: {SIMULATION_TIME_STEP}")
    print(f"Min number of volleys: {MIN_NUMBER_OF_VOLLEYS}")
    print(f"Max number of volleys: {MAX_NUMBER_OF_VOLLEYS}")
    print(f"Min magazine fill percentage: {MIN_MAGAZINE_FILL_PERCENTAGE}")
    print(f"Max magazine fill percentage: {MAX_MAGAZINE_FILL_PERCENTAGE}")
    print(f"Enabled metrics: {', '.join(sorted(ENABLED_METRICS))}")
    print("\n")

if __name__ == "__main__":
    main()
