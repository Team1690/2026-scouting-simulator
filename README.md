# 2026 Fuel Scouting Sim

**Fuel Scouting Simulation**
In one line it is: A playground where we simulate robots shooting fuel and see how accurate our scouting data actually is.

## What is the Point?
In the 2026 FRC game there are 400-600 fuel's (balls) per match and each robot shoots around 100-300 fuels per match (estimates before the season started so this could be off). Since we don't want scouters to manually count every single shot we created this simulation to test different methods of calculating how much fuel a robot shot and how many hits it scored and see if there is a method we can use to make it easier for the scouters.

We simulate a "real" FRC tournament with 24 robots, each with a unique firing pattern based on mathematical equations. The matchmaking is based on the real FRC scheduling algorithm, ensuring realistic match distributions.

**This simulation was created with 3 main goals:**
    1. Find the accuracy of each method
    2. Find the best method
    3. Find the method we can stack

## How It Works?

**Robot Creation**
Now features TWO sets of 24 unique robots (48 total configs) to test different behaviors:
1. **Time Based Robots**: The original set. Firing patterns are pure functions of time (e.g. shot rate increases as time goes on).
2. **Magazine Size Based Robots**: New set. Firing patterns depend on how full the magazine is (e.g. shoots faster when full, slower when empty).

Each robot has:
- Magazine size (fuel capacity)
- Firing rate function (dynamic shot patterns)
- Accuracy percentage
- Maximum fire rate

**Match Scheduling**
Matches are scheduled using the official FRC algorithm. Each match has 6 robots (3 red alliance, 3 blue alliance) with minimized repeat pairings.

**Match Simulation**
During each match robots perform 1-6 volleys (randomly chosen) with realistic fuel loads (10-100% of their magazine capacity). // 10-100% to avoide the 0 case and realisticly robots dont shoot when they got less then 10% of their magazine.

## Scouting Metrics (Scouting Methods):

### 1. **Magazine Size Bucket Metric (Oz’s method)**
Instead of entering an exact number of total balls fired the scouter selects the closest magazine size bucket: 25%, 50%, 75%, or 100%.

### 2. **Iterative Average Fire Rate**
Takes the alliance score and divides it between the 3 robots. based on their firing time If a robots calculated fire rate goes over their max fire rate it takes half of their score and adds it to their alliance partners (evenly split between the two). This keeps iterating until all scores are realistic. Then it averages these fire rates across all matches to predict each robots performance.

### 3. **OPR**
used in the FIRST community to compare the performance of teams on the field. read more on the blue team alliance blog.

### 4. **Match Average Rate (Fixed Window)**
After the first match, calculates the robots score rate (hits/time). Then in future matches uses that saved rate multiplied by the observed time to estimate total hits. basically assumes the robot will maintain the same fire rate it showed in its first match.

### 5. **Volley Average Rate (Fixed Window)**
Similar to method 4 (Match Average Rate) but uses only the first volley instead of the full first match. Takes the fire rate from the very first volley (shots/time not hits/time) and applies it to all future volleys and matches.

### 6. **Weight Based Metric**
Takes the total alliance hits and distributes them back to individual robots weighted by their "scouted shots" (how many shots were scouted using the magazine method). Basically, if we saw Robot A take 70% of the shots, we give them 70% of the hits.

### 7. **Weight Based Metric (Max Fire Rate Cap)**
Same as the standard Weight Based Metric, but with a sanity check: a robot cannot have hit more balls than it could physically fire in that time (Max Fire Rate * Time). If a robot gets too many hits assigned, we cap it and redistribute the extra hits to the other robots.

### 8. **Weight Based Metric (First Volley)**
Similar to the standard Weight Based Metric, but uses the *First Volley* fire rate to predict the scouted shots instead of using the magazine method to count shots.


### Files Descriptions

- **`2026_fuel_scouting_sim.py`**: same as main.py for most project, its the main file that runs the simulation
- **`robot_model.py`**: defines the `RobotModel` class (the robot)
- **`robot_configs.py`**: the 24 time-based robot configurations
- **`robot_configs_magazine_size.py`**: the 24 magazine-size-based robot configurations
- **`fire_rate_functions.py`**: contains the time-based firing rate functions
- **`magazine_size_fire_rate_functions.py`**: contains the magazine-based firing rate functions
- **`simulation_logic.py`**: implements the `scout_robot_match()` function (the match simulation)
- **`match_maker.py`**: frc scheduling algorithm to create balanced match schedules
- **`metrics.py`**: contains the different scouting metrics
- **`utils.py`**: utility functions (it has just the error calculations)

## Fire Rate Functions Visualization
To visualize the different robots firing patterns check out these folders:
- **`time based functions png's`**: Contains summary pages for the time-based robots.
- **`magazine size based functions png's`**: Contains summary pages for the magazine-based robots.

## disclaimer
the code is highly unoptimized and unreadable. Good luck.
