import asyncio
from mavsdk import System

async def move_forward(system, distance):
    # Get the current position of the drone
    async for position in system.telemetry.position():
        current_position = position
        
    # Move the drone forward by the specified distance
    target_position = current_position.translate(0.0, distance, 0.0)
    await system.offboard.set_position_ned(target_position)

async def move_right(system, distance):
    # Get the current position of the drone
    async for position in system.telemetry.position():
        current_position = position
        
    # Move the drone to the right by the specified distance
    target_position = current_position.translate(distance, 0.0, 0.0)
    await system.offboard.set_position_ned(target_position)

# Connect to the drone
drone = System()
await drone.connect(system_address="udp://DRONE_IP:PORT")

# Move the drone forward by 5 meters
await move_forward(drone, 5.0)

# Move the drone to the right by 3 meters
await move_right(drone, 3.0)
