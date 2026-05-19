import time
import random
print("NorthLight Launch (Function sytem)")

# Functions
def weather_check():
   mission_state = "Checking Weather"
   print("Mission Status:", mission_state)
   windspeed = int (input("Windspeed: "))
   cloudheight = int (input("Cloud Height in Feet: "))
   temp = int (input("Temperature in C: "))
   precip = (input("Rain? Y or N: "))
   if windspeed < 12 and cloudheight > 10000 and temp < 18 and precip == "N":
    launch_approved()
   else:
    print("Weather is No-Go. Hold Launch.")
    time.sleep(1)
    print("System Terminating.")
# Gets called from weather
def launch_approved():
    print("Weather systems verified, approved for launch.")
    time.sleep(1)
    print("Initating launch countdown sequence.")
    random_failure()
# Failure set to occur if random number picked is between 90 and 100. Will launch successfully if failure occurs. 
def random_failure():
   failure = (random.randint (0, 100))
   if failure > 90 and failure < 100:
      failures = ["M1D failure imminent", "Propellant Leak", "Guidance Calibration failed"]
      print (random.choice(failures))
      time.sleep(1)
      mission_state = "Failed."
      print("Mission Status:", mission_state)
      SystemExit
   elif failure > 0 and failure < 90: 
      countdown()

countdown_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
def countdown():
    mission_state = "Countdown"
    print("Mission Status:", mission_state, "T -")
    for i in range(0, 10, 1): 
        countdown_list[i]
        time.sleep(1)
        print (countdown_list[i])    
    liftoff()
# Defines the launch time for telemetry_timer to utilize when forming MET. 
def liftofftime():
    launch_time = time.time()
    return launch_time

def liftoff():
    time.sleep(1)
    print("Ignition")
    time.sleep(1)
    print("liftoff")
    mission_state = "Ascent" 
    print("Mission Status:", mission_state)
    liftofftime()
    return mission_state
# Acceleration (unrealistic #) causes velocity to increase which causes altitude_tel to increase. 
def telemetry_timer_ascent(altitude, fuel, velocity):
    current_time = time.time()
    mission_time = (current_time - liftoff_time)
    acceleration = int (.6 * 60)
    velocity = int (0 + (acceleration * mission_time))
    altitude_tel = int (altitude + (velocity * mission_time))
    altitude = altitude_tel
    fuel_burn = acceleration * .05
    fuel_new = int (fuel - fuel_burn)
    fuel = fuel_new
    print("MET: T+", convert(mission_time), "Altitude:" , altitude_tel, "Velocity:", velocity, "Fuel:", fuel, end='\r')
    return altitude, fuel, velocity 

# Switches to 0 acceleration which causes velocity, and altitude to slow/stop directly. Occurs when mission state is Orbit.
def telemetry_timer_orbit(altitude, fuel, velocity):
    current_time = time.time()
    mission_time = (current_time - liftoff_time)
    acceleration = 0
    velocity = int (0 + (acceleration * mission_time))
    altitude_tel = int (altitude + (velocity * mission_time))
    altitude = altitude_tel
    fuel_burn = acceleration * .05
    fuel_new = int (fuel - fuel_burn)
    fuel = fuel_new
    print("MET: T+", convert(mission_time), "Altitude:" , altitude_tel, "Velocity:", velocity, "Fuel:", fuel, end='\r')
    return altitude, fuel, velocity 

# Converts MET to readable form instead of default. 
def convert(mission_time):
    sec = mission_time
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)   

# Start of script running (outside of definitions and functions)
weather_check()
# Starting values for telemetry system
mission_state = "Checking Weather"
liftoff_time = liftofftime()
altitude = 0 
fuel = 100 
velocity = 0
altitude, fuel, velocity = telemetry_timer_ascent(altitude, fuel, velocity)
mission_state = liftoff()

while mission_state == "Ascent":
   altitude, fuel, velocity = telemetry_timer_ascent(altitude, fuel, velocity)
   time.sleep(1)
   if altitude <= 10000:
    telemetry_timer_ascent(altitude, fuel, velocity)
   elif altitude >= 10000:
    mission_state = "Orbit"
    print("Mission Status:", mission_state, end='\n')

while mission_state == "Orbit":
   telemetry_timer_orbit(altitude, fuel, velocity)
   time.sleep(1)

