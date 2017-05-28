import atexit
import socket
import time

DEBUGGING = False
TIME_INTERVAL = 5

def exit_handler(sock):
    if DEBUGGING:
        print 'sending quit to the client'
    sock.send('quit')

SERVERIP = '127.0.0.1'
PORT = 9999

flag_location = raw_input('Enter location of flag file (abolute path):')

sock = socket.socket()
sock.connect((SERVERIP, PORT))
atexit.register(exit_handler, sock)

name = raw_input('Enter the name of this machine:')
sock.send(name)
if DEBUGGING:
    print 'sending name ' + name

while(True):
    f = open(flag_location, 'r')
    flag = f.read().strip()
    sock.send(name + '-' + flag)
    if DEBUGGING:
        print 'sending flag ' + flag
    time.sleep(TIME_INTERVAL)
    

