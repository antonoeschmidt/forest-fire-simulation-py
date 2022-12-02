import json
import sys

from simulation import program

if __name__ == "__main__":
    print(f'File:{sys.argv[1]}')
    config_file = open(sys.argv[1], mode='r')
    config = config_file.read()

    a = json.loads(config)

    program(str(a))
