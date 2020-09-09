import _thread
import time

from pong import Pong
from mainmodel import PolicyGradient
game = Pong(2,server=True,sync=False,headless=True)##,debug=True)
_thread.start_new_thread(game.start,())
time.sleep(5)
model = PolicyGradient(resume=True)
model.start()
#####################################################################################
###  Dont Use this as this has a very high latency due to there being a lot of   ####
### threads running and even threads under other threads which doesnt make sense ####
###   But this is only true for one system I tested on, Others seem to benefit   ####
###                           from this approach                                 ####
#####################################################################################
