#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, jsonify, flash, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os
import SimpleHTTPServer
import SocketServer
import threading
from socket import *
import sys
import json
from flask_cors import CORS, cross_origin

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#
class Machine():
    
    def __init__(self, name, socket):
        self.name = name
        self.flags = {}
        self.socket = socket
        
    def add_flag(self, flag):
        if flag in self.flags:
            flag_count[flag] += 1
        else:
            flags[flag] = 1
            
    def flag_count(self, flag):
        if flag in self.flags:
            return self.flags[flag]
        else:
            return 0
        
    def __str__(self):
        return self.name + ' ' + str(self.flags)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'secret!'
#db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Server
#----------------------------------------------------------------------------#
BUFF = 1024
HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)
serversock = socket(AF_INET, SOCK_STREAM)
serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversock.bind(ADDR)
serversock.listen(5)
clients = []

def listenForClient():
     while 1:
        clientsock, addr = serversock.accept()
        name = clientsock.recv(1024)
        print 'receiving name ' + name
        m = Machine(name, clientsock)
        clients.append(m)
        t = threading.Thread(target=listenToClient, args=(clientsock, addr))
        t.deamon = True
        t.start()
        
def listenToClient(client, addr):
        while True:
            try:
                data = client.recv(1024)
                print 'receiving flag ' + data
                if data:
                    name = data.split('-')[0]
                    flag = data.split('-')[1]
                    filter(lambda x : x.name == name, clients)[0].add_flag(flag)
                else:
                    raise error('Client disconnected')
            except:
                clients.remove(filter(lambda x: x.socket == client, clients)[0])
                client.close()
                return False

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('clients.html', data = clients)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    t = threading.Thread(target=listenForClient, args=())
    t.daemon = True
    t.start()
    app.run(use_reloader=False)

