
NUMBER_OF_RUNS = 25

MATCHES_PER_ROBOT = 15
ITERATIONS = 10000 # Iterations of match making
NUMBER_OF_SCHEDULES = 3 # Pre-generate this many schedules and reuse them across runs

MIN_ACCURACY = 0.50
MAX_ACCURACY = 0.95
MIN_MAGAZINE_SIZE = 20
MAX_MAGAZINE_SIZE = 80

MATCH_ACCURACY_VARIANCE = 0.1
SCOUT_MIN_TIME_ERROR = -0.5
SCOUT_MAX_TIME_ERROR = 0.5
SCOUT_MAGAZINE_ERROR = 0.20 # error margin of the scouter on the magazine percentage metrics

SIMULATION_TIME_STEP = 0.05
MIN_NUMBER_OF_VOLLEYS = 1
MAX_NUMBER_OF_VOLLEYS = 6
MIN_MAGAZINE_FILL_PERCENTAGE = 0.1
MAX_MAGAZINE_FILL_PERCENTAGE = 1.0

RATE_OF_FIRE_JITTER = 1
MAX_TIME_TO_DEPLETE = 1000.0

NOTIFICATION_STEP = 25

# Which metrics to run. Comment out any metric you don't need to speed up the simulation.
ENABLED_METRICS = {
    # "fire_rate",                                    # IterativeAverageFireRateMetric
    # "fixed_window",                                 # MatchAvgRateFixedWindowMetric
    # "volley_avg_rate",                              # VolleyAvgRateFixedWindowMetric
    "opr",                                          # OPR
    # "weight_based_max_fire_rate",                   # WeightBasedMaxFireRateMetric
    "weight_based",                                 # WeightBasedMetric
    "weight_based_first_volley",                    # WeightBasedFirstVolleyMetric
    "first_volley_accuracy_weight",                 # FirstVolleyAccuracyWeightMetric
    # "first_volley_accuracy_weight_tournament",      # FirstVolleyAccuracyWeightMetricTournament
    "first_volley_bps_weighted_accuracy",           # FirstVolleyBPSWeightedAccuracy
    # "first_volley_bps_weighted_accuracy_tournament",# FirstVolleyBPSWeightedAccuracyTournament
    "fire_time_weight",                             # FireTimeWeightMetric
}
