import socket as socket
import logging
from emoji import demojize
import re
import time, threading
from threading import Thread as Thread
from threading import Event
from essential_generators import DocumentGenerator
import threading
import time
import logging
from random import randrange
from wledconnector import WledConnector as wled
from chat import Chat as chat
from datetime import datetime
from ui import ui as ui
import tkinter as tk
import tkinter.scrolledtext as tkst
import random
import json

class TwitchChatSocket:
    def __init__(self, server, port, nickname, token, channel):
        super().__init__()
        self.server = server
        self.port = port
        self.nickname = nickname
        self.token = token
        self.channel = channel
        self.gen = DocumentGenerator()
        self.useArtNet = False
        self.wledEnabled = False
        self.connected = False

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN #{self.channel}\n".encode('utf-8'))
        self.connected = True
        return True
    
    def disconect(self):
        self.receiceThread.stop()
        self.sock.close()
        self.lblConnected.config(text='Disconnected', fg="red")
        self.btnConnectText.set("Disconnect")
        self.connected = False

    def listen(self):
        self.connect()

        if self.wledEnabled:
            self.receiceThread = Receive(self.sock, self.wled)
        else:
            self.receiceThread = Receive(self.sock)

        # bot
        #self.timer("CurseLit", 1)

        self.receiceThread.start()

        return self.receiceThread

    def getSocket(self):
        return self.sock

    def useUI(self):
        self.ui = UI(self)
        self.useUI = True

    def useWled(self, wled):
        self.wled = wled
        self.wledEnabled = True

    def useBot(self):
        self.timer()

    def repeat(self, message):
        self.sendMessage(message)

    def repeatUser(self, user, message):
        if user in self.nickname:
            self.sendMessage(message)

    def message(self, msg):
        print(msg)
        self.sendMessage(msg)

        filter_msg = "CurseLit"
        ocurrence = msg.count(filter_msg)
        if ocurrence > 0:
            print(f">>> {ocurrence} {filter_msg} detected!")
        
    def sendMessage(self, message):
        self.sock.send(f"PRIVMSG {self.channel} :{message}\r\n".encode('utf-8'))

    def timer(self, message, delay, randomLength=False):
        stopFlag = Event()
        thread = BotThread(stopFlag, self.sock,  self.server, self.port, self.nickname, self.channel, message, delay, randomLength)
        thread.start()
        return thread

    def spamBot(self):
        if self.btnSpam.cget('text') == 'Stop spamming':
            self.spammingThread.stopped.set()
            self.btnSpam.config(text='Start spamming')
        else:
            #msg = chat.maximumEmote(self.entrySpam.get())
            msg = self.entrySpam.get()

            self.spammingThread = self.timer(msg, float(self.entrySpamDuration.get()))
            self.btnSpam.config(text='Stop spamming')
        

class BotThread(Thread):
    def __init__(self, event, sock, server, port, nickname, channel, message, delay=1, randomLength=False):
        Thread.__init__(self)
        self.stopped = event
        self.sock = sock
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.message = message
        self.delay = delay
        self.randomLength = randomLength
        self.gen = DocumentGenerator()

    def run(self):
        str = self.message
        while not self.stopped.wait(self.delay):
            print(f"MESSAGE: {self.message}")
            self.message = chat.messageNtime(str, random.randint(1, 20))
            result = self.sock.send(f"PRIVMSG #{self.channel} :{self.message}\r\n".encode('utf-8'))

            print(f"{result}. timer runned at: {datetime.now()}")


class Receive(Thread):
    def __init__(self, sock, wled=None, ui=None):
        Thread.__init__(self)
        self.sock = sock
        self.rgb_colors = []

        if wled is not None:
            self.useWled = True
        else:
            self.useWled = False

        self.wled = wled
        self.ui = ui
        self.loadColors()

    def useUI(self, ui):
        self.ui = ui

    def manageChangeColor(self, message, user):

        allowedUsers = ''
        if not message[0] == '!':
            return

        msg = message[1:len(message)].replace('\r\n', '').lower()

        if allowedUsers in user:
            for color in self.rgb_colors:
                if(msg in color['name'].lower()):
                    print(f"changeColor")
                    self.wled.changeColor(color['rgb']['r'], color['rgb']['g'], color['rgb']['b'])
                    return

        if "!color" in message and allowedUsers in user:
            command = message.split()

            if len(command) == 4:
                self.wled.changeColor(int(command[1]), int(command[2]), int(command[3]))

        if "!effect" in message and allowedUsers in user:
            command = message.split()

            if len(command) == 2:
                effect = command[1]
                self.wled.changeEffect(effect)

        if "!speed" in message and allowedUsers in user:
            command = message.split()

            if len(command) == 2:
                speed = command[1]
                self.wled.changeSpeed(speed)

        if "!intensity" in message and allowedUsers in user:
            command = message.split()

            if len(command) == 2:
                intensity = command[1]
                self.wled.changeIntensity(intensity)

        if "!reset" in message and allowedUsers in user:
            command = message.split()
            self.wled.reset()


        if "!strobe" in message:
            print(f"changeColor")
            self.wled.sendSequence(128, 79, 255, 255, 0, 0, 255, 3, 1)

    def loadColors(self):
        with open('json/moneykey_colors.json') as f:
            self.rgb_colors = json.load(f)

    def run(self):
        while True:
            resp = self.sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            
            elif len(resp) > 0:
                message = resp.split(':').pop()
                user = resp.split(':').pop(1).split('!').pop(0)

                print(f"{user} : {message}")

                if self.ui is not None:
                    ui.receveiceMessage(user, message)

                if "CurseLit" in message:
                    print(f"CurseLit detected!")
                    if self.useWled:
                        print(f"sequence 'fire' sent to led!")
                        self.wled.fireOrange(3)
                if "TwitchLit" in message:
                    print(f"TwitchLit detected!")
                    if self.useWled:
                        print(f"sequence 'fire' sent to led!")
                        self.wled.fireMauve(3)

                if "djmone" in message:
                    print(f"djmone emotes detected!")
                    if self.useWled:
                        self.wled.sendSequence(128, 79, 255, 255, 0, 0, 255, 3, 1)

                # change color in chat
                self.manageChangeColor(message, user)