import random
import mdp
           

class MDPOfflineSolver():
    def __init__(self, problem):
        self.problem = problem
        
        self.gamma = 0.90 # discount value
        self.convergeLimit = 0.001 # limit when the iteration is converged
        self.it = 0 #iteration steps
        
        
        self.values = {} # dictionary for the values, saved for each state
        self.policy = {}
        
    def computeQValues(self, s, values):
        Q = {}
        for a in self.problem.getActions(s):
            moves = self.problem.getTransitionFunction(s, a)
            V = 0
            for m in moves:
                T = m[0]  # transition function / probability
                R = m[1]  # reward for this transition
                sP = m[2]  # new state s'
                V += T * (R + self.gamma * values[sP])
            Q[a] = V
                
        return Q
        
    def policyExtraction(self, values):
        p = {}
        for s in self.problem.getStates():
            actions = self.problem.getActions(s)
            curMax = -float("inf")
            curA = None
            for a in actions:
                moves = self.problem.getTransitionFunction(s, a)
                V = 0
                for m in moves:
                    T = m[0]  # transition function / probability
                    R = m[1]  # reward for this transition
                    sP = m[2]  # new state s'
                    V += T * (R + self.gamma * values[sP])
                if V > curMax:
                    curMax = V
                    curA = a
                
            p[s] = curA
                
        return p  
    
    def computePolicy(self):
        return self.policyExtraction(self.values)

class PolicyIterator(MDPOfflineSolver):
        
    def policyEvaluation(self, curP, curV):
        converged = False
        while not converged:
        # for i in range(71):
            maximum = -float("inf")
            for s in self.problem.getStates():
                moves = self.problem.getTransitionFunction(s, curP[s])
                V = 0
                for m in moves:
                    T = m[0]  # transition function / probability
                    R = m[1]  # reward for this transition
                    sP = m[2]  # new state s'
                    V += T * (R + self.gamma * curV[sP])
                    
                
                diff = abs(V - curV[s])
                maximum = max(diff, maximum)
                
                curV[s] = V        
            
            if maximum < self.convergeLimit:
                converged = True
            
        return curV
    
    def run(self):
        # Initialize policy
        for s in self.problem.getStates():
            self.policy[s] = random.choice(self.problem.getActions(s))  # randomize action taking
            self.values[s] = 0
            
        converged = False
        self.it = 0
        while not converged:
        # for i in range(71):
            self.it += 1
            self.values = self.policyEvaluation(self.policy, self.values)
            newP = self.policyExtraction(self.values)
            
            if newP == self.policy:
                converged = True
                
            self.policy = newP
            

class ValueIterator(MDPOfflineSolver):
                    
    def valueMaximization(self, values):
        newVS = {}
        for s in self.problem.getStates():
            Q = self.computeQValues(s, values)
            newVS[s] = max(Q.values())
            
        return newVS
            
    def run(self):
        converged = False
        for s in self.problem.getStates():
            self.values[s] = 0  # initialize everything with zero first
        
        self.it = 0
        while not converged:
        # for i in range(71):
            self.it += 1
            newVS = self.valueMaximization(self.values)
            m = -float("inf")
            for s in newVS.keys():
                diff = abs(newVS[s] - self.values[s])
                m = max(diff, m)
            if m < self.convergeLimit:
                converged = True
                
            self.values = newVS
            # self.printValues(curV)
            # print('Maximal Difference: ' + str(m))
        self.policy = self.policyExtraction(self.values)
        
class QLearner():
    def __init__(self, problem):
        self.problem = problem
        
        # initialize
        self.gamma = 0.9
        self.epsilon = 0.8
        
        # initialize 
        self.QValues = {}
        self.policy = {}
        self.N = {} # variable for the 'learning' 
        
    def getQValue(self, s, a):
        '''
        Return the Q-Value of a state-action pair, if it exists
        '''
        return self.QValues.get((s, a),0)
    
    def getQValues(self, s):
        '''
        Return all Q-Values of a state
        '''
        Q = {}
        for a in self.problem.getActions(s):
            Q[a] = self.QValues.get((s, a),0)
        return Q
        
    def updateN(self, s, a):
        '''
        Return the Q-Value of a state-action pair, if it exists
        '''
        self.N[(s, a)] = self.N.get((s, a),1) + 1
    
    def updatePolicy(self, s):
        '''
        Return the maximal Q-Value, i.e. the value, for a state and the necessary action 
        '''
        actions = self.problem.getActions(s)
        vmax = -float("inf")
        for a in actions:
            v = self.getQValue(s, a)
            if  v > vmax:
                vmax = v
                amax = a
                
        self.policy[s] = amax
            
        return vmax
        
    def updateQ(self, s, a, sP, R):
        # update policy and get the value for the next state
        v = self.updatePolicy(sP)
        self.updateN(s, a)
        
        # update QValues
        alpha = 1 / self.N[s, a]
        sample = R + self.gamma * v
        self.QValues[s, a] = (1 - alpha) * self.getQValue(s, a) + alpha * sample
        
    def run(self):
        def choseAction(s):
            # chose an action depending on probability
            a = random.choice(self.problem.getActions(s)) 
            p = self.policy.get(s, a) # returns the value or the default value "a" 
            return random.choice(int((1 - self.epsilon) * 100) * [p] + int(self.epsilon * 100) * [a])
        
        s = random.choice(self.problem.getStartStates())
        maxI = 5000 
        for i in range(maxI):
            if i > maxI / 2:
                self.epsilon = self.epsilon
                
            if self.problem.isGoalState(s):
                s = random.choice(self.problem.getStartStates())
            a = choseAction(s)
            R, sP = self.problem.takeAction(s, a)
            self.updateQ(s, a, sP, R)
            
            # step to next field
            s = sP
            
problem = mdp.GridWorldProblem() # mdp.RacingProblem()

vI = ValueIterator(problem)
pI = PolicyIterator(problem)

vI.run()
pI.run()


qLearner = QLearner(problem)
qLearner.run()

mdp.printPolicy(vI.computePolicy())
mdp.printPolicy(pI.computePolicy())
mdp.printPolicy(qLearner.policy)