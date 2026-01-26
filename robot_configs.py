from robot_model import RobotModel
import math
from fire_rate_functions import *
import random

def get_accuracy():
    return random.uniform(0.4, 0.9)

def get_magazine_size():
    return random.randint(20, 70)

def get_all_robots():

    robot1 = RobotModel(
        name="Quick fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=2,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: quick_fire(t)
    )

    robot2 = RobotModel(
        name="Log",
        magazine_size=get_magazine_size(),
        max_fire_rate=5,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: 2 * math.log(t + 1)
    )

    robot3 = RobotModel(
        name="Inconsistent jam - Askof's function",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=inconsistent_jam_fire
    )

    robot4 = RobotModel(
        name="Consistent spray",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=consistent_spray_fire
    )

    robot5 = RobotModel(
        name="Burst then jam",
        magazine_size=get_magazine_size(),
        max_fire_rate=9,
        accuracy=get_accuracy(),
        fire_rate_function=burst_then_jam_fire
    )

    robot6 = RobotModel(
        name="Stutter wave",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=stutter_wave_fire
    )

    robot7 = RobotModel(
        name="Steady fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=6,
        accuracy=get_accuracy(),
        fire_rate_function=steady_fire
    )

    robot8 = RobotModel(
        name="Warmup fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=warmup_fire
    )

    robot9 = RobotModel(
        name="Saw fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=saw_fire
    )

    robot10 = RobotModel(
        name="Triangle fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=triangle_fire
    )

    robot11 = RobotModel(
        name="Double pulse fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=double_pulse_fire
    )

    robot12 = RobotModel(
        name="Exp decay fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=9,
        accuracy=get_accuracy(),
        fire_rate_function=exp_decay_fire
    )

    robot13 = RobotModel(
        name="Exp ramp fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=exp_ramp_fire
    )

    robot14 = RobotModel(
        name="Log ramp fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=log_ramp_fire
    )

    robot15 = RobotModel(
        name="Spike fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=11,
        accuracy=get_accuracy(),
        fire_rate_function=spike_fire
    )

    robot16 = RobotModel(
        name="ramping up using sine wave - Sobol's function",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=sobols_function
    )

    robot17 = RobotModel(
        name="Jammy fire",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=jammy_fire
    )

    robot18 = RobotModel(
        name="y=6",
        magazine_size=get_magazine_size(),
        max_fire_rate=6,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: 6.0
    )

    robot19 = RobotModel(
        name="y=abs(2sin(t))",
        magazine_size=get_magazine_size(),
        max_fire_rate=8,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: abs(2 * math.sin(t))
    )

    robot20 = RobotModel(
        name="y=abs(t)",
        magazine_size=get_magazine_size(),
        max_fire_rate=10,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: abs(t)
    )

    robot21 = RobotModel(
        name="y=10",
        magazine_size=get_magazine_size(),
        max_fire_rate=10,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: 10
    )

    robot22 = RobotModel(
        name="sqrt",
        magazine_size=get_magazine_size(),
        max_fire_rate=4,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: math.sqrt(t)
    )

    robot23 = RobotModel(
        name="67",
        magazine_size=get_magazine_size(),
        max_fire_rate=7,
        accuracy=get_accuracy(),
        fire_rate_function=six_seven
    )

    robot24 = RobotModel(
        name="t^2",
        magazine_size=get_magazine_size(),
        max_fire_rate=110,
        accuracy=get_accuracy(),
        fire_rate_function=lambda t: t * t
    )

    all_robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10, robot11, robot12, robot13, robot14, robot15, robot16, robot17, robot18, robot19, robot20, robot21, robot22, robot23, robot24]
    return all_robots
