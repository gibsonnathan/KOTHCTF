#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, jsonify, flash, redirect, url_for
import os
import SocketServer
import threading
from socket import *
import sys
import json
from flask_cors import CORS, cross_origin

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#
'''
    represents a connected client
'''
class Machine():
    
    def __init__(self, name, socket):
        self.name = name
        self.flags = {}
        self.socket = socket
        self.alive = True
        
    def add_flag(self, flag):
        if flag in self.flags:
            self.flags[flag] += 1
        else:
            self.flags[flag] = 1
            
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
DEBUGGING = False

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

'''
    listens for a client to connect and starts a thread to handle subsequent client
    interactions 
'''
def listenForClient():
     while 1:
        clientsock, addr = serversock.accept()
        name = clientsock.recv(1024)
        if DEBUGGING:
            print 'connection received from ' + name
        m = Machine(name, clientsock)
        clients.append(m)
        t = threading.Thread(target=listenToClient, args=(m,))
        t.deamon = True
        t.start()
    
'''
    handles communication between the server and a client, listens for updates from 
    the client which consist of a machine-flag message or a disconnect message
'''
def listenToClient(m):
    listening = True
    while listening:
        data = m.socket.recv(1024)
        if DEBUGGING:
            print 'client sent ' + data
        if 'quit' in data:
            close = 1
            m.alive = False
            m.socket.close()
            listening = False            
        else:
            name = data.split('-')[0]
            flag = data.split('-')[1]
            m.add_flag(flag)
        
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
'''
    shows all of the currently connected clients
'''
@app.route('/')
def home():
    return render_template('clients.html', data = clients)

'''
    shows the current scores on all clients
'''
@app.route('/scoreboard')
def scoreboard():
    l = []
    print clients
    for client in clients:
        l.append({'name' : client.name, 'flags' : client.flags})
        
    response = app.response_class(
        response=json.dumps(l),
        status=200,
        mimetype='application/json'
    )
    return response

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    t = threading.Thread(target=listenForClient, args=())
    t.daemon = True
    t.start()
    app.run(use_reloader=False)

