import random

class ScouterModel:
    def __init__(self, time_error_min, time_error_max, magazine_error):
        self.time_error_min = time_error_min
        self.time_error_max = time_error_max
        self.magazine_error = magazine_error

        self.buckets = [25, 50, 75, 100]

    def observe_time(self, actual_time):
        average_error = (self.time_error_min + self.time_error_max) / 2

        range_size = self.time_error_max - self.time_error_min
        standard_deviation = range_size / 6 # 99.7% of values lie within -+ 3 standard deviations (thats a total of 6 parts)

        random_error = random.gauss(average_error, standard_deviation)

        if random_error > self.time_error_max:
             random_error = self.time_error_max
        elif random_error < self.time_error_min:
             random_error = self.time_error_min

        observed_time = actual_time + random_error

        return observed_time

    def observe_magazine_level(self, actual_percentage):
        percentage_val = actual_percentage * 100

        closest_bucket = self.buckets[0]
        min_diff = abs(percentage_val - self.buckets[0])

        for bucket in self.buckets:
            diff = abs(percentage_val - bucket)
            if diff < min_diff:
                min_diff = diff
                closest_bucket = bucket

        random_chance = random.random()

        if random_chance < self.magazine_error:
            current_index = 0
            for i in range(len(self.buckets)):
                if self.buckets[i] == closest_bucket:
                    current_index = i
                    break

            neighbors = []

            if current_index > 0: # if its not the first index
                neighbors.append(self.buckets[current_index - 1])

            if current_index < len(self.buckets) - 1: # if its not the last index
                neighbors.append(self.buckets[current_index + 1])

            if len(neighbors) > 0: # if there are neighbors
                mistake_bucket = random.choice(neighbors)
                return mistake_bucket

        return closest_bucket
