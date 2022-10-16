import asyncio
import websockets
import json

from ca.simple_fire import SimpleCa


async def handler(websocket, path):
    grid_size = 50
    ca = SimpleCa(grid_size, grid_size)
    ca.ignite(3, 3)
    data = {}
    while not ca.done():
        ca.step()
        grid = ca.data()
        data["grid_size"] = grid_size
        data["grid"] = grid
        await websocket.send(json.dumps(data))
        # time.sleep(1)


start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
