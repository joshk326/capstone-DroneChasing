#!/usr/bin/env python3
import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

class Drone():
	def __init__(self, ip):
		self.ip = ip
		self.drone_sys = System()
	async def connect(self):
		try:	
			await self.drone_sys.connect(system_address="udp://"+self.ip+":14540")
			print("Waiting for drone to connect...")
			async for state in self.drone_sys.core.connection_state():
				if state.is_connected:
					print(f"-- Connected to drone!")
					break
			print("Waiting for drone to have a global position estimate...")
			async for health in self.drone_sys.telemetry.health():
				if health.is_global_position_ok and health.is_home_position_ok:
					print("-- Global position estimate OK")
					break

			print("-- Arming")
			await self.drone_sys.action.arm()

			print("-- Setting initial setpoint")
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
			
			await self.start_offboard()
		except:
			print("Error connecting drone")
			return
	async def disconnect(self):
		async for position_ned in self.drone_sys.telemetry.position_velocity_ned():
			if position_ned.position.down_m < 0.1:
				print("-- Drone is on the ground")
				await self.stop_offboard()
				await self.drone_sys.action.disarm()
				break
			else:
				print("-- Drone is still in the air")
				await self.land()
				await self.stop_offboard()
				await self.drone_sys.action.disarm()
				break
	async def start_offboard(self):
		print("-- Starting offboard")
		try:
			await self.drone_sys.offboard.start()
			await asyncio.sleep(2)
		except OffboardError as error:
			print(f"Starting offboard mode failed with error code: {error._result.result}")
			print("-- Disarming")
			await self.drone_sys.action.disarm()
			return
	async def stop_offboard(self):
		print("-- Stopping offboard")
		try:
			await self.drone_sys.offboard.stop()
		except OffboardError as error:
			print(f"Stopping offboard mode failed with error code: {error._result.result}")
	async def get_position(self):
		async for position_ned in self.drone_sys.telemetry.position_velocity_ned():
			return position_ned.position.north_m, position_ned.position.east_m, position_ned.position.down_m
	async def get_location(self):
		async for position in self.drone_sys.telemetry.position():
			latitude = position.latitude_deg
			longitude = position.longitude_deg
			absolute_altitude = position.absolute_altitude_m
			return latitude, longitude, absolute_altitude
	async def forward(self, distance, sleep_t):
		if(isinstance(distance, float) and isinstance(sleep_t, int)):
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0] + distance, current_position[1], current_position[2], 0.0))
			print("-- Going forward: " + str(distance) + "m")
			await asyncio.sleep(sleep_t)
		else:
			print("distance must be a float and sleep must an integer")
	async def backward(self, distance, sleep_t):
		if(isinstance(distance, float) and isinstance(sleep_t, int)):
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0] - distance, current_position[1], current_position[2], 0.0))
			print("-- Going backwards: " + str(distance) + "m")
			await asyncio.sleep(sleep_t)
		else:
			print("distance must be a float and sleep must an integer")
	async def right(self, distance, sleep_t):
		if(isinstance(distance, float) and isinstance(sleep_t, int)):
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1] + distance, current_position[2], 0.0))
			print("-- Going right: " + str(distance) + "m")
			await asyncio.sleep(sleep_t)
		else:
			print("distance must be a float and sleep must an integer")
	async def left(self, distance, sleep_t):
		if(isinstance(distance, float) and isinstance(sleep_t, int)):
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1] - distance, current_position[2], 0.0))
			print("-- Going left: " + str(distance) + "m")
			await asyncio.sleep(sleep_t)
		else:
			print("distance must be a float and sleep must an integer")
	async def up(self, distance, sleep_t):
		if(isinstance(distance, float) and isinstance(sleep_t, int)):
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1], current_position[2] - distance, 0.0))
			print("-- Going up: " + str(distance) + "m")
			await asyncio.sleep(sleep_t)
		else:
			print("distance must be a float and sleep must an integer")
	async def down(self, distance, sleep_t):
		if(isinstance(distance, float) and isinstance(sleep_t, int)):
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1], current_position[2] + distance, 0.0))
			print("-- Going down: " + str(distance) + "m")
			await asyncio.sleep(sleep_t)
		else:
			print("distance must be a float and sleep must an integer")
	async def takeoff(self, altitude=5.0):
		if(isinstance(altitude, float)):
			print("-- Taking off to an altitude of: " + str(altitude) +"m")
			current_position = await self.get_position()
			await self.drone_sys.offboard.set_position_ned(PositionNedYaw(current_position[0], current_position[1], current_position[2] - altitude, 0.0))
			await asyncio.sleep(10)
		else:
			print("altitude must be a float")
	async def land(self):
		print("-- Landing")
		await self.drone_sys.action.land()
		await asyncio.sleep(10)
