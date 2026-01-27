import numpy as np
import random
from robot_model import RobotModel

class MagazineSizeMetric:
    def __init__(self):
        self.buckets = [25, 50, 75, 100]

    def recorded_observation_by_scouter(self, time_observed, actual_percentage):
        percentage_val = actual_percentage * 100 # convert from a number between 0 and 1 to a percentage (between 0 and 100)

        closest_bucket = self.buckets[0] # start with an initial closest guess
        min_diff = abs(percentage_val - self.buckets[0]) # start with an initial closest diff

        for bucket in self.buckets: # loop through all buckets to find the real closest one (ik there is a better way but this what I could think of)
            diff = abs(percentage_val - bucket)
            if diff < min_diff:
                min_diff = diff
                closest_bucket = bucket

        return time_observed, closest_bucket

class IterativeAverageFireRateMetric:
    def __init__(self, all_robots):
        self.robot_averages = {}
        for robot in all_robots:
            self.robot_averages[robot.name] = [0, 0]

    def calculate_score_by_fire_rate(self, robots_stats, total_score, max_iterations):
        self.robot_scores = {}
        robot_match_score = [total_score / 3, total_score / 3, total_score / 3]
        final_fire_rates = {}

        for iteration in range(max_iterations):
            rebalanced = False
            for i, robot in enumerate(robots_stats):
                robot_name = robot["name"]
                robot_total_fire_time = robot["total_fire_time"]
                robot_score = robot_match_score[i]
                robot_avg_fire_rate = robot_score / robot_total_fire_time
                if robot_avg_fire_rate > robot["max_fire_rate"] and iteration < max_iterations - 1:
                    robot_match_score[i] = robot_score / 2
                    robot_avg_fire_rate = robot_match_score[i] / robot_total_fire_time
                    robot_match_score[(i + 1) % len(robot_match_score)] += robot_score / 4
                    robot_match_score[(i + 2) % len(robot_match_score)] += robot_score / 4
                    rebalanced = True

                final_fire_rates[robot_name] = (robot_avg_fire_rate, robot_total_fire_time) # Store this robots final calculated fire rate and their total firing time

            if not rebalanced:
                break

        # update averages across matches
        for robot_name in final_fire_rates:
            robot_data = final_fire_rates[robot_name]
            robot_avg_fire_rate = robot_data[0]
            robot_total_fire_time = robot_data[1]

            number_of_matches = self.robot_averages[robot_name][0] # update number of matches
            self.robot_averages[robot_name][1] = (number_of_matches * self.robot_averages[robot_name][1] + robot_avg_fire_rate) / (number_of_matches + 1) # calculate new average
            self.robot_scores[robot_name] = self.robot_averages[robot_name][1] * robot_total_fire_time
            # self.robot_scores[robot_name] = robot_avg_fire_rate * robot_total_fire_time
            self.robot_averages[robot_name][0] += 1 # track how many matches this robot has been in

        return self.robot_scores

    def get_averages(self):
        return self.robot_averages

    def get_scores(self):
        return self.robot_scores

class OPR:
    def __init__(self, all_robots):
        self.teams = all_robots
        self.match_observations = [] # (list_of_teams, score)
        self.opr_values = {}

    def add_match(self, red_teams, red_score, blue_teams, blue_score):
        self.match_observations.append((red_teams, red_score))
        self.match_observations.append((blue_teams, blue_score))

    def calculate_opr(self):
        sorted_teams = sorted(list(self.teams), key=lambda team: team.name)
        n_teams = len(sorted_teams)

        # each team to a matrix index (0 to N-1)
        team_to_index = {}
        for i, team in enumerate(sorted_teams):
            team_to_index[team] = i

        n_matches = len(self.match_observations)
        M = np.zeros((n_matches, n_teams)) # Normal Equation matrix (M)
        s = np.zeros(n_matches) # Normal Equation vector (s)

        for i, (teams, score) in enumerate(self.match_observations): # take all the teams in the match and the score
            s[i] = score
            for team in teams:
                if team in team_to_index.keys():
                    M[i][team_to_index[team]] = 1 # for each team in the same match set the matrix value to 1

        M_transpose = M.T # M transpose
        A = M_transpose @ M # A = M^T * M | left side of the normal equation
        B = M_transpose @ s # B = M^T * s | right side of the normal equation

        # solve the linear system A * oprs = B using the least squares
        # np.linalg.lstsq returns a tuple with 4 values: (solution, residuals, rank, singular_values)
        solution, residuals, rank, s_values = np.linalg.lstsq(A, B, rcond=None) # rcond=none means it automatically determines an appropriate cutoff value
        oprs = solution # just looks better

        for team, opr in zip(sorted_teams, oprs): # zip() pairs the first team with the first OPR and so on
            self.opr_values[team.name] = opr

        return self.opr_values

    def get_opr(self):
        return self.opr_values

class MatchAvgRateFixedWindowMetric:
    def __init__(self):
        self.robot_rates = {}

    def calculate_AvgRateFixedWindow(self, robot_name, actual_hits, time_taken):
        if robot_name in self.robot_rates: # if we already have a rate for this robot then use it for the time taken
            saved_rate = self.robot_rates[robot_name]
            fixed_window_scouted_hits = saved_rate * time_taken
            return fixed_window_scouted_hits
        else:
            rate = actual_hits / time_taken

            self.robot_rates[robot_name] = rate

            return actual_hits

    def get_rates(self):
        return self.robot_rates

class VolleyAvgRateFixedWindowMetric:
    def __init__(self, all_robots):
        self.robot_volley_scores: dict[str, float] = {}

        for robot in all_robots:
            self.robot_volley_scores[robot.name] = {"first_volley_rate": 0, "volleys_score": 0}

    def calculate_volley_avg_rate_fixed_window(self, stats: dict):
        if self.robot_volley_scores[stats["name"]]["first_volley_rate"] == 0:
            self.robot_volley_scores[stats["name"]]["first_volley_rate"] = (stats["stats_per_volley"][0]["points"] + stats["stats_per_volley"][0]["misses"]) / stats["stats_per_volley"][0]["time_to_empty"]

        robot_volley_score = self.robot_volley_scores[stats["name"]]["first_volley_rate"] * stats["total_fire_time"]
        self.robot_volley_scores[stats["name"]]["volleys_score"] = robot_volley_score
        return robot_volley_score

    def reset_robot_volleys(self, robot_name):
        self.robot_volley_scores[robot_name]["first_volley_rate"] = 0
        self.robot_volley_scores[robot_name]["volleys_score"] = 0

    def get_volley_scores(self):
        return self.robot_volley_scores

class WeightBasedMaxFireRateMetric:
    def __init__(self, all_robots):
        self.final_scores = {}
        for robot in all_robots:
            self.final_scores[robot.name] = 0.0

    def calculate_weight_based_max_fire_rate(self, robot_stats: dict, total_score: int):
        scouted_shots = {}
        capacities = {}
        uncapped = []
        final_scores = {}

        for robot_stats in robot_stats:
            scouted_shots[robot_stats["name"]] = robot_stats["total_scouted_shots"]
            capacities[robot_stats["name"]] = robot_stats["max_fire_rate"] * robot_stats["total_fire_time"]
            final_scores[robot_stats["name"]] = 0.0
            uncapped.append(robot_stats["name"])

        remaining_score = total_score

        while uncapped:
            current_total_shots = sum(scouted_shots[robot_name] for robot_name in uncapped)
            above_cap = []

            for robot_name in uncapped:
                if current_total_shots > 0:
                    share = remaining_score * scouted_shots[robot_name] / current_total_shots

                    if share > capacities[robot_name]:
                        above_cap.append(robot_name)

            if not above_cap:
               for robot_name in uncapped:
                   final_scores[robot_name] += remaining_score * scouted_shots[robot_name] / current_total_shots
               break
            else:
                for robot_name in above_cap:
                    final_scores[robot_name] = capacities[robot_name]
                    remaining_score -= capacities[robot_name]
                    uncapped.remove(robot_name)

        for robot_name, final_score in final_scores.items():
            self.final_scores[robot_name] += final_score

    def get_final_scores(self):
        return self.final_scores


class WeightBasedMetric:
    def __init__(self, all_robots):
        self.final_scores = {}
        for robot in all_robots:
            self.final_scores[robot.name] = 0.0

    def calculate_weight_based_metric(self, robot_stats: dict, total_score: int):
        scouted_shots = {}
        capacities = {}
        uncapped = []
        final_scores = {}

        for robot_stats in robot_stats:
            scouted_shots[robot_stats["name"]] = robot_stats["total_scouted_shots"]
            capacities[robot_stats["name"]] = robot_stats["max_fire_rate"] * robot_stats["total_fire_time"]
            final_scores[robot_stats["name"]] = 0.0
            uncapped.append(robot_stats["name"])

        remaining_score = total_score

        current_total_shots = sum(scouted_shots[robot_name] for robot_name in uncapped)

        for robot_name in uncapped:
            final_scores[robot_name] += remaining_score * scouted_shots[robot_name] / current_total_shots

        for robot_name, final_score in final_scores.items():
            self.final_scores[robot_name] += final_score

    def get_final_scores(self):
        return self.final_scores
