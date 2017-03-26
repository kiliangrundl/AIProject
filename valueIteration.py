import numpy as np

'''
This file handles some MDPs
'''

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
            return ['north', 'east', 'south', 'west']
        
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
            if a == 'north':
                news = ['X'+s[1], s[0]+str(int(s[1])-1), s[0]+str(int(s[1])+1)]
                if s[0] == 'A':
                    news[0] = 'B'+s[1] 
                elif s[0] == 'B':
                    news[0] = 'C'+s[1]
            elif a == 'south':    
                news = ['X'+s[1], s[0]+str(int(s[1])-1), s[0]+str(int(s[1])+1)]
                if s[0] == 'C':
                    news[0] = 'B'+s[1] 
                elif s[0] == 'B':
                    news[0] = 'A'+s[1]
            elif a == 'east':
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
    
        
            

class ValueIterator():
    def __init__(self, problem):
        self.VS = {}
        self.problem = problem
        self.gamma = 0.90
        
        # initialize the values to zero
        for s in problem.getStates():
            self.VS[s] = 0
        
    def update(self):
        newVS = {}
        for s in self.VS.keys():
            actions = self.problem.getActions(s)
            curMax = -float("inf")
            for a in actions:
                moves = self.problem.getTransitionFunction(s, a)
                V = 0
                for m in moves:
                    T = m[0] # transition function / probability
                    R = m[1] # reward for this transition
                    sP = m[2] # new state s'
                    V += T * (R + self.gamma * self.VS[sP])
                curMax = max([curMax,V])
                
            newVS[s] = curMax
            if curMax == -float("inf"):
                newVS[s] = 0
            
        return newVS
            
    def run(self):
        converged = False
        #while not converged:
        for i in range(71):
            for k in sorted(self.VS.keys()):
                print(k + ': ' + '%.2f' % (self.VS[k]))
            newVS = self.update()
            diff = np.array(newVS.values()) - np.array(self.VS.values())
            self.VS = newVS
            if max(abs(diff)) < 0.1:
                converged = True
            print('')
            
vI = ValueIterator(GirdWorldProblem())
vI.run()    




