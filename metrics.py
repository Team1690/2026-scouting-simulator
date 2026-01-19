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
        give_to_others = [0, 0, 0]

        for _ in range(max_iterations):
            for i, robot in enumerate(robots_stats):
                robot_name = robot["name"]
                robot_total_fire_time = robot["total_fire_time"]

                robot_score = total_score // 3 + give_to_others[i]
                give_to_others[i] = 0

                robot_avg_fire_rate = robot_score / robot_total_fire_time

                if robot_avg_fire_rate > robot["max_fire_rate"]:
                    robot_score = robot_score // 2
                    give_to_others[(i + 1) % len(give_to_others)] = robot_score // 4
                    give_to_others[(i + 2) % len(give_to_others)] = robot_score // 4
                    robot_avg_fire_rate = robot_score / robot_total_fire_time

                self.robot_averages[robot_name][0] += 1
                number_of_matches = self.robot_averages[robot_name][0]
                self.robot_averages[robot_name][1] = (number_of_matches * self.robot_averages[robot_name][1] + robot_avg_fire_rate) / (number_of_matches + 1)
                self.robot_scores[robot_name] = self.robot_averages[robot_name][1] * robot_total_fire_time

        return self.robot_scores

    def get_averages(self):
        return self.robot_averages

    def get_scores(self):
        return self.robot_scores
