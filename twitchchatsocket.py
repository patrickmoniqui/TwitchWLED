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
from chat import Chat as chat
from datetime import datetime
from ui import ui as ui
import tkinter as tk
import tkinter.scrolledtext as tkst

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
        self.useWled = False
        self.buildUi()

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN #{self.channel}\n".encode('utf-8'))
        return True

    def listen(self):
        thread = Receive(self.sock, self.chatMessages)
        thread.start()

    def useWled(self, ip):
        self.useWled = True
        self.wledconnect = WledConnector(ip)

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

    def timer(self, message):
        stopFlag = Event()
        thread = BotThread(stopFlag, self.sock,  self.server, self.port, self.nickname, self.channel, message)
        thread.start()
        return thread

    def btnConnectClick(self):
        if self.connect():
            self.btnConnectText.set("Disconnect")
            self.listen()
            self.lblConnected.config(text='Connected', fg="green")
            print("connected")

    def spamBot(self):
        if self.btnSpam.cget('text') == 'Stop spamming':
            self.spammingThread.stopped.set()
            self.btnSpam.config(text='Start spamming')
        else:
            self.spammingThread = self.timer(chat.maximumEmote(self.entrySpam.get()))
            self.btnSpam.config(text='Stop spamming')
        
    def buildUi(self):
        window = tk.Tk()
        label = tk.Label(text="Twitch username")
        entry = tk.Entry()
        entry.insert(0, self.channel)
        self.lblConnected = tk.Label(text="Disconnected", fg="red")
        self.btnConnectText = tk.StringVar()
        self.btnConnectText.set("Connect")
        btnConnect = tk.Button(textvariable=self.btnConnectText, command=self.btnConnectClick)
        cbLed = tk.Checkbutton(text="WLED integration")
        self.chatMessages = tkst.ScrolledText(
            wrap   = tk.WORD,
        )

        self.btnSpam = tk.Button(text="Spam", command=self.spamBot)
        self.entrySpam = tk.Entry()

        label.pack()
        entry.pack()
        self.lblConnected.pack()
        cbLed.pack()
        btnConnect.pack()
        
        self.entrySpam.pack()
        self.btnSpam.pack()

        self.chatMessages.pack()

        window.mainloop()

class BotThread(Thread):
    def __init__(self, event, sock, server, port, nickname, channel, message):
        Thread.__init__(self)
        self.stopped = event
        self.sock = sock
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.message = message
        self.gen = DocumentGenerator()

    def run(self):
       while not self.stopped.wait(1):
            result = self.sock.send(f"PRIVMSG #{self.channel} :{self.message}\r\n".encode('utf-8'))
            print(f"{result}. timer runned at: {datetime.now()}")


class Receive(Thread):
    def __init__(self,sock, chatMessages):
        Thread.__init__(self)
        self.sock = sock
        self.chatMessages = chatMessages
        
    def run(self):
        while True:
            resp = self.sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            
            elif len(resp) > 0:
                message = resp.split(':').pop()
                user = resp.split(':').pop(1).split('!').pop(0)
                print(f"{user} : {message}")
                self.chatMessages.insert(tk.INSERT, f"{user} : {message}")

                # if "CurseLit" in message:
                #     print(f"CurseLit detected!")
                #     if self.useWled:
                #         print(f"sequence 'fire' sent to led!")
                #         self.wledconnect.fireOrange(3)
                # if "TwitchLit" in message:
                #     print(f"TwitchLit detected!")
                #     if self.useWled:
                #         print(f"sequence 'fire' sent to led!")
                #         self.wledconnect.fireMauve(3)