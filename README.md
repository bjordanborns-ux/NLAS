# NLAS
Northlight Launch Awareness System (NLAS) is a Python launch display project built to improve situational awareness at a launch console. I started this as a personal project to improve Python skills and learn more about launch operations.

**Currently in pre-alpha. Bugs and issues are expected.**

### Current Features:

- User inputs for wind, clouds, temp., rain
- Automatic Weather Go/No-Go based on user inputs
- Randomized system failures
- Countdown timer and mission elapsed timer
- Mission status updates
- Writes a telemetry CSV and a mission log (log.txt).
  - Use a unique CSV name for each run.
  - log.txt resets at the start of each run.

### Planned updates:

- Multiple systems with realistic go/ no go decisions
- All staging event callouts through payload separation
- Simulated (simplified) altitude and velocity telemetry
- Audio callouts for different events
- User selected go/ no go decision of launch
- Various outcomes based on user decision
- Simple GUI for panel
- Multiple randomized system failures
- Advanced physics and telemetry data

### How to run:

1. Download repository
2. Open project in preferred IDE
3. Run `python main.py`

### Requirements
- Python 3.12+
  
*NLAS currently runs in the terminal.*

### Weather GO/NO-GO verification

Eight scenarios were checked against the expected weather decision.
All eight matched. The all-clear case returned GO. The simulator
returned NO-GO at and beyond each numeric limit and when rain was
present. The checks evaluated the weather decision before simulated
system failures.

### Contact
Questions, comments, concerns? 

Blake Jordan-Borns
bjordanborns@gmail.com
