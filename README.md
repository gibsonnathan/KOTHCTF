# KOTHCTF
Currently in developmental state.

The idea is a King of the Hill capture the flag scoring engine. 

#Mechanics
Admin:
An administrator sets up vulnerable machines by running the client program and designating where the flag file is located on the machine. 
The client program periodically sends the flag contained in the flag file to the server. Scores can be viewed on / route of the web server.


Player:
As a player your goal is to put your team name in the flag file on vulnerable machines. The more often your team name is in the flag file, 
the more the server will increase your score.

#How to use
1.) install dependencies
2.) python app.py
3.) put client.py on each scored machine and run python client.py
4.) /scoreboard displays the each flag that has been placed on the server along with how many times that flag was scored.

#TODO
add functionality for scoring services
