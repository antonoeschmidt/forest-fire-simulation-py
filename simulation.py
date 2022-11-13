import asyncio
import json
import queue
from typing import Tuple

from drone.drone import Drone
from threading import Thread
import threading
import simpy
import websockets
from ca.cellular_automaton import CellularAutomaton
from ca.simple_cell import SimpleCa
from drone.fire_drone_manager import DroneController, Coordinate

simulation_done = threading.local()
simulation_done.x = False


def drone_progression(env: simpy.core.Environment, drone_base_station: DroneController):
    while True:
        yield env.timeout(1)
        drone_base_station.step()


def fire_progression(env: simpy.core.Environment, forest: CellularAutomaton):
    while True:
        yield env.timeout(1)
        forest.step()


def data_progression(env: simpy.core.Environment, forest: CellularAutomaton, drone_base_station: DroneController,
                     grid_size):
    while True:
        yield env.timeout(1)
        # TODO -> update model with drone data.

        drone_locations = []
        for drone in drone_base_station.drones:
            drone_locations.append((drone.position.x, drone.position.y))
        data = {'grid': forest.data(), 'grid_size': grid_size, 'wind': forest.wind, 'drones': drone_locations}
        queue.put(data)


def program(grid_size: int = 30,
            wind: list[int] = [3, 1],
            ignition_points: list[Tuple[int, int]] = None,
            slow_simulation: bool = False,
            run_until: int = 10,
            seed: int = 1):
    # If we want to slow down the Simulation, use the RealtimeEnvironment
    # https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html

    if slow_simulation:
        env = simpy.RealtimeEnvironment(factor=1, strict=False)
    else:
        env = simpy.Environment()

    forest = SimpleCa(grid_size, grid_size, (wind[0], wind[1]), seed)
    for ignition_point in ignition_points:
        forest.ignite(ignition_point[1], ignition_point[0])
    base_station_location = (28, 28)
    drones = []
    for i in range(1):
        drones.append(Drone(50, base_station_location, env))

    # drone_base_station = BaseStation(drones, base_station_location, forest)
    drone_base_station = DroneController(20, forest, 5, Coordinate(2, 2))

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


def grid(simulation_data):
    grid_size = simulation_data['grid_size']
    wind = simulation_data['wind']
    seed = simulation_data['seed']

    forest = SimpleCa(grid_size, grid_size, (wind[0], wind[1]), seed)

    data = {'grid': forest.data(), 'grid_size': grid_size, 'wind': forest.wind, 'drones': []}

    return data


def run(simulation_data):
    print("Started run")
    simulation = Thread(target=program(simulation_data['grid_size'],
                                       simulation_data['wind'],
                                       simulation_data['start_cell'],
                                       simulation_data['slow_simulation'],
                                       simulation_data['run_until'],
                                       simulation_data['seed']))

    simulation.start()
    print("Run done")
