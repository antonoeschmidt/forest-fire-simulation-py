import json

from simulation import program

if __name__ == "__main__":
    config_file = open('config.json', mode='r')
    config = config_file.read()

    a = json.loads(config)

    program(str(a))
