from fileinput import filename
import time
import random
import csv

print("NorthLight Launch (Function sytem)")
# prompts user to select save name only during first instance of telemetrycsv function call. After that, it will append to the same file.
filename = input("Enter desired save name: ")
filename = str(filename)

full_filename = f'{filename}.csv' 
log_file_path = 'log.txt'

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
   telemetrycsv_save(full_filename)
   windspeed = int (input("Windspeed: "))
   cloudheight = int (input("Cloud Height in Feet: "))
   temp = int (input("Temperature in C: "))
   precip = (input("Rain? Y or N: "))
   if windspeed < 12 and cloudheight > 10000 and temp < 18 and precip == "N":
    launch_approved()
   else:
    print("Weather is No-Go. Hold Launch.")
    telemetrycsv_update(full_filename)
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

info_failure = {
   "Failure": "None"
}

# TESTING set failure to occur nearly everytime. 
# Failure set to occur if random number picked is between 90 and 100. Will launch successfully if failure occurs. 
def random_failure():
   failure = (random.randint (0, 100))
   if failure > 1 and failure < 100:
      print("Holding launch countdown")
      time.sleep(1)
      failures = list(failure_list.values())  
      selected_failure = random.choice(failures) 
      print (selected_failure["message"], selected_failure["severity"], selected_failure["system"])
      info = (selected_failure["message"], selected_failure["severity"], selected_failure["system"])
      info = str(info)
      info_failure["Failure"] = info
      if selected_failure["shutdown"]:
        time.sleep(1)
        print("Shutdown required")
        telemetry_dict["mission_state"] = "Shutdown"
        log_event()
        failure_csv(full_filename)
        exit()
      else:
        time.sleep(1)
        print("Component not critical, resuming countdown")
        time.sleep(1)
        telemetrycsv_update(full_filename)
        countdown()     
   elif failure > 0 and failure < 1: 
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

# Timers dictionary for ease of future timer addition.
# liftoff_time used to calculate MET in time calculation function.

timer_dict = {
   "liftoff_time" : time.time(),
}

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
    time_update = int(current_time - timer_dict["liftoff_time"])
    return time_update

met_dict = {
   "mission_time" : time_calculation() 
}

# Calculates acceleration for velocity and altitude calculations. Set to 0.6 Gs for testing purposes.
def acceleration_calculation():
    acceleration = int(.6 * 60)
    return acceleration

# Pulls mission time and acceleration from acceleration and time calculation functions to calculate velocity.
def velocity_calculation(acceleration):
    velocity_tel = int(0 + (acceleration * int(met_dict["mission_time"])))
    return velocity_tel

# Pulls mission time, velocity, and altitude to calculate altitude. Altitude is then returned to be used in telemetry timer and altitude calculation for next loop.
def altitude_calculation():
    altitude_tel = int (telemetry_dict["altitude"] + (telemetry_dict["velocity"] * int(met_dict["mission_time"])))
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
def telemetry_timer_ascent():
    print("MET: T+", convert(), "Altitude:" , telemetry_dict["altitude"], "Velocity:", telemetry_dict["velocity"], "Fuel:", telemetry_dict["fuel"], end='\r')

# Switches to 0 acceleration which causes velocity, and altitude to slow/stop directly. Occurs when mission state is Orbit.
def telemetry_timer_orbit():
    print("MET: T+", convert(), "Altitude:" , telemetry_dict["altitude"], "Velocity:", telemetry_dict["velocity"], "Fuel:", telemetry_dict["fuel"], end='\r')

# Converts MET to readable form instead of default. 
def convert():
    sec = met_dict["mission_time"]
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)   
#-------------------------------------------------------------------
# telemetry automatically writes to csv "telemetry.csv" every second.

def telemetrycsv_save(full_filename):
  if telemetry_dict["mission_state"] == "Checking Weather":
     with open(full_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time","State", "Velocity", "Altitude", "Fuel"])
        writer.writerow([met_dict["mission_time"], telemetry_dict["mission_state"], telemetry_dict["velocity"], telemetry_dict["altitude"],telemetry_dict["fuel"]])
   
# appends throughout running, then updates every 5 seconds using loop.
def telemetrycsv_update(full_filename):
  if telemetry_dict["mission_state"] == "Ascent" or telemetry_dict["mission_state"] == "Orbit":
    with open(full_filename, "a", newline="" ) as f:
        writer = csv.writer(f)
        writer.writerow([met_dict["mission_time"], telemetry_dict["mission_state"], telemetry_dict["velocity"], telemetry_dict["altitude"],telemetry_dict["fuel"]])

# controls telemetry csv logging during failure or weather scrub.
# writes time, mission state in whicih the failure occured, and the information given to info_failure.
def failure_csv(full_filename):
   with open(full_filename, "a", newline="") as f:
      writer = csv.writer(f)
      writer.writerow([timestamp(), telemetry_dict["mission_state"], info_failure["Failure"]])

#--------------------------------------------------------------------
# Start of script running (outside of definitions and functions)

weather_check()

# ------------------------------------------------------------------------------------------------------------------------------
# ASCENT PHASE
# Mission state gets switched to ascent during liftoff function
while telemetry_dict["mission_state"] == ("Ascent"):
#   updates mission time starting at acent phase through time_calculaiton function.
   met = (time_calculation())
   met_dict["mission_time"] = met
#    sets altitude from outside of loop to calculate altitude for telemetry timer during ascent and orbit.
   altitude_tel = (altitude_calculation())
   telemetry_dict["altitude"] = altitude_tel
#    sets fuel from out of loop to calculate fuel for telemetry timer during ascent and orbit.   
   fuel_tel = fuel_calculation(acceleration_calculation())
   telemetry_dict["fuel"] = fuel_tel
#    sets velo to calculate velocity for telemetry timer during ascent and orbit.   
   velocity_tel = (velocity_calculation(acceleration_calculation()))
   telemetry_dict["velocity"] = velocity_tel
   time.sleep(1)
   if telemetry_dict["altitude"] <= 10000:
    telemetry_timer_ascent()
    telemetrycsv_update(full_filename)
# After orbit is achieved mission state switches to Orbit and creates a new line
   elif telemetry_dict["altitude"] >= 10000:
    print()
    print("Orbit insertion nominal")
    time.sleep(1)
    telemetry_dict["mission_state"] = "Orbit"
    log_event()

# ------------------------------------------------------------------------------------------------------------------------------
# ORBIT PHASE
# Sets orbit telemetry timer function to run after orbit achieved. Pulls time, altitude, fuel, velocity from ascent function. 
while telemetry_dict["mission_state"] == "Orbit" and time_calculation() <= 25:
   #   updates mission time for csv and telemetry time_calculaiton function during orbit phase.
   met = (time_calculation())
   met_dict["mission_time"] = met 
   telemetry_timer_orbit()
   telemetrycsv_update(full_filename)
   time.sleep(1)

if telemetry_dict["mission_state"] == "Orbit" and time_calculation() >= 25:
# After set time, orbit finishes and mission complete. Mission log prints with important flight events.
   print()
   print("Mission Completed. Log saved.")
   exit()