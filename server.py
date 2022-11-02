#!/usr/bin/env python

import asyncio
import websockets

async def chat(websocket, path):
	while(True):
            await websocket.send("welcome")
            msg = await websocket.recv()
            print(f"From Client: {msg}")

            msg = input("Enter message to client(type 'q' to exit): ")
            if msg == "q":
                break
            await websocket.send(msg)

start_server = websockets.serve(chat, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()