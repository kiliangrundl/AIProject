import time

class Action():
    """
    Class to describe actions, consisting of a move and a costTotal
    """
    
    def __init__(self, move, cost):
        self.move = move
        self.costTotal = cost
        
    def getMove(self):
        return self.move
    
    def getCost(self):
        return self.costTotal
    
class FringeMember:
    """
    stores the path of the fringe, the totalCosts of the path and the cost of the last action in it
    
    TODO: describe the costs more general
    """

    def __init__(self, path, totalCost):
        self.path = path
        self.costTotal = totalCost
        
    def getPath(self):
        return self.path
    
    def getCostTotal(self):
        return self.costTotal

class SearchProblem:
    """Is the mother class of all search problems

    """
        
    def getStartState(self):
        ''' get the start state of a problem '''
        
    def getPossibleActions(self, s):
        'Get possible candidates for the current state'
        
    def getGoals(self):
        'Return possible goal states (for heuristics), TODO: maybe better options available'
        
    def getNewPosition(self, s, action):
        'Return the new position'
    
    def solved(self, s):
        ''' Check if the solution to the problem is found '''

class SailProblem(SearchProblem):
    def __init__(self, g, xFields, yFields):
        self.g = g
        self.xFields = xFields
        self.yFields = yFields
        
    def getStartState(self):
        SearchProblem.getStartState(self)
        return (4,4)
        
    def getPossibleActions(self, s):
        SearchProblem.getPossibleActions(self, s)
        actions = []
        if s[0] < self.xFields:
            actions.append(Action((1,0),1))
        if s[0] > 0:
            actions.append(Action((-1,0),1))
        if s[1] > 0:
            actions.append(Action((0,-1),1))
        if s[1] < self.yFields:
            actions.append(Action((0,1),1))
        return actions
    
    def getGoals(self):
        SearchProblem.getGoals(self)
        return self.g
    
    def getNewPosition(self, s, action):
        return (s[0]+action.getMove()[0],s[1]+action.getMove()[1]) 
        
    def solved(self, s):
        SearchProblem.solved(self, s)
        if s in self.g:
            return True
        else:
            return False
            
class MainTestSearch(SearchProblem):
    """
    This is the graph that always appears in the lecture
    """
    
    def getStartState(self):
        SearchProblem.getStartState(self)
        return 'S'
    
    def getPossibleActions(self, s):
        if s == 'S':
            actions = [Action('d',3), Action('e',9), Action('p',1)]
        if s == 'a':
            actions = []
        if s == 'b':
            actions = [Action('a',2)]
        if s == 'c':
            actions = [Action('a',1)]
        if s == 'd':
            actions = [Action('b',1), Action('c',8), Action('e',2)]
        if s == 'e':
            actions = [Action('h',8), Action('r',2)]
        if s == 'f':
            actions = [Action('c',1), Action('G',2)]
        if s == 'h':
            actions = [Action('p',1), Action('q',1)]
        if s == 'p':
            actions = [Action('q',15)]
        if s == 'q':
            actions = []
        if s == 'r':
            actions = [Action('f',1)]            
        
        return actions
    
    def getGoals(self):
        SearchProblem.getGoals(self)
        return ['G']
    
    def getNewPosition(self, s, action):
        return action.getMove()
        
    def solved(self, s):
        if s == 'G':
            return True
        else:
            return False

class EasyTestSearchOne(SearchProblem):
    """
    This is the graph appears in between
    """
    
    def getStartState(self):
        SearchProblem.getStartState(self)
        return 'S'
    
    def getPossibleActions(self, s):
        if s == 'S':
            actions = [Action('A',1), Action('G',5)]
        if s == 'A':
            actions = [Action('G',3)]
        return actions
    
    def getGoals(self):
        SearchProblem.getGoals(self)
        return ['G']
    
    def getNewPosition(self, s, action):
        return action.getMove()
        
    def solved(self, s):
        if s == 'G':
            return True
        else:
            return False
        
def pessimisticHeuristicEasyTestSearchOne(fringe, problem):
    pos = fringe.getPath()[-1]
    
    if pos == 'S':
        return 7
    if pos == 'A':
        return 6
    if pos == 'G':
        return 0
    
def optimisticHeuristicEasyTestSearchOne(fringe, problem):
    pos = fringe.getPath()[-1]
    
    if pos == 'S':
        return 3
    if pos == 'A':
        return 2
    if pos == 'G':
        return 0
    
class SearchStrategy:
    """Is the mother class of all search strategies

        problem: Member
        @type problem: SearchProblem
        other_member: Another member
    """
    
    def __init__(self, problem):
        ':type problem: SearchProblem'
        self.problem = problem

        self.fringe = set()
        self.currentFringe = FringeMember([problem.getStartState()], 0)
        self.fringe.add(self.currentFringe)
        
    def updateCurrentFringemember(self):
        'return the current path'
        
    def getCurrentFringe(self):
        return self.currentFringe
        
    def getCurrentState(self):
        return self.currentFringe.getPath()[-1]
    
    def updateFringe(self, actions):
        'Add the Candidates to the fringe'
        for action in actions:
            newPos = self.problem.getNewPosition(self.getCurrentState(), action)
            if newPos not in self.currentFringe.getPath():
                self.fringe.add(FringeMember(self.currentFringe.getPath()+[newPos], self.currentFringe.getCostTotal()+action.getCost()))
                
        self.fringe.remove(self.currentFringe)
        if self.fringe:
            self.updateCurrentFringemember()
    
    def explore(self):
        ''' Explore the problem'''
        possibleActions = self.problem.getPossibleActions(self.getCurrentState())
        self.updateFringe(possibleActions)
        
class DepthFirstSearch(SearchStrategy):
        
    def updateCurrentFringemember(self):
        self.currentFringe = max(self.fringe, key=lambda x: len(x.getPath()))
        
class BreathFirstSearch(SearchStrategy):
    
    def updateCurrentFringemember(self):
        self.currentFringe = min(self.fringe, key=lambda x: len(x.getPath()))
        
class UniformCostSearch(SearchStrategy):
    
    def updateCurrentFringemember(self):
        self.currentFringe = min(self.fringe, key=lambda x: x.getCostTotal())        
      
      
class manhattenDistance2D():
    
    def __init__(self, goals):
        self.goals = goals
    
    def heuristicFun(self, fringe, problem):
        pos = fringe.getPath()[-1]
        
        def distMeas(y):
            return abs(y[0]-pos[0])+abs(y[1]-pos[1])
        
        return distMeas(min(self.goals, key=distMeas))
      
class GreedySearch(SearchStrategy):
    
    def __init__(self, problem, heuristic):
        SearchStrategy.__init__(self, problem)
        self.heuristic = heuristic
        
    def updateCurrentFringemember(self):
        self.currentFringe = min(self.fringe, key=lambda x: self.heuristic(x, self.problem))
        
class AstarSearch(SearchStrategy):
    
    def __init__(self, problem, heuristic):
        SearchStrategy.__init__(self, problem)
        self.heuristic = heuristic
        
    def updateCurrentFringemember(self):
        self.currentFringe = min(self.fringe, key=lambda x: self.heuristic(x, self.problem)+x.getCostTotal())

def treeSearch(problem, strategy):
    ':type problem: SearchProblem'
    ':type strategy: SearchStrategy'
   
    start = time.time()
    found = False
    #problem.initialize()
    while True:
        'If there are no new candidate the search has failed'
        if strategy.getCurrentFringe() is None:
            break
        
        if problem.solved(strategy.getCurrentState()):
            'If the problem is solved we are happy'
            found = True
            break
        else:
            'If the problem is not solved, we have to explore with the canidate'
            strategy.explore()
            
    if found:
        print('Solution: with costTotal ' + str(strategy.getCurrentFringe().getCostTotal()) + ' and path: ' + str(strategy.getCurrentFringe().getPath()))
    else:
        print('No Solution found')
    end = time.time()
    print(end - start)
    return found
            

