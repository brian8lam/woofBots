#bot.py
#The code for the bot

import cfg
import utils
import socket
import re
import time
import thread
import os
import threading
from datetime import datetime, timedelta
from time import sleep


start = datetime.now()

def main():
   #print("hello")
   #Networking things
   s = socket.socket()
   s.connect((cfg.HOST, cfg.PORT))
   s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
   s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
   s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

   CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
   utils.chat(s, "Hi everyone!")

   thread.start_new_thread(utils.threatFillOpList, ())
   #thread.start_new_thread(utils.constantGreeting(s), ()) #look into multiprocessing / multithreading (threding library?)

   timeCount = 0
   while True:
       try:
        response = s.recv(1024)
       #if the connection to tmi.twitch.tv connects will get a pong
        if not response: break
        r = response.decode("utf-8")
        if r == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twtich.tv\r\n".encode("utf-8"))
        else:
           username = re.search(r"\w+", r).group(0)
           message = CHAT_MSG.sub("", r)
           print(r)
           timeCount += 1

           # Multithreading for all the greeting
           # Hope this works and doesn't break
           #t = threading.Thread(target=utils.constantGreeting(s))
           #t.daemon = True
           #t.start()

           # Custom Commands

           #Not a real timer sadly, This will increment each time a command is issued.
           if timeCount == 500:
               utils.chat(s, "Masc4Masc Mondays: Solo Stream with Jason! 8PM EST until 11P/12AM")
               utils.chat(s, "Tabby Tuesdays: Solo Stream with Trent! 8PM EST until 11P/12AM")
               utils.chat(s, "Thirsty Thursdays: Solo Stream with Matt! 10PM EST until 12AM")
               utils.chat(s, "Festive Friday: Join the entire crew for party games! 7:30PM EST (ish) until we go to the bar (12A/1A)")
               utils.chat(s, "Shady Saturday: Come talk shit and spill the T! 2PM EST until 8PM EST. WOOF!")
               timecCount = 0
           #if timeCount == 1000:
           #    utils.chat(s, "Remeber to follow and turn on the notification settings to know when we go on. To get more information about us, see the details portion of the stream.")
           #    timeCount = 0
           print utils.isOp(username)
           if message.strip() == "!schedule" and utils.isOp(username) and cfg.CHAN == "supercubs":
               utils.chat(s, "Masc4Masc Mondays: Solo Stream with Jason! 8PM EST until 11P/12AM")
               utils.chat(s, "Tabby Tuesdays: Solo Stream with Trent! 8PM EST until 11P/12AM")
               utils.chat(s, "Thirsty Thursdays: Solo Stream with Matt! 10PM EST until 12AM")
               utils.chat(s, "Festive Friday: Join the entire crew for party games! 7:30PM EST (ish) until we go to the bar (12A/1A)")
               utils.chat(s, "Shady Saturday Come talk shit and spill the T! 2PM EST (ish) until 8PM EST. WOOooF!")

           #!commands whispers the command list NOT WORKING! -- needs a seperate connection to Group chat :/ Not sure..
           if message.split()[0] == "!commands" and utils.isOp(username):
               utils.whisper(s, message.split(' ', 2)[1], message.split(' ', 2)[2])
           #!ban Hammer
           if message.split()[0] == "!ban" and utils.isOp(username):
               user = message.split()[1]
               try:
                   utils.ban(s, message.split()[1])
               except:
                   utils.chat(s, "No name")
           #!timeout
           if message.split()[0] == "!timeout" and utils.isOp(username):
               user = message.split()[1]
               try:
                   utils.timeout(s, message.split()[1])
               except:
                   utils.chat(s, "No name")
           #!eliminate <name>
           if message.split()[0] == "!eliminate":
               utils.eliminate(s, message.split()[1], username)
           #!eliminated <name>
           if message.split()[0] == "!eliminated" and utils.isOp(username):
               utils.eliminated(s, message.split()[1])
           #!game (In testing)
           if message.strip() == "!game":
               #if len(message.strip()) > 1: #get requests package installed
                #   utils.chat(s, utils.currentPlaying())
               utils.showGame(s)
           #!create Command
           if message.split()[0] == "!create" and utils.isOp(username): # I could make this safer by checking of the word has ! before the command else add it.
               utils.createCommands(message.split(' ', 2)[1], message.split(' ', 2)[2])
           #!useCommands created
           if unicode(message.strip()) in cfg.commands:
               utils.useCommands(s, message.strip())
           #!delete commands
           if message.split()[0] == "!delete" and utils.isOp(username):
               utils.removeCommands(message.split()[1])
           #!uptime
           if message.strip() == "!uptime":
               then = datetime.now()
               utils.chat(s, cfg.CHAN + " have been on for: " + (then - start))
           #!valentine
           if message.split()[0] == "!valentine":
               utils.valentine(s, message.split(' ', 1)[1], username)
           #!total
           if message.strip() == "!total":
               utils.total(s)
           #!switch
           if message.strip() == "!switch" and utils.isOp(username):
               utils.chat(s, "Come join us at midinght release of the switch on March 3rd. We will be streaming for the release of the switch, more info to come!!!")

           #if message.strip() == "!points":
           #   utils.points(s, username + " points are " + utils.points(username))
           #if message.strip() == "!mods":
           #   print cfg.oplist
           #   if utils.isOp(username):
           #        utils.chat(s, username + " is a mod or higher")

       except:
        print "Main broke!"
       sleep(1)


if __name__ == "__main__":
    main()

#Make it so that it will repeat messages of either !messages !socialmedia(supercubs pages, Yasdomdaddy pages)
#Users:
    # !firetemple --> link to youtube link of firetemple fail
    # !help --> link all options usr can send --> not sure how to use whisper
        # I want to have it check if it's isOp then use this command to show all else !isOp will show something else

#Admins:
    # !Jasongram ??
    # !trentgram
    # !mattgram
    # !unban <user> Do i need this?
    # !untimeout <user>

    # !openraffle (variable)
        # clear list
        # create boolean stating there is raffle open -- this is the main check
        # have variable stored
        # change boolean to true
    # !<variable>
        # runs a different method that grabs all names that are typing that variable
        # check if name is already in the list if so don't put the person's name in it.
    # !closeraffle
        # change boolean to false
    # !winner
        # remove bot from list list.remove(value)
        # random number gen to choose out of the array
        # multiplier equation later on for it
    # !game
        # !game <game> - will update game once having requests is installed
            # requests.put("http://api.twitch.tv/kraken/channels/" + cfg.CHAN, game=varGame)
        # will show what game is currently playing

#Done/Works:
    #!eliminate <name>
    #!eliminated <name>
    # !create
        # look into this on how to make it so that it allows you to create your own if statement
            #basic template of "if message.strip() == array[i]
                                # utils.chat (s, array2[i])
        # I guess i can make an associative array, Index as command, second is the array that gets what's printed for that specific index.
        # ^^ issue of storage, unless it's a one time thing
    # !ban <user> - not needed has /ban on basicis twitch chat
    # !timeout <user>
    #  !messages ??
    #!valentine
    #!total
    #!uptime