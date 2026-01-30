import math

def charge_discharge_magazine_size_fire_rate(a: float, m: float, magazine_percentage: float):
    if m < 0.1:
        m = 0.1

    changing_point = math.log(a+1) / m
    fx = 0

    if 0 <= magazine_percentage <= changing_point:
        fx = math.exp(m * magazine_percentage) - 1
    elif changing_point < magazine_percentage <= 100 - changing_point:
        fx = a
    elif 100 - changing_point < magazine_percentage <= 100:
        fx = (a+1) * (1 - math.exp(m * (magazine_percentage - 100)))

    if fx == 0:
        fx = 1

    return fx

def discharge_magazine_size_fire_rate(a: float, m: float, magazine_percentage: float):
    if m < 0.1:
        m = 0.1

    fx = 0

    if 0 < magazine_percentage <= 100:
        fx = a * (1 - math.exp(-m * magazine_percentage))

    if fx == 0:
        fx = 1

    return fx

def cooldown_magazine_size_fire_rate(a: float, magazine_percentage: float):
    fx = 0

    if 0 <= magazine_percentage <= a:
        fx = magazine_percentage
    elif a < magazine_percentage <= 100:
        fx = a

    if fx == 0:
        fx = 1

    return fx
