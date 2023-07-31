import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            for client in connected_clients:
                await client.send(message)
                print(f"Received: {message}")
    except:
        pass
    finally:
        connected_clients.remove(websocket)

async def receive_messages():
    async with websockets.connect("ws://localhost:8765/") as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

async def send_message():
    async with websockets.connect("ws://localhost:8765/") as websocket:
        while True:
            user_input = input("Enter message: ")
            await websocket.send(user_input)
            print(f"Sent: {user_input}")

# Run the WebSocket server and both sending and receiving tasks
start_server = websockets.serve(handle_client, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(asyncio.gather(receive_messages(), send_message()))
asyncio.get_event_loop().run_forever()
