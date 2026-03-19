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

        error_range = self.magazine_error * 100
        standard_deviation = error_range / 3

        noise = random.gauss(0, standard_deviation)
        noise = max(-error_range, min(error_range, noise))

        noisy_percentage = percentage_val + noise

        # Find closest bucket
        closest_bucket = self.buckets[0]
        min_diff = abs(noisy_percentage - self.buckets[0])

        for bucket in self.buckets:
            diff = abs(noisy_percentage - bucket)
            if diff < min_diff:
                min_diff = diff
                closest_bucket = bucket

        return closest_bucket
