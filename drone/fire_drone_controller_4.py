from typing import Tuple, List
from bresenham import bresenham
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from ca.cellular_automaton import CellularAutomaton
from drone.fire_coordinate import Coordinate
from drone.fire_state import DroneState
from drone.fire_drone import FireDrone


class DroneSettings(object):

    def __init__(self, drone_speed: int, drone_base_location: Coordinate, number_of_drones: int, wind: Tuple[int, int], **kwargs):
        self.number_of_drones = number_of_drones
        self.location = drone_base_location
        self.drone_speed = drone_speed
        self.wind = wind


class DroneControllerFour(object):
    """Controls and dispatch drones
    """

    def __init__(self, forest: CellularAutomaton, settings: DroneSettings):
        """Creates a new drone controller
        """
        self.location = Coordinate(
            settings.location['x'], settings.location['y'])
        self.number_of_drones = settings.number_of_drones
        self.drone_speed = settings.drone_speed
        self.targets: List[Coordinate] = []
        self.forest = forest
        self.targets: List[Coordinate] = []
        self.ticks = 0
        self.wind = settings.wind
        self.barrier = self.calculate_barrier(
            self.number_of_drones, self.drone_speed)
        self.drones = [FireDrone(x, settings.drone_speed, self.location.x, self.location.y) for x in
                       range(self.number_of_drones)]

        print(f"Drones: {self.number_of_drones}")

    def step(self) -> None:
        """Updating all drones respectively

        @return: None
        """
        print(len(self.barrier))

        for drone in self.drones:
            if DroneState.IDLE == drone.state:
                if len(self.barrier) > 0:
                    drone.set_target(self.barrier.pop())
                    drone.state = DroneState.FIRE_FIGHTING
                else:
                    pass

            if not drone.reached_target():
                drone.advance()
                continue

            elif DroneState.REFILLING == drone.state:
                if len(self.barrier) > 0:
                    try:
                        drone.set_target(self.barrier.pop())
                        drone.state = DroneState.FIRE_FIGHTING
                    except StopIteration:
                        pass
                else:
                    drone.set_location(Coordinate(
                        self.location.x, self.location.y))
                    drone.state = DroneState.IDLE

            elif DroneState.FIRE_FIGHTING == drone.state:
                self.forest.drop_water(drone.target.x, drone.target.y, 100)
                drone.state = DroneState.REFILLING
                drone.set_target(Coordinate(self.location.x, self.location.y))

    def calculate_barrier(self, no_of_drones: int, drone_speed: int):
        ignition_point = self.forest.ignition_points[0]
        ignition_point = Coordinate(ignition_point[0], ignition_point[1])

        rounds = int(ignition_point.distance(self.location) / drone_speed)
        north_west = (ignition_point.x - rounds, ignition_point.y - rounds)
        south_west = (ignition_point.x - rounds, ignition_point.y + rounds)
        south_east = (ignition_point.x + rounds, ignition_point.y + rounds)
        north_east = (ignition_point.x + rounds, ignition_point.y - rounds)

        nw_to_sw = list(
            bresenham(north_west[0], north_west[1], south_west[0], south_west[1]))
        sw_to_se = list(
            bresenham(south_west[0], south_west[1], south_east[0], south_east[1]))
        se_to_ne = list(
            bresenham(south_east[0], south_east[1], north_east[0], north_east[1]))
        ne_to_nw = list(
            bresenham(north_east[0], north_east[1], north_west[0], north_west[1]))

        x_direction, y_direction = "negative", "negative"

        if self.wind[0] > 0:
            x_direction = "positive"
        if self.wind[1] > 0:
            y_direction = "positive"
        # x barrier is the barrier that blocks the x wind
        x_barrier = []
        # the barrier is always one in depth, so we start at 2.
        for i in range(1, abs(self.wind[0] - 1)):
            initial_barrier = se_to_ne if x_direction == "positive" else nw_to_sw
            factor = i * (1 if x_direction == "positive" else (-1))

            x_barrier = x_barrier + [(coord[0] + factor, coord[1]) for coord in initial_barrier]

        y_barrier = []
        for i in range(1, abs(self.wind[1] - 1)):
            initial_barrier = sw_to_se if y_direction == "positive" else ne_to_nw
            factor = i * (1 if y_direction == "positive" else (-1))

            y_barrier = y_barrier + [(coord[0], coord[1] + factor) for coord in initial_barrier]

        if x_direction == "positive" and y_direction == "positive":
            barrier = barrier + ne_to_nw + nw_to_sw
            if abs(self.wind[0]) > abs(self.wind[1]):
                barrier = barrier + sw_to_se + y_barrier + se_to_ne + x_barrier
            else:
                barrier = barrier + se_to_ne + x_barrier + sw_to_se + y_barrier
            

        elif x_direction == "positive" and y_direction == "negative":
            if abs(self.wind[0]) > abs(self.wind[1]):
                barrier = se_to_ne + x_barrier + ne_to_nw + y_barrier
            else:
                barrier = ne_to_nw + y_barrier + se_to_ne + x_barrier
            barrier = barrier + nw_to_sw + sw_to_se

        elif x_direction == "negative" and y_direction == "positive":
            if abs(self.wind[0]) > abs(self.wind[1]):
                barrier = nw_to_sw + x_barrier + sw_to_se + y_barrier
            else:
                barrier = sw_to_se + y_barrier + nw_to_sw + x_barrier
            barrier = barrier + ne_to_nw + se_to_ne

        elif x_direction == "negative" and y_direction == "negative":
            if abs(self.wind[0]) > abs(self.wind[1]):
                barrier = nw_to_sw + x_barrier + ne_to_nw + y_barrier
            else:
                barrier = ne_to_nw + y_barrier + nw_to_sw + x_barrier
            barrier = barrier + se_to_ne + sw_to_se

        barrier = [Coordinate(x[0], x[1]) for x in barrier if self.forest.cols > x[0] > 0
                   and self.forest.rows > x[1] > 0]

        if no_of_drones < len(barrier):
            self.calculate_barrier(no_of_drones * 2, 1 + (drone_speed / 2))

        return barrier

    def find_fires(self):
        """Find list of fires - the order of importance (FIFO)
        """
        clusters = self.find_clusters()
        fires = []

        for cluster in clusters:
            cluster_fires = []
            south, north, east, west = (
                0, 0), (0, self.forest.rows), (0, 0), (self.forest.cols, 0)
            for cell in cluster:
                x, y = cell
                if y > south[1]:
                    south = (x, y)
                if y < north[1]:
                    north = (x, y)
                if x > east[0]:
                    east = (x, y)
                if x < west[0]:
                    west = (x, y)

            west_x = west[0] - 1 if west[0]-1 > -1 else west[0]
            east_x = east[0] + 1 if east[0]+1 < self.forest.cols else east[0]
            north_y = north[1] - 1 if north[1]-1 > -1 else north[1]
            south_y = south[1] + 1 if south[1] + \
                1 < self.forest.rows else south[1]

            south_to_east = list(bresenham(south[0], south_y, east_x, east[1]))
            east_to_north = list(bresenham(east_x, east[1], north[0], north_y))
            north_to_west = list(bresenham(north[0], north_y, west_x, west[1]))
            west_to_south = list(bresenham(west_x, west[1], south[0], south_y))

            additonal = []
            distance = 3
            for p in south_to_east:
                if p[0] + distance < self.forest.cols:
                    additonal.append((p[0] + distance, p[1]))
                if p[1] + distance < self.forest.rows:
                    additonal.append((p[0], p[1] + distance))

            for p in east_to_north:
                if p[0] + distance < self.forest.cols:
                    additonal.append((p[0] + distance, p[1]))
                if p[1] - distance > 0:
                    additonal.append((p[0], p[1] - distance))

            for p in north_to_west:
                if p[0] - distance > 0:
                    additonal.append((p[0] - distance, p[1]))
                if p[1] - distance > 0:
                    additonal.append((p[0], p[1] - distance))

            for p in west_to_south:
                if p[0] - distance > 0:
                    additonal.append((p[0] - distance, p[1]))
                if p[1] + distance < self.forest.rows:
                    additonal.append((p[0], p[1] + distance))

            # cluster_fires = south_to_east + east_to_north + north_to_west + west_to_south + additonal
            # cluster_fires = additonal

            for fire in additonal:
                if self.forest.get(fire[0], fire[1]).burned == False:
                    cluster_fires.append(fire)

            # Removing duplicates
            cluster_fires = [p for p in (set(tuple(i) for i in cluster_fires))]
            fires = fires + cluster_fires

        return [Coordinate(fire[0], fire[1]) for fire in fires]

    def find_clusters(self):
        """Find clusters of fires"""
        clusters = []
        no_of_clusters = len(self.forest.ignition_points)
        x = []
        y = []

        for i, cell in enumerate(self.forest.grid):
            if (not cell.burned) and cell.fire > 0:
                x.append(self.forest.xy(i)[0])
                y.append(self.forest.xy(i)[1])

        data = list(zip(x, y))
        if len(data) < no_of_clusters:
            no_of_clusters = len(data)

        if len(data) < 2:
            return [data]

        kmeans = KMeans(n_clusters=no_of_clusters, random_state=0).fit(data)
        for i in range(no_of_clusters):
            cluster = []
            for index, point in enumerate(data):
                if kmeans.labels_[index] == i:
                    cluster.append(point)
            clusters.append(cluster)

        # Uncomment to see the clusters in a plot
        # plt.scatter(x, y, c=kmeans.labels_)
        # plt.show()

        return clusters
