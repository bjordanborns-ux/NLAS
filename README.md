# NLAS

Northlight Launch Awareness System (NLAS) is a Python launch display project built to improve situational awareness at a launch console. I started this as a personal project to improve Python skills and learn more about launch operations.

**Currently in pre-alpha. Bugs and issues are expected.**

## Current Features

- User inputs for wind, clouds, temperature, and rain
- Automatic weather GO/NO-GO based on user inputs
- Randomized system failures
- Countdown timer and mission elapsed timer
- Mission status updates
- Writes a telemetry CSV and a mission log (`log.txt`)
  - Use a unique CSV name for each run.
  - `log.txt` resets at the start of each run.

## Planned Updates

- Multiple systems with realistic GO/NO-GO decisions
- All staging event callouts through payload separation
- Simulated (simplified) altitude and velocity telemetry
- Audio callouts for different events
- User-selected GO/NO-GO decision of launch
- Various outcomes based on user decision
- Simple GUI for panel
- Multiple randomized system failures
- Advanced physics and telemetry data

## How to Run

1. Download repository.
2. Open project in preferred IDE.
3. Run `python main.py`.

## Requirements

- Python 3.12+

*NLAS currently runs in the terminal.*

## Weather GO/NO-GO Verification

Eight scenarios were checked against the expected weather decision. All eight matched. The all-clear case returned GO. The simulator returned NO-GO at and beyond each numeric limit and when rain was present. The checks evaluated the weather decision before simulated system failures.

### Verification Results

| Test | Weather Condition / Inputs | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | All conditions within limits | GO | GO | PASS |
| 2 | Wind at limit | NO-GO | NO-GO | PASS |
| 3 | Temperature at limit | NO-GO | NO-GO | PASS |
| 4 | Rain present | NO-GO | NO-GO | PASS |
| 5 | Cloud height at limit | NO-GO | NO-GO | PASS |
| 6 | Wind below limit, cloud height at limit | NO-GO | NO-GO | PASS |
| 7 | Cloud height below limit, wind at limit | NO-GO | NO-GO | PASS |
| 8 | Wind below limit, Cloud height below limit, temp. at limit | NO-GO | NO-GO | PASS |

**Verification summary:** 8/8 scenarios produced the expected weather decision.

## Example Terminal Output

The following output is from a simulated NLAS launch:

```text
NorthLight Launch Awareness System
Enter desired save name: Test
Mission Status: Checking Weather
Windspeed: 0
Cloud Height in Feet: 30000
Temperature in C: 17
Rain? Y or N: N
Weather systems verified, approved for launch.
Initating launch countdown sequence.
Mission Status: Countdown
10
9
8
7
6
5
4
3
2
1
Ignition
Liftoff
Mission Status: Ascent
MET: T+ 0:00:20 Altitude: 95760 Velocity: 720 Fuel: 58
Orbit insertion nominal
Mission Status: Orbit
MET: T+ 0:00:45 Altitude: 386880 Velocity: 400 Fuel: 56
Orbit Raised to Correct Altitude. Log saved.
```

## Example Telemetry CSV Output

NLAS generates a CSV file containing telemetry data from the simulated mission.

The following is from one simulation run:

```csv
Time,State,Velocity,Altitude,Fuel
0,Checking Weather,0,0,100
0,Ascent,0,0,98
1,Ascent,36,0,96
2,Ascent,72,72,94
3,Ascent,108,288,92
4,Ascent,144,720,90
5,Ascent,180,1440,88
6,Ascent,216,2520,86
7,Ascent,252,4032,84
8,Ascent,288,6048,82
9,Ascent,324,8640,80
10,Ascent,360,11880,78
11,Ascent,396,15840,76
12,Ascent,432,20592,74
13,Ascent,468,26208,72
14,Ascent,504,32760,70
15,Ascent,540,40320,68
16,Ascent,576,48960,66
17,Ascent,612,58752,64
18,Ascent,648,69768,62
19,Ascent,684,82080,60
20,Ascent,720,95760,58
23,Orbit,756,110880,56
24,Orbit,756,110880,56
```

## Contact

Questions, comments, concerns?

Blake Jordan-Borns  
bjordanborns@gmail.com
