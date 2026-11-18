from fileinput import filename
import time
import random
import csv
import json

print("NorthLight Launch Awareness System")
# prompts user to select save name only during first instance of telemetrycsv function call. After that, it will append to the same file.
filename = input("Enter desired save name: ")
filename = str(filename)

TEST_MODE = False

def timesleep1():
    if not TEST_MODE:
        time.sleep(1)

# ----------------------------------------------------------------
# TELEMETRY, FAILURE, WEATHER LOGGING (.CSV and .TXT)
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

# ----------------------------------------------------------------
# WEATHER AND RANGE CONSOLE

def weather_check():
   telemetry_dict["mission_state"] = "Checking Weather"
   log_event()
   telemetrycsv_save(full_filename)
   weather_info["Wind"] = int(input("Windspeed: "))
   weather_info["Clouds"] = int(input("Cloud Height in Feet: "))
   weather_info["Temp"] = int(input("Temperature in C: "))
   weather_info["Rain"] = (input("Rain? Y or N: ")).strip().upper()
   update_weather_json()
   if weather_info["Wind"] < 12 and weather_info["Clouds"] > 10000 and weather_info["Temp"] < 18 and weather_info["Temp"] > 10 and weather_info["Rain"] == "N":
    launch_approved()
   else:
    print("WARNING: Automated weather verification failed.")
    systems_poll(weather_ok=False)
    telemetrycsv_update(full_filename)
    timesleep1()

def hold_procedure():
    telemetry_dict["mission_state"] = "Hold"
    log_event()
    hold_feedback_csv()
    print("\n========== NLAS LAUNCH HOLD ==========")
    print("LAUNCH STATUS: HOLD")
    print("Countdown authorization denied.")
    print("======================================")
    raise SystemExit

      
weather_info = {
   "Wind" : 0 ,
   "Clouds" : 30000 ,
   "Temp" : 15 ,
   "Rain" : "N"
}

weather_json = json.dumps(weather_info)

def update_weather_json():
   with open("weather.json", "w") as f:
      json.dump(weather_info, f, indent=4)

# Gets called from weather
def launch_approved():
    print("Weather systems verified, starting system Go/No-Go polling.")
    timesleep1()
    systems_poll(weather_ok=True)

# ----------------------------------------------------------------
# Systems GO/NO-GO
# User input system go/no-go functions.
system_status = {
   "Weather" : "",
   "Propulsion" : "",
   "GNC" : "",
   "Electrical" : ""
}

def systems_poll(weather_ok):
   for i in system_status:
      if i == "Weather":
                  print(f"Automated weather verification status: {weather_ok}")
                  print("Requesting final Weather Officer GO/NO-GO.")
      while True:   
         status = input(f"Enter {i} GO/NO-GO Status: ").strip().upper()
         if status in ("GO", "NO-GO"):
            system_status[i] = status
            break
         else:
            print("Invalid input. Enter Go or No-go.")
   print("SYSTEMS POLL COMPLETE")
   print("\n========== NLAS SYSTEMS POLL ==========\n")

   for system, status in system_status.items():
      print(f"{system:<15} {status}")

   print("\n---------------------------------------")

   if weather_ok and all(status == "GO" for status in system_status.values()):
    print("FINAL LAUNCH STATUS: GO")
    print("---------------------------------------")
    timesleep1()
    random_failure()
   else:
      hold_procedure()

# ----------------------------------------------------------------
# FAILURES
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
   if failure >= 90 and failure <= 100:
      print("Holding launch countdown")
      timesleep1()
      failures = list(failure_list.values())  
      selected_failure = random.choice(failures) 
      print (selected_failure["message"], selected_failure["severity"], selected_failure["system"])
      info = (selected_failure["message"], selected_failure["severity"], selected_failure["system"])
      info = str(info)
      info_failure["Failure"] = info
      if selected_failure["shutdown"]:
        timesleep1()
        print("Shutdown required")
        telemetry_dict["mission_state"] = "Shutdown"
        log_event()
        failure_csv(full_filename)
        exit()
      else:
        timesleep1()
        print("Component not critical, resuming countdown")
        timesleep1()
        telemetrycsv_update(full_filename)
        countdown()     
   elif failure >= 0 and failure < 90: 
      countdown()

# ----------------------------------------------------------------
# COUNTDOWN/LIFTOFF

countdown_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
def countdown():
    telemetry_dict["mission_state"] = "Countdown"
    log_event()
    for i in range(0, 10, 1): 
        countdown_list[i]
        timesleep1()
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
    timesleep1()
    print("Ignition")
    timesleep1()
    print("Liftoff")
    telemetry_dict["mission_state"] = "Ascent" 
    log_event()
    liftofftime()

# ----------------------------------------------------------------
# TELEMETRY AND TIME CALCULATIONS
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
    acceleration = .6*9.81
    return acceleration

# Pulls mission time and acceleration from acceleration and time calculation functions to calculate velocity.
def velocity_calculation(acceleration):
    met=met_dict["mission_time"]
    velocity_tel = acceleration*met
    return velocity_tel

# Pulls mission time and accelaration to calculate altitude. Altitude is then returned to be used in telemetry timer and altitude calculation for next loop.
def altitude_calculation(acceleration):
    met=met_dict["mission_time"]
    altitude_tel = 0.5*acceleration*met**2
    return altitude_tel
# 

# Calculates fuel decline by using a constant burn rate of 0.3/sec and multiplying that by mission time to determine fuel amount. 
def fuel_calculation(): 
    fuel_burn_rate = 0.30  
    met=met_dict["mission_time"]
    fuel_tel = max(0.0,100.0-fuel_burn_rate*met)
    return fuel_tel


# ----------------------------------------------------------------
# TELEMETRY AND MET DISPLAY
# Centralized mission data refactor to allow there to be only one source of telemetry and mission data. 
telemetry_dict = {
   "mission_state": "Checking Weather",
   "velocity": 0,
   "altitude": 0,
   "fuel": 100
}

# Continues monitoring telemetry and switching timer during ascent phase of flight
# Acceleration (unrealistic #) causes velocity to increase which causes altitude_tel to increase. 
# Converts MET to readable form instead of default. 
def convert():
    sec = met_dict["mission_time"]
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec) 

def telemetry_timer():
    print(f"MET: T+{convert()} Altitude: {telemetry_dict["altitude"]:.2f} Velocity: {telemetry_dict["velocity"]:.2f} Fuel: {telemetry_dict["fuel"]:.2f}", end='\r')

json_telemetry = json.dumps(telemetry_dict)

def json_update_telemetry():
   with open("telemetry.json", "w") as f:
      json.dump(telemetry_dict, f, indent=4)
   
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
  if telemetry_dict["mission_state"] == "Ascent" or telemetry_dict["mission_state"] == "Raising Orbit":
    with open(full_filename, "a", newline="" ) as f:
        writer = csv.writer(f)
        writer.writerow([met_dict["mission_time"], telemetry_dict["mission_state"], telemetry_dict["velocity"], telemetry_dict["altitude"],telemetry_dict["fuel"]])

# controls telemetry csv logging during failure or weather scrub.
# writes time, mission state in whicih the failure occured, and the information given to info_failure.
def failure_csv(full_filename):
   with open(full_filename, "a", newline="") as f:
      writer = csv.writer(f)
      writer.writerow([timestamp(), telemetry_dict["mission_state"], info_failure["Failure"]])

# writes time, and weather conditions stored into weather dictionary, if weather scrub is triggered. 
def hold_feedback_csv():
      with open(full_filename, "a", newline="") as f:
         writer = csv.writer(f)
         writer.writerow(["Time", "Wind (kts)", "Clouds (ft AGL)", "Temp (Celsius)", "Rain", "Wx Approval", "Prop", "GNC", "Elec"])
         writer.writerow([timestamp(), weather_info["Wind"], weather_info["Clouds"], weather_info["Temp"], weather_info["Rain"], system_status["Weather"], system_status["Propulsion"], system_status["GNC"], system_status["Electrical"]])
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
   acceleration = acceleration_calculation()
#    sets altitude from outside of loop to calculate altitude for telemetry timer during ascent and orbit.
   altitude_tel = (altitude_calculation(acceleration))
   telemetry_dict["altitude"] = altitude_tel
#    sets fuel from out of loop to calculate fuel for telemetry timer during ascent and orbit.   
   fuel_tel = fuel_calculation()
   telemetry_dict["fuel"] = fuel_tel
#    sets velo to calculate velocity for telemetry timer during ascent and orbit.   
   velocity_tel = (velocity_calculation(acceleration))
   telemetry_dict["velocity"] = velocity_tel
   json_update_telemetry()
   time.sleep(1)
   if telemetry_dict["altitude"] <= 100000:
    telemetry_timer()
    telemetrycsv_update(full_filename)
# After orbit is achieved mission state switches to Orbit and creates a new line
   elif telemetry_dict["altitude"] >= 100000:
    print()
    print("Orbit insertion nominal. Raising Orbit")
    time.sleep(1)
    telemetry_dict["mission_state"] = "Raising Orbit"
    orbit_start_time = time_calculation()
    log_event()

# ------------------------------------------------------------------------------------------------------------------------------
# ORBIT PHASE
# Sets orbit telemetry timer function to run after orbit achieved. Pulls time, altitude, fuel, velocity from ascent function. 
while telemetry_dict["mission_state"] == "Raising Orbit" and time_calculation()-orbit_start_time < 25:
   #   updates mission time for csv and telemetry time_calculaiton function during orbit phase.
   met = (time_calculation())
   met_dict["mission_time"] = met 
   telemetry_timer()
   telemetrycsv_update(full_filename)
   time.sleep(1)

while telemetry_dict["mission_state"] == "Raising Orbit" and time_calculation()-orbit_start_time >= 25 and time_calculation()-orbit_start_time <= 45:
   met = (time_calculation())
   met_dict["mission_time"] = met
   telemetry_dict["velocity"] = 400
   telemetry_timer()
   telemetry_dict["altitude"] = altitude_tel
   time.sleep(1)
   
if telemetry_dict["mission_state"] == "Raising Orbit" and time_calculation()-orbit_start_time >= 45:
# After set time, orbit finishes and mission complete. Mission log prints with important flight events.
   print()
   print("Orbit Raised to Correct Altitude. Log saved.")
   exit()