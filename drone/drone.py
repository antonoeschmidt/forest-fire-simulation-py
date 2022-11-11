import math
from typing import Tuple

# The drone class doesn't contain a lot of info. It has some basic methods but nothing too fancy.
class drone():
    
    def __init__(self, capacity: int, base_station_location: Tuple[int, int], env):
        self.env = env
        self.speed = 5 # squares a tick
        self.capacity = capacity # liters of water
        self.recharge_time = 0
        self.range = 999999999
        self.wind_resistance = 0
        self.position = base_station_location
        self.destination = base_station_location
        self.has_water = True
        self.water_dropped = env.event()
        self.base_station_location = base_station_location

    def reset(self):
        pass

    def pythagoras(self, a1, a2, b1, b2):
        a = abs(a1 - a2)
        b = abs(b1 - b2)
        return math.sqrt(a ** 2 + b ** 2)
    
    ## pythagoras to get distance.
    def get_distance(self):
        return self.pythagoras(self.position[0], self.destination[0], self.position[1], self.destination[1])
    
    
    
    ## is at drop destination
    def has_reached_destination(self):
        a = self.position[0] == self.destination[0]
        b = self.position[1] == self.destination[1]
        c = self.position[0] != self.base_station_location[0]
        d = self.position[1] != self.base_station_location[1]
        return a and b and c and d
    
    ## not sure what i have to write
    def drop_water(self):
        self.has_water = False
        self.destination = self.base_station_location
    
    def reaching_destination_in_next_step(self):
        self.get_distance() <= self.speed
    # update location
    def step(self):
        
        a_diff = abs(self.position[0] - self.destination[0])
        b_diff = abs(self.position[1] - self.destination[1])
        distance_remaining = self.get_distance() / self.speed
        if distance_remaining <= 1:
            self.position = self.destination
            if self.position == self.base_station_location:
                self.has_water = True
        
        # moves the drone to the spot
        elif distance_remaining > 1:
            a_diff = a_diff / distance_remaining
            b_diff = b_diff / distance_remaining
            a = 0
            b = 0

            if self.position[0] > self.destination[0]:
                a = self.position[0] - a_diff
            else:
                a = self.position[0] + a_diff
            if self.position[1] > self.destination[1]:
                b = self.position[1] - b_diff
            else:
                b = self.position[1] + b_diff
            self.position = (a,b)
        
    
    

    def set_destination(self, destination: Tuple[int, int]):
        self.destination = destination