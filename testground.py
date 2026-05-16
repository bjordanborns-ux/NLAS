import time
import random
print("NorthLight Launch (Function sytem)")
  
# Telemetry Functions:

Altitude = ()

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

def launch_approved():
    print("Weather systems verified, approved for launch.")
    time.sleep(1)
    print("Initating countdown sequence. T-")
    random_failure()

def random_failure():
   failure = (random.randint (0, 100))
   if failure > 90 and failure < 100:
      failures = ["M1D failure imminent", "Propellant Leak", "Guidance Calibration failed"]
      print (random.choice(failures))
      time.sleep(1)
      mission_state = "Failed."
      print("Mission Status:", mission_state)
   elif failure > 0 and failure < 90: 
      countdown()

countdown_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
def countdown():
    mission_state = "Countdown"
    print("Mission Status:", mission_state)
    for i in range(0, 10, 1): 
        countdown_list[i]
        time.sleep(1)
        print (countdown_list[i])    
    liftoff()

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

def mission_timer():
    
    current_time = time.time()
    mission_time = (current_time - liftoff_time)
    print("MET: T+", convert(mission_time), end='\r')

def convert(mission_time):
    sec = mission_time
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)   

# Start of script running (outside of definitions and functions)
weather_check()
liftoff_time = liftofftime()
mission_state = "Ascent"
while mission_state == "Ascent":
   mission_timer()
   time.sleep(1)




