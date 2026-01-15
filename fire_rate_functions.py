import math

def quick_fire(t: float): # Omer's function - small bursts with brief pauses
    return 2.0 if (t - math.floor(t)) < 0.8 else 0.0

def inconsistent_jam_fire(t: float): # askof's function - inconsistent shooting with jams
    t = t % 10 # loop the pattern every 10 seconds (cuz this function stops at 10 x=10 so we need to loop until we finish the fuel at the magazine)
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

def consistent_spray_fire(t: float):  # mostly stable there is small waves and brief reload pauses
    t = t % 10
    if 0 <= t <= 1.0:
        return 8.0 * t
    elif 1.0 < t <= 2.5:
        return 8.0
    elif 2.5 < t <= 3.0:
        return -10.0 * (t - 2.5) + 8.0
    elif 3.0 < t <= 3.7:
        return 3.0 + (3.0 / 0.7) * (t - 3.0)
    elif 3.7 < t < 4.0:
        return 0.0
    elif 4.0 <= t <= 6.5:
        return 6.5 + 1.5 * math.sin(math.pi * (t - 4.0) / 2.5)
    elif 6.5 < t < 7.2:
        return 0.0
    elif 7.2 <= t <= 10.0:
        return - (5.0 / 2.8) * (t - 7.2) + 7.0
    else:
        return 0.0


def burst_then_jam_fire(t: float):  # hard burst with jams and then steady fire
    t = t % 10
    if 0 <= t <= 0.6:
        return 15.0 * t
    elif 0.6 < t <= 1.0:
        return 9.0
    elif 1.0 < t <= 1.2:
        return 0.0
    elif 1.2 < t <= 2.0:
        return 8.0 * math.exp(-2.0 * (t - 1.2))
    elif 2.0 < t <= 2.5:
        return 0.0
    elif 2.5 < t <= 4.0:
        return (7.0 / 1.5) * (t - 2.5)
    elif 4.0 < t <= 5.0:
        return 7.0
    elif 5.0 < t <= 5.5:
        return -12.0 * (t - 5.0) + 7.0
    elif 5.5 < t <= 6.0:
        return 10.0 * (t - 5.5) + 1.0
    elif 6.0 < t <= 7.0:
        return 6.0
    elif 7.0 < t <= 7.4:
        return 0.0
    elif 7.4 < t <= 8.5:
        x = (t - 7.4) / 1.1
        return 2.0 + 5.0 * math.log(1.0 + (math.e - 1.0) * x)
    elif 8.5 < t <= 10.0:
        return - (4.0 / 1.5) * (t - 8.5) + 7.0
    else:
        return 0.0


def stutter_wave_fire(t: float):  # lots of “stutter”, waves, multiple short jams, peak ~8
    t = t % 10
    if 0 <= t <= 1.0:
        return 4.0 + 3.0 * math.sin(math.pi * t)
    elif 1.0 < t <= 1.3:
        return 0.0
    elif 1.3 < t <= 3.0:
        return 2.0 + 5.0 * (1.0 - math.exp(-1.5 * (t - 1.3)))
    elif 3.0 < t <= 4.0:
        return -3.0 * (t - 3.0) + 7.0
    elif 4.0 < t <= 4.2:
        return 0.0
    elif 4.2 < t <= 6.0:
        return 5.5 + 1.5 * math.sin(2.0 * math.pi * (t - 4.2) / 1.2)
    elif 6.0 < t <= 7.0:
        return -5.0 * (t - 6.0) + 7.0
    elif 7.0 < t <= 7.8:
        return 0.0
    elif 7.8 < t <= 9.0:
        u = (t - 7.8) / 1.2
        return 2.0 + 6.0 * (u * u)
    elif 9.0 < t <= 10.0:
        return -5.0 * t + 53.0
    else:
        return 0.0
