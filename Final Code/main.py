#!/usr/bin/env python3
# import asyncio, os
import movement, vision


''' This will me the main file ran combining both our movement and vision code '''

if __name__ == '__main__':
	drone = Drone("")

	asyncio.run(drone.connect())