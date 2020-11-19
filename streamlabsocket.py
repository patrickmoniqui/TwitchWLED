import ssl
import websocket
import threading
import time, threading
from threading import Thread as Thread
from threading import Event
from wledconnector import WledConnector as wled
import json

try:
    import thread
except ImportError:
    import _thread as thread
import time

class StreamlabSocket:
    def __init__(self, socketToken):
        super().__init__()
        self.socketToken = socketToken
        self.server = f"wss://sockets.streamlabs.com/socket.io/?token={socketToken}&EIO=3&transport=websocket"

        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        self.ws.connect(self.server)
        self.wledEnabled = False

    def listen(self):
        thread = threading.Thread(target = self.run, args = ())
        thread.start()
        t = threading.Thread(target = self.ping_interval, args = ())
        t.start()

        return thread

    def ping_interval(self):
        starttime = time.time()
        pi = 25
        while True:
            self.ws.send("2")
            time.sleep(pi - ((time.time() - starttime) % pi))

    def run(self):
        while True:
            resp = self.ws.recv()

            if resp.startswith("42"):
                try:
                    jsonResponse = json.loads(resp[2:])
                    type = jsonResponse[1]['type']
                    print(type)

                    if type == 'donation':
                        print('donation')

                        if self.wledEnabled:
                            self.led.blink(0, 255, 0, 10) #green

                    if type == 'follow':
                        print('follow')

                        if self.wledEnabled:
                            self.led.blink(0, 0, 255) #blue

                    if type == 'subscription':
                        print('subscription')

                        if self.wledEnabled:
                            self.led.blink(255, 0, 0, 10) #red

                    if type == 'raid':
                        print('raid')

                        if self.wledEnabled:
                            self.led.blink(255, 255, 0, 20) #yellow

                    if type == 'host':
                        print('host')

                        if self.wledEnabled:
                            self.led.blink(255, 255, 0, 10) #yellow

                    if type == 'bits':
                        print('bits')

                        if self.wledEnabled:
                            self.led.blink(127, 0, 127) #purple

                    if type == 'loyalty_store_redemption':
                        print('loyalty_store_redemption')

                        if self.wledEnabled:
                            self.wled.changeColor(255, 0, 0)

                except:
                    print("exception")
                    # default led sequence
                    if self.wledEnabled:
                        self.led.blink(0, 0, 255, 10) #blue

    def useWled(self, wled):
        self.wledEnabled = True
        self.led = wled