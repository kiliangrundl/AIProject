import random

def printPolicy(p):
    for k in sorted(p.keys()):
        print(k + ': ' + p[k], end=' | ')
    print('')
           
def printValues(curV):
    for k in sorted(curV.keys()):
        print(k + ': ' + '%.2f' % (curV[k]), end=' | ')
    print('')
    
def printQValues(curQ):
    for k in sorted(curQ.keys()):
        print(k + ': ' + '%.2f' % (curQ[k]), end=' | ')
    print('')

class MDP():
        
    def takeAction(self, s, a):
        # Select one action of the randomized once
        moves = self.getTransitionFunction(s, a)
        my_list = []
        for m in moves: 
            my_list = my_list + int(m[0] * 100) * [(m[1], m[2])]  # TODO: this only work, because the probabilities in the TransitionFunction are 80%, 10% and 10% always. This is not the general case... Still it would be a okay approach for the other problems!
            
        return random.choice(my_list)

class RacingProblem(MDP):
    '''
    The racing problem as described in the course as a MDP
    '''
    
    def isGoalState(self, s):
        if s == 'overheated':
            return True
        else:
            return False
        
    def getStartStates(self):
        return ['cool', 'warm']
    
    def getStates(self):
        return ['cool', 'warm', 'overheated']
    
    def getActions(self, s):
        if s == 'cool':
            return ['slow', 'fast']
        elif s == 'warm':
            return ['slow', 'fast']
        else:
            return ['exit']
        
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
        else: # s == 'warm':
            if a == 'slow':
                return [(0.5, 1, 'cool'), (0.5, 1, 'warm')]
            elif a == 'fast':
                return [(1, -10, 'overheated')]
            else:
                return [(1,0,'overheated')]
        
class GridWorldProblem(MDP):
    '''
    The GridWorldProblem as a MDP
    '''
    def isGoalState(self, s):
        if s == 'finish':
            return True
        else:
            return False
        
    def getStartStates(self):
        return ['A1']
    
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
        lR = -1
        if s == 'C4':
            return [(1, 1, 'finish')]
        elif s == 'B4':
            return [(1, -1, 'finish')]
        elif s == 'finish':
            return [(1, 0, 'finish')]
        else:
            if a == 'n':
                news = ['X' + s[1], s[0] + str(int(s[1]) - 1), s[0] + str(int(s[1]) + 1)]
                if s[0] == 'A':
                    news[0] = 'B' + s[1] 
                elif s[0] == 'B':
                    news[0] = 'C' + s[1]
            elif a == 's':    
                news = ['X' + s[1], s[0] + str(int(s[1]) - 1), s[0] + str(int(s[1]) + 1)]
                if s[0] == 'C':
                    news[0] = 'B' + s[1] 
                elif s[0] == 'B':
                    news[0] = 'A' + s[1]
            elif a == 'e':
                news = [s[0] + str(int(s[1]) + 1), s, s]
                if s[0] == 'A':
                    news[1] = 'B' + s[1]
                    news[2] = 'X' + s[1] 
                elif s[0] == 'B':
                    news[1] = 'A' + s[1]
                    news[2] = 'C' + s[1]
                elif s[0] == 'C':
                    news[1] = 'X' + s[1]
                    news[2] = 'B' + s[1]
            else:  # west
                news = [s[0] + str(int(s[1]) - 1), s, s]
                if s[0] == 'A':
                    news[1] = 'B' + s[1]
                    news[2] = 'X' + s[1] 
                elif s[0] == 'B':
                    news[1] = 'A' + s[1]
                    news[2] = 'C' + s[1]
                elif s[0] == 'C':
                    news[1] = 'X' + s[1]
                    news[2] = 'B' + s[1]
                    
            # If the new possible state does not exist, replace it with the old state
            F = news
            for i in range(len(news)):
                if news[i] not in self.getStates():
                    F[i] = s
            
            return [(0.8, lR, F[0]), (0.1, lR, F[1]), (0.1, lR, F[2])]