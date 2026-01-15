from robot_model import RobotModel
import math
import random

class Match:
    def __init__(self, red_alliance: tuple[RobotModel, RobotModel, RobotModel], blue_alliance: tuple[RobotModel, RobotModel, RobotModel]):
        self.red_alliance = red_alliance
        self.blue_alliance = blue_alliance

    def __str__(self):
        return f"Red: {self.red_alliance}, Blue: {self.blue_alliance}"

def make_matches(robots: list[RobotModel], matches_per_robot: int, iterations: int) -> tuple[list[Match], int]:
    assert len(robots) % 6 == 0, "Number of robots must be a multiple of 6"

    best_scheduled_score = 0
    best_matches: list[Match] = []

    for iteration in range(iterations):
        matches: list[Match] = []

        for _ in range(matches_per_robot):
            shuffled_robots = robots.copy()
            random.shuffle(shuffled_robots)

            i = 0
            while i < len(shuffled_robots):
                red_alliance = shuffled_robots[i:i + 3]
                blue_alliance = shuffled_robots[i + 3:i + 6]
                matches.append(Match(red_alliance, blue_alliance))
                i += 6

        scheduled_scores: dict[str, dict[str, int]] = {}
        for robot in robots:
            scheduled_scores[robot.name] = {}

        for match in matches:
            for i in range(3):
                for j in range(3):
                    if i != j:
                        scheduled_scores[match.red_alliance[i]][match.red_alliance[j]] += 1
                        scheduled_scores[match.red_alliance[i]][match.red_alliance[j]] *= 3

            for i in range(3):
                for j in range(3):
                    scheduled_scores[match.red_alliance[i]][match.blue_alliance[j]] += 1
                    scheduled_scores[match.red_alliance[i]][match.blue_alliance[j]] *= 2

            for i in range(3):
                for j in range(3):
                    if i != j:
                        scheduled_scores[match.blue_alliance[i]][match.blue_alliance[j]] += 1
                        scheduled_scores[match.blue_alliance[i]][match.blue_alliance[j]] *= 3

            for i in range(3):
                for j in range(3):
                    scheduled_scores[match.blue_alliance[i]][match.red_alliance[j]] += 1
                    scheduled_scores[match.blue_alliance[i]][match.red_alliance[j]] *= 2

        scheduled_score = 0
        for scores in scheduled_scores.values():
            scheduled_score += sum(scores.values())

        if scheduled_score < best_scheduled_score or not best_matches:
            best_scheduled_score = scheduled_score
            best_matches = matches.copy()

    return best_matches, best_scheduled_score
