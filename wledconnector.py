import requests
import time


class WledConnector:
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.mode = 0
        self.storeCurrentState()

    def setupArtNet(self, universe, first_channel, number_of_channel):
        self.artnet_universe = universe
        self.artnet_first_channel = first_channel
        self.artnet_number_of_channel = number_of_channel
        #self.artnet_node = ArtNetNode(self.ip)
        # self.node.start()
        #self.universe = node.add_universe(0)
        # self.channel  = universe.add_channel(129,3
        self.mode = 1

    def setupApi(self):
        self.mode = 0

    def fireOrange(self, duration):
        print(f"send 'fire' via {self.getMode()}")
        if self.mode == 0:
            self.storeCurrentState()
            params = "win&FX=45&SX=255&IX=255&R=255&G=128&B=0"
            response = requests.get(f"{self.ip}/{params}")
            time.sleep(5)
            self.restoreCurrentState()

        if self.mode == 1:
            self.channel.add_fade([255, 0, 0], 5000)

    def fireMauve(self, duration):
        print(f"send 'fire' via {self.getMode()}")
        if self.mode == 0:
            self.storeCurrentState()
            params = "win&FX=45&SX=255&IX=255&R=138&G=43&B=226"
            response = requests.get(f"{self.ip}/{params}")
            time.sleep(5)
            self.restoreCurrentState()

        if self.mode == 1:
            self.channel.add_fade([255, 0, 0], 5000)

    def getMode(self):
        if self.mode == 0:
            return "Wled API"
        if self.mode == 1:
            return "ArtNet"

    def storeCurrentState(self):
        params = "json/state"
        response = requests.get(f"{self.ip}/{params}")
        self.state = response.json()

    def sendState(self, newState):
        params = "json/state"
        response = requests.post(f"{self.ip}/{params}", json=newState)

    def restoreCurrentState(self):
        print(f"restoring current state")
        if self.mode == 0:
            params = "json/state"
            response = requests.post(f"{self.ip}/{params}", json=self.state)

        if self.mode == 1:
            self.channel.add_fade([255, 0, 0], 5000)
