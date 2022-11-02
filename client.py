#!/usr/bin/env python

import asyncio
import websockets

async def chat():
	async with websockets.connect('ws://localhost:8765') as websocket:
            while(True):
                msg = input("Enter message to server (type 'q' to exit):")
                if msg == "q":
                    break
                await websocket.send(msg)

                msg = await websocket.recv()
                print(f"From Server: {msg}")

asyncio.get_event_loop().run_until_complete(chat())