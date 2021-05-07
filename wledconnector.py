import requests
import time
import threading
import asyncio

class WledConnector:
    instance = None
    priority = 0
    currentPriority = 0
    effects = []

    def setup(self, ips):
        self.ips = ips
        self.state = [object] * len(ips)
        self.storeCurrentState()
        self.cpt = 0
        self.effects = self.getListEffects()

    @staticmethod 
    def getInstance():
        if WledConnector.instance == None:
            WledConnector()

        return WledConnector.instance

    def __init__(self):
      """ Virtually private constructor. """
      if WledConnector.instance != None:
         raise Exception("This class is a singleton!")
      else:
         WledConnector.instance = self
    
    def sendSequence(self, A=None, FX=None, SX=None, IX=None, R=None, G=None, B=None, duration=5, priority=0):
        if self.priority >= self.currentPriority:
            self.currentPriority = self.priority
            self.cpt += 1

            if self.cpt == 1:
                self.storeCurrentState()

            params = "win"

            if A is not None:
                params+= f"&A={A}"

            if FX is not None:
                params+= f"&FX={FX}"

            if SX is not None:
                params+= f"&SX={SX}"

            if IX is not None:
                params+= f"&IX={IX}"

            if R is not None:
                params+= f"&R={R}"

            if G is not None:
                params+= f"&G={G}"

            if B is not None:
                params+= f"&B={B}"


            self.activate = True

            for i in range(0, len(self.ips)):
                response = requests.get(f"{self.ips[i]}/{params}")

            time.sleep(duration)

            self.activate = False

            if self.cpt == 1:
                self.restoreCurrentState()

            self.cpt -= 1

            self.currentPriority = 0
            self.priority = 0

    def sendSequence2(self, A=None, FX=None, SX=None, IX=None, R=None, G=None, B=None, priority=0, duration=-1):
        if self.priority >= self.currentPriority:
            self.currentPriority = self.priority
            self.cpt += 1

            params = "win"

            if A is not None:
                params+= f"&A={A}"

            if FX is not None:
                params+= f"&FX={FX}"

            if SX is not None:
                params+= f"&SX={SX}"

            if IX is not None:
                params+= f"&IX={IX}"

            if R is not None:
                params+= f"&R={R}"

            if G is not None:
                params+= f"&G={G}"

            if B is not None:
                params+= f"&B={B}"


            self.activate = True

            for i in range(0, len(self.ips)):
                response = requests.get(f"{self.ips[i]}/{params}")

            self.activate = False

            self.cpt -= 1

            self.currentPriority = 0
            self.priority = 0

    def blink(self, R, G, B, duration=5):
        self.priority = 2
        A = None
        FX = 1
        SX = 200
        IX = 127

        self.sendSequence(A, FX, SX, IX, R, G, B, duration, 1)
        print("blink sequence done")

    def fireOrange(self, duration):
        self.priority = 1
        A = None
        FX = 45
        SX = 255
        IX = 255
        R = 255
        G = 128
        B = 0

        self.sendSequence(A, FX, SX, IX, R, G, B, duration, 0)
        print("fireOrange sequence done")

    def fireMauve(self, duration):
        self.priority = 1
        A = None
        FX = 45
        SX = 255
        IX = 255
        R = 138
        G = 42
        B = 226

        self.sendSequence(A, FX, SX, IX, R, G, B, duration, 0)
        print("fireMauve sequence done")

    def changeEffect(self, FX):

        if FX.isdigit():
           self.sendSequence2(FX=FX, duration=-1)
        else: 
            if isinstance(FX, str):
                for idx, val in enumerate(self.effects):
                    if val.replace(" ", "").lower() == FX.lower():
                        self.sendSequence2(FX=idx, duration=-1)
                        break

    def changeSpeed(self, SX):
        if SX.isdigit():
            self.sendSequence2(SX=SX)

    def changeIntensity(self, IX):
        if IX.isdigit():
           self.sendSequence2(IX=IX)

    def reset(self):
        self.sendSequence2(A=255, SX=127, IX=127, FX=0)
    
    def changeColor(self, R, G, B):

        if (int(R) >= 0 and int(R) <= 255) and (int(G) >= 0 and int(G) <= 255) and (int(B) >= 0 and int(B) <= 255):
            params = f"win&R={R}&G={G}&B={B}"

            for i in range(0, len(self.ips)):
                response = requests.get(f"{self.ips[i]}/{params}")

            print("changeColor sequence done")

    def getListEffects(self):
        params = "json/effects"

        response = requests.get(f"{self.ips[0]}/{params}")
        return response.json()

    def storeCurrentState(self):
        params = "json/state"
        
        for i in range(0, len(self.ips)):
            response = requests.get(f"{self.ips[i]}/{params}")
            self.state[i] = response.json()

    def sendState(self, newState):
        params = "json/state"

        for i in range(0, len(self.ips)):
            response = requests.post(f"{self.ips[i]}/{params}", json=newState)

    def restoreCurrentState(self):
        print(f"restoring current state")
        
        params = "json/state"

        for i in range(0, len(self.ips)):
                requests.post(f"{self.ips[i]}/{params}", json=self.state[i])