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

   while True:
       response = s.recv(1024).decode("utf-8")
       #if the connection to tmi.twitch.tv connects will get a pong
       if response == "PING :tmi.twitch.tv\r\n":
           s.send("PONG :tmi.twtich.tv\r\n".encode("utf-8"))
       else:
           username = re.search(r"\w+", response).group(0)
           message = CHAT_MSG.sub("", response)
           print(response)

           #Custom Commands
           if message.strip() == "!time":
               utils.chat(s, "It is currently " + time.strftime("%I: %M %p %Z on %A, %B %d %Y."))
           if message.strip() == "!messages": #and utils.isOp(username):
               utils.chat(s, "Masc4Masc Mondays: Solo Stream with Jason!")
               utils.chat(s, "Tabby Tuesdays: Solo Stream with Trent!")
               utils.chat(s, "Thirsty Thursdays: Solo Stream with Matt!")
               utils.chat(s, "Festive Friday: Join the entire crew for party games! 7:30PM EST (ish) until we go to the bar (12A/1A)")
               utils.chat(s, "Shady Saturday Come talk shit and spill the T! 2PM EST (ish) until 8PM EST. WOOooF!")
           if message.strip() == "!points":
               utils.chat (s, username + " points are " + utils.points(username))
       sleep(1)


if __name__ == "__main__":
    main()