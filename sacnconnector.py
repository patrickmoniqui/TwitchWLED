import sacn
import time

class SacnConnector:
    def __init__(self):
        print("")


    def flash(self, adresse=None, adresses=None):
        sender = sacn.sACNsender()  # provide an IP-Address to bind to if you are using Windows and want to use multicast
        sender.start()  # start the sending thread
        sender.activate_output(1)  # start sending out data in the 1st universe
        sender[1].multicast = True  # set multicast to True
        #sender[1].destination = "192.168.0.145"  # or provide unicast information.
        # Keep in mind that if multicast is on, unicast is not used

        print("sending dmx")

        dmx512 = [0] * 512

        if adresses is not None:
            for adr in adresses:
                if adr-1 > 0 and adr-1 <= 512:
                    dmx512[adr-1] = 255

        if adresse is not None:
            if adresse-1 > 0 and adresse-1 <= 512:
                dmx512[adresse-1] = 255

        for x in range(0, 5):
            sender[1].dmx_data = tuple(dmx512)
            time.sleep(1)
            sender[1].dmx_data = (0, 0) # some test DMX data
            time.sleep(1)

        sender.stop()  # do not forget to stop the sender

        print("finish")

dmx = SacnConnector()
dmx.flash(adresses=[201, 202, 203, 204, 205, 206])