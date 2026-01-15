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
    name="Inconsistent jam",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=inconsistent_jam_fire
)

robot4 = RobotModel(
    name="Consistent spray",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=consistent_spray_fire
)

robot5 = RobotModel(
    name="Burst then jam",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=burst_then_jam_fire
)

robot6 = RobotModel(
    name="Stutter wave",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=stutter_wave_fire
)

robot7 = RobotModel(
    name="Steady fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=steady_fire
)

robot8 = RobotModel(
    name="Warmup fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=warmup_fire
)

robot9 = RobotModel(
    name="Saw fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=saw_fire
)

robot10 = RobotModel(
    name="Triangle fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=triangle_fire
)

robot11 = RobotModel(
    name="Double pulse fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=double_pulse_fire
)

robot12 = RobotModel(
    name="Exp decay fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=exp_decay_fire
)

robot13 = RobotModel(
    name="Exp ramp fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=exp_ramp_fire
)

robot14 = RobotModel(
    name="Log ramp fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=log_ramp_fire
)

robot15 = RobotModel(
    name="Spike fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=spike_fire
)

robot16 = RobotModel(
    name="End push fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=end_push_fire
)

robot17 = RobotModel(
    name="Jammy fire",
    magazine_size=100,
    accuracy=0.9,
    fire_rate_function=jammy_fire
)

all_robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10, robot11, robot12, robot13, robot14, robot15, robot16, robot17]
