import asyncio
import json
import queue
from threading import Thread
import threading
from typing import List
import simpy
import websockets
from ca.cellular_automaton import CellularAutomaton
from ca.simple_cell import SimpleCa

simulation_done = threading.local()
simulation_done.x = False

def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton, grid_size: int):
    while True:
        yield env.timeout(1)
        forest.step()
        data = {'grid': forest.data(), 'grid_size': grid_size, 'wind': forest.wind, 'stats': {'x': forest.stats.x, 'y': forest.stats.y}}
        queue.put(data)

def program(grid_size: int = 30, 
            wind: list[int] = [3,1], 
            start_cell: list[int] = [15,15], 
            slow_simulation: bool = False, 
            run_until: int = 10):
    print(f"grid_size: {grid_size}, slow_sim: {slow_simulation}")
    forest = SimpleCa(grid_size, grid_size, (wind[0], wind[1]))
    forest.ignite(start_cell[0], start_cell[1])

    # If we want to slow down the Simulation, use the RealtimeEnvironment
    # https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html

    if slow_simulation:
        env = simpy.RealtimeEnvironment(factor=1, strict=False)
    else:
        env = simpy.Environment()

    env.process(fire_progression(env, forest, grid_size))
    env.run(until=run_until)

    simulation_done.x = True


async def handler(websocket):
    """
    Do not use time.sleep to "slow down" simulation, this might result in the queue getting full :O
    """
    while True:
        item = queue.get()
        await websocket.send(json.dumps(item))

def websocket():
    asyncio.run(websocket1())

async def websocket1():
    print("Websocket Started")
    async with websockets.serve(handler, "0.0.0.0", 8000):
        await asyncio.Future()  # run forever
    print("Websocket Finished")
    
def start_websocket():
    global queue
    queue = queue.Queue()
    ws = Thread(target=websocket)
    ws.start()

def run(simulation_data):
    print("Started run")
    simulation = Thread(target=program(simulation_data['grid_size'],
     simulation_data['wind'], 
     simulation_data['start_cell'], 
     simulation_data['slow_simulation'], 
     simulation_data['run_until']))
     
    simulation.start()
    print("Run done")
