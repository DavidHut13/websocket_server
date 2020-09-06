import asyncio
import websockets
import json
import uuid
from datetime import datetime, timedelta


SERVER_ADDRESS = "localhost"
SERVER_PORT = 5050
CLIENTS_CONNECTED = set()
MESSAGE_DICT = {
    'message': 'test',
    'sender': 'David',
    'id': 0,
    'time_stamp': ''
}







async def handle_connection(websocket, path):
    
    CLIENTS_CONNECTED.add(websocket)
    print('[User Connected]')
    try:
        while True:
            print('[Listening]...')
            print(f'{CLIENTS_CONNECTED}')
            utc_time = datetime.utcnow()
            central_time = (utc_time + timedelta(hours=-5))
            formatnow = central_time.strftime("%A,%d %b, %y %I:%M:%S %p")
            message = await websocket.recv()
            MESSAGE_DICT['message'] = message
            MESSAGE_DICT['id'] = str(uuid.uuid1())
            MESSAGE_DICT['time_stamp'] = str(formatnow)
            print('[Recieved Message]')
            json_string = json.dumps(MESSAGE_DICT)
            for client in CLIENTS_CONNECTED:
              await client.send(json_string)
            
               
    finally:
        print('[User Disconnected]')
        CLIENTS_CONNECTED.remove(websocket)

print('[Server Started]')
start_server = websockets.serve(handle_connection, SERVER_ADDRESS, SERVER_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
