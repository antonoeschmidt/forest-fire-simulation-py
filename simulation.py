import asyncio

import simpy
import websockets

from ca.cellular_automaton import CellularAutomaton
from ca.simple_fire import SimpleCa


def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton, websocket):
    while True:
        yield env.timeout(1)
        forest.step()
        data = {'grid': forest.data(), 'grid_size': 20}
        await websocket.send(data)


async def program(websocket):
    forest = SimpleCa(20, 20)

    env = simpy.Environment()

    env.process(fire_progression(env, forest, websocket))

    env.run(until=100)


async def main():
    async with websockets.serve(program, "localhost", 8000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
