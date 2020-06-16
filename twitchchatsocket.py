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
from wledconnector import WledConnector

class TwitchChatSocket:
    def __init__(self, server, port, nickname, token, channel):
        super().__init__()
        self.server = server
        self.port = port
        self.nickname = nickname
        self.token = token
        self.channel = channel
        self.gen = DocumentGenerator()
        self.useArtNet = 0

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))

    def listen(self):
        #self.timer()

        while True:
            resp = self.sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            
            elif len(resp) > 0:
                message = resp.split(':').pop()
                user = resp.split(':').pop(1).split('!').pop(0)
                print(f"{user} : {message}")
                #self.repeatUser("jeanmichellecanard", message)
                #if not self.nickname in user:
                #self.sendMessage(self.gen.sentence())
                watch_word = "CurseLit" 
                if watch_word in message:
                    print(f"{watch_word} detected!")
                    if self.useWled:
                        print(f"sequence 'fire' sent to led!")
                        self.wledconnect.fire(3)

    def useWled(self, ip,):
        self.useWled = 1
        self.wledconnect = WledConnector(ip)

    def bot(self, message, interval):
        threading.Timer(interval, self.bot_timer).start()

    def bot_timer(self):
        print("bot_timer")
        print(time.ctime())
        self.sendMessage("CurseLit")

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

    def timer(self):
        message = "TwitchUnity"
        stopFlag = Event()
        thread = MyThread(stopFlag, self.sock,  self.server, self.port, self.nickname, self.timer, self.channel, message)
        thread.start()              

class MyThread(Thread):
    def __init__(self, event, sock, server, port, nickname, token, channel, message):
        Thread.__init__(self)
        self.stopped = event
        self.sock = sock
        self.server = server
        self.port = port
        self.nickname = nickname
        self.token = token
        self.channel = channel
        self.message = message
        self.gen = DocumentGenerator()


    def run(self):
        while not self.stopped.wait(60):
            self.message = self.gen.sentence()
            self.sock.send(f"PRIVMSG {self.channel} :{self.message}\r\n".encode('utf-8'))