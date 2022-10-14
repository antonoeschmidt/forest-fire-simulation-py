import simpy

from processes.forest import Forest

def fire(env, forest):
    yield env.timeout(1)
    forest.step()


# Modify this to work as in https://simpy.readthedocs.io/en/latest/examples/carwash.html 
def setup(env, num_machines, washtime, t_inter):
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the carwash
    carwash = Carwash(env, num_machines, washtime)

    # Create 4 initial cars
    for i in range(4):
        env.process(car(env, 'Car %d' % i, carwash))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
        i += 1
        env.process(car(env, 'Car %d' % i, carwash))

if __name__ == "__main__":
    env = simpy.Environment()

    forest = Forest(20, 20)

    env.process(fire(env,forest))

    env.run(until=15)

    forest.fire.print()