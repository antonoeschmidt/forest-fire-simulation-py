import ast
import asyncio
import datetime
import json
import math
import os
import queue
from typing import Tuple, List

from threading import Thread
import threading
import simpy
import websockets
from ca.cellular_automaton import CellularAutomaton, CellObject, VegetationType
from ca.iteration_one import IterationOne
from ca.iteration_two import IterationTwo
from ca.simple_cell import SimpleCa, ForestSettings
from drone.fire_drone_controller_2 import DroneControllerTwo, Coordinate, DroneSettings
from drone.fire_drone_controller_1 import DroneControllerOne

simulation_done = threading.local()
simulation_done.x = False


def drone_progression(env: simpy.core.Environment, drone_base_station: DroneControllerTwo):
    while True:
        yield env.timeout(1)
        drone_base_station.step()


def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton):
    while True:
        yield env.timeout(1)
        forest.step()


def data_progression(env: simpy.core.Environment, forest: CellularAutomaton, drone_base_station: DroneControllerTwo,
                     grid_size):
    while True:
        yield env.timeout(1)
        # TODO -> update model with drone data.

        drone_locations = []
        for drone in drone_base_station.drones:
            drone_locations.append((drone.position.y, drone.position.x))
        data = {'grid': forest.data(), 'grid_size': grid_size, 'wind': forest.wind, 'drones': drone_locations,
                'stats.csv': {'x': forest.stats.x, 'y': forest.stats.y}}

        try:
            queue.put(data)
        except Exception:
            pass


class Settings(object):
    def __init__(self,
                 grid_size: int,
                 slow_simulation: bool,
                 run_until: int,
                 ignition_points: List[Tuple[int, int]],
                 forest_iteration: int = 4,
                 drone_iteration: int = 3,
                 **kwargs):
        self.run_until = run_until
        self.ignition_points = ignition_points
        self.slow_simulation = slow_simulation
        self.grid_size = grid_size
        self.forest_iteration = forest_iteration
        self.drone_iteration = drone_iteration


def determine_burn_factor_basic(cell: CellObject, wind: Tuple[int, int]) -> float:
    """
    Function used to determine burn factor given the cell and wind
    @param cell:
    @param wind:
    @return:
    """
    (x_wind, y_wind) = wind

    wind_strength = math.sqrt(x_wind ** 2 + y_wind ** 2)
    wind_strength = wind_strength * 3

    burn_factor = 0
    if VegetationType.LOW_VEG.value == cell.veg:
        burn_factor = 10
    elif VegetationType.MED_VEG.value == cell.veg:
        burn_factor = 20
    elif VegetationType.HIGH_VEG.value == cell.veg:
        burn_factor = 30
    else:
        pass

    return wind_strength + burn_factor


def program(settings_json: str):
    # loaded_json = json.loads(settings_json)
    loaded_json = ast.literal_eval(settings_json)
    settings = Settings(**loaded_json)

    print(f"grid_size: {settings.grid_size}, slow_sim: {settings.slow_simulation}")

    # If we want to slow down the Simulation, use the RealtimeEnvironment
    # https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html

    if settings.slow_simulation:
        env = simpy.RealtimeEnvironment(factor=1, strict=False)
    else:
        env = simpy.Environment()

    forest_settings = ForestSettings(**loaded_json)
    forest_settings.determine_burn_factor = determine_burn_factor_basic

    path = f'stats/{datetime.datetime.now().strftime("%A_%d_%H_%M_%S")}'
    os.makedirs(path)

    configuration = open(f'{path}/configuration.json', mode='w+')
    configuration.write(settings_json)
    configuration.close()

    if settings.forest_iteration == 1:
        forest = IterationOne(settings.grid_size, settings.grid_size, forest_settings, f'{path}/stats.csv')
    elif settings.forest_iteration == 2:
        forest = IterationTwo(settings.grid_size, settings.grid_size, forest_settings, f'{path}/stats.csv')
    elif settings.forest_iteration == 3:
        forest = SimpleCa(settings.grid_size, settings.grid_size, forest_settings, f'{path}/stats.csv')
    elif settings.forest_iteration == 4:
        forest = SimpleCa(settings.grid_size, settings.grid_size, forest_settings, f'{path}/stats.csv')
    else:
        raise Exception("Iteration not yet supported")

    for ignition_point in settings.ignition_points:
        forest.ignite(ignition_point[1], ignition_point[0])

    if settings.drone_iteration == 1:
        drone_base_station = DroneControllerOne(forest, DroneSettings(**loaded_json))
    elif settings.drone_iteration == 2:
        drone_base_station = DroneControllerTwo(forest, DroneSettings(**loaded_json))
    elif settings.drone_iteration == 3:
        drone_base_station = DroneControllerTwo(forest, DroneSettings(**loaded_json))
    else:
        raise Exception("Iteration not yet supported")

    env.process(fire_progression(env, forest))
    env.process(drone_progression(env, drone_base_station))
    env.process(data_progression(env, forest, drone_base_station, settings.grid_size))

    ticks = 0
    while True:
        ticks = ticks + 1
        env.run(until=ticks)

        if forest.done():
            break

        if ticks >= settings.run_until:
            break

    print(f"Simulation done: {ticks} ticks ({settings.run_until} allocated)")

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


def grid(simulation_data):
    grid_size = simulation_data['grid_size']
    seed = simulation_data['seed']

    forest = SimpleCa(grid_size, grid_size, ForestSettings(0, 0, 0, 0, None, (0, 0), seed))

    data = {'grid': forest.data(), 'grid_size': grid_size, 'wind': forest.wind, 'drones': []}

    return data


def run(simulation_data: str):
    print("Started run")
    simulation = Thread(target=program(simulation_data))

    simulation.start()
    print("Run done")
