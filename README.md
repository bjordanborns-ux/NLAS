# NLAS

Northlight Launch Awareness System (NLAS) is a Python launch display project built to improve situational awareness at a launch console. I started this as a personal project to improve Python skills and learn more about launch operations.

**Currently in pre-alpha. Bugs and issues are expected.**

## Current Features

- User inputs for wind speed, cloud height, temperature, and rain
- Automatic weather GO/NO-GO evaluation
- Operator GO/NO-GO polling for Weather, Propulsion,
  Guidance and Navigation (GNC), and Electrical systems
- Launch authorization logic and HOLD procedures
- Randomized system failures with severity and shutdown conditions
- Launch countdown and mission elapsed timer (MET)
- Simplified simulated altitude, velocity, and fuel telemetry
- Mission status updates
- CSV telemetry recording and mission event logging
- JSON output for weather and telemetry data

## Planned Updates

- Expanded system-specific GO/NO-GO criteria
- Staging event callouts through payload separation
- Improved physics and telemetry calculations
- Audio callouts for mission events
- Additional randomized failure scenarios
- Expanded operator decision-making and mission outcomes
- Graphical user interface (GUI)
- Improved data logging and telemetry visualization

## How to Run

1. Download repository.
2. Open project in preferred IDE.
3. Run `python main.py`.

## Requirements

- Python 3.12+

*NLAS currently runs in the terminal.*

## Limitations of NLAS

NLAS is an educational launch operations simulation and
is not intended for operational flight use.

The current physics model uses simplified constant
acceleration and fuel consumption calculations.
Atmospheric drag, changing vehicle mass, gravity losses,
and orbital mechanics are not currently modeled.

Weather constraints do not represent the launch commit criteria of any specific launch vehicle.

Future versions will introduce more realistic flight
dynamics and telemetry calculations.

## Weather GO/NO-GO Verification

Eight scenarios were checked against the expected weather decision. All eight matched. The all-clear case returned GO. The simulator returned NO-GO at and beyond each numeric limit and when rain was present. 

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

## Systems GO/NO-GO Verification

Eight verification scenarios were executed to evaluate the NLAS pre-launch GO/NO-GO decision logic. Testing included individual system NO-GO conditions, simultaneous NO-GO conditions, automated weather alerts, nominal launch authorization, and invalid operator inputs. All eight scenarios passed their respective verification criteria. These tests evaluated launch authorization logic prior to the simulation of randomized system failures.

### Verification Results

| Test | WX | Prop | GNC | Elec | Expected | Actual | Result |
|---|---|---|---|---|---|---|---|
| 1 | GO | GO | GO | NO-GO | HOLD | HOLD | PASS |
| 2 | GO | GO | NO-GO | GO | HOLD | HOLD | PASS |
| 3 | GO | NO-GO | GO | GO | HOLD | HOLD | PASS |
| 4 | NO-GO | GO | GO | GO | HOLD | HOLD | PASS | 
| 5 | GO (WX alerted from weather_check) | GO | GO | GO | HOLD | HOLD | PASS |
| 6 | GO | GO | GO | GO | APPROVED | APPROVED | PASS |
| 7 | GO | NO-GO | NO-GO | GO | HOLD | HOLD | PASS |
| 8 | GO | GO | GO | GO | Re-Prompt | Re-Prompted | PASS |

**Verification summary:** 8/8 verification scenarios passed. 7 scenarios validated launch authorization and HOLD status, while one evaluated operator input validation.

## Example Terminal Output

The following output is from a simulated NLAS launch:

```
NorthLight Launch Awareness System
Enter desired save name: test
Mission Status: Checking Weather
Windspeed: 0
Cloud Height in Feet: 30000
Temperature in C: 17
Rain? Y or N: N
Weather systems verified, starting system Go/No-Go polling.
Automated weather verification status: True
Requesting final Weather Officer GO/NO-GO.
Enter Weather GO/NO-GO Status: GO
Enter Propulsion GO/NO-GO Status: GO
Enter GNC GO/NO-GO Status: GO
Enter Electrical GO/NO-GO Status: GO
SYSTEMS POLL COMPLETE

========== NLAS SYSTEMS POLL ==========

Weather         GO
Propulsion      GO
GNC             GO
Electrical      GO

---------------------------------------
FINAL LAUNCH STATUS: GO
---------------------------------------
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
MET: T+0:03:04 Altitude: 99638.21 Velocity: 1083.02 Fuel: 44.80
Orbit insertion nominal. Raising Orbit
Mission Status: Raising Orbit
MET: T+0:03:37 Altitude: 100724.18 Velocity: 400.00 Fuel: 44.500
Orbit Raised to Correct Altitude. Log saved.
```

## Example Telemetry CSV Output

NLAS generates a CSV file containing telemetry data from the simulated mission (10 Second example).
```
Time,State,Velocity,Altitude,Fuel
0,Checking Weather,0,0,100
0,Ascent,0.0,0.0,100.0
1,Ascent,5.886,2.943,99.7
2,Ascent,11.772,11.772,99.4
3,Ascent,17.658,26.487000000000002,99.1
4,Ascent,23.544,47.088,98.8
5,Ascent,29.43,73.575,98.5
6,Ascent,35.316,105.94800000000001,98.2
7,Ascent,41.202,144.207,97.9
8,Ascent,47.088,188.352,97.6
9,Ascent,52.974000000000004,238.383,97.3
10,Ascent,58.86,294.3,97.0
```

## Contact

Questions, comments, concerns?

Blake Jordan-Borns  
bjordanborns@gmail.com
