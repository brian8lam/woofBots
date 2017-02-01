#bot.py
#The code for the bot

import cfg
import utils
import socket
import re
import time
import thread
import os
from time import sleep

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
   timeCount = 0
   while True:
       response = s.recv(1024).decode("utf-8")
       #if the connection to tmi.twitch.tv connects will get a pong
       if response == "PING :tmi.twitch.tv\r\n":
           s.send("PONG :tmi.twtich.tv\r\n".encode("utf-8"))
       else:
           username = re.search(r"\w+", response).group(0)
           message = CHAT_MSG.sub("", response)
           print(response)
           timeCount += 1
           if timeCount == 120:
               utils.chat(s, "Masc4Masc Mondays: Solo Stream with Jason! 7:30P/8PM EST until 11P/12AM")
               utils.chat(s, "Tabby Tuesdays: Solo Stream with Trent! 7:30P/8PM EST until 11P/12AM")
               utils.chat(s, "Thirsty Thursdays: Solo Stream with Matt! 10PM EST until 12AM")
               utils.chat(s, "Festive Friday: Join the entire crew for party games! 7:30PM EST (ish) until we go to the bar (12A/1A)")
               utils.chat(s, "Shady Saturday: Come talk shit and spill the T! 2PM EST until 8PM EST. WOOF!")
           if timeCount == 200:
               utils.chat(s, "Remeber to follow and turn on the notification settings to know when we go on. To get more information about us, see the details portion of the stream.")
               timeCount = 0
           #Custom Commands
           if message.strip() == "!mods":
               if utils.isOp(username):
                    utils.chat(s, username + " is a mod or higher")
           if message.strip() == "!time":
               utils.chat(s, "It is currently " + time.strftime("%I: %M %p %Z on %A, %B %d %Y."))
           if message.strip() == "!messages": #and utils.isOp(username):
               utils.chat(s, "Masc4Masc Mondays: Solo Stream with Jason!")
               utils.chat(s, "Tabby Tuesdays: Solo Stream with Trent!")
               utils.chat(s, "Thirsty Thursdays: Solo Stream with Matt!")
               utils.chat(s, "Festive Friday: Join the entire crew for party games! 7:30PM EST (ish) until we go to the bar (12A/1A)")
               utils.chat(s, "Shady Saturday Come talk shit and spill the T! 2PM EST (ish) until 8PM EST. WOOooF!")
           #if message.strip() == "!points":
           #    utils.chat (s, username + " points are " + utils.points(username))
           if message.strip() == "!socialmedia":
               utils.chat(s, "You can find us at.")
           if message.split()[0] == "!ban":
               user = message.split()[1]
               try:
                   utils.ban(s, message.split()[1])
               except:
                   utils.chat(s, "No name")
           if message.split()[0] == "!timeout":
               user = message.split()[1]
               try:
                   utils.timeout(s, message.split()[1])
               except:
                   utils.chat(s, "No name")
           if message.split()[0] == "!create":
               utils.createCommands(message.split(' ', 2)[1], message.split(' ', 2)[2])
           if message.strip() in utils.commands:
               utils.usecommand(s, utils.commands[message.strip()])
           if message.strip() == "!firetemple":
               utils.chat(s, "'Woop Woop!' *5 hours later* FailFish")
       sleep(1)


if __name__ == "__main__":
    main()

#Make it so that it will repeat messages of either !messages !socialmedia(supercubs pages, Yasdomdaddy pages)
#Users:
    # !firetemple --> link to youtube link of firetemple fail
    # !help --> link all options usr can send


#Admins:
    # !Jasongram ??
    # !trentgram
    # !mattgram
    # !messages ??
    # !ban <user> - not needed has /ban on basicis twitch chat
    # !timeout <user>
    # !unban <user>
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
        #random number gen to choose out of the array
        # multiplier equation later on for it
    # !create
        # look into this on how to make it so that it allows you to create your own if statement
            #basic template of "if message.strip() == array[i]
                                # utils.chat (s, array2[i])
        # I guess i can make an associative array, Index as command, second is the array that gets what's printed for that specific index.
        # ^^ issue of storage, unless it's a one time thing
