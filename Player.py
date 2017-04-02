import Arena
import mdpSolver

'''
The players that exist
'''

class Player(Arena.Mover):
    def __init__(self, problem):
        Arena.Mover.__init__(self)
        self.score = 0
        self.problem = problem
        
    def initialize(self):
        Arena.Mover.initialize(self)
        self.score = 0

    def start(self, root):
        self.root = root
        self.problem.initialize()
        Arena.initializeCanvas(self, root)
        self.play()        
    
    def play(self):
        self.problem.initialize()
        self.root.after(1000, self.run)

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
            self.root.after(200, self.run)
        else:
            print(self.score)
            self.root.after(1000, self.play)          

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
  
         
class RAGQApproximator(mdpSolver.QApproximator, Player):
    def __init__(self, problem):
        mdpSolver.QApproximator.__init__(self, problem)
        Player.__init__(self, problem)
        self.rounds = 1000
        self.round = 1
        
    def run(self):
        s = self.problem.getState()
        a = self.choseAction(s)
        
        R, sP = self.problem.takeAction(s, a)
        self.updateQ(s, a, sP, R)
        
        if not self.problem.isGoalState(sP):
            self.root.after(5, self.run)
        else:
            self.round += 1
            print(self.score)
            for prop in self.properties:
                print(prop.__class__.__name__, ' ' , prop.weight)
            if self.round < self.rounds:
                self.root.after(10, self.play)        