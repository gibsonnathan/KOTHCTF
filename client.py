import socket
import time

SERVERIP = '127.0.0.1'
PORT = 9999

flag_location = raw_input('Enter location of flag file (abolute path):')

sock = socket.socket()
sock.connect((SERVERIP, PORT))

name = raw_input('Enter the name of this machine:')
sock.send(name)
print 'sending name ' + name

while(True):
    f = open(flag_location, 'r')
    flag = f.read().strip()
    sock.send(name + '-' + flag)
    print 'sending flag ' + flag
    time.sleep(5)
    

