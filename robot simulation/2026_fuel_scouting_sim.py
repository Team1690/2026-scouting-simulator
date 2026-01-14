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
                return float('unc')
                
            current_fuel_in_magazine -= self.fire_rate_function(t) * dt
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


def main():
    robots_to_simulate = ["Inconsistent shooting with jam - Askof's function"]

    robot1 = RobotModel(
        name="bot1",
        magazine_size=20,
        accuracy=0.6,
        fire_rate_function=lambda t: quick_fire(t)
    )

    robot2 = RobotModel(
        name="Log",
        magazine_size=20, 
        accuracy=0.6, 
        fire_rate_function=lambda t: 2 * math.log(t + 1)
    )

    robot3 = RobotModel(
        name="Inconsistent shooting with jam - Askof's function",
        magazine_size=100,
        accuracy=0.9,
        fire_rate_function=inconsistent_jam_fire
    )

    all_robots = [robot1, robot2, robot3]

    magazine_percentage = random.uniform(0.1, 1.0) # random fill between 10% and 100% for the magazine
    scout = ScoutModel() # the simulated scouter

    print(f"Starting simulation (Fuel Level: {magazine_percentage*100:.1f}%)")

    for robot in all_robots:
        if robot.name in robots_to_simulate: # check if we want to run this robot
            print(f"\nSimulation for: {robot.name}")

            print(f"Model settings: Magazine Size: {robot.magazine_size}, Accuracy: {robot.accuracy}")
            print("\n")
            
            current_fuel = round(magazine_percentage * robot.magazine_size)
            print(f"Fuel amount in magazine: {current_fuel}")

            points, misses = robot.get_points_for_magazine(magazine_percentage)
            
            time_to_empty = robot.time_to_deplete(0.05, magazine_percentage)
            print(f"Time to deplete: {time_to_empty:.2f}s")
            
            obs_time, obs_bucket = scout.recorded_observation_by_scouter(time_to_empty, magazine_percentage)
            print(f"Scout result: Bucket {obs_bucket}%, [Observer recorded time (perfect): {obs_time:.2f}s]") 

            print("\nStats:")
            
            real_percentage = magazine_percentage * 100
            error = 100 * abs(obs_bucket - real_percentage) / real_percentage
            print(f"Shots error: {error:.2f}% (Real: {real_percentage:.1f}%, Observed: {obs_bucket:.1f}%)")

            scouter_points = abs(obs_bucket / 100 * robot.magazine_size)
            hits_error = 100 * abs(scouter_points - points) / points
            print(f"Hits error: {hits_error:.2f}% (Real: {points}, Observed: {scouter_points})")
            
            if current_fuel > 0:
                real_accuracy = (points / current_fuel) * 100
                print(f"\nReal accuracy: {real_accuracy:.2f}% (Placed: {robot.accuracy * 100:.1f}%)")

            print(f"Total shots: {current_fuel} ({points} hits, {misses} misses)")

if __name__ == "__main__":
    main()
