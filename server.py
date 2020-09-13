import asyncio
import websockets
import json
import uuid
import copy
from datetime import datetime, timedelta


SERVER_ADDRESS = "localhost"
SERVER_PORT = 5050
CLIENTS_CONNECTED = set()
rooms = [
    {
        'id': 0,
        'member_list': []
    }
]
MESSAGE_DICT = {
    'message': 'test',
    'sender': 'David',
    'id': 0,
    'time_stamp': '',
    'room_id': 0
}


async def handle_connection(websocket, path):
    CLIENTS_CONNECTED.add(websocket)
    print('[User Connected]')
    try:
        while True:
            print('[Listening]...')
            print(f'{CLIENTS_CONNECTED}')
            message = await websocket.recv()
            completed_message = handle_incoming_messages(message)
            await send_message(completed_message)
                     
    finally:
        print('[User Disconnected]')
        CLIENTS_CONNECTED.remove(websocket)


async def send_message(message):
    if message['room_id'] == 0:
        json_message = json.dumps(message)
        for client in CLIENTS_CONNECTED:
            await client.send(json_message)
    for room in rooms:
        if message['room_id'] == room['id']:
            json_message = json.dumps(message)
            for member in room['member_list']:
              await member.send(json_message)  
    

def create_room(websocket,path):
    new_room_id = str(uuid.uuid1())
    new_room = {
         'id': new_room_id,
        'member_list': [{websocket}]
    }
    dict_copy = new_room.copy()
    rooms.append(dict_copy)

def remove_room():
        pass

def remove_member_from_room():
        pass

async def save_to_Database():
    pass

def handle_incoming_messages(message):
    # messageObj = json.loads(message)
    utc_time = datetime.utcnow()
    central_time = (utc_time + timedelta(hours=-5))
    formatnow = central_time.strftime("%A,%d %b, %y %I:%M:%S %p")
    # MESSAGE_DICT['message'] = messageObj['message']
    MESSAGE_DICT['message'] = message
    MESSAGE_DICT['id'] = str(uuid.uuid1())
    MESSAGE_DICT['time_stamp'] = str(formatnow)
    MESSAGE_DICT['sender'] = 'David'
    return MESSAGE_DICT


def start_server():
    print('[Server Started]')
    start_server = websockets.serve(handle_connection, SERVER_ADDRESS, SERVER_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    


if __name__ == "__main__":
    start_server()
    