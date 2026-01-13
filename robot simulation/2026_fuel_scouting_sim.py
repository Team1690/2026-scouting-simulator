from __future__ import annotations
import random
import math

class RobotModel:
    def __init__(self, name: str, magazine_size: int, accuracy: float, fire_rate_function, max_fire_rate: float):
        self.name = name
        self.magazine_size = magazine_size
        self.accuracy = accuracy
        self.fire_rate_function = fire_rate_function
        self.max_fire_rate = max_fire_rate

    def get_points_for_magazine(self, magazine_precentage: float):
        hits = 0
        misses = 0
        
        shots_count = round(self.magazine_size * magazine_precentage)
        for _ in range(shots_count):
            if random.random() < self.accuracy:
                hits += 1
            else:
                misses += 1

        return hits

    def time_to_deplete(self,  dt: float, magazine_precentage: float):
        t = 0.0
        current_fuel_in_magazine = round(self.magazine_size * magazine_precentage)

        while current_fuel_in_magazine > 0:
            current_fuel_in_magazine -= self.fire_rate_function(t) * dt
            t += dt
            
        return t

def quick_fire(t: float):
    return 2.0 if (t - math.floor(t)) < 0.8 else 0.0

def inconsistent_jam_fire(t: float): # askof's function - peeks at 8,
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
    robot = RobotModel(
        name="bot1",
        magazine_size=20,
        accuracy=0.6,
        fire_rate_function=lambda t: quick_fire(t),
        max_fire_rate=2.0 
    )

    magazine_precentage = random.random()
    
    print(f"Robot name: {robot.name}")
    print(f"Magazine size: {round(magazine_precentage * robot.magazine_size)}")
    print(f"Points for magazine: {robot.get_points_for_magazine(magazine_precentage)}")
    time_to_deplete = robot.time_to_deplete(0.05, magazine_precentage)
    print(f"Time to deplete: {time_to_deplete}")

    robot2 = RobotModel(
        name="Log",
        magazine_size=20, 
        accuracy=0.6, 
        fire_rate_function=lambda t: 2 * math.log(t + 1),
        max_fire_rate=5.0
    )
    
    print(f"\nRobot name: {robot2.name}")
    print(f"Magazine size: {round(magazine_precentage * robot2.magazine_size)}")
    print(f"Points for magazine: {robot2.get_points_for_magazine(magazine_precentage)}")
    print(f"Time to deplete: {robot2.time_to_deplete(0.05, magazine_precentage)}")

    robot3 = RobotModel(
        name="Inconsistent shooting with jam - Askof's function",
        magazine_size=100,
        accuracy=0.8,
        fire_rate_function=inconsistent_jam_fire,
        max_fire_rate=8.0 # peaks at 8
    )

    print(f"\nRobot name: {robot3.name}")
    print(f"Magazine size: {round(magazine_precentage * robot3.magazine_size)}")
    print(f"Points for magazine: {robot3.get_points_for_magazine(magazine_precentage)}")
    print(f"Time to deplete: {robot3.time_to_deplete(0.05, magazine_precentage)}")
    
    print("\nScout Model Observation:")
    scout = ScoutModel()
    observation = scout.recorded_observation_by_scouter(time_to_deplete, magazine_precentage)
    print(f"Actual Percent: {magazine_precentage*100:.2f}%")
    print(f"Observed: {observation}")


if __name__ == "__main__":
    main()
