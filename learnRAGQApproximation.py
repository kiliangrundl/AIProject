#/usr/bin/python3

'''
This file executes the learning process with the QApproximationLearner

Different property functions are suggested and exemplary taken
'''

import tkinter
import Arena
import Player
import mdpSolver



class ManhattenGhostDistance(mdpSolver.PropertyFunction):
    def evaluate(self, s, a):
        def distMeas(y):
            return abs(y[0] - pos[0]) + abs(y[1] - pos[1])
        
        minDist = 1000
        d = self.problem.computeDirection(a)
        pos = [s[0][0] + d[0], s[0][1] + d[1]] 
        for i in range(1 + len(self.problem.coins), len(s)):
            mPos = s[i]
            dist = distMeas(mPos)
            if dist < minDist:
                minDist = dist
                
        if minDist == 0:
            return 10
        else: 
            return 1 / minDist
        
class GhostDistance(mdpSolver.PropertyFunction):
    def __init__(self, problem):
        mdpSolver.PropertyFunction.__init__(self, problem)
            
    def evaluate(self, s, a):
        
        d = self.problem.computeDirection(a)
        pos = [s[0][0] + d[0], s[0][1] + d[1]]
        goals = [] 
        for i in range(1 + len(self.problem.coins), len(s)):
            goals.append(tuple(s[i]))
        dist = self.problem.computeActualDistance(tuple(pos), goals)
                
        if dist == 0:
            return 2
        else: 
            return 1 / (dist)
    
class ManhattenCoinDistance(mdpSolver.PropertyFunction):
    
    def evaluate(self, s, a):
        def distMeas(y):
            return abs(y[0] - pos[0]) + abs(y[1] - pos[1])
        
        minDist = 1000
        d = self.problem.computeDirection(a)
        pos = [s[0][0] + d[0], s[0][1] + d[1]] 
        for i in range(1, len(self.problem.coins)):
            if s[i][1] == 'e':  # if coin exists, get its position
                dist = distMeas(s[i][0])
                if dist < minDist:
                    minDist = dist
                    
        if minDist == 0:
            return 10
        else: 
            return 1 / minDist
        
class CoinDistance(mdpSolver.PropertyFunction):
    def __init__(self, problem):
        mdpSolver.PropertyFunction.__init__(self, problem)
        
    def evaluate(self, s, a):
        
        d = self.problem.computeDirection(a)
        pos = [s[0][0] + d[0], s[0][1] + d[1]]
        goals = [] 
        for i in range(1, len(self.problem.coins)):
            if s[i][1] == 'e':  # if coin exists, get its position
                goals.append(tuple(s[i][0]))
        dist = self.problem.computeActualDistance(tuple(pos), goals)
                
        if dist == 0:
            return 2
        else: 
            return 1 / (dist)      
        
class distanceToLink(mdpSolver.PropertyFunction): 
    def __init__(self, problem):
        mdpSolver.PropertyFunction.__init__(self, problem)
        self.goals = problem.computeLinkPositions()
    
    def evaluate(self, s, a): 
        d = self.problem.computeDirection(a)
        pos = [s[0][0] + d[0], s[0][1] + d[1]]
        dist = self.problem.computeActualDistance(pos, self.goals)
        
        if dist == 0:
            return 2
        else: 
            return 1 / (dist)    
    
class numberOfCoins(mdpSolver.PropertyFunction): 
    def __init__(self, problem):
        mdpSolver.PropertyFunction.__init__(self, problem)
    
    def evaluate(self, s, a): 
        n = 0
        for i in range(1, len(self.problem.coins)):
            if s[i][1] == 'e':  # if coin exists, get its position
                n += 1
        return 1 / (n * n * n)
                         
# define the problem
arena = Arena.Arena1()

# Define a player
player = Player.RAGQApproximator(arena)
player.addPropertyFunction(GhostDistance(arena))
player.addPropertyFunction(CoinDistance(arena))
#player.addPropertyFunction(distanceToLink(arena))
#player.addPropertyFunction(numberOfCoins(arena))
arena.addPlayer(player)

root = tkinter.Tk()
root.after(0, player.start, root)
tkinter.mainloop()


