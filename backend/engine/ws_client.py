"""This module will act as the client owned by the gameloop to communicate
with the server.  The organization looks like of like this:
    
    game_loop has a ws_client
    ws_server is running
    
    game_loop client (this module) connects to ws_server
    players connect to ws_server
    
    game_loop sends messages to players by
    using this client to talk to the server,
    and then the server relays those on to the
    clients.  This is pretty much how NodeJS does it too."""

import asyncio
from multiprocessing import Process
from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory

# the event loop on which this client will run; this is a threading thing
# i.e., the spawned thread runs the methods in this loop forever
# we can make the thread do stuff by adding them to the loop, which is sort of
# like a "to do" queue
client_loop = None

def start_client_process(address="127.0.0.1", port=9000):
    # address and port are those of the server

    # start the client running in a new process
    p = Process(target=start_client, args=(address, port))
    p.start()
    print("client was started.")

def start_client(address, port):
    # see http://autobahn.ws/python/websocket/programming.html

    # because starting a client requires an integer port,
    # while starting a server requires a string port, accept both.
    if isinstance(port, str):
        port = int(port)

    composite_address = 'ws://' + address + ':' + str(port)
    print('client composite address of {}'.format(composite_address))
    factory = WebSocketClientFactory(composite_address)
    factory.protocol = MyClientProtocol

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    global client_loop
    client_loop = loop

    print("client creating connection to address {} and port {}".format(address, str(port)))
    coro = loop.create_connection(factory, address, port)
    loop.run_until_complete(coro)
    loop.run_forever()


class MyClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        print("client opened connection")

    def onMessage(self, payload, isBinary):
        pass
