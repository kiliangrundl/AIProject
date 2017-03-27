import numpy as np

class RacingProblem():
    '''
    The racing problem as described in the course as a MDP
    '''
    def getStates(self):
        return ['cool', 'warm', 'overheated']
    
    def getActions(self, s):
        if s == 'cool':
            return ['slow', 'fast']
        elif s == 'warm':
            return ['slow', 'fast']
        else:
            return []
        
    def getTransitionFunction(self, s, a):
        '''
        the transition functions from one state to the other
        returns a list of tuples, containg the (probability, reward, nextState)
        '''
        if s == 'cool':
            if a == 'slow':
                return [(1, 1, 'cool')]
            elif a == 'fast':
                return [(0.5, 2, 'cool'), (0.5, 2, 'warm')]
            else:
                raise Exception('FAILURE')
        elif s =='warm':
            if a == 'slow':
                return [(0.5, 1, 'cool'), (0.5, 1, 'warm')]
            elif a == 'fast':
                return [(1, -10, 'overheated')]
            else:
                raise Exception('FAILURE')
        else:
            raise Exception('FAILURE')
        
class GirdWorldProblem():
    '''
    The GridWorldProblem as a MDP
    '''
    
    def getStates(self):
        return ['A1', 'A2', 'A3', 'A4', 'B1', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4', 'finish']
    
    def getActions(self, s):
        if s == 'C4' or s == 'B4':
            return ['exit']
        else:
            return ['n', 'e', 's', 'w']
        
    def getTransitionFunction(self, s, a):
        '''
        the transition functions from one state to the other
        returns a list of tuples, containg the (probability, reward, nextState)
        '''
        lR = 0
        if s == 'C4':
            return [(1,1,'finish')]
        elif s == 'B4':
            return [(1,-1,'finish')]
        elif s == 'finish':
            return [(1,0,'finish')]
        else:
            if a == 'n':
                news = ['X'+s[1], s[0]+str(int(s[1])-1), s[0]+str(int(s[1])+1)]
                if s[0] == 'A':
                    news[0] = 'B'+s[1] 
                elif s[0] == 'B':
                    news[0] = 'C'+s[1]
            elif a == 's':    
                news = ['X'+s[1], s[0]+str(int(s[1])-1), s[0]+str(int(s[1])+1)]
                if s[0] == 'C':
                    news[0] = 'B'+s[1] 
                elif s[0] == 'B':
                    news[0] = 'A'+s[1]
            elif a == 'e':
                news = [s[0]+str(int(s[1])+1), s, s]
                if s[0] == 'A':
                    news[1] = 'B'+s[1]
                    news[2] = 'X'+s[1] 
                elif s[0] == 'B':
                    news[1] = 'A'+s[1]
                    news[2] = 'C'+s[1]
                elif s[0] == 'C':
                    news[1] = 'X'+s[1]
                    news[2] = 'B'+s[1]
            else: #west
                news = [s[0]+str(int(s[1])-1), s, s]
                if s[0] == 'A':
                    news[1] = 'B'+s[1]
                    news[2] = 'X'+s[1] 
                elif s[0] == 'B':
                    news[1] = 'A'+s[1]
                    news[2] = 'C'+s[1]
                elif s[0] == 'C':
                    news[1] = 'X'+s[1]
                    news[2] = 'B'+s[1]
                    
            # If the new possible state does not exist, replace it with the old state
            F = news
            for i in range(len(news)):
                if news[i] not in self.getStates():
                    F[i] = s
            
            return [(0.8, lR, F[0]), (0.1, lR, F[1]), (0.1, lR, F[2])]
    
        
            

class MDPSolver():
    def __init__(self, problem):
        self.problem = problem
        self.gamma = 0.90
        
    def printPolicy(self, p):
        for k in sorted(p.keys()):
            print(k + ': ' + p[k], end=' | ')
        print('')
               
    def printValues(self, curV):
        for k in sorted(curV.keys()):
            print(k + ': ' + '%.2f' % (curV[k]), end = ' | ')
        print('')
        
    def policyExtraction(self, curV):
        p = {}
        for s in curV.keys():
            actions = self.problem.getActions(s)
            curMax = -float("inf")
            curA = None
            for a in actions:
                moves = self.problem.getTransitionFunction(s, a)
                V = 0
                for m in moves:
                    T = m[0] # transition function / probability
                    R = m[1] # reward for this transition
                    sP = m[2] # new state s'
                    V += T * (R + self.gamma * curV[sP])
                if V > curMax:
                    curMax = V
                    curA = a
                
            p[s] = curA
                
        return p  

        
    def valueUpdate(self, curP, curV):
        newVS = {}
        newVS2 = curV
        converged = False
        while not converged:
        #for i in range(71):
            for s in curP.keys():
                moves = self.problem.getTransitionFunction(s, curP[s])
                V = 0
                for m in moves:
                    T = m[0] # transition function / probability
                    R = m[1] # reward for this transition
                    sP = m[2] # new state s'
                    V += T * (R + self.gamma * curV[sP])
                    
                newVS[s] = V
                
            m = -float("inf")
            for s in newVS.keys():
                diff = abs(newVS[s] - newVS2[s])
                m = max(diff, m)
            if m < 0.0000000001:
                converged = True
                
            newVS2 = newVS        

            
        return newVS
    
    def policyIteration(self):
        # Initialize policy
        curP = {}
        curV = {}
        for s in self.problem.getStates():
            curP[s] = self.problem.getActions(s)[0] # always take the first action
            curV[s] = 0
            
        converged = False
        it = 0
        while not converged:
        #for i in range(71):
            curV = self.valueUpdate(curP, curV)
            newP = self.policyExtraction(curV)
            
            if newP == curP:
                converged = True
                
            curP = newP
            
            it += 1
            
        return curP, curV, it
    
    def computeQValues(self, s, VS):
        Q = {}
        for a in self.problem.getActions(s):
            moves = self.problem.getTransitionFunction(s, a)
            V = 0
            for m in moves:
                T = m[0] # transition function / probability
                R = m[1] # reward for this transition
                sP = m[2] # new state s'
                V += T * (R + self.gamma * VS[sP])
            Q[a] = V
                
        return Q
                    
    def valueMaximization(self, VS):
        newVS = {}
        for s in VS.keys():
            Q = self.computeQValues(s, VS)
            newVS[s] = max(Q.values())
            
        return newVS
            
    def valueIteration(self):
        converged = False
        curV = {}
        for s in self.problem.getStates():
            curV[s] = 0 # initialize everything with zero first
        
        it = 0
        while not converged:
        #for i in range(71):
            newVS = self.valueMaximization(curV)
            m = -float("inf")
            for s in newVS.keys():
                diff = abs(newVS[s] - curV[s])
                m = max(diff, m)
            if m < 0.001:
                converged = True
                
            curV = newVS
            #self.printValues(curV)
            #print('Maximal Difference: ' + str(m))
            it += 1
            
        return self.policyExtraction(curV), curV, it
        
            
vI = MDPSolver(GirdWorldProblem())
pol1, V1, it1 = vI.valueIteration()
pol2, V2, it2 = vI.policyIteration()

vI.printPolicy(pol1)
print(it1)
vI.printPolicy(pol2)
print(it2)

#print(vI.computeQValues('A2', V1))
#print(vI.computeQValues('A2', V2))




