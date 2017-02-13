#utils.py
#A bunch of utility functions

import cfg
import urllib2
import json
import time, thread
from time import sleep

eliminateList = {}

#Function: chat
#Send a chat message to the server.
#   Parameters:
#       sock -- the socket over which to send the message
#       msg -- the message to send
def chat(sock, msg):
    str = "PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg)
    sock.send(str)

#Function: whisper
#Send a whisper to the person
#   Parameters:
#       sock -- the socket over which to send the message
#       msg -- the message to send
#       usr -- to the user
def whisper(sock, msg, usr):
    str = "PRIVMSG #{} :/w:{} :{}\r\n ".format(cfg.CHAN, msg, usr)
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
        url = "http://api.twitch.tv/kraken/users/"+usr+"/follows/channels/"+cfg.CHAN
        twitchAPI = urllib2.urlopen(url)
        fJson = json.loads(twitchAPI.read())
        if "error" in fJson:
            return False
        else:
            return True
    except:
        return False

#Function: eliminate
#User inputs which user will be eliminated
#   Parameters:
#       sock -- the socket over which to send the message that it was accepted
#       name -- the name of the person they chose
#       user -- the user who inputed the message
def eliminate(sock, name, user):
    try:
            eliminateList[user] = name.lower();
            chat(sock, user + " thinks " + name + " is going home tonight!!!")
    except:
        "something broke!"

#Fucntion: eliminated
#Mod inputs which user won the elimination
#   Parameters:
#       sock -- the socket which to send the message of who won through the array
#       winner -- the winner who won the event
def eliminated(sock, winner):
    try:
        n = "Congrats to these people who guessed " + winner + " would be eliminated: "
        print eliminateList
        for (name, item) in eliminateList.iteritems():
            print item
            if unicode(item) == unicode(winner.lower()):
                n = n + name + " "
        chat(sock, n);
        print n
    except:
        "something broke!"

#Function: showGame
#Shows what game the current user is playing
#   Parameters:z
#       sock -- the socket over which to send the game
def showGame(sock):
    try:
        url = "http://api.twitch.tv/kraken/channel/" + cfg.CHAN
        twitchAPI = urllib2.urlopen(url)
        fJson = json.load(twitchAPI.read())
        for i in fJson["game"]:
            chat(sock, i)
    except:
        'Shit Broke!'

#Function: createCommands
#Create temperary commands that you can add to your stream for the hell of it
#   Parameters:
#       c -- what command that we are going to store
#       p -- what is going to be said when command is used
def createCommands(c, p):
    if unicode(c) in cfg.commands:
        print cfg.commands
    try:
        cfg.commands[c] = p
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
        if unicode(c) in cfg.commands:
            chat(sock, unicode(cfg.commands[c]))
    except:
        chat(sock, "Broke!")

#Function: removeCommands
#Removes a command from the commands list
#   Parameters:
#       c -- the command that will be removed from the list
def removeCommands(c):
    try:
        if unicode(c) in cfg.commands:
            del(cfg.commands[c])
    except:
        return False

#Function: valentines
#For Valentines day event, users can give Valentines to people
#   Parameters:
#       sock -- the socket to send the response
#       name -- the user gave the Valentine to
#       username --
def valentines(sock, name, username):
    if not(username in cfg.valentine):
        cfg.valentine[username] = 2
    if name[:1] == "@":
        name == name.split('@')[0]
    if not(name in cfg.valentine):
        cfg.valentine[name] = 2
    cfg.valentine[name] = cfg.valentine[name] + 1
    chat(sock, "%s gave a Valentine to $s <3" %(username, name))

#Function: total
#Returns the total of the array
#   Parameters:
#       sock -- the socket to send the response
#       list -- the list that you want to print out
def total(sock, list):
    for (index, value) in list:
        chat(sock, "%s : %d" %(index, value))

#Function: constantGreeting
#Prints out the command continuously after a certain amount of time
def constantGreeting(sock):
        try:
            chat(sock, "Masc4Masc Mondays: Solo Stream with Jason! 7:30P/8PM EST until 11P/12AM")
            chat(sock, "Tabby Tuesdays: Solo Stream with Trent! 7:30P/8PM EST until 11P/12AM")
            chat(sock, "Thirsty Thursdays: Solo Stream with Matt! 10PM EST until 12AM")
            chat(sock, "Festive Friday: Join the entire crew for party games! 7:30PM EST (ish) until we go to the bar (12A/1A)")
            chat(sock, "Shady Saturday: Come talk shit and spill the T! 2PM EST until 8PM EST. WOOF!")
        except:
            'nothing'


#Function: threadFillOpList
#In a seperate thread, fill up the op list
def threatFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/"+ cfg.CHAN +"/chatters"
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