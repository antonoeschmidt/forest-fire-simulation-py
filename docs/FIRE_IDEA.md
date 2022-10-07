# The basic idea to model forest fire

Divide the "map" into cells (.e.g, square meters). Each cell has a coordinate and a state (i.e. low/high-vegetation, burning or burned).

Now, each cell is also a process. Then for each tick, all burning cells has a change to spread to a neighbouring cell, i.e. changing it's state to burn if it is not burned (or blocked in the future). 

Having each cell as a process only being activated at each tick makes it possible for us to change the environment for each tick. E.g., having a weather "manager" to change the wind and therefore change then how far a cell can spread and in which direction. 

Furthermore, each cell should also be responsible for burning out, e.g., it can only burn for a number of ticks based on heat and vegetation.

Having each cell as a process makes sense. Let's say we have to cell, high and low negation. High burns first and then it's spreads to low. Because low have bad odds, it might burn out before the high veg one and since the high veg cell is its own process, it stills lives and can spread to another cell. 


Downside is, our simulation will have A LOT of processes, but I don't know is that is bad or not.


---
Maybe the map should be a resource?



---
This https://realpython.com/simpy-simulating-with-python/ explains pretty good how models are constructed and their lifetime.