import _thread
import time

from pong import Pong
from mainmodel import PolicyGradient
print("ENTER DIFFICULTY")
print("EASY     --> 1")
print("MODERATE --> 2")
print("HARD     --> 3")
levelodiff=input()
game = Pong(levelodiff,server=True)##,debug=True)
_thread.start_new_thread(game.start,())
time.sleep(5)
model = PolicyGradient()
model.start()
#####################################################################################
###  Dont Use this as this has a very high latency due to there being a lot of   ####
### threads running and even threads under other threads which doesnt make sense ####
#####################################################################################
