import numpy as np
import pickle
import socket
from io import BytesIO
import _thread
import time
class PolicyGradient:
	def sigmoid(self,x):
		return 1.0 / (1.0+np.exp(-x))
	def preprocess(self,img):
		return img.reshape(-1)

	def semi_returns(self,rewards):
		discounted_r = np.zeros_like(rewards)
		sums=0
		for t in reversed(range(0,rewards.size)):
			if rewards[t]!=0:
				sums=0
			sums+=r[t]
			discount_r[t] = sums
		return discounted_r
	def fc(self,x):
		h=np.dot(self.model['W1'],x)
		h[h<0]=0
		logp = np.dot(self.model['W2'],h)
		p = self.sigmoid(logp)
		return p,h

	def backward(self):
		dW2 = np.dot(self.eph.T,self.epdlogp).ravel()
		dh = np.outer(self.epdlogp,self.model['W2'])
		dh[self.eph<=0] = 0
		dW1 = np.dot(dh.T,self.epx)
		return {'dW1':dW1,'dW2':dW2}
	def __init__(self,resume=False,render=False,hiddenUnits = 250,batch_size = 10,learningRate= 1e-3,gamma = 0.99,decayRate = 0.99,host=None,port=12345):
		if resume:
			self.model = pickle.load(open("checkpoint.p",'rb'))
		else:
			self.model={}
			self.model['W1']=np.random.randn(hiddenUnits,70*50)/60 ## Needs changes
			self.model['W2']=np.random.randn(hiddenUnits)/np.sqrt(hiddenUnits)

		self.grad_buff = {k: np.zeros(v.shape) for k,v in self.model.items()}
		self.rmsprop_cache = {k : np.zeros(v.shape) for k,v in self.model.items()}
		self.learningRate=learningRate
		self.batch_size = batch_size
		self.gamma = gamma
		self.decayRate = decayRate
		self.render = render
		self.dim = 70*50
		self.socket=None
		self.host = host
		self.port = port
		self.handshake = False
		self.runningFlag=True
		self.ongoingFlag=True
	def propriety_control(self,dummy):
		while self.runningFlag:
			a=input()
			if a=='p':
				print("Pausing the training session" if self.ongoingFlag else "Resuming the training session")
				self.ongoingFlag= not self.ongoingFlag
			elif 'q':
				self.ongoingFlag=False
				print("Interupting saving the previous checkpoint to interrupt.p .")
				pickle.dump(self.model, open('interrupt.p', 'wb'))
				time.sleep(0.02)
				exit()
			## If cases to pause the environment
		## This is to give a basic control over the training and other things
		return True
	def connect_env(self,host): ## didnt use try except as to view particular errors
		if host is None:
			host = socket.gethostname()
		self.socket = socket.socket()
		self.socket.connect((host,self.port))
		print("Connection established with "+str(host)+" on port "+str(self.port))
		self.handshake=True
	def get_frame(self):
		if self.handshake:
			self.socket.send('r'.encode('utf-8'))
			#while True:
				#inp_buffer=self.socket.recv(1024)
				#if not inp_buffer: break
				#img_buffer+=inp_buffer
			img_buffer = self.socket.recv(4096)  ## THis much of buffer is sufficient for the image used here
			#print("Image Fetched in network")
			return np.load(BytesIO(img_buffer))['frame']
		else:
			raise Exception('Connect to the environment first')

	def get_reward(self):
		if self.handshake:
			self.socket.send('s'.encode('utf-8'))
			return int(self.socket.recv(1024).decode('utf-8'))
		else:
			raise Exception('Connect to the environment first')
	def send_action(self,action):
		if self.handshake:
			self.socket.send(('a-'+action).encode('utf-8')) ## Add a confirmation
		else:
			raise Exception('Connect to the environment first')
	def start(self,n=10000000000000000):
		_thread.start_new_thread(self.connect_env, (self.host,))
		_thread.start_new_thread(self.propriety_control, (True,))
		while not self.handshake:
			time.sleep(0.05)
		self.send_action('1') ##For initiating
		observation = self.get_frame()
		print('Image fetched in main')
		returns = None
		prev_x = None
		xs,hs,dlogps,drs=[],[],[],[]
		eps_no=0
		reward_sum=0
		while self.ongoingFlag:
			if  eps_no >n:
				pickle.dump(self.model, open('ending_'+str(n)+'.p', 'wb'))
				print("Stopping the training as "+str(n)+" episodes are complete")
				break
			if self.render:
				cv2.imshow("OUTPUT DONT Use This!!!",observation)
				cv2.waitKey(5)
			cur_x = self.preprocess(observation)
			x = cur_x - prev_x if prev_x is not None else np.zeros(self.dim)
			prev_x = cur_x
			aprob, h = self.fc(x)
			action = 1 if np.random.uniform() < aprob else 2
			xs.append(x)
			hs.append(h)
			y = 1 if action==1 else 0
			dlogps.append(y-aprob)
			self.send_action(str(action))
			observation = self.get_frame()
			reward = self.get_reward()
			done = True if reward!=0 else False
			reward_sum+=reward
			drs.append(reward)
			if done:
				eps_no+=1
				self.epx=np.vstack(xs)
				self.eph=np.vstack(hs)
				self.epdlogp = np.vstack(dlogps)
				self.epr = np.vstack(drs)
				xs,hs,dlogps,drs = [],[],[],[]
				discounted_epr = self.semi_returns(epr)
				discounted_epr -= np.mean(discounted_epr)
				discounted_epr /=  np.std(discounted_epr)
				epdlogp  *= discounted_epr
				grad = self.backward()
				for k in self.model: self.grad_buff[k]+=grad[k]
				if eps_np%self.batch_size  == 0 :
					for k,v in self.model.iteritems():
						g = self.grad_buff[k]
						self.rmsprop_cache[k] = self.decay_rate*rmsprop_cache[k] + (1-self.decay_rate)* g**2
						self.model[k] += self.learning_rate*g / (np.sqrt(self.rmsprop_cache[k])+1e-5)
						self.grad_buff[k] = np.zeros_like(v)
				returns = reward_sum if returns is None else returns*0.99 + reward_sum*0.01
				print(('This episode' if eps_no==0 else 'Another episode') + ' is completed with total reward: '+str(reward_sum)+' and runnign mean: '+str(returns))
				if episode_no%100==0:
					 pickle.dump(self.model, open('save.p', 'wb'))
				reward_sum=0
				time.sleep(0.05)## THis is for the ball to go away from the boundary after someone has won
				observation = self.get_frame()
				prev_x=None
				if reward !=0:
					print('episode '+str(eps_no)+' game finished reward '+str(reward)+ ('' if reward==-1 else '!!!!!!'))

if __name__ == "__main__":
	model = PolicyGradient()
	model.start()
