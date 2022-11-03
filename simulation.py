import asyncio
import json
import queue
from drone.drone import drone
from drone.base_station import base_station
from threading import Thread

import simpy
import websockets

from ca.cellular_automaton import CellularAutomaton
from ca.simple_cell import SimpleCa

def drone_progression(env: simpy.core.Environment, drones, forest):
    while True:
        yield env.timeout(1)
        drones.step()

def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton, drone_base_station):
    while True:
        yield env.timeout(1)
        forest.step()
        drone_base_station.step()
        data = {'grid': forest.data(), 'grid_size': 30, 'wind': forest.wind }
        queue.put(data)


def program():
    

    # If we want to slow down the Simulation, use the RealtimeEnvironment
    # https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html
    if slowSimulation:
        env = simpy.RealtimeEnvironment(factor=1, strict=False)
    else:
        env = simpy.Environment()

    forest = SimpleCa(30, 30, env, (3,1))
    forest.ignite(29, 29)
    base_station_location = (2,2)
    drones = [drone(50, base_station_location, env), drone(50, base_station_location, env), drone(50, base_station_location, env)]
    drone_base_station = base_station(drones, base_station_location, forest) 
    

    env.process(fire_progression(env, forest, drone_base_station))
    #env.process(drone_progression(env, drones, forest))
    end_event = env.event()
    env.run(until=40)
    end_event.succeed()
    
    print("Simulation done")


async def handler(websocket):
    """
    Do not use time.sleep to "slow down" simulation, this might result in the queue getting full :O
    """
    while True:
        item = queue.get()
        await websocket.send(json.dumps(item))


async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    slowSimulation = True
    queue = queue.Queue()
    simulation = Thread(target=program)
    simulation.start()

    asyncio.run(main())
