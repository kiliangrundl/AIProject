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
    def __init__(self):
        ''' Initialize the problem '''
        
    def getPossibleActions(self, s):
        'Get possible candidates for the current state'
        
    def getNewPosition(self, s, action):
        'Return the new position'
    
    def solved(self, s):
        ''' Check if the solution to the problem is found '''

class SailProblem(SearchProblem):
    def __init__(self, g, xFields, yFields):
        self.g = g
        self.xFields = xFields
        self.yFields = yFields
        
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
    
    def getNewPosition(self, s, action):
        return (s[0]+action.getMove()[0],s[1]+action.getMove()[1]) 
        
    def solved(self, s):
        SearchProblem.solved(self, s)
        if s in self.g:
            return True
        else:
            return False
            
class TestGraph(SearchProblem):
    
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
    
    def getNewPosition(self, s, action):
        return action.getMove()
        
    def solved(self, s):
        if s == 'G':
            return True
        else:
            return False

class SearchStrategy:
    """Is the mother class of all search strategies

        problem: Member
        @type problem: SearchProblem
        other_member: Another member
    """
    
    def __init__(self, problem, startState):
        ':type problem: SearchProblem'
        self.problem = problem

        self.fringe = set()
        self.currentFringe = FringeMember([startState], 0)
        self.fringe.add(self.currentFringe)
        
    def updateCurrentFringemember(self):
        'return the current path'
        
    def getCurrentFringe(self):
        return self.currentFringe
        
    def getCurrentState(self):
        return self.currentFringe.getPath()[-1]
    
    def updateFringe(self, actions):
        'Add the Candidates to the fringe'
    
    def explore(self):
        ''' Explore the problem'''
        possibleActions = self.problem.getPossibleActions(self.getCurrentState())
        self.updateFringe(possibleActions)
        
class UninformedSearch(SearchStrategy):
    def __init__(self, problem, startState):
        SearchStrategy.__init__(self, problem, startState)

    def updateFringe(self, actions):
        SearchStrategy.updateFringe(self, actions)        
        for action in actions:
            newPos = self.problem.getNewPosition(self.getCurrentState(), action)
            if newPos not in self.currentFringe.getPath():
                self.fringe.add(FringeMember(self.currentFringe.getPath()+[newPos], self.currentFringe.getCostTotal()+action.getCost()))
                
        self.fringe.remove(self.currentFringe)
        try:
            self.updateCurrentFringemember()
        except:
            self.currentFringe = None
        
class DepthFirstSearch(UninformedSearch):
        
    def updateCurrentFringemember(self):
        self.currentFringe = max(self.fringe, key=lambda x: len(x.getPath()))
        
class BreathFirstSearch(UninformedSearch):
    
    def updateCurrentFringemember(self):
        self.currentFringe = min(self.fringe, key=lambda x: len(x.getPath()))
        
class UniformCostSearch(UninformedSearch):
    
    def updateCurrentFringemember(self):
        self.currentFringe = min(self.fringe, key=lambda x: x.getCostTotal())        
        
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
            
        
s = (5,4) # initial State
problem = SailProblem([(8,8)], 10, 10)
#s = 'S'
#problem = TestGraph()

   
print("DepthFirstSearch")
treeSearch(problem, DepthFirstSearch(problem, s))

print("BreathFirstSearch")
treeSearch(problem, BreathFirstSearch(problem, s))
    
print("UniformCostSearch")
treeSearch(problem, UniformCostSearch(problem, s))
