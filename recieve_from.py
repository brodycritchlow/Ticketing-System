import asyncio
import websockets
import json

from ticket import GenericTicket

async def echo(websocket, path):
    async for message in websocket:
        needed_values = {'seat', 'event', 'purchase_price', 'purchase_date', 'owner'}
        gt_ = {}
        for k,v in json.loads(message).items():
            needed_values.remove(k)
            gt_[k] = v
        for k in needed_values:
            gt_[k] = None
        print(GenericTicket(**gt_))

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()