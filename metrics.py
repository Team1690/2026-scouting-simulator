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

    # //todo: implement add_match

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
                if team in team_to_index:
                    M[i][team_to_index[team]] = 1 # for each team in the same match set the matrix value to 1

        M_transpose = M.T # M transpose
        A = M_transpose @ M # A = M^T * M | left side of the normal equation
        B = M_transpose @ s # B = M^T * s | right side of the normal equation

        # solve the linear system A * oprs = B using the least squares
        # np.linalg.lstsq returns a tuple with 4 values: (solution, residuals, rank, singular_values)
        solution, residuals, rank, s_values = np.linalg.lstsq(A, B, rcond=None) # rcond=none means it automatically determines an appropriate cutoff value
        oprs = solution # just looks better

        team_oprs = {} # tuple of (team, opr)
        for team, opr in zip(sorted_teams, oprs): # zip() pairs the first team with the first OPR and so on
            team_oprs[team] = opr

        return team_oprs
