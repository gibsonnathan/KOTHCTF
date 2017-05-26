#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, jsonify, flash, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
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
        
    def add_flag(flag):
        if flag in flag_count:
            flag_count[flag] += 1
        else:
            flag_count[flag] = 1
            
    def flag_count(flag):
        if flag in flags:
            return flags[flag]
        else:
            return 0

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
        #build machine object
        clients.append(clientsock)
        t = threading.Thread(target=listenToClient, args=(clientsock, addr))
        t.deamon = True
        t.start()
        
'''
    protocol that the clients send:
    machine-flag
'''
def listenToClient(client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    machine = data.split('-')[0]
                    flag = data.split('-')[1]
                    print machine 
                    print flag
                else:
                    raise error('Client disconnected')
            except:
                clients.remove(client)
                client.close()
                return False

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('clients.html', data = clients)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        flag = request.form['flag']
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    t = threading.Thread(target=listenForClient, args=())
    t.daemon = True
    t.start()
    app.run(use_reloader=False)

