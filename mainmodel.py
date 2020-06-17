import numpy as np
import pickle

class PolicyGradient:
	def sigmoid(self,x):
		return 1.0/(1.0+np.exp(-x))
	def preprocess(self,img):
		pass

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
		h = np.dot(h,np.array(h>0,dtyp=np.uint8))
		logp = np.dot(self.model['W2'],h)
		p = self.sigmoid(logp)
		return p,h

	def backward(self):
		dW2 = np.dot(self.eph.T,self.epdlogp).ravel()
		dh = np.outer(self.epdlogp,self.model['W2'])
		dh[self.eph<=0] = 0
		dW1 = np.dot(dh.T,self.epx)
		return {'dW1':dW1,'dW2':dW2}
	def __init__(self,resume=False,render=False,hiddenUnits = 250,batch_size = 10,learningRate= 1e-3,gamma = 0.99,decayRate = 0.99):
		if resume:
			self.model = pickle.load(open("checkpoint.p",'rb'))
		else:
			self.model={}
			self.model['W1']=np.random.randn(hiddenUnits,80*80)/80 ## Needs changes
			self.model['W2']=np.random.randn(hiddenUnits)/np.sqrt(hiddenUnits)

		self.grad_buff = {k: np.zeros(v.shape) for k,v in model.iteritems()}
		self.rmsprop_cache = {k : np.zeros(v.shape) for k,v in model.iteritems()}
		self.learningRate=learningRate
		self.batch_size = batch_size
		self.gamma = gamma
		self.decayRate = decayRate
		self.render = render
		self.dim = 70*50
	def connect_env(self):
		pass
	def get_frame(self):
		pass
	def get_reward(self):
		pass
	def send_action(self):
		pass
	def start(self):
		self.connect_env()
		observation = self.get_frame()
		returns = None
		prev_x = None
		xs,hs,dlogs,drs=[],[],[],[]
		eps_no=0
		reward_sum=0
		while True:
			if render:
				cv2.imshow("OUTPUT DONT Use This!!!",observation)
				cv2.waitKey(5)
			cur_x = self.preprocess(observation)
			x = cur_x - prev_x if prev_x is not None else np.zeros(self.dim)
			prev_x = cur_x
			aprob, h = self.fc(x)
			action = 2 if np.random.uniform() < aprob else 3
			xs.append(x)
			hs.append(h)
			y = 1 if action==2 else 0
			dlogps.append(y-aprob)
			observation = self.get_frame()
			reward = self.get_reward()
			done = True if reward!=0 else False
			reward_sum+=reward
			drs.append(reward)
			if done:
				eps_no+=1
				self.epx=np.vstack(xs)
				self.eph=np.vstack(hs)
				self.epdlogp = np.vstack(dlogs)
				self.epr = np.vstack(drs)
				xs,hs,dlogps,drs = [],[],[],[]
				discounted_epr = discount_rewards(epr)
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
					reward_sum=0
				time.sleep(0.05)## THis is for the ball to go away from the boundary after someone has won
				observation = self.get_frame()
				prev_x=None
				if reward !=0:
					print('episode '+str(eps_no)+' game finished reward '+str(reward)+ ('' if reward==-1 else '!!!!!!'))
