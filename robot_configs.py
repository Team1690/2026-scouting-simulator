from robot_model import RobotModel
import math
from fire_rate_functions import *

robot1 = RobotModel(
    name="Quick fire",
    magazine_size=100,
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
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=inconsistent_jam_fire
)

robot4 = RobotModel(
    name="Consistent spray fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=consistent_spray_fire
)

robot5 = RobotModel(
    name="Burst then jam fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=burst_then_jam_fire
)

robot6 = RobotModel(
    name="Stutter wave fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=stutter_wave_fire
)

all_robots = [robot1, robot2, robot3, robot4, robot5, robot6]
