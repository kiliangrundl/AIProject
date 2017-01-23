from treeSearch import *

        
s = (4,4) # initial State
problem = SailProblem([(14,18)], 20, 20)
#s = 'S'
#problem = MainTestSearch()
#s = 'S' # initial State
#problem = EasyTestSearchOne()
heuristic = manhattenDistanceSail

   
print("DepthFirstSearch")
#treeSearch(problem, DepthFirstSearch(problem, s))

print("BreathFirstSearch")
#treeSearch(problem, BreathFirstSearch(problem, s))
    
print("UniformCostSearch")
#treeSearch(problem, UniformCostSearch(problem, s))

print("GreedySearch")
treeSearch(problem, GreedySearch(problem, s, heuristic))

print("AstarSearch")
treeSearch(problem, AstarSearch(problem, s, heuristic))