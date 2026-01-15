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
