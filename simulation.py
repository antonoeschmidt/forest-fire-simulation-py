import asyncio
import json
import time
from threading import Thread
import queue

import simpy
import websockets

from ca.cellular_automaton import CellularAutomaton
from ca.simple_fire import SimpleCa


def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton):
    while True:
        yield env.timeout(1)
        forest.step()
        data = {'grid': forest.data(), 'grid_size': 20}
        queue.put(data)


async def program():
    forest = SimpleCa(20, 20)
    forest.ignite(2, 2)
    env = simpy.Environment()

    env.process(fire_progression(env, forest))

    env.run(until=100)


async def handler(websocket):
    while True:
        item = queue.get()
        await websocket.send(json.dumps(item))
        time.sleep(1)


async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever


queue = queue.Queue()

if __name__ == "__main__":
    asyncio.run(program())
    asyncio.run(main())

    # simulation = Thread(target=program, args=(queue,))
    # websocket1 = Thread(target=main, args=(queue,))
    #
    # simulation.start()
    # websocket1.start()
