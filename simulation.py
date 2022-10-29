import asyncio
import json
import queue
from threading import Thread

import simpy
import websockets

from ca.cellular_automaton import CellularAutomaton
from ca.simple_cell import SimpleCa


def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton):
    while True:
        yield env.timeout(1)
        forest.step()
        data = {'grid': forest.data(), 'grid_size': 30, 'wind': forest.wind}
        queue.put(data)


def program():
    forest = SimpleCa(30, 30, (3,1))
    forest.ignite(2, 2)

    # If we want to slow down the Simulation, use the RealtimeEnvironment
    # https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html
    if slowSimulation:
        env = simpy.RealtimeEnvironment(factor=1, strict=False)
    else:
        env = simpy.Environment()

    env.process(fire_progression(env, forest))

    env.run(until=100)
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
