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
        canvas.pack(fill=tkinter.BOTH, expand=1)
        root.resizable(width=False, height=False)
    
        # create a toplevel menu
        menubar = tkinter.Menu(root)
        #menubar.add_command(label="Restart", command=self.start)
        #root.bind_all("<Control-r>", self.start)
        # display the menu
        root.config(menu=menubar)
    
        canvas.initialize()
        root.after(100, canvas.refresh)
    
        #tkinter.mainloop()

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
        print(R, '/', self.score)
        
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
                avgScore.append(sum(score[i-N:i])/N)
            #    print('Average over the last 100 games: ' + str()
        #print('Average over the last 100 games: ' + str(sum(score[i-N:i])/N))
        #for s in self.policy:
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

# define the problem
arena = Arena.SimpleArena1()

# Define a player
player = RAGQLearner(arena)
arena.addPlayer(player)

root = tkinter.Tk()
root.after(0, player.start)
tkinter.mainloop()


