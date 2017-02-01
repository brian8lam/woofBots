#utils.py
#A bunch of utility functions

import cfg
import urllib2
import json
import time, thread
from time import sleep

followers = {}
commands = {}

#Function: Chat
#Send a chat message to the server.
#   Parameters:
#       sock -- the socket over which to end the message
#       msg -- the message to send
def chat(sock, msg):
    str = "PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg)
    sock.send(str)

#Function: ban
#Ban a user from the channel
#   Parameters:
#       sock -- the socket over which to send the ban command
#       usr -- the user to be banned
def ban(sock, usr):
    chat(sock, ".ban {}".format(usr))

#Function: timeout
#Timeout a user for a set period of time
#   Parameters:
#       sock -- the socket over which to send the timeout command
#       usr -- the user to be timed out
#       seconds -- the length of the timeout in seconds (default: 600secs)
def timeout(sock, usr, seconds=600):
    chat(sock, ".timeout {}".format(usr, seconds))

#Function: follow
#Checks if the user is following
#   Parameters:
#       usr -- the user that is being checked to see if they are following CHAN
def follow(usr):
    #communicates with twitch api to see if the user is following the specified channel

    try:
        twitchAPI = urllib2.urlopen("http://api.twitch.tv/kraken/users/"+usr+"/follows/channels/"+cfg.CHAN)
        fJson = json.loads(twitchAPI.read())
        if "error" in fJson:
            return False
        else:
            return True
    except:
        return False

#Function: createCommands
#Create temperary commands that you can add to your stream for the hell of it
#   Parameters:
#       c -- what command that we are going to store
#       p -- what is going to be said when command is used
def createCommands(c, p):
    if c in commands:
        return "It already exists."
    try:
        commands[c] = p
    except:
        return "Something broke :("
    return "It already exists"

#Function: useCommands
#Uses the commands that are made in the list and returns the phrase stored
#   Parameters:
#       sock -- socket that is going to be displayed to
#       c -- the command that was being used
def useCommands(sock, c):
    try:
        if c in commands:
            return commands[c]
    except:
        return "Command doesn't exist"
    return "Command doesn't exist"


#Function: threadFillOpList
#In a seperate thread, fill up the op list
def threatFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/dkhusky8/chatters"
            req = urllib2.Request(url, headers={"accept": "*/*"})
            response = urllib2.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                cfg.oplist.clear()
            data = json.loads(response)
            for i in data["chatters"]["moderators"]:
                cfg.oplist[i] = "mod"
            for i in data["chatters"]["global_mods"]:
                cfg.oplist[i] = "global_mod"
            for i in data["chatters"]["admins"]:
                cfg.oplist[i] = "admin"
            for i in data["chatters"]["staff"]:
                cfg.oplist[i] = "staff"
        except:
            'do nothing'
        sleep(5)

#Function: isOp
#Checks if user is in the oplist if is returns true else false
def isOp(usr):
    return usr in cfg.oplist