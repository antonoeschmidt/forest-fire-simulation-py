import simpy

# Set up the environment
env = simpy.Environment()

# Assume you've defined checkpoint_run() beforehand
env.process(checkpoint_run(env, num_booths, check_time, passenger_arrival))

# Let's go!
env.run(until=10)