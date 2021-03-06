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
        
    def getSearchStartState(self):
        ''' get the start state of a problem '''
        
    def getSearchActions(self, pos):
        'Get possible candidates for the current state'
        
    def getGoals(self):
        'Return possible goal states (for heuristics), TODO: maybe better options available'
        
    def getNewPosition(self, s, action):
        'Return the new position'
    
    def solvedSearch(self, s):
        ''' Check if the solution to the problem is found '''

class SailProblem(SearchProblem):
    def __init__(self, g, xFields, yFields):
        self.g = g
        self.xFields = xFields
        self.yFields = yFields
        
    def getSearchStartState(self):
        SearchProblem.getSearchStartState(self)
        return (4, 4)
        
    def getSearchActions(self, pos):
        SearchProblem.getSearchActions(self, pos)
        actions = []
        if pos[0] < self.xFields:
            actions.append(Action((1, 0), 1))
        if pos[0] > 0:
            actions.append(Action((-1, 0), 1))
        if pos[1] > 0:
            actions.append(Action((0, -1), 1))
        if pos[1] < self.yFields:
            actions.append(Action((0, 1), 1))
        return actions
    
    def getGoals(self):
        SearchProblem.getGoals(self)
        return self.g
    
    def getNewPosition(self, s, action):
        return (s[0] + action[0], s[1] + action[1]) 
        
    def solvedSearch(self, s):
        SearchProblem.solvedSearch(self, s)
        if s in self.g:
            return True
        else:
            return False
            
class MainTestSearch(SearchProblem):
    """
    This is the graph that always appears in the lecture
    """
    
    def getSearchStartState(self):
        SearchProblem.getSearchStartState(self)
        return 'S'
    
    def getSearchActions(self, pos):
        if pos == 'S':
            actions = [Action('d', 3), Action('e', 9), Action('p', 1)]
        if pos == 'a':
            actions = []
        if pos == 'b':
            actions = [Action('a', 2)]
        if pos == 'c':
            actions = [Action('a', 1)]
        if pos == 'd':
            actions = [Action('b', 1), Action('c', 8), Action('e', 2)]
        if pos == 'e':
            actions = [Action('h', 8), Action('r', 2)]
        if pos == 'f':
            actions = [Action('c', 1), Action('G', 2)]
        if pos == 'h':
            actions = [Action('p', 1), Action('q', 1)]
        if pos == 'p':
            actions = [Action('q', 15)]
        if pos == 'q':
            actions = []
        if pos == 'r':
            actions = [Action('f', 1)]            
        
        return actions
    
    def getGoals(self):
        SearchProblem.getGoals(self)
        return ['G']
    
    def getNewPosition(self, s, action):
        return action
        
    def solvedSearch(self, s):
        if s == 'G':
            return True
        else:
            return False

class EasyTestSearchOne(SearchProblem):
    """
    This is the graph appears in between
    """
    
    def getSearchStartState(self):
        SearchProblem.getSearchStartState(self)
        return 'S'
    
    def getSearchActions(self, pos):
        if pos == 'S':
            actions = [Action('A', 1), Action('G', 5)]
        if pos == 'A':
            actions = [Action('G', 3)]
        return actions
    
    def getGoals(self):
        SearchProblem.getGoals(self)
        return ['G']
    
    def getNewPosition(self, s, action):
        return action
        
    def solvedSearch(self, s):
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

        self.fringe = []
        self.currentFringe = FringeMember([problem.getSearchStartState()], 0)
        self.fringe.append(self.currentFringe)
        
    def updateCurrentFringemember(self):
        'return the current path'
        
    def getCurrentFringe(self):
        return self.currentFringe
        
    def getCurrentState(self):
        return self.currentFringe.getPath()[-1]
    
    def updateFringe(self, actions):
        'Add the Candidates to the fringe'
        for action in actions:
            newPos = self.problem.getNewPosition(self.getCurrentState(), action.getMove())
            if newPos not in self.currentFringe.getPath():
                self.fringe.append(FringeMember(self.currentFringe.getPath() + [newPos], self.currentFringe.getCostTotal() + action.getCost()))
                
        self.fringe.remove(self.currentFringe)
        if self.fringe:
            self.updateCurrentFringemember()
    
    def explore(self):
        ''' Explore the problem'''
        distanceToLink = self.problem.getSearchActions(self.getCurrentState())
        self.updateFringe(distanceToLink)
        
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
            return abs(y[0] - pos[0]) + abs(y[1] - pos[1])
        
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
        self.currentFringe = min(self.fringe, key=lambda x: self.heuristic(x, self.problem) + x.getCostTotal())

def treeSearch(problem, strategy, maxCost=float("inf")):
    ':type problem: SearchProblem'
    ':type strategy: SearchStrategy'
   
    # start = time.time()
    # problem.initialize()
    while True:
        'If there are no new candidate the search has failed'
        if strategy.getCurrentFringe() is None:
            break
        
        if problem.solvedSearch(strategy.getCurrentState() or strategy.getCurrentFringe().getCostTotal() > maxCost):
            'If the problem is solvedSearch we are happy'
            break
        else:
            'If the problem is not solvedSearch, we have to explore with the canidate'
            strategy.explore()
            
    # if found:
    #    print('Solution: with costTotal ' + str(strategy.getCurrentFringe().getCostTotal()) + ' and path: ' + str(strategy.getCurrentFringe().getPath()))
    # else:
    #    print('No Solution found')
    # end = time.time()
    # print(end - start)
            

