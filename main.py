import tkinter
import Arena
import mdpSolver
import matplotlib.pyplot as plt

def initializeCanvas(problem):
    '''
    Routine uch that the arena can be painted or not in a different thread
    '''
    paint = True
    if paint:
        
        # TODO: solve this more nicely
        try:
            root.bind("<Key>", player.keyInput)
        except:
            pass
        
        canvas = Arena.ArenaCanvas(root, problem)
        canvas.initialize()
        #canvas.pack()
        canvas.pack(fill=tkinter.BOTH, expand=1)
        #root.resizable(width=False, height=False)
    
        # create a toplevel menu
        menubar = tkinter.Menu(root)
        # menubar.add_command(label="Restart", command=self.start)
        # root.bind_all("<Control-r>", self.start)
        # display the menu
        root.config(menu=menubar)
    
        root.after(100, canvas.refresh)
    
        # tkinter.mainloop()

class Player(Arena.Mover):
    def __init__(self, problem):
        Arena.Mover.__init__(self)
        self.score = 0
        self.problem = problem
        
    def initialize(self):
        Arena.Mover.initialize(self)
        self.score = 0

    def start(self):
        self.problem.initialize()
        initializeCanvas(self.problem)
        self.play()        
    
    def play(self):
        self.problem.initialize()
        root.after(1000, self.run)

    def getScore(self):
        return self.score
    
    def addScore(self, points):
        self.score += points

class RAG(Player):
    
    def choseAction(self):
        '''
        A manual player acts basically all the time...
        '''
        return self.action
        
        
    def keyInput(self, event):
        if event.keysym == 'Right':
            self.right()
        if event.keysym == 'Left':
            self.left()
        if event.keysym == 'Up':
            self.up()
        if event.keysym == 'Down':
            self.down()   
            
    def run(self):
        a = self.choseAction()
        R, sP = self.problem.takeAction(self.problem.getState(), a)
        
        if not self.problem.isGoalState(sP):
            root.after(700, self.run)
        else:
            print(self.score)
            root.after(1000, self.play)          

class RAGQLearner(mdpSolver.QLearner, Player):
    def __init__(self, problem):
        mdpSolver.QLearner.__init__(self, problem)
        Player.__init__(self, problem)
        
    def start(self):
        score = []
        avgScore = []
        N = 50
        for i in range(1000):
            self.problem.initialize()
            self.run()
            score.append(self.getScore())
            if i % N == 0 and i > 0:
                avgScore.append(sum(score[i - N:i]) / N)
            #    print('Average over the last 100 games: ' + str()
        # print('Average over the last 100 games: ' + str(sum(score[i-N:i])/N))
        # for s in self.policy:
        #    # compute how often this state was visited
        #    n = 0
        #    for a in self.problem.getActions(s):
        #        try:
        #            n += self.N[(s,a)]
        #        except:
        #            n += 0 
        #    if n != 0:
        #        print(s, ' ', round(self.getValue(s)), ' ', self.policy[s])
        plt.plot(avgScore)
        plt.show()
    
    def run(self):
        s = self.problem.getState()
        a = self.choseAction(s)
        
        R, sP = self.problem.takeAction(s, a)
        self.updateQ(s, a, sP, R)

        if not self.problem.isGoalState(s):
            self.run()
  
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
            return 1 / (dist * dist)
    
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
        
class numberOfActions(mdpSolver.PropertyFunction): 
    def evaluate(self, s, a): 
        d = self.problem.computeDirection(a)
        pos = [s[0][0] + d[0], s[0][1] + d[1]]
        return len(self.problem.getStateActions(pos))
    
        
class numberOfCoins(mdpSolver.PropertyFunction): 
    def evaluate(self, s, a): 
        n = 0
        for i in range(1, len(self.problem.coins)):
            if s[i][1] == 'e':  # if coin exists, get its position
                n += 1
        return 1 / n
        
         
class RAGQApproximator(mdpSolver.QApproximator, Player):
    def __init__(self, problem):
        mdpSolver.QApproximator.__init__(self, problem)
        Player.__init__(self, problem)
        
    def start(self):
        Player.start(self)
    
    def run(self):
        s = self.problem.getState()
        a = self.choseAction(s)
        
        R, sP = self.problem.takeAction(s, a)
        self.updateQ(s, a, sP, R)
        
        if not self.problem.isGoalState(sP):
            root.after(5, self.run)
        else:
            print(self.score)
            for prop in self.properties:
                print(prop.__class__.__name__, ' ' , prop.weight)
            root.after(10, self.play)         


# define the problem
arena = Arena.Arena1()

# Define a player
player = RAGQApproximator(arena)
player.addPropertyFunction(GhostDistance(arena))
player.addPropertyFunction(CoinDistance(arena))
#player.addPropertyFunction(numberOfActions(arena))
#player.addPropertyFunction(numberOfCoins(arena))
arena.addPlayer(player)

root = tkinter.Tk()
root.after(0, player.start)
tkinter.mainloop()


