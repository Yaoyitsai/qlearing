#Describe the problems I met during my implementation:

#我遇到最大的問題是在def __init__(self, **args)裡要初始化Q-values
#一開始在trace其他py檔前我用二維陣列來存放state, action, qvalue 的值
#ex:[[state_1,action_1,qvalue_1],[state_2,action_2,qvalue_2]....]
#但因為不確定所有的action和state,所以沒有辦法做好初始化的動作,導致後面在計算時有nontype error
#直到後來在trace graphicsGridworldDisplay.py時,發現其中drawQValues() method裡
#將qValues用dictionary的方式來存取(state, action)這對pair
#於是我才用一樣的方式來初始化我的qvalue
#第二個問題是在實作computeActionFromQValues時
#一開始沒想到用一個tmp來存qvalue和action這對pair
#如此在比較完qvalue後便可直接回傳best action
#導致卡在透過getQvalue比較完value值後不知道該如何access這個值的action
#其他的小問題就是在實作getAction & update時沒有發現到一些已經寫好的variables和function可以拿來使用
#------其餘的comments寫在下方的code------

# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        "*** YOUR CODE HERE ***"
        #comments & why I implement it:
        #我使用dictionary的資料結構來做資料的查找
        #這麼做的原因是可以直接使用(state,action)這對pair當作key值來存取Q的value
        self.Q={}

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #comments:
        if (state,action) in self.Q: #當(state,action)這對pair在dictionary裡
            return self.Q[(state,action)] #就回傳他的qvalue
        else: #否則就回傳0.0
            return 0.0
        #why I implement it:
        #因為當 computeValueFromQValues and computeActionFromQValues要access qvalue時
        #只能透過calling this getQValue method

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #comments:
        #設一個名為tmp_s_a的list存這些當前state合法的action的qvalue
        tmp_s_a = [] 
        if not self.getLegalActions(state): #檢查這個state是否有合法的action
            return 0.0 #若沒有就回傳0.0
        else: #若合法就將這些合法的action透過for迴圈將getQValue(state, action),append進這個tmp_s_a
            for action in self.getLegalActions(state):
                tmp_s_a.append(self.getQValue(state, action))
        return max(tmp_s_a) #最後回傳max_action Q(state,action)
        #why I implement it:
        #因為透過實作這個computeValueFromQValues method
        #才能在update計算nextstate的qvalue時呼叫這個method
        #透過給state的值來找到當前最佳的qvalue

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the te
          rminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        #comments:
        #設一個名為tmp_s_a的list 存 (當前state合法的action的value)和(此action)這對pair
        tmp_s_a = [] 
        if not self.getLegalActions(state):#檢查這個state是否有合法的action
            return None #若沒有就回傳none
        else: #若合法就把這對(qvalue,action)的pair,append進這個tmp_s_a
            for action in self.getLegalActions(state):
                tmp_s_a.append((self.getQValue(state, action), action))
            for i in tmp_s_a: #設一個ans存max(tmp_s_a)
              if i == max(tmp_s_a):
                  ans=i       
        return ans[1] #回傳best action
        #why I implement it:
        #因為透過實作這個computeActionFromQValues method
        #才能在getAction呼叫這個method時
        #透過給state的值來找到當前最佳的action


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        #comments:
        #這裡要實作epsilon-greedy action selection
        #所以當機率為self.epsilon時,從getLegalActions(state)裡
        #透過random.choice(list)來random選出action
        #若機率不為self.epsilon時
        #則透過computeActionFromQValues(state)
        #回傳 best action
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state)
        #why I implement it:
        #因為透過實作這個getAction method才能在機率為epsilo時隨機選出action

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #comments:
        #先利用computeValueFromQValues計算nextState的qvalue
        #再利用qlearning的更新公式計算新的qvalue
        #最後利用dictionary的方式放入這個(state,action)相對應的value裡
        next_v = self.computeValueFromQValues(nextState)
        next_v = (1-self.alpha) * self.getQValue(state, action) + self.alpha * (reward + self.discount * next_v)
        self.Q[(state, action)] = next_v
        #why I implement it:
        #因為透過實作這個update method才能將每個action帶來的reward更新到這個Q-table
        #且在一開始dictionary裡沒東西時也能初始化值


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
