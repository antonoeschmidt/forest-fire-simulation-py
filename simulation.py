import asyncio
import json
import queue
from drone.drone import drone
from drone.base_station import base_station
from threading import Thread
import threading
import simpy
import websockets
from ca.cellular_automaton import CellularAutomaton
from ca.simple_cell import SimpleCa


simulation_done = threading.local()
simulation_done.x = False

def drone_progression(env: simpy.core.Environment, drone_base_station):
    while True:
        yield env.timeout(1)
        drone_base_station.step()

def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton):
    while True:
        yield env.timeout(1)
        forest.step()
       
def data_progression(env: simpy.core.Environment, forest: CellularAutomaton, drone_base_station: base_station, grid_size):
    while True:
        yield env.timeout(1)
        #TODO -> update model with drone data.
        data = {'grid': forest.data(), 'grid_size': grid_size, 'wind': forest.wind }
        queue.put(data)


def program(grid_size: int = 30, 
            wind: list[int] = [3,1], 
            start_cell: list[int] = [15,15], 
            slow_simulation: bool = False, 
            run_until: int = 10):

    # If we want to slow down the Simulation, use the RealtimeEnvironment
    # https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.htmlz

    if slow_simulation:
        env = simpy.RealtimeEnvironment(factor=1, strict=False)
    else:
        env = simpy.Environment()

    forest = SimpleCa(grid_size, grid_size, (wind[0], wind[1]))
    forest.ignite(start_cell[0], start_cell[1])    
    base_station_location = (28,28)
    drones = []
    for i in range(5):
        drones.append(drone(50, base_station_location, env))
    #drones = [drone(50, base_station_location, env), drone(50, base_station_location, env), drone(50, base_station_location, env)]
    drone_base_station = base_station(drones, base_station_location, forest) 
    

    env.process(fire_progression(env, forest))
    env.process(drone_progression(env, drone_base_station))
    env.process(data_progression(env, forest, drone_base_station, grid_size))
    
    env.run(until=run_until)
    print("Simulation done")

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