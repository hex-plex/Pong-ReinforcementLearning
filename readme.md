# Pong with Reinforcement learning
I have tried baking a rudimentary RL environment and a agent recipe to learn more about the eco-system.<br/>
I have made [pong.py](https://github.com/hex-plex/Pong-ReinforcementLearning/blob/master/pong.py) a environment which one can host either locally (localhost) or on  0.0.0.0 (LAN).Allowing to communicate to [mainmodel.py](https://github.com/hex-plex/Pong-ReinforcementLearning/blob/master/mainmodel.py) which has to be connected to the same host and the same port. <br/>
I have used a simple socket connection to transfer data rather than a flask/django backend as they are based on it giving a advantage of speed of communication. <br/>
both the scripts have debug mode which allows one to see in which state or stage they are in. <br/>
## Requirements
This requires only few basic libraries it only runs on python3, rather a small update can make it compatible with python2.
The libraries
```bash
pickle
numpy
cv2
pygame
# Below are mostly available preinstalled in any python distribution
socket
BytesIO # from io in python3 or directly in python2
_thread # for python 3 and thread in python2
```
Which are quite rudimentary and neccessary part of the code.

## Multithreading
Here I have use many threads to assure that no data is missed while anyother calculation or process is running on the main thread as there might be some unwanted lag between inputs.Also another thread on mainmodel exists which take inputs  from the user for pausing and resuming its learning session
## Sockets
I have used sockets to send data between scripts rather than using a instance of model and the pong env on the same script well that would work just fine (or better removing all the lag of communication) , but my goal was to make it more appealing and to make me learn more real life skills that is if I train a agent with raspberry pi ( or any other weaker mobile device for that matter ) as a part of the environment or in the environment a more viable option than running both simulation and the RL agent would be to do the computation and send in actions to it. This also gave me a good understanding about data compression and network security ,though here there is none used as it just accepts the first connection to the env. <br/>
<br/>
with the use of socket one could manually control the environment with keyboard and also have a RL agent learning (half - Duplex).  

## Demo
To launch the env with mostly default values just running [pong.py](https://github.com/hex-plex/Pong-ReinforcementLearning/blob/master/pong.py) directly would start the server with default configs.
Its always recommended to use its instance, apply your configuration you want it to run and start the server.
```python
from pong import Pong

env = Pong( levelodiff=1, ## This is the level of the inbuilt AI that plays against you.
                          ## Set it to 4 and chill out (really try it!!) the scale is 1-3
            debug=False,  ## If set to True it will print the stage the environment is in and info the data inputs and outputs
            render=False, ## It would render the image that is sent to the model, This slows down the process so not a good idea to use it.
            server=True,  ## This is to set server mode on , if set false the environment will be no different from ordinary pong game.
            host="",      ## This is to specify where you want to host it, "" maps to local host "0.0.0.0" doesnt really map
                          ## to your ip address yet
            port=12345    ## This your port no. of the connection.
          )               ## This is to just initiate the environment

env.start()## This starts the env ie., hosts itself as per the given parameter and waits for a connection in async while continuing the game
```

To launch the RL agent running the [mainmodel.py](https://github.com/hex-plex/Pong-ReinforcementLearning/blob/master/mainmodel.py) directly will run it in default config. <br/>
To customize to your config import and create an instance and run the client. <br/>
```python
from mainmodel import PolicyGradient

## This uses two hidden layer to out-put 2 probabilities
agent = PolicyGradient( resume=False,  ## This is usefull to continue training from previos checkpoint.
                        render=True,   ## This will render the image got through the socket,useful if model is in another computer
                        host=None,     ## If the value is None it trys to find a localhost , else specific host is to be provided as a str
                        port=12345,    ## default value is 12345 set is as required.
                        hiddenUnits=250, ## This no of hiddenUnits in first layer depending on the dimension of input.
                        batch_size=10, ## This is to set batch size for batch reiforcement learning rather than using single episode.
                        learningRate=1e-3, ## This is to set learning rate
                        gamma=0.99,    ## This is to set gamma or the discount
                        decayRate=0.99 ## This is decayRate for RMSprop
                      )                ## This creates an instance of PolicyGradient algorithm as a client_socket

agent.start()         ## This starts the agent ie., connects to the server and communicates and learns from its experience.
```

Running them should launch the env and agent would start leaning. There is a propriety control in mainmodel.py which takes input in its terminal as
- 'p'    ==> Pausing/Resuming the training process
- 'q'    ==> Quit the training process , But this makes a Checkpoint as interrupt.p
- 'ping' ==> This pings the pong server 10 times and returns the average time it took to send and receive packets.
else with a better score of agent, the model is saved continuosly as save.p.

## TODO

- [X] Make a pong game or search for some source  code
- [X] Then host a server on flask on local server for the game so as to be able to send reward and control it using parallel computing(supposedly for pi).
- [X] Make a basic model out of numpy
- [ ] <del>Stack it against Open Gym AI Retro</del> - Training to be done

## Bugs
- [X] The state after the score being changed is the same as the one just before scoring hence confusing the Neural Net
- [X] <del>The training process is slowed due to network , enable the async mechanishms</del> enabling this leads to drop few states by the environment to seemlessly continue but as the change from one state to other is small it should not be a problem.
Nothing for now only further test would say
## This is a demo of the pong game
<img src="/images/pong-game.png"> <br/>
More to come<br/>
......<br/>
<img src="/initial_training.gif"> <br/>
This clip from initial training session.
