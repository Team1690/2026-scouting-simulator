from __future__ import annotations
import random
import math

class RobotModel:
    def __init__(self, name: str, magazine_size: int, accuracy: float, fire_rate_function):
        self.name = name
        self.magazine_size = magazine_size
        self.accuracy = accuracy
        self.fire_rate_function = fire_rate_function

    def get_points_for_magazine(self, magazine_percentage: float):
        hits = 0
        misses = 0
        
        shots_count = round(self.magazine_size * magazine_percentage)
        for _ in range(shots_count):
            if random.random() < self.accuracy:
                hits += 1
            else:
                misses += 1

        return hits, misses

    def time_to_deplete(self,  dt: float, magazine_percentage: float):
        t = 0.0
        current_fuel_in_magazine = round(self.magazine_size * magazine_percentage)
        
        max_time = 1000.0

        while current_fuel_in_magazine > 0:
            if t > max_time:
                return float('inf')
                
            current_fuel_in_magazine -= self.fire_rate_function(t) * dt + random.gauss(0, 1) # add some jitter
            t += dt
            
        return t

def quick_fire(t: float):
    return 2.0 if (t - math.floor(t)) < 0.8 else 0.0

def inconsistent_jam_fire(t: float): # askof's function - peeks at 8,
    t = t % 10 # loop the pattern every 10 seconds (cuz this function stops at 10 x=10 so we need to loop until we finish the fuel at the magazine)
    if 0 <= t <= 1.5:
        return 4 * t
    elif 1.5 < t <= 2:
        return -2 * t + 9
    elif 2 < t <= 3:
        return 5 + 3 * math.log(1 + (math.e - 1) * (t - 2))
    elif 3 < t < 4:
        return 0.0
    elif 4 <= t <= 6:
        return 4 * t - 16
    elif 6 < t <= 7.5:
        return -4 * t + 32
    elif 7.5 < t <= 8:
        return 2 * t - 13
    elif 8 < t <= 10:
        return -1.5 * t + 15
    else:
        return 0.0


class ScoutModel:
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


def calculate_error(observed: float, actual: float):
    if actual == 0:
        return 0
    return 100 * abs(observed - actual) / actual

def main():
    robots_to_simulate = ["Quick fire", "Log", "Inconsistent shooting with jam - Askof's function"]

    robot1 = RobotModel(
        name="Quick fire",
        magazine_size=80,
        accuracy=0.9,
        fire_rate_function=lambda t: quick_fire(t)
    )

    robot2 = RobotModel(
        name="Log",
        magazine_size=100,
        accuracy=0.9, 
        fire_rate_function=lambda t: 2 * math.log(t + 1)
    )

    robot3 = RobotModel(
        name="Inconsistent shooting with jam - Askof's function",
        magazine_size=120,
        accuracy=0.9,
        fire_rate_function=inconsistent_jam_fire
    )

    all_robots = [robot1, robot2, robot3]

    scout = ScoutModel() # the simulated scouter

    robots_data = [] # a robot spesific data

    for robot in all_robots:
        if robot.name not in robots_to_simulate: # check if we want to run this robot
            continue

        total_shots = 0
        total_hits = 0
        total_scouted_hits = 0

        number_of_volleys = random.randint(1, 6) # random number of vollies to simulate
        for i in range(number_of_volleys):
            print(f"\nSimulation run {i + 1} / {number_of_volleys}")

            magazine_percentage = random.uniform(0.1, 1.0) # random fill between 10% and 100% for the magazine
            print(f"Starting simulation (Fuel Level: {magazine_percentage * 100:.1f}%)")

            print(f"\nSimulation for: {robot.name}")

            print(f"Model settings: Magazine Size: {robot.magazine_size}, Accuracy: {robot.accuracy}")
            print("\n")
            
            current_fuel = round(magazine_percentage * robot.magazine_size)
            total_shots += current_fuel # add the fuel to the total shots
            print(f"Fuel amount in magazine: {current_fuel}")

            points, misses = robot.get_points_for_magazine(magazine_percentage)
            total_hits += points # add the points to the total hits
            
            time_to_empty = robot.time_to_deplete(0.05, magazine_percentage)
            print(f"Time to deplete: {time_to_empty:.2f}s")
            
            obs_time, obs_bucket = scout.recorded_observation_by_scouter(time_to_empty, magazine_percentage)
            print(f"Scout result: Bucket {obs_bucket}%, [Observer recorded time (perfect): {obs_time:.2f}s]") 

            print("\nStats:")
            
            scouter_shots = obs_bucket / 100 * robot.magazine_size
            error = calculate_error(scouter_shots, current_fuel)
            print(f"Shots error: {error:.2f}% (Real: {current_fuel:.1f}, Observed: {scouter_shots:.1f})")

            scouter_points = abs(obs_bucket / 100 * robot.magazine_size)
            total_scouted_hits += scouter_points # add the points to the total scouted hits
            hits_error = calculate_error(scouter_points, points)
            print(f"Hits error: {hits_error:.2f}% (Real: {points}, Observed: {scouter_points})")
            
            if current_fuel > 0:
                real_accuracy = (points / current_fuel) * 100
                print(f"\nReal accuracy: {real_accuracy:.2f}% (Placed: {robot.accuracy * 100:.1f}%)")

            print(f"Total shots: {current_fuel} ({points} hits, {misses} misses)")
            
        print("\n")
        print(f"=" * 20)
        print(f"SUMMERY RESULTS:")
        print(f"Robot: {robot.name}")
        print(f"=" * 20)

        print(f"\nNumber of volleys: {number_of_volleys}")

        print(f"\nTotal shots: {total_shots}")
        print(f"Total hits: {total_hits}")
        print(f"Total scouted hits: {total_scouted_hits}")

        print(f"\nStats:")

        total_accuracy = total_hits / total_shots
        print(f"Total accuracy: {100 * total_accuracy:.2f}%")

        total_shots_error = calculate_error(total_scouted_hits, total_shots)
        print(f"Total shots error: {total_shots_error:.2f}%")

        total_hits_error = calculate_error(total_scouted_hits, total_hits)
        print(f"Total hits error: {total_hits_error:.2f}%")

        # save the data for the current robot
        robot_stats = {
            "name": robot.name,
            "accuracy": total_accuracy * 100,
            "shots_error": total_shots_error,
            "hits_error": total_hits_error,
            "total_shots": total_shots
        }
        robots_data.append(robot_stats) # add the robot stats to the end of the list

    print("\n" * 2)
    print("=" * 40)
    print("FINAL COMPARISON OF ALL THE ROBOTS")
    print("=" * 40)

    print(f"Simulation number of runs: {number_of_volleys}")

    for data in robots_data:
        print(f"\nRobot Name: {data['name']}")
        print(f"- Overall Accuracy: {data['accuracy']:.2f}%")
        print(f"- Average Shots Error: {data['shots_error']:.2f}%")
        print(f"- Average Hits Error: {data['hits_error']:.2f}%")

if __name__ == "__main__":
    main()
