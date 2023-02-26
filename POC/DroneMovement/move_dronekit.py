import time
from dronekit import connect, VehicleMode

# Connect to the drone
connection_string = 'udp:DRONE_IP:PORT' # Change to the IP address of your drone
vehicle = connect(connection_string, wait_ready=True)

# Set the vehicle mode to GUIDED
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name=='GUIDED':
    time.sleep(1)

# Arm the vehicle and takeoff
vehicle.armed = True
vehicle.simple_takeoff(5) # Change the altitude to the desired height

# Move the drone forward
vehicle.simple_goto(vehicle.location.global_relative_frame + LocationGlobalRelative(10, 0, 0))

# Move the drone to the right
vehicle.simple_goto(vehicle.location.global_relative_frame + LocationGlobalRelative(0, 10, 0))

# Move the drone up
vehicle.simple_goto(vehicle.location.global_relative_frame + LocationGlobalRelative(0, 0, -10))

# Move the drone to the left
vehicle.simple_goto(vehicle.location.global_relative_frame + LocationGlobalRelative(-10, 0, 0))

# Move the drone back
vehicle.simple_goto(vehicle.location.global_relative_frame)

# Land the vehicle and disarm
vehicle.mode = VehicleMode("LAND")
while not vehicle.mode.name=='LAND':
    time.sleep(1)

vehicle.armed = False

# Close the connection to the vehicle
vehicle.close()
