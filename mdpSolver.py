import random
       

class MDPOfflineSolver():
    def __init__(self, problem):
        self.problem = problem
        
        self.gamma = 0.90  # discount value
        self.convergeLimit = 0.001  # limit when the iteration is converged
        self.it = 0  # iteration steps
        
        
        self.values = {}  # dictionary for the values, saved for each state
        self.policy = {}
        
    def computeQValues(self, s, values):
        Q = {}
        for a in self.problem.getStateActions(s):
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
            actions = self.problem.getStateActions(s)
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
            self.policy[s] = random.choice(self.problem.getStateActions(s))  # randomize action taking
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
        self.epsilon = 0
        
        # initialize 
        self.QValues = {}
        self.policy = {}
        self.N = {}  # variable for the 'learning' 
        
    def getQValue(self, s, a):
        '''
        Return the Q-Value of a state-action pair, if it exists
        '''
        return self.QValues.get((s, a), 0)
    
    def computeValue(self, s):
        '''
        compute the value of a state from the Q-Values
        '''
        Q = self.computeQValues(s)
        return max(Q.values())
    
    def computeQValues(self, s):
        '''
        Return all Q-Values of a state
        '''
        Q = {}
        for a in self.problem.getStateActions(s):
            Q[a] = self.QValues.get((s, a), 0)
        return Q
        
    def updateN(self, s, a):
        '''
        Return the Q-Value of a state-action pair, if it exists
        '''
        self.N[(s, a)] = self.N.get((s, a), 1) + 1
    
    def updatePolicyStandard(self, s):
        '''
        Return the maximal Q-Value, i.e. the value, for a state and the necessary action 
        '''
        actions = self.problem.getStateActions(s)
        vmax = -float("inf")
        for a in actions:
            v = self.getQValue(s, a)
            if  v > vmax:
                vmax = v
                amax = a
                
        self.policy[s] = amax
            
        return vmax
    
    def updatePolicyExplorationFunction(self, s):
        '''
        Return the maximal Q-Value, i.e. the value, for a state and the necessary action, but take into account that non visited places get higher values 
        '''
        k = 10
        actions = self.problem.getStateActions(s)
        vmax = -float("inf")
        for a in actions:
            n = self.N.get((s, a), 1)
            v = self.getQValue(s, a) + k / (n + 1)
            if  v > vmax:
                vmax = v
                amax = a
                
        self.policy[s] = amax
            
        return vmax        
        
    
    def updateQ(self, s, a, sP, R):
        # update policy and get the value for the next state
        # v = self.updatePolicyStandard(sP)
        v = self.updatePolicyExplorationFunction(sP)
        self.updateN(s, a)
        
        # update QValues
        alpha = 1 / self.N[s, a]
        sample = R + self.gamma * v
        self.QValues[s, a] = (1 - alpha) * self.getQValue(s, a) + alpha * sample

    def choseAction(self, s):
        # chose an action depending on probability
        a = random.choice(self.problem.getStateActions(s)) 
        p = self.policy.get(s, a)  # returns the value or the default value "a" 
        return random.choice(int((1 - self.epsilon) * 100) * [p] + int(self.epsilon * 100) * [a])
        
    def run(self):
        s = random.choice(self.problem.getStartStates())
        maxI = 1000 
        for i in range(maxI):
            if i > maxI / 2:
                self.epsilon = self.epsilon
                
            if self.problem.isGoalState(s):
                s = random.choice(self.problem.getStartStates())
            a = self.choseAction(s)
            R, sP = self.problem.takeAction(s, a)
            self.updateQ(s, a, sP, R)
            
            # step to next field
            s = sP

class PropertyFunction():
    '''
    mother for property function
    '''
    def __init__(self, problem):
        self.weight = 1
        self.problem = problem # get access to the problem (easier than direct state evaluation)
        
    def evaluate(self, s, a):
        return 0

class QApproximator():
    def __init__(self, problem):
        self.problem = problem
        
        self.properties = []
        
        # initialize
        self.gamma = 0.9
        self.epsilon = 0
        self.N = 0
        
    def addPropertyFunction(self, prop):
        self.properties.append(prop)
        
    def computeQValue(self, s, a):
        '''
        Return the Q-Value of a state-action pair, if it exists
        '''
        Q = 0
        if self.problem.isGoalState(s):
            return Q
        for prop in self.properties:
            Q += prop.evaluate(s,a) * prop.weight
            
        return Q

    def computeQValues(self, s):
        '''
        Return all Q-Values of a state
        '''
        Q = {}
        for a in self.problem.getStateActions(s):
            Q[a] = self.computeQValue(s, a)
        return Q
    
    def computeValue(self, s):
        '''
        compute the value of a state from the Q-Values
        '''
        return max(self.computeQValues(s).values())
    
        
    def computePolicy(self, s):
        '''
        Return the maximal Q-Value, i.e. the value, for a state and the necessary action 
        '''
        Qs = self.computeQValues(s)
        vmax = max(Qs.values())
        amax = list(Qs.keys())[list(Qs.values()).index(vmax)]
                
        return amax
    
    def updateQ(self, s, a, sP, R):
        # update policy and get the value for the next state
        Qcur = self.computeQValue(s, a)
        v = self.computeValue(sP)
        difference = R + self.gamma * v - Qcur
        
        # update QValues
        self.N += 1
        alpha = 0.05 # 1 / self.N
        for prop in self.properties:
            prop.weight += alpha * difference * prop.evaluate(s, a)

    def choseAction(self, s):
        # chose an action depending on probability
        #a = random.choice(self.problem.getStateActions(s)) 
        #p = self.computePolicy(s)  # returns the value or the default value "a" 
        #return random.choice(int((1 - self.epsilon) * 100) * [p] + int(self.epsilon * 100) * [a])
        return self.computePolicy(s)
        
    def run(self):
        s = random.choice(self.problem.getStartStates())
        maxI = 1000 
        for i in range(maxI):
            if i > maxI / 2:
                self.epsilon = self.epsilon
                
            if self.problem.isGoalState(s):
                s = random.choice(self.problem.getStartStates())
            a = self.choseAction(s)
            R, sP = self.problem.takeAction(s, a)
            self.updateQ(s, a, sP, R)
            
            # step to next field
            s = sP              
