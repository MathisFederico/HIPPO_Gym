import asyncio
import logging
import ssl
import websockets
import json

from hippo_gym.event.event_handler import EventHandler


class Communicator:

    def __init__(self, out_q, queues, address=None, port=5000, use_ssl=True, force_ssl=False, fullchain_path='SSL/fullchain.pem',
                 privkey_path='SSL/privkey.pem'):
        self.out_q = out_q
        self.address = address
        self.port = port
        self.ssl = use_ssl
        self.force_ssl = force_ssl
        self.fullchain = fullchain_path
        self.privkey = privkey_path
        self.event_handler = EventHandler(queues)
        self.users = set()
        self.start()

    async def consumer_handler(self, websocket):
        async for message in websocket:
            try:
                message = json.loads(message)
                self.event_handler.parse(message)

            except Exception as e:
                print(e)

    async def producer_handler(self, websocket):
        done = False
        while not done:
            message = await self.producer()
            if message:
                if message == 'done':
                    done = True
                await websocket.send(json.dumps(message))
            await asyncio.sleep(0.01)
        return

    async def producer(self):
        message = None
        if not self.out_q.empty():
            message = self.out_q.get()
            message = json.dumps(message)
        return message

    async def handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
        producer_task = asyncio.ensure_future(self.producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()
        await websocket.close()
        return

    def start(self):
        if not self.force_ssl:
            self.start_non_ssl_server()
        if self.ssl or self.force_ssl:
            self.start_ssl_server()

    def start_non_ssl_server(self):
        server = websockets.serve(self.handler, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
        logging.info('Non-SSL websocket started')
        print('NON SSL UP')

    def start_ssl_server(self):
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(self.fullchain, keyfile=self.privkey)
            ssl_server = websockets.serve(self.handler, None, self.port, ssl=ssl_context)
            asyncio.get_event_loop().run_until_complete(ssl_server)
            asyncio.get_event_loop().run_forever()
            logging.info('SSL websocket started')
            print('SSL UP')
        except Exception as e:
            logging.info('SSL failed to initialize')
            logging.error(f'SSL failed with error: {e}')
            print(f'SSL Failed: {e}')

async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
    producer_task = asyncio.ensure_future(self.producer_handler(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()
    await websocket.close()
    return