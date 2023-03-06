#!/usr/bin/env python3
import asyncio, os

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def get_position(system):
	async for position_ned in system.telemetry.position_velocity_ned():
		return position_ned.position.north_m, position_ned.position.east_m, position_ned.position.down_m

async def get_location(system):
	async for position in system.telemetry.position():
		latitude = position.latitude_deg
		longitude = position.longitude_deg
		absolute_altitude = position.absolute_altitude_m
		return latitude, longitude, absolute_altitude

async def move_forward(system, distance):
    current_position = await get_position(system)
    await system.offboard.set_position_ned(PositionNedYaw(current_position[0] + distance, current_position[1], current_position[2], 0.0))

async def move_back(system, distance):
    current_position = await get_position(system)
    await system.offboard.set_position_ned(PositionNedYaw(current_position[0] - distance, current_position[1], current_position[2], 0.0))

async def move_right(system, distance):
    current_position = await get_position(system)
    await system.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1] + distance, current_position[2], 0.0))

async def move_left(system, distance):
    current_position = await get_position(system)
    await system.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1] - distance, current_position[2], 0.0))

async def move_up(system, distance):
    current_position = await get_position(system)
    await system.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1], current_position[2] - distance, 0.0))

async def move_down(system, distance):
    current_position = await get_position(system)
    await system.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1], current_position[2] + distance, 0.0))

async def custom_takeoff(system, altitude):
	current_position = await get_position(system)
	await system.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1], current_position[2] - altitude, 0.0))

async def run():
	""" Does Offboard control using position NED coordinates. """

	drone = System()
	await drone.connect(system_address="udp://:14540")

	print("Waiting for drone to connect...")
	async for state in drone.core.connection_state():
		if state.is_connected:
			print(f"-- Connected to drone!")
			break

	print("Waiting for drone to have a global position estimate...")
	async for health in drone.telemetry.health():
		if health.is_global_position_ok and health.is_home_position_ok:
			print("-- Global position estimate OK")
			break

	print("-- Arming")
	await drone.action.arm()

	print("-- Setting initial setpoint")
	await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

	print("-- Starting offboard")
	try:
		await drone.offboard.start()
		await asyncio.sleep(2)
	except OffboardError as error:
		print(f"Starting offboard mode failed with error code: {error._result.result}")
		print("-- Disarming")
		await drone.action.disarm()
		return

	
	while True:
		latitude, longitude, absolute_altitude = await get_location(drone)

		os.system('cls' if os.name == 'nt' else 'clear')
		print("========================================")
		print("Latitude: " + str(latitude))
		print("Longitude: " + str(longitude))
		print("Altitude: " + str(absolute_altitude))
		print("========================================")
		print("What do you want to do?") 
		print("1. Takeoff")
		print("2. Land")
		print("3. Move forward")
		print("4. Move back")
		print("5. Move right")
		print("6. Move left")
		print("7. Move up")
		print("8. Move down")
		print("9. Exit")

		choice = input("Enter your choice: ")

		if choice == "1":
			print("-- Taking off")
			await custom_takeoff(drone, 5.0)
			await asyncio.sleep(10)
		elif choice == "2":
			print("-- Landing")
			await drone.action.land()
			await asyncio.sleep(10)
		elif choice == "3":
			distance = float(input("Enter the distance: "))
			print("-- Moving forward " + str(distance) + "m")
			await move_forward(drone, distance)
			await asyncio.sleep(10)
		elif choice == "4":
			distance = float(input("Enter the distance: "))
			print("-- Moving back " + str(distance) + "m")
			await move_back(drone, distance)
			await asyncio.sleep(10)
		elif choice == "5":
			distance = float(input("Enter the distance: "))
			print("-- Moving right " + str(distance) + "m")
			await move_right(drone, distance)
			await asyncio.sleep(10)
		elif choice == "6":
			distance = float(input("Enter the distance: "))
			print("-- Moving left " + str(distance) + "m")
			await move_left(drone, distance)
			await asyncio.sleep(10)
		elif choice == "7":
			distance = float(input("Enter the distance: "))
			print("-- Moving up " + str(distance) + "m")
			await move_up(drone, distance)
			await asyncio.sleep(10)
		elif choice == "8":
			distance = float(input("Enter the distance: "))
			print("-- Moving down " + str(distance) + "m")
			await move_down(drone, distance)
			await asyncio.sleep(10)
		elif choice == "9":
			break
		else:
			print("{choice} is an invalid option")

	async for position_ned in drone.telemetry.position_velocity_ned():
		if position_ned.position.down_m < 0.1:
			print("-- Drone is on the ground")
			break
		else:
			print("-- Drone is still in the air")
			print("-- Landing")
			await drone.action.land()
			await asyncio.sleep(10)
			break
	

	print("-- Stopping offboard")
	try:
		await drone.offboard.stop()
	except OffboardError as error:
		print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    asyncio.run(run())
