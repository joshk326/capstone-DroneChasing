#!/usr/bin/env python3
from movement import Drone, asyncio


''' This will me the main file ran combining both our movement and vision code '''
async def run():
	drone = Drone("")
	if(await drone.connect() == False):
		return

	await drone.takeoff()

	await drone.left(5.0, 4)

	await drone.right(5.0, 4)

	await drone.up(5.0, 4)

	await drone.down(5.0, 4)

	await drone.land()

	await drone.disconnect()


if __name__ == '__main__':
	asyncio.run(run())
