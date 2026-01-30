from robot_model import RobotModelMagazineSizeFireRate
import math
from fire_rate_functions import *
from magazine_size_fire_rate_functions import charge_discharge_magazine_size_fire_rate, discharge_magazine_size_fire_rate, cooldown_magazine_size_fire_rate
import random
import functools

def get_accuracy():
    return random.uniform(0.4, 0.9)

def get_magazine_size():
    return random.randint(20, 70)

def get_all_robots():

    robot1 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a1_m0.1",
        magazine_size=get_magazine_size(),
        max_fire_rate=1,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=1, m=0.1)
    )

    robot2 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a2.3_m0.8",
        magazine_size=get_magazine_size(),
        max_fire_rate=2.3,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=2.3, m=0.8)
    )

    robot3 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a3.6_m1.5",
        magazine_size=get_magazine_size(),
        max_fire_rate=3.6,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=3.6, m=1.5)
    )

    robot4 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a4.9_m2.2",
        magazine_size=get_magazine_size(),
        max_fire_rate=4.9,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=4.9, m=2.2)
    )

    robot5 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a6.1_m2.9",
        magazine_size=get_magazine_size(),
        max_fire_rate=6.1,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=6.1, m=2.9)
    )

    robot6 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a7.4_m3.6",
        magazine_size=get_magazine_size(),
        max_fire_rate=7.4,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=7.4, m=3.6)
    )

    robot7 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a8.7_m4.3",
        magazine_size=get_magazine_size(),
        max_fire_rate=8.7,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=8.7, m=4.3)
    )

    robot8 = RobotModelMagazineSizeFireRate(
        name="ChargeDischarge_a10_m5",
        magazine_size=get_magazine_size(),
        max_fire_rate=10,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(charge_discharge_magazine_size_fire_rate, a=10, m=5)
    )

    robot9 = RobotModelMagazineSizeFireRate(
        name="Discharge_a1_m0.1",
        magazine_size=get_magazine_size(),
        max_fire_rate=1,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=1, m=0.1)
    )

    robot10 = RobotModelMagazineSizeFireRate(
        name="Discharge_a2.3_m0.8",
        magazine_size=get_magazine_size(),
        max_fire_rate=2.3,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=2.3, m=0.8)
    )

    robot11 = RobotModelMagazineSizeFireRate(
        name="Discharge_a3.6_m1.5",
        magazine_size=get_magazine_size(),
        max_fire_rate=3.6,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=3.6, m=1.5)
    )

    robot12 = RobotModelMagazineSizeFireRate(
        name="Discharge_a4.9_m2.2",
        magazine_size=get_magazine_size(),
        max_fire_rate=4.9,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=4.9, m=2.2)
    )

    robot13 = RobotModelMagazineSizeFireRate(
        name="Discharge_a6.1_m2.9",
        magazine_size=get_magazine_size(),
        max_fire_rate=6.1,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=6.1, m=2.9)
    )

    robot14 = RobotModelMagazineSizeFireRate(
        name="Discharge_a7.4_m3.6",
        magazine_size=get_magazine_size(),
        max_fire_rate=7.4,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=7.4, m=3.6)
    )

    robot15 = RobotModelMagazineSizeFireRate(
        name="Discharge_a8.7_m4.3",
        magazine_size=get_magazine_size(),
        max_fire_rate=8.7,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=8.7, m=4.3)
    )

    robot16 = RobotModelMagazineSizeFireRate(
        name="Discharge_a10_m5",
        magazine_size=get_magazine_size(),
        max_fire_rate=10,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(discharge_magazine_size_fire_rate, a=10, m=5)
    )

    robot17 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a1",
        magazine_size=get_magazine_size(),
        max_fire_rate=1,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=1)
    )

    robot18 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a2.3",
        magazine_size=get_magazine_size(),
        max_fire_rate=2.3,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=2.3)
    )

    robot19 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a3.6",
        magazine_size=get_magazine_size(),
        max_fire_rate=3.6,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=3.6)
    )

    robot20 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a4.9",
        magazine_size=get_magazine_size(),
        max_fire_rate=4.9,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=4.9)
    )

    robot21 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a6.1",
        magazine_size=get_magazine_size(),
        max_fire_rate=6.1,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=6.1)
    )

    robot22 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a7.4",
        magazine_size=get_magazine_size(),
        max_fire_rate=7.4,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=7.4)
    )

    robot23 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a8.7",
        magazine_size=get_magazine_size(),
        max_fire_rate=8.7,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=8.7)
    )

    robot24 = RobotModelMagazineSizeFireRate(
        name="Cooldown_a10",
        magazine_size=get_magazine_size(),
        max_fire_rate=10,
        accuracy=get_accuracy(),
        magazine_size_fire_rate_function=functools.partial(cooldown_magazine_size_fire_rate, a=10)
    )

    all_robots = [
        robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8,
        robot9, robot10, robot11, robot12, robot13, robot14, robot15, robot16,
        robot17, robot18, robot19, robot20, robot21, robot22, robot23, robot24
    ]
    return all_robots
