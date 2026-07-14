import time
import random

log_file_path = 'log.txt'
# Starting values for telemetry system
print("NorthLight Launch (Function sytem)")
mission_state = "Ready"
altitude = 0 
fuel = 100 
velocity = 0

# Functions
# when mission status changes the change is logged. dependent on mission state which func is run
def log_event(mission_state):
   printlog = "Mission Status:"
   if mission_state == "Checking Weather":
      mission_logtxtinit(mission_state)
   else:
      mission_logtxtsec(mission_state, altitude, fuel, velocity)
   print(printlog, mission_state)

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
def mission_logtxtinit(mission_state):
   with open(log_file_path, 'w') as log_file:
       t = timestamp()
       timest = (t)
       log_file.write(mission_state)
       log_file.write('\n')
       log_file.write(timest)

# if mission state is past checking weather, log with skip a line and add the next mission state once reached
def mission_logtxtsec(mission_state, altitude, fuel, velocity):
    with open(log_file_path, 'a') as log_file:
       log_file.write('\n')
       log_file.write(mission_state)
       log_file.write('\n')
       log_file.write(f"altitude: {altitude}\n")
       log_file.write(f"fuel: {fuel}\n")
       log_file.write(f"velocity: {velocity}\n")

def weather_check():
   mission_state = "Checking Weather"
   log_event(mission_state)
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
   return mission_state

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
    random_failure()

# failure dictionary for failure messages and codes.
failure_list = { 
   "FLR-001": "M1D failure imminent",
   "FLR-002": "Propellant Leak",
   "FLR-003": "Guidance Calibration failed"
}

# Failure set to occur if random number picked is between 90 and 100. Will launch successfully if failure occurs. 
def random_failure():
   failure = (random.randint (0, 100))
   if failure > 90 and failure < 100:
      failures = failure_list["FLR-001"], failure_list["FLR-002"], failure_list["FLR-003"]
      print (random.choice(failures))
      time.sleep(1)
      mission_state = "Shutdown"
      log_event(mission_state)
      exit()
   elif failure > 0 and failure < 90: 
      countdown()

countdown_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
def countdown():
    mission_state = "Countdown"
    log_event(mission_state)
    for i in range(0, 10, 1): 
        countdown_list[i]
        time.sleep(1)
        print (countdown_list[i])   
    return mission_state

# Defines the launch time for telemetry_timer to utilize when forming MET. 
def liftofftime():
    launch_time = time.time()
    return launch_time

def liftoff(mission_state):
    time.sleep(1)
    print("Ignition")
    time.sleep(1)
    print("Liftoff")
    mission_state = "Ascent" 
    log_event(mission_state)
    liftofftime()
    return mission_state

# Calculates mission time for other calculations and telemetry timer to use.
def time_calculation():
    current_time = time.time()
    mission_time = (current_time - liftoff_time)
    return mission_time

# Calculates acceleration for velocity and altitude calculations. Set to 0.6 Gs for testing purposes.
def acceleration_calculation():
    acceleration = int (.6 * 60)
    return acceleration

# Pulls mission time and acceleration from acceleration and time calculation functions to calculate velocity.
def velocity_calculation(mission_time, acceleration):
    velocity = int (0 + (acceleration * mission_time))
    return velocity

# Pulls mission time, velocity, and altitude to calculate altitude. Altitude is then returned to be used in telemetry timer and altitude calculation for next loop.
def altitude_calculation(mission_time, velocity, altitude):
    altitude_tel = int (altitude + (velocity * mission_time))
    altitude = altitude_tel
    return altitude
# Pulls acceleration and fuel to calculate fuel burn and new fuel level. New fuel level is returned to telemetry_timer function.
def fuel_calculation(acceleration, fuel): 
    fuel_burn = acceleration * .05
    fuel_new = int (fuel - fuel_burn)
    fuel = fuel_new
    return fuel

# Acceleration (unrealistic #) causes velocity to increase which causes altitude_tel to increase. 
def telemetry_timer_ascent(mission_time, altitude, fuel, velocity):
    print("MET: T+", convert(mission_time), "Altitude:" , altitude, "Velocity:", velocity, "Fuel:", fuel, end='\r')
    return altitude, fuel, velocity

# Switches to 0 acceleration which causes velocity, and altitude to slow/stop directly. Occurs when mission state is Orbit.
def telemetry_timer_orbit(mission_time, altitude, fuel, velocity):
    print("MET: T+", convert(mission_time), "Altitude:" , altitude, "Velocity:", velocity, "Fuel:", fuel, end='\r')
    return altitude, fuel, velocity 

# Converts MET to readable form instead of default. 
def convert(mission_time):
    sec = mission_time
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)   

# Start of script running (outside of definitions and functions)
weather_check()
printlog = "Mission Status:"
# Starting values for telemetry system
mission_state = "Checking Weather"
liftoff_time = liftofftime()
altitude = 0 
fuel = 100 
velocity = 0

# mission state gets switched to ascent during liftoff function

mission_state = liftoff(mission_state)

while mission_state == "Ascent":
#    sets altitude from outside of loop to calculate altitude for telemetry timer during ascent and orbit.
   altitude = altitude_calculation(time_calculation(), velocity_calculation(time_calculation(), acceleration_calculation()), altitude)
#    sets fuel from out of loop to calculate fuel for telemetry timer during ascent and orbit.   
   fuel = fuel_calculation(acceleration_calculation(), fuel)
#    sets velo to calculate velocity for telemetry timer during ascent and orbit.   
   velocity = velocity_calculation(time_calculation(), acceleration_calculation())
   time.sleep(1)
   if altitude <= 10000:
    telemetry_timer_ascent(time_calculation(), altitude, fuel, velocity)

#    After orbit is achieved mission state switches to Orbit and creates a new line
   elif altitude >= 10000:
    print()
    print("Orbit insertion nominal")
    time.sleep(1)
    mission_state = "Orbit"
    log_event(mission_state)
# sets orbit telemetry timer function to run after orbit achieved. Pulls time, altitude, fuel, velocity from ascent function. 
while mission_state == "Orbit" and time_calculation() <= 25:
   telemetry_timer_orbit(time_calculation(), altitude, fuel, velocity)
   time.sleep(1)

if mission_state == "Orbit" and time_calculation() >= 25:
#    after set time, orbit finishes and mission complete. Mission log prints with important flight events.
   print()
   print("Mission Completed. Log saved.")
   exit()