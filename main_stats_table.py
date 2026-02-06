from __future__ import annotations
from scouter_model import ScouterModel
from match_maker import make_matches
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
import numpy as np

def calculate_summary_statistics(data):
    if not data:
        return {
            "Mean": 0.0, "Median": 0.0, "Std Dev": 0.0, "Min": 0.0, "Max": 0.0, "Count": 0, "Bias": 0.0
        }

    abs_data = np.abs(data)

    return {
        "Mean": np.mean(abs_data),
        "Median": np.median(abs_data),
        "Std Dev": np.std(abs_data),
        "Min": np.min(abs_data),
        "Max": np.max(abs_data),
        "Count": len(data),
        "Bias": np.mean(data)
    }

def calculate_actual_statistics(actual_list, predicted_list):
    if not actual_list or not predicted_list:
        return {
            "Avg Scored": 0.0, "Median Scored": 0.0, "Avg Predicted": 0.0, "Median Predicted": 0.0, "Real Min": 0.0, "Real Max": 0.0, "Pred Min": 0.0, "Pred Max": 0.0
        }

    return {
        "Avg Scored": np.mean(actual_list),
        "Median Scored": np.median(actual_list),
        "Avg Predicted": np.mean(predicted_list),
        "Median Predicted": np.median(predicted_list),
        "Real Min": np.min(actual_list),
        "Real Max": np.max(actual_list),
        "Pred Min": np.min(predicted_list),
        "Pred Max": np.max(predicted_list)
    }

def run_simulation(all_robots):
    schedule, schedule_score = make_matches(all_robots, MATCHES_PER_ROBOT, ITERATIONS)
    # No need to track match_results for stats unless debugging
    # match_results = []

    scout = ScouterModel(SCOUT_MIN_TIME_ERROR, SCOUT_MAX_TIME_ERROR, SCOUT_MAGAZINE_ERROR)
    fire_rate_metric = IterativeAverageFireRateMetric(all_robots)
    fixed_window_metric = MatchAvgRateFixedWindowMetric()
    volley_avg_rate_fixed_window_metric = VolleyAvgRateFixedWindowMetric(all_robots)
    opr = OPR(all_robots)
    weight_based_max_fire_rate_metric = WeightBasedMaxFireRateMetric(all_robots)
    weight_based_metric = WeightBasedMetric(all_robots)
    weight_based_first_volley_metric = WeightBasedFirstVolleyMetric(all_robots)
    first_volley_accuracy_weight_metric = FirstVolleyAccuracyWeightMetric(all_robots)
    first_volley_accuracy_weight_metric_tournament = FirstVolleyAccuracyWeightMetricTournament(all_robots)
    first_volley_bps_weighted_accuracy_metric = FirstVolleyBPSWeightedAccuracy(all_robots)
    first_volley_bps_weighted_accuracy_tournament_metric = FirstVolleyBPSWeightedAccuracyTournament(all_robots)

    # Temporary storage for robot stats in this run
    current_run_robot_stats = {robot.name: {
        "total_hits": 0, "total_shots": 0, "scouted_shots": 0, "total_fire_time": 0,
        "matches_played": 0, "volleys_fired": 0,
        "total_AvgRateFixedWindow": 0, "total_VolleyAvgRate": 0
    } for robot in all_robots}

    for i, match in enumerate(schedule):
        current_match_data = {
            "red_team_robots": [], "blue_team_robots": [],
            "red_team_hits": 0,
            "blue_team_hits": 0
        }

        # Red Team
        for robot in match.red_alliance:
            stats = scout_robot_match(robot, scout, MATCH_ACCURACY_VARIANCE)
            current_match_data["red_team_robots"].append(stats)
            current_match_data["red_team_hits"] += stats["total_hits"]

            stats["AvgRateFixedWindow"] = fixed_window_metric.calculate_AvgRateFixedWindow(robot.name, stats["total_hits"], stats["total_fire_time"])
            stats["VolleyAvgRate"] = volley_avg_rate_fixed_window_metric.calculate_volley_avg_rate_fixed_window(stats)

        # Metrics for Red
        fire_rate_metric.calculate_score_by_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"], 10)
        weight_based_max_fire_rate_metric.calculate_weight_based_max_fire_rate(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        weight_based_metric.calculate_weight_based_metric(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        weight_based_first_volley_metric.calculate_weight_based_first_volley_metric(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        first_volley_accuracy_weight_metric.calculate_first_volley_accuracy_weight(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        first_volley_accuracy_weight_metric_tournament.calculate_first_volley_accuracy_weight_tournament(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        first_volley_bps_weighted_accuracy_metric.calculate_first_volley_bps_weighted_accuracy(current_match_data["red_team_robots"], current_match_data["red_team_hits"])
        first_volley_bps_weighted_accuracy_tournament_metric.calculate_first_volley_bps_weighted_accuracy_tournament(current_match_data["red_team_robots"], current_match_data["red_team_hits"])

        for robot in current_match_data["red_team_robots"]:
             volley_avg_rate_fixed_window_metric.reset_robot_volleys(robot['name'])

        # Blue Team
        for robot in match.blue_alliance:
            stats = scout_robot_match(robot, scout, MATCH_ACCURACY_VARIANCE)
            current_match_data["blue_team_robots"].append(stats)
            current_match_data["blue_team_hits"] += stats["total_hits"]

            stats["AvgRateFixedWindow"] = fixed_window_metric.calculate_AvgRateFixedWindow(robot.name, stats["total_hits"], stats["total_fire_time"])
            stats["VolleyAvgRate"] = volley_avg_rate_fixed_window_metric.calculate_volley_avg_rate_fixed_window(stats)

        # Metrics for Blue
        fire_rate_metric.calculate_score_by_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"], 10)
        weight_based_max_fire_rate_metric.calculate_weight_based_max_fire_rate(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        weight_based_metric.calculate_weight_based_metric(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        weight_based_first_volley_metric.calculate_weight_based_first_volley_metric(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        first_volley_accuracy_weight_metric.calculate_first_volley_accuracy_weight(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        first_volley_accuracy_weight_metric_tournament.calculate_first_volley_accuracy_weight_tournament(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        first_volley_bps_weighted_accuracy_metric.calculate_first_volley_bps_weighted_accuracy(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])
        first_volley_bps_weighted_accuracy_tournament_metric.calculate_first_volley_bps_weighted_accuracy_tournament(current_match_data["blue_team_robots"], current_match_data["blue_team_hits"])

        for robot in current_match_data["blue_team_robots"]:
             volley_avg_rate_fixed_window_metric.reset_robot_volleys(robot['name'])

        opr.add_match(match.red_alliance, current_match_data["red_team_hits"], match.blue_alliance, current_match_data["blue_team_hits"])
        opr.calculate_opr()

        # Update stats
        for team_robots in [current_match_data["red_team_robots"], current_match_data["blue_team_robots"]]:
            for robot_data in team_robots:
                name = robot_data["name"]
                current_run_robot_stats[name]["total_shots"] += robot_data["total_shots"]
                current_run_robot_stats[name]["total_hits"] += robot_data["total_hits"]
                current_run_robot_stats[name]["scouted_shots"] += robot_data["total_scouted_shots"]
                current_run_robot_stats[name]["matches_played"] += 1
                current_run_robot_stats[name]["volleys_fired"] += robot_data["volleys"]
                current_run_robot_stats[name]["total_fire_time"] += robot_data["total_fire_time"]
                current_run_robot_stats[name]["total_AvgRateFixedWindow"] += robot_data["AvgRateFixedWindow"]
                current_run_robot_stats[name]["total_VolleyAvgRate"] += robot_data["VolleyAvgRate"]

    # Calculate errors for this run
    errors = {
        "Magazine Size Hits Error": [],
        "Max Fire Rate Hits Error": [],
        "First Volley Hits Error": [],
        "OPR": [],
        "Weight Based + Max Fire Rate (Magazine) Hits Error": [],
        "Weight Based (Magazine) Hits Error": [],
        "Weight Based (First Volley) Hits Error": [],
        "First Volley Accuracy Weight Hits Error": [],
        "Magazine Size Shots Error": [],
        "First Volley Shots Error": [],
        "First Volley Accuracy Weight (Tournament) Hits Error": [],
        "First Volley BPS Weighted Accuracy Hits Error": [],
        "First Volley BPS Weighted Accuracy (Tournament) Hits Error": []
    }

    # Track actual values for each metric (actual, predicted)
    actual_values = {
        "Magazine Size Hits Error": {"actual": [], "predicted": []},
        "Max Fire Rate Hits Error": {"actual": [], "predicted": []},
        "First Volley Hits Error": {"actual": [], "predicted": []},
        "OPR": {"actual": [], "predicted": []},
        "Weight Based + Max Fire Rate (Magazine) Hits Error": {"actual": [], "predicted": []},
        "Weight Based (Magazine) Hits Error": {"actual": [], "predicted": []},
        "Weight Based (First Volley) Hits Error": {"actual": [], "predicted": []},
        "First Volley Accuracy Weight Hits Error": {"actual": [], "predicted": []},
        "Magazine Size Shots Error": {"actual": [], "predicted": []},
        "First Volley Shots Error": {"actual": [], "predicted": []},
        "First Volley Accuracy Weight (Tournament) Hits Error": {"actual": [], "predicted": []},
        "First Volley BPS Weighted Accuracy Hits Error": {"actual": [], "predicted": []},
        "First Volley BPS Weighted Accuracy (Tournament) Hits Error": {"actual": [], "predicted": []}
    }

    for robot_name, stats in current_run_robot_stats.items():
        actual_hits = stats["total_hits"]
        actual_shots = stats["total_shots"]
        scouted_shots = stats["scouted_shots"]

        # Magazine Hits Error
        errors["Magazine Size Hits Error"].append(calculate_error(scouted_shots, actual_hits))
        actual_values["Magazine Size Hits Error"]["actual"].append(actual_hits)
        actual_values["Magazine Size Hits Error"]["predicted"].append(scouted_shots)

        # Magazine Shots Error
        errors["Magazine Size Shots Error"].append(calculate_error(scouted_shots, actual_shots))
        actual_values["Magazine Size Shots Error"]["actual"].append(actual_shots)
        actual_values["Magazine Size Shots Error"]["predicted"].append(scouted_shots)

        # Max Fire Rate Hits Error
        robot_avg_fire_rate = fire_rate_metric.get_averages()[robot_name][1]
        fire_rate_scouted_hits = robot_avg_fire_rate * stats['total_fire_time']
        errors["Max Fire Rate Hits Error"].append(calculate_error(fire_rate_scouted_hits, actual_hits))
        actual_values["Max Fire Rate Hits Error"]["actual"].append(actual_hits)
        actual_values["Max Fire Rate Hits Error"]["predicted"].append(fire_rate_scouted_hits)

        # Volley Hits Error
        volley_avg_rate_total = stats['total_VolleyAvgRate']
        errors["First Volley Hits Error"].append(calculate_error(volley_avg_rate_total, actual_hits))
        actual_values["First Volley Hits Error"]["actual"].append(actual_hits)
        actual_values["First Volley Hits Error"]["predicted"].append(volley_avg_rate_total)

        # Volley Shots Error
        errors["First Volley Shots Error"].append(calculate_error(volley_avg_rate_total, actual_shots))
        actual_values["First Volley Shots Error"]["actual"].append(actual_shots)
        actual_values["First Volley Shots Error"]["predicted"].append(volley_avg_rate_total)

        # OPR
        opr_value = opr.get_opr().get(robot_name, 0)
        real_hits_per_match = actual_hits / stats['matches_played'] if stats['matches_played'] > 0 else 0
        errors["OPR"].append(calculate_error(opr_value, real_hits_per_match))
        actual_values["OPR"]["actual"].append(real_hits_per_match)
        actual_values["OPR"]["predicted"].append(opr_value)

        # Weight Based Metrics
        weight_based_max_fire_rate_prediction = weight_based_max_fire_rate_metric.get_final_scores()[robot_name]
        errors["Weight Based + Max Fire Rate (Magazine) Hits Error"].append(calculate_error(weight_based_max_fire_rate_prediction, actual_hits))
        actual_values["Weight Based + Max Fire Rate (Magazine) Hits Error"]["actual"].append(actual_hits)
        actual_values["Weight Based + Max Fire Rate (Magazine) Hits Error"]["predicted"].append(weight_based_max_fire_rate_prediction)

        weight_based_prediction = weight_based_metric.get_final_scores()[robot_name]
        errors["Weight Based (Magazine) Hits Error"].append(calculate_error(weight_based_prediction, actual_hits))
        actual_values["Weight Based (Magazine) Hits Error"]["actual"].append(actual_hits)
        actual_values["Weight Based (Magazine) Hits Error"]["predicted"].append(weight_based_prediction)

        weight_based_first_volley_prediction = weight_based_first_volley_metric.get_final_scores()[robot_name]
        errors["Weight Based (First Volley) Hits Error"].append(calculate_error(weight_based_first_volley_prediction, actual_hits))
        actual_values["Weight Based (First Volley) Hits Error"]["actual"].append(actual_hits)
        actual_values["Weight Based (First Volley) Hits Error"]["predicted"].append(weight_based_first_volley_prediction)

        first_volley_accuracy_weight_prediction = first_volley_accuracy_weight_metric.get_final_scores()[robot_name]
        errors["First Volley Accuracy Weight Hits Error"].append(calculate_error(first_volley_accuracy_weight_prediction, actual_hits))
        actual_values["First Volley Accuracy Weight Hits Error"]["actual"].append(actual_hits)
        actual_values["First Volley Accuracy Weight Hits Error"]["predicted"].append(first_volley_accuracy_weight_prediction)

        first_volley_accuracy_weight_tournament_prediction = first_volley_accuracy_weight_metric_tournament.get_final_scores()[robot_name]
        errors["First Volley Accuracy Weight (Tournament) Hits Error"].append(calculate_error(first_volley_accuracy_weight_tournament_prediction, actual_hits))
        actual_values["First Volley Accuracy Weight (Tournament) Hits Error"]["actual"].append(actual_hits)
        actual_values["First Volley Accuracy Weight (Tournament) Hits Error"]["predicted"].append(first_volley_accuracy_weight_tournament_prediction)

        first_volley_bps_weighted_accuracy_prediction = first_volley_bps_weighted_accuracy_metric.get_final_scores()[robot_name]
        errors["First Volley BPS Weighted Accuracy Hits Error"].append(calculate_error(first_volley_bps_weighted_accuracy_prediction, actual_hits))
        actual_values["First Volley BPS Weighted Accuracy Hits Error"]["actual"].append(actual_hits)
        actual_values["First Volley BPS Weighted Accuracy Hits Error"]["predicted"].append(first_volley_bps_weighted_accuracy_prediction)

        first_volley_bps_weighted_accuracy_tournament_prediction = first_volley_bps_weighted_accuracy_tournament_metric.get_final_scores()[robot_name]
        errors["First Volley BPS Weighted Accuracy (Tournament) Hits Error"].append(calculate_error(first_volley_bps_weighted_accuracy_tournament_prediction, actual_hits))
        actual_values["First Volley BPS Weighted Accuracy (Tournament) Hits Error"]["actual"].append(actual_hits)
        actual_values["First Volley BPS Weighted Accuracy (Tournament) Hits Error"]["predicted"].append(first_volley_bps_weighted_accuracy_tournament_prediction)

    return errors, actual_values

def run_full_simulation_suite(robot_getter, suite_label):
    aggregated_errors = {
        "Magazine Size Hits Error": [],
        "Max Fire Rate Hits Error": [],
        "First Volley Hits Error": [],
        "OPR": [],
        "Weight Based + Max Fire Rate (Magazine) Hits Error": [],
        "Weight Based (Magazine) Hits Error": [],
        "Weight Based (First Volley) Hits Error": [],
        "First Volley Accuracy Weight Hits Error": [],
        "Magazine Size Shots Error": [],
        "First Volley Shots Error": [],
        "First Volley Accuracy Weight (Tournament) Hits Error": [],
        "First Volley BPS Weighted Accuracy Hits Error": [],
        "First Volley BPS Weighted Accuracy (Tournament) Hits Error": []
    }

    aggregated_actual_values = {
        "Magazine Size Hits Error": {"actual": [], "predicted": []},
        "Max Fire Rate Hits Error": {"actual": [], "predicted": []},
        "First Volley Hits Error": {"actual": [], "predicted": []},
        "OPR": {"actual": [], "predicted": []},
        "Weight Based + Max Fire Rate (Magazine) Hits Error": {"actual": [], "predicted": []},
        "Weight Based (Magazine) Hits Error": {"actual": [], "predicted": []},
        "Weight Based (First Volley) Hits Error": {"actual": [], "predicted": []},
        "First Volley Accuracy Weight Hits Error": {"actual": [], "predicted": []},
        "Magazine Size Shots Error": {"actual": [], "predicted": []},
        "First Volley Shots Error": {"actual": [], "predicted": []},
        "First Volley Accuracy Weight (Tournament) Hits Error": {"actual": [], "predicted": []},
        "First Volley BPS Weighted Accuracy Hits Error": {"actual": [], "predicted": []},
        "First Volley BPS Weighted Accuracy (Tournament) Hits Error": {"actual": [], "predicted": []}
    }

    all_robots = robot_getter()

    print(f"\nStarting {suite_label} with {NUMBER_OF_RUNS} runs...")

    for i in range(NUMBER_OF_RUNS):
        if (i+1) % 5 == 0 or i == 0:
            print(f"Run {i + 1} / {NUMBER_OF_RUNS}")

        run_errors, run_actual_values = run_simulation(all_robots)

        for metric, error_list in run_errors.items():
            aggregated_errors[metric].extend(error_list)

        for metric, values in run_actual_values.items():
            aggregated_actual_values[metric]["actual"].extend(values["actual"])
            aggregated_actual_values[metric]["predicted"].extend(values["predicted"])

    return aggregated_errors, aggregated_actual_values

def print_table(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    header_row = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    for row in rows:
        print(" | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)))

def print_suite_results(stats, actual_values, suite_label):
    print(f"\n\n{'='*30} {suite_label} RESULTS {'='*30}\n")

    error_rows = []
    actual_rows = []

    for metric, errors in stats.items():
        summary = calculate_summary_statistics(errors)
        actual_stats = calculate_actual_statistics(
            actual_values[metric]["actual"],
            actual_values[metric]["predicted"]
        )

        error_row = [
            metric,
            f"{summary['Mean']:.2f}%",
            f"{summary['Median']:.2f}%",
            f"{summary['Std Dev']:.2f}%",
            f"{summary['Min']:.2f}%",
            f"{summary['Max']:.2f}%",
            f"{summary['Bias']:.2f}%",
            summary['Median']  # For sorting
        ]
        error_rows.append(error_row)

        actual_row = [
            metric,
            f"{actual_stats['Avg Scored']:.2f}",
            f"{actual_stats['Median Scored']:.2f}",
            f"{actual_stats['Avg Predicted']:.2f}",
            f"{actual_stats['Median Predicted']:.2f}",
            f"{actual_stats['Real Min']:.2f}",
            f"{actual_stats['Real Max']:.2f}",
            f"{actual_stats['Pred Min']:.2f}",
            f"{actual_stats['Pred Max']:.2f}",
            summary['Median']  # For sorting (same order as error table)
        ]
        actual_rows.append(actual_row)

    # Sort both tables by median error
    error_rows.sort(key=lambda x: x[-1])
    actual_rows.sort(key=lambda x: x[-1])

    # Remove the sorting key from rows
    for row in error_rows:
        row.pop()
    for row in actual_rows:
        row.pop()

    # there was a print isscue and deviding it into two tables fixed it
    # Print Table 1: Error Statistics
    print("--- Error Statistics ---\n")
    error_headers = ["Metric", "Mean", "Median", "Std Dev", "Min", "Max", "Bias"]
    print_table(error_headers, error_rows)

    # Print Table 2: Actual Value Statistics
    print("\n--- Actual Value Statistics ---\n")
    actual_headers = ["Metric", "Avg Scored", "Median Scored", "Avg Predicted", "Median Predicted", "Real Min", "Real Max", "Pred Min", "Pred Max"]
    print_table(actual_headers, actual_rows)

def main():
    print(f"Running simulation with:")
    print(f"Runs: {NUMBER_OF_RUNS}")
    print(f"Matches per robot: {MATCHES_PER_ROBOT}")
    print(f"Iterations: {ITERATIONS}")
    print("-" * 40)

    time_based_stats, time_based_actual = run_full_simulation_suite(get_time_based_robots, "TIME BASED ROBOT CONFIGS")
    magazine_stats, magazine_actual = run_full_simulation_suite(get_magazine_robots, "MAGAZINE SIZE BASED ROBOT CONFIGS")

    print_suite_results(time_based_stats, time_based_actual, "TIME BASED ROBOT CONFIGS")
    print_suite_results(magazine_stats, magazine_actual, "MAGAZINE SIZE BASED ROBOT CONFIGS")

if __name__ == "__main__":
    main()
