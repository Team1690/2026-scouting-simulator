import random

class RobotModel:
    def __init__(self, name: str, magazine_size: int, accuracy: float, fire_rate_function):
        self.name = name
        self.magazine_size = magazine_size
        self.accuracy = accuracy
        self.fire_rate_function = fire_rate_function

    def __repr__(self): # make the robot name show up when we print the robot (ty stack overflow)
        return self.name

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
