from __future__ import annotations
import random
import math

class Robot:
    def __init__(self, magazine_size: int, accuracy: float, fire_rate_function):
        self.magazin_size = magazine_size
        self.accuracy = accuracy
        self.fire_rate_function = fire_rate_function

    def get_points_for_magazine(self, magazine_precentage: float):

        hits: int = 0
        misses: int = 0
        
        for _ in range(round(self.magazin_size * magazine_precentage)):
            if random.random() < self.accuracy:
                hits += 1
            else:
                misses += 1

        return hits

    def time_to_deplete(self,  dt: float, magazine_precentage: float):
        t = 0.0
        current_fuel_in_magazine: float = round(self.magazin_size * magazine_precentage)

        while current_fuel_in_magazine > 0:
            current_fuel_in_magazine -= self.fire_rate_function(t) * dt
            t += dt
            
        return t

def quick_fire(t: float):
    return 2.0 if (t - math.floor(t)) < 0.8 else 0.0
        

def main():
    robot = Robot(20, 0.6, lambda t: quick_fire(t))

    magazine_precentage = random.random()
    
    print(f"Magazine size: {round(magazine_precentage * robot.magazin_size)}")
    print(f"Points for magazine: {robot.get_points_for_magazine(magazine_precentage)}")
    print(f"Time to deplete: {robot.time_to_deplete(0.05, magazine_precentage)}")


    robot2 = Robot(20, 0.6, lambda t: 2 * math.log(t + 1))
    
    print("\nRobot 2")
    print(f"Magazine size: {round(magazine_precentage * robot2.magazin_size)}")
    print(f"Points for magazine: {robot2.get_points_for_magazine(magazine_precentage)}")
    print(f"Time to deplete: {robot2.time_to_deplete(0.05, magazine_precentage)}")
    


if __name__ == "__main__":
    main()
