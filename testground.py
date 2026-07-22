import time
import random

log_file_path = 'log.txt'
# Starting values for telemetry system
print("NorthLight Launch (Function sytem)")

# Functions
# when mission status changes the change is logged. dependent on mission state which func is run
def log_event():
   printlog = "Mission Status:"
   if telemetry_dict["mission_state"] == "Checking Weather":
      mission_logtxtinit()
   else:
      mission_logtxtsec()
   print(printlog, telemetry_dict["mission_state"])

def converttime():
    t = time.time()
    sec = int(t)
    # divmod = how many seconds go into 1 minute with how much leftover, etc. for minutes to hours also.
    minute, sec = divmod(sec, 60)
    hour, minute = divmod(minute, 60)
    # %d = put whole number here, %02d = put a 2 digit whole number here.
    return '%d:%02d:%02d' % (hour, minute, sec)   

def timestamp():
    from time import localtime, strftime
    return strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())

# if mission state is initial (checking weather), log will erase previous log and start creating new entries.
def mission_logtxtinit():
   with open(log_file_path, 'w') as log_file:
       t = timestamp()
       timest = (t)
       log_file.write(telemetry_dict["mission_state"])
       log_file.write('\n')
       log_file.write(timest)

# if mission state is past checking weather, log with skip a line and add the next mission state once reached
def mission_logtxtsec():
    with open(log_file_path, 'a') as log_file:
       log_file.write('\n')
       log_file.write(telemetry_dict["mission_state"])
       log_file.write('\n')
       log_file.write(f"altitude: {telemetry_dict["altitude"]}\n")
       log_file.write(f"fuel: {telemetry_dict["fuel"]}\n")
       log_file.write(f"velocity: {telemetry_dict["velocity"]}\n")

def weather_check():
   telemetry_dict["mission_state"] = "Checking Weather"
   log_event()
   windspeed = int (input("Windspeed: "))
   cloudheight = int (input("Cloud Height in Feet: "))
   temp = int (input("Temperature in C: "))
   precip = (input("Rain? Y or N: "))
   if windspeed < 12 and cloudheight > 10000 and temp < 18 and precip == "N":
    launch_approved()
   else:
    print("Weather is No-Go. Hold Launch.")
    time.sleep(1)
    weather_scrub()

def weather_scrub():
   print("Holding for Weather. Standby.")
   time.sleep(3)
   print("Launch scrubbed. System termination initiated.")
   exit()

# Gets called from weather
def launch_approved():
    print("Weather systems verified, approved for launch.")
    time.sleep(1)
    print("Initating launch countdown sequence.")
    time.sleep(1)
    random_failure()

# failure dictionary for failure messages and codes.
failure_list = {
   "FLR-001": {"message" : "M1D Failure Imminent", "severity": "High", "system" : "Propulsion", "shutdown": True},
   "FLR-002": {"message": "Propellant Leak", "severity": "High", "system" : "Propulsion", "shutdown": True},
   "FLR-003": {"message" : "Guidance Calibration Failed", "severity": "Medium", "system" : "GNC", "shutdown": False},
   "FLR-004": {"message" : "Battery Failure", "severity": "Medium", "system" : "Electrical", "shutdown": False}
}

# TESTING set failure to occur nearly everytime. 
# Failure set to occur if random number picked is between 90 and 100. Will launch successfully if failure occurs. 
def random_failure():
   failure = (random.randint (0, 100))
   if failure > 90 and failure < 100:
      print("Holding launch countdown")
      time.sleep(1)
      failures = list(failure_list.values())  
      selected_failure = random.choice(failures)
      print (selected_failure["message"], selected_failure["severity"], selected_failure["system"])
      if selected_failure["shutdown"]:
        time.sleep(1)
        print("Shutdown required")
        telemetry_dict["mission_state"] = "Shutdown"
        log_event()
        exit()
      else:
        time.sleep(1)
        print("Component not critical, resuming countdown")
        time.sleep(1)
        countdown()     
   elif failure > 0 and failure < 90: 
      countdown()

countdown_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
def countdown():
    telemetry_dict["mission_state"] = "Countdown"
    log_event()
    for i in range(0, 10, 1): 
        countdown_list[i]
        time.sleep(1)
        print (countdown_list[i])
    liftoff()

# Defines the launch time for telemetry_timer to utilize when forming MET. 
def liftofftime():
    timer_dict["liftoff_time"] = time.time()

def liftoff():
    time.sleep(1)
    print("Ignition")
    time.sleep(1)
    print("Liftoff")
    telemetry_dict["mission_state"] = "Ascent" 
    log_event()
    liftofftime()
    

# Calculates mission time for other calculations and telemetry timer to use.
def time_calculation():
    current_time = time.time()
    mission_time = (current_time - timer_dict["liftoff_time"])
    return mission_time

# Calculates acceleration for velocity and altitude calculations. Set to 0.6 Gs for testing purposes.
def acceleration_calculation():
    acceleration = int (.6 * 60)
    return acceleration

# Pulls mission time and acceleration from acceleration and time calculation functions to calculate velocity.
def velocity_calculation(mission_time, acceleration):
    velocity_tel = int (0 + (acceleration * mission_time))
    return velocity_tel

# Pulls mission time, velocity, and altitude to calculate altitude. Altitude is then returned to be used in telemetry timer and altitude calculation for next loop.
def altitude_calculation(mission_time):
    altitude_tel = int (telemetry_dict["altitude"] + (telemetry_dict["velocity"] * mission_time))
    return altitude_tel
# 
# Pulls acceleration and fuel to calculate fuel burn and new fuel level. New fuel level is returned to telemetry_timer function.
def fuel_calculation(acceleration): 
    fuel_burn = acceleration * .05
    fuel_rem = telemetry_dict["fuel"]
    fuel_tel = int (fuel_rem - fuel_burn)
    return fuel_tel

# Centralized mission data refactor to allow there to be only one source of telemetry and mission data. 
telemetry_dict = {
   "mission_state": "Checking Weather",
   "velocity": 0,
   "altitude": 0,
   "fuel": 100
}

# Acceleration (unrealistic #) causes velocity to increase which causes altitude_tel to increase. 
def telemetry_timer_ascent(mission_time):
    print("MET: T+", convert(mission_time), "Altitude:" , telemetry_dict["altitude"], "Velocity:", telemetry_dict["velocity"], "Fuel:", telemetry_dict["fuel"], end='\r')
    return mission_time

# Switches to 0 acceleration which causes velocity, and altitude to slow/stop directly. Occurs when mission state is Orbit.
def telemetry_timer_orbit(mission_time):
    print("MET: T+", convert(mission_time), "Altitude:" , telemetry_dict["altitude"], "Velocity:", telemetry_dict["velocity"], "Fuel:", telemetry_dict["fuel"], end='\r')
    return mission_time 

# Converts MET to readable form instead of default. 
def convert(mission_time):
    sec = mission_time
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)   

#--------------------------------------------------------------------
# Start of script running (outside of definitions and functions)
weather_check()

# Timers dictionary for ease of future timer addition.
# liftoff_time used to calculate MET in time calculation function.

timer_dict = {
   "liftoff_time" : time.time()
}

# Mission state gets switched to ascent during liftoff function

while telemetry_dict["mission_state"] == ("Ascent"):
#    sets altitude from outside of loop to calculate altitude for telemetry timer during ascent and orbit.
   altitude_tel = (altitude_calculation(time_calculation()))
   telemetry_dict["altitude"] = altitude_tel
#    sets fuel from out of loop to calculate fuel for telemetry timer during ascent and orbit.   
   fuel_tel = fuel_calculation(acceleration_calculation())
   telemetry_dict["fuel"] = fuel_tel
#    sets velo to calculate velocity for telemetry timer during ascent and orbit.   
   velocity_tel = (velocity_calculation(time_calculation(), acceleration_calculation()))
   telemetry_dict["velocity"] = velocity_tel
   time.sleep(1)
   if telemetry_dict["altitude"] <= 10000:
    telemetry_timer_ascent(time_calculation())

# After orbit is achieved mission state switches to Orbit and creates a new line
   elif telemetry_dict["altitude"] >= 10000:
    print()
    print("Orbit insertion nominal")
    time.sleep(1)
    telemetry_dict["mission_state"] = "Orbit"
    log_event()
# Sets orbit telemetry timer function to run after orbit achieved. Pulls time, altitude, fuel, velocity from ascent function. 
while telemetry_dict["mission_state"] == "Orbit" and time_calculation() <= 25:
   telemetry_timer_orbit(time_calculation())
   time.sleep(1)

if telemetry_dict["mission_state"] == "Orbit" and time_calculation() >= 25:
# After set time, orbit finishes and mission complete. Mission log prints with important flight events.
   print()
   print("Mission Completed. Log saved.")
   exit()